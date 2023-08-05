# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Code used to fit pipeline."""
import datetime
import json
import logging
import math
import uuid
from collections import defaultdict
from typing import Any, Dict, Optional, Tuple, cast

import azureml.automl.core.inference as inference
import numpy as np
import sklearn
from azureml.automl.core import package_utilities
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.automl_utils import retry_with_backoff
from azureml.automl.core.model_explanation import (
    ModelExpSupportStr, _get_valid_notebook_path_link)
from azureml.automl.core.onnx_convert.onnx_convert_constants import \
    OnnxConvertConstants
from azureml.automl.core.shared import constants, logging_utilities, utilities
from azureml.automl.core.shared.exceptions import (
    AutoMLException, ClientException, ErrorTypes, PipelineRunException,
    RunStateChangeException, ServiceException, UserException)
from azureml.automl.core.shared.limit_function_call_exceptions import \
    TimeoutException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.systemusage_telemetry import (
    SystemResourceUsageTelemetry, SystemResourceUsageTelemetryFactory)
from azureml.automl.runtime import (cpu_utilities, pipeline_run_helper,
                                    training_utilities)
from azureml.automl.runtime._run_history import RunType
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.exceptions import AzureMLException
from azureml.exceptions import ServiceException as AzureMLServiceException

from .automl_pipeline import AutoMLPipeline
from .data_context import TransformedDataContext
from .fit_output import FitOutput
from .onnx_convert import OnnxConverter

logger = logging.getLogger(__name__)


def fit_pipeline(automl_pipeline: AutoMLPipeline,
                 automl_settings: AutoMLBaseSettings,
                 automl_run_context: AutoMLAbstractRunContext,
                 fit_iteration_parameters_dict: Optional[Dict[str, Any]] = None,
                 remote: bool = True,
                 transformed_data_context: Optional[TransformedDataContext] = None,
                 dataset: Optional[DatasetBase] = None,
                 elapsed_time: Optional[int] = None,
                 onnx_cvt: Optional[OnnxConverter] = None,
                 bypassing_model_explain: Optional[str] = None,
                 feature_configs: Optional[Dict[str, Any]] = None) -> FitOutput:
    """
    Run a single iteration of an AutoML experiment.

    This method is automatically called during a regular AutoML
    experiment. fit_pipeline will evaluate the pipeline for this iteration, fit the pipeline with the provided data,
    calculate the various metrics relevant for this experiment, and log all the results in the specified AzureML Run's
    history.

    :param automl_pipeline: AutoMLPipeline object containing pipeline id and serialized script.
    :param automl_settings: User settings specified when creating AutoMLConfig.
    :param automl_run_context: child run context object
    :param fit_iteration_parameters_dict: Remaining data specific parameters for fit such as 'x_raw_column_names'.
    :param remote: flag whether this is a remote run or local run.
    :param transformed_data_context: TransformedDataContext, contains X,y and other transformed data.
    :param dataset: Containing X, y and other transformed data info.
    :param elapsed_time: How long this experiment has already taken in minutes
    :param onnx_cvt: The onnx converter.
    :param bypassing_model_explain: Should this function run model explainability for this pipeline or skip it.
    :param feature_configs: Feature configuration dictionary for different AutoML features.
    :return: AzureML Run Properties for this child run
    """
    start_time = datetime.datetime.now()

    telemetry_logger = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry(interval=10)

    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][Starting fit_pipeline]".format(automl_run_context.run_id)
    )

    logging_utilities.log_system_info(logger, prefix_message="[RunId:{}]".format(automl_run_context.run_id))

    logger.info("Using child run {0}".format(automl_run_context.run_id))

    # Initialize FitOutput object
    fit_output = FitOutput(automl_settings, automl_pipeline)

    if dataset is None and transformed_data_context is None and fit_iteration_parameters_dict is None:
        raise PipelineRunException(
            "Can't create a ClientDataset without transformed_data_context or fit_iteration_parameters_dict",
            target=PipelineRunException.PIPELINE_RUN_REQUIREMENTS,
            reference_code=ReferenceCodes._FIT_PIPELINE_DATASET_REQS_NONE,
            has_pii=False)

    resource_tracker = cpu_utilities.ResourceUsageTracker()

    try:
        with resource_tracker:
            if dataset is None:
                # Get dataset for training
                if transformed_data_context is not None:
                    logger.info("Generating ClientDataset from transformed data.")
                    dataset = training_utilities.init_client_dataset(transformed_data_context=transformed_data_context,
                                                                     cache_store=transformed_data_context.cache_store,
                                                                     automl_settings=automl_settings,
                                                                     remote=remote,
                                                                     keep_in_memory=False)

                elif fit_iteration_parameters_dict is not None:
                    logger.info("Generating ClientDataset from fit iteration params dictionary.")
                    dataset = training_utilities.init_client_dataset_from_fit_iteration_params(
                        fit_iteration_parameters_dict=fit_iteration_parameters_dict,
                        automl_settings=automl_settings,
                        remote=remote,
                        keep_in_memory=False
                    )
                else:
                    raise PipelineRunException(
                        "Can't create a ClientDataset without transformed_data_context or "
                        "fit_iteration_parameters_dict",
                        target=PipelineRunException.PIPELINE_RUN_REQUIREMENTS,
                        has_pii=False)

            # Check if dataset is set for training
            if dataset is None:
                raise PipelineRunException("Can't continue without a dataset object",
                                           target=PipelineRunException.PIPELINE_RUN_REQUIREMENTS,
                                           reference_code=ReferenceCodes._FIT_PIPELINE_DATASET_NONE,
                                           has_pii=False)

            # Check remaining time before pipeline run
            # If no time remaining, raises TimeoutException
            iteration_timeout_min = _check_iteration_time(
                automl_settings,
                constants.FitPipelineComponentName.PREPRARE_DATA,
                start_time,
                automl_pipeline.is_ensemble_pipeline,
                elapsed_time
            )

            # Fit Pipeline
            try:
                telemetry_logger.send_usage_telemetry_log(
                    prefix_message="[RunId:{}][Before executing pipeline]".format(automl_run_context.run_id)
                )

                # Run Pipeline
                pipeline_run_output = pipeline_run_helper.run_pipeline(automl_settings,
                                                                       automl_pipeline,
                                                                       automl_run_context,
                                                                       iteration_timeout_min,
                                                                       dataset,
                                                                       remote)
                fit_output.record_pipeline_results(pipeline_run_output)

                # Check the result of pipeline run output.
                _check_fit_output_result(fit_output)

                logger.info("Pipeline execution finished with a score of {0}".format(fit_output.score))

                telemetry_logger.send_usage_telemetry_log(
                    prefix_message="[RunId:{}][After executing pipeline]".format(automl_run_context.run_id)
                )
            except (AutoMLException, AzureMLServiceException, AzureMLException) as e:
                fit_output.add_error('fit', e)
                raise
            except Exception as e:
                fit_output.add_error('fit', e)
                raise PipelineRunException.from_exception(e).with_generic_msg(
                    "Training child iteration failed for unexpected reason.")

            with automl_run_context.get_run() as run:
                # Save model and log metrics
                with logging_utilities.log_activity(
                        logger,
                        activity_name=constants.TelemetryConstants.METRIC_AND_SAVE_MODEL_NAME,
                        custom_dimensions={'run_id': automl_run_context.run_id}):

                    try:
                        telemetry_logger.send_usage_telemetry_log(
                            prefix_message="[RunId:{}][Start artifact save in fit pipeline]".format(
                                automl_run_context.run_id
                            )
                        )

                        _save_artifacts(fit_output, dataset, automl_settings, automl_run_context, automl_settings.path)

                        telemetry_logger.send_usage_telemetry_log(
                            prefix_message="[RunId:{}][End artifact save in fit pipeline]".format(
                                automl_run_context.run_id
                            )
                        )
                    except (AutoMLException, AzureMLServiceException, AzureMLException):
                        raise
                    except Exception as e:
                        ex = ClientException.from_exception(
                            e, target="SaveArtifact", reference_code=ReferenceCodes._FIT_PIPELINE_SAVE_ARTIFACT) \
                            .with_generic_msg("Failed to get scoring file.")
                        fit_output.add_error(constants.ARTIFACT_TAG, ex)
                        raise ex

                    # Save CV trained models
                    need_CV_trained_models = automl_settings.enable_ensembling or \
                        automl_settings.enable_stack_ensembling
                    if need_CV_trained_models and \
                            fit_output.fitted_pipelines_train != constants.Defaults.INVALID_PIPELINE_OBJECT:
                        # we need to persist the partially trained fitted models as well
                        # they will be used for computing the scores during ensemble hill climbing
                        logger.info("Save CV trained models.")
                        automl_run_context.save_model_output(
                            fit_output.fitted_pipelines_train, constants.MODEL_PATH_TRAIN, automl_settings.path)

                # Convert pipeline into ONNX
                if onnx_cvt is not None and automl_settings.enable_onnx_compatible_models:
                    with logging_utilities.log_activity(
                            logger,
                            activity_name=constants.TelemetryConstants.ONNX_CONVERSION,
                            custom_dimensions={'run_id': automl_run_context.run_id}):
                        # Convert to ONNX if user indicates using ONNX compatible models,
                        # after we got this valid fitted_pipeline.
                        # Inject the exp name, run id data into the onnx model.
                        onnx_mdl_name = 'AutoML_ONNX_Model_[{}]'.format(run.id)
                        exp_name = ''
                        if hasattr(run, 'experiment') and run.experiment is not None and \
                                hasattr(run.experiment, 'name'):
                            exp_name = run.experiment.name
                        onnx_mdl_desc = {
                            'AutoMLSDKVer': onnx_cvt.producer_version,
                            'ExperimentName': exp_name,
                            'RunId': run.id,
                            'PipeId': automl_pipeline.pipeline_id
                        }
                        telemetry_logger.send_usage_telemetry_log(
                            prefix_message="[RunId:{}][Start ONNX Convert in fit pipeline]".format(
                                automl_run_context.run_id
                            )
                        )
                        onnx_model, featurizer_onnx_model, estimator_onnx_model, _ = \
                            onnx_cvt.convert(raw_model=fit_output.fitted_pipeline,
                                             model_name=onnx_mdl_name,
                                             model_desc=onnx_mdl_desc)
                        telemetry_logger.send_usage_telemetry_log(
                            prefix_message="[RunId:{}][End ONNX Convert in fit pipeline]".format(
                                automl_run_context.run_id
                            )
                        )
                        # If the converted onnx model is valid, save the ONNX model.
                        if onnx_model is not None:
                            automl_run_context.save_onnx_model_output(onnx_model,
                                                                      constants.MODEL_PATH_ONNX,
                                                                      automl_settings.path)
                            fit_output.set_onnx_model(onnx_model)
                            onnx_resource = onnx_cvt.get_converted_onnx_model_resource()
                            fit_output.set_onnx_model_resource(onnx_resource)
                            if onnx_resource:
                                automl_run_context.save_onnx_model_resource(
                                    onnx_resource, constants.MODEL_RESOURCE_PATH_ONNX, automl_settings.path)
                        if automl_settings.enable_split_onnx_featurizer_estimator_models:
                            # Save the splited onnx models.
                            if featurizer_onnx_model is not None:
                                automl_run_context.save_onnx_model_output(featurizer_onnx_model,
                                                                          OnnxConvertConstants.FeaturizerOnnxModelPath,
                                                                          automl_settings.path)
                                fit_output.set_onnx_featurizer_model(featurizer_onnx_model)
                            if estimator_onnx_model is not None:
                                automl_run_context.save_onnx_model_output(estimator_onnx_model,
                                                                          OnnxConvertConstants.EstimatorOnnxModelPath,
                                                                          automl_settings.path)
                                fit_output.set_onnx_estimator_model(estimator_onnx_model)

                # Log metric scores
                _log_metrics(run, fit_output.scores)
                _log_metrics_info(fit_output.scores, pipeline_id=fit_output.pipeline_id,
                                  run_id=automl_run_context.run_id)

                # Log time spent to complete the training and check how much time is remaining
                remaining_time = _check_iteration_time(
                    automl_settings, constants.FitPipelineComponentName.COMPLETE_RUN, start_time,
                    automl_pipeline.is_ensemble_pipeline, elapsed_time,
                    raise_exception=False
                )

                # Get model explain for this child run after the pipeline fit runs successfully.
                if automl_settings.model_explainability:
                    if bypassing_model_explain is None:
                        # Check if there's time to perform model explain
                        if automl_settings.iteration_timeout_minutes is None or remaining_time is None or \
                                remaining_time > automl_settings.iteration_timeout_minutes / 2:
                            with logging_utilities.log_activity(
                                    logger,
                                    activity_name=constants.TelemetryConstants.MODEL_EXPLANATION,
                                    custom_dimensions={'run_id': automl_run_context.run_id}):
                                telemetry_logger.send_usage_telemetry_log(
                                    prefix_message="[RunId:{}][Start model explain in fit pipeline]".format(
                                        automl_run_context.run_id
                                    )
                                )
                                try:
                                    with dataset.open_dataset():
                                        from azureml.train.automl.runtime.automl_explain_utilities import \
                                            _automl_auto_mode_explain_model
                                        _automl_auto_mode_explain_model(
                                            run, dataset, automl_settings,
                                            logger, fit_output.fitted_pipeline,
                                            model_exp_feature_config=cast(Dict[str, Any], feature_configs).get(
                                                'model_explainability'))
                                except Exception as e:
                                    fit_output.add_error(constants.MODEL_EXPLANATION_TAG, e,
                                                         is_critical=False)
                                    logging_utilities.log_traceback(e, logger, is_critical=False)
                                    logger.warning(
                                        "[RunId:{}]Failed model explanation in fit pipeline.".format(run.id)
                                    )
                                telemetry_logger.send_usage_telemetry_log(
                                    prefix_message="[RunId:{}][End model explain in fit pipeline]".format(
                                        automl_run_context.run_id
                                    )
                                )
                        else:
                            # model_explain is enabled but not have enough time.
                            logger.warning("Remaining time is not enough for model explanation.")
                            print("Remaining time is not enough for model explanation. "
                                  "Please use the workflow described at " + _get_valid_notebook_path_link())
                    else:
                        logger.info("Bypassing model explanations as the explanations for the best run "
                                    "will be performed during training")

                _update_run_with_fit_output(automl_run_context, fit_output, resource_tracker, telemetry_logger)

                # Mark the run as completed, with a retry
                # todo Have JOS set the child run status (it already is for the Parent Run)
                _mark_run_as_complete(run, automl_run_context.run_id)
                return fit_output
    except KeyboardInterrupt:
        logger.warning("Received a KeyboardInterrupt, cancelling the run.")
        # User requested to quickly bail out - raise this exception as is, skip any non-essential state setting
        try:
            with automl_run_context.get_run() as run:
                run.cancel()
        except AzureMLServiceException as e:
            logging_utilities.log_traceback(e, logger)
            logger.error("Failed to mark the run as Canceled due to an error on the service.")
        raise
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        # TODO: Bug #657527 fix nativeclient and local runs to handle is_critical
        #  and add exception to fit_output as non critical exception instead of logging
        if 'is_critical' not in fit_output.errors.values():
            fit_output.add_error('overall', e)
        try:
            with automl_run_context.get_run() as run:
                if isinstance(e, TimeoutException):
                    logger.warning(
                        "Cancelling the Run {} due to timeout.".format(str(automl_run_context.run_id))
                    )
                    run.cancel()
                else:
                    run._fail_with_error(e)
        except AzureMLServiceException as e:
            logging_utilities.log_traceback(e, logger)
            logger.error("Failed to mark the run as Canceled/Failed, due to an error on the service.")
        finally:
            _update_run_with_fit_output(automl_run_context, fit_output, resource_tracker, telemetry_logger)
            return fit_output


def _update_run_with_fit_output(automl_run_context: AutoMLAbstractRunContext, fit_output: FitOutput,
                                resource_tracker: cpu_utilities.ResourceUsageTracker,
                                telemetry_logger: SystemResourceUsageTelemetry) -> None:
    # TODO: remove once backend can handle nulls
    fit_output_sanitized = fit_output.get_sanitized_output_dict()
    with automl_run_context.get_run() as run:
        # Check to see if any property already exists, and exclude if already present
        fit_output_sanitized.update({
            'dependencies_versions': json.dumps(package_utilities.get_sdk_dependencies())
        })

        # Add v2 metrics to properties
        fit_output_sanitized.update({
            'num_cores': cpu_utilities.get_cpu_core_count(),
            'num_logical_cores': cpu_utilities.get_cpu_core_count(True),
            'peak_memory_usage': resource_tracker.peak_mem_usage,
            'vm_configuration': cpu_utilities.get_cpu_name(),
            'core_hours': resource_tracker.total_cpu_time / 3600
        })

        existing_properties = run.get_properties()
        run.add_properties({
            k: str(fit_output_sanitized[k])
            for k in fit_output_sanitized
            if k not in existing_properties
        })
    telemetry_logger.send_usage_telemetry_log(
        prefix_message="[RunId:{}][End fit_pipeline]".format(automl_run_context.run_id),
    )
    telemetry_logger.stop()


def _save_artifacts(fit_output: FitOutput,
                    dataset: DatasetBase,
                    automl_settings: AutoMLBaseSettings,
                    automl_run_context: AutoMLAbstractRunContext,
                    working_dir: str) -> None:
    # Container for location of files to be saved in the artifact store
    files_to_save = {}
    models_to_save = {constants.MODEL_PATH: fit_output.fitted_pipeline}

    with automl_run_context.get_run() as run:
        # Add dependencies path
        # log all dependencies
        all_dependencies = package_utilities._all_dependencies()
        # TODO Change to log only azureml packages
        # logger.info("All versions str:\n{}".format(json.dumps(all_dependencies)))
        files_to_save[constants.DEPENDENCIES_PATH] = json.dumps(all_dependencies, indent=4)

        # add conda environment file path
        is_text_dnn = hasattr(fit_output.fitted_pipeline, 'steps') and any(
            [getattr(step[1], "_is_text_dnn", False) for step in fit_output.fitted_pipeline.steps])
        try:
            files_to_save[constants.CONDA_ENV_FILE_PATH] = inference._create_conda_env_file(
                include_dnn_packages=is_text_dnn
            )
        except ImportError:
            # ModuleNotFoundError not exist in all python versions
            logger.warning("Skipping to create conda env file for native client. ")
        except Exception as e:
            ex = ClientException.from_exception(e, target="SaveArtifact",
                                                reference_code=ReferenceCodes._FIT_PIPELINE_CREATE_CONDA_ENV_FILE) \
                .with_generic_msg("Failed to get scoring file.")
            fit_output.add_error(constants.ARTIFACT_TAG, ex)
            raise ex

        # Add scoring file path and get model name to save
        if dataset.get_raw_data_type() is None and not automl_settings.enable_streaming:
            ex = ClientException("Failed to get scoring file: dataset's raw_data_type is not set.",
                                 has_pii=False, target="SaveArtifact",
                                 reference_code=ReferenceCodes._FIT_PIPELINE_DATASET_GET_RAW_DATA_TYPE)
            fit_output.add_error(constants.ARTIFACT_TAG, ex)
            raise ex
        try:
            # Models trained with streaming (i.e. Dataflow) can only infer on a pandas Dataframe
            if_pandas_type = (automl_settings.enable_streaming or
                              dataset.get_raw_data_type() == inference.PandasParameterType)
            scoring_file_str, model_name = inference._get_scoring_file(
                if_pandas_type=if_pandas_type,
                input_sample_str=dataset._get_raw_data_snapshot_str(),
                automl_run_id="{}".format(run.id),
                is_forecasting=automl_settings.is_timeseries)
            files_to_save[constants.SCORING_FILE_PATH] = scoring_file_str
        except Exception as e:
            ex = ClientException.from_exception(e, target="SaveArtifact",
                                                reference_code=ReferenceCodes._FIT_PIPELINE_GET_SCORING_FILE)\
                .with_generic_msg("Failed to get scoring file.")
            fit_output.add_error(constants.ARTIFACT_TAG, ex)
            raise ex

        # Add pipeline graph file (the graph can be an empty dict)
        # Visualization for streaming currently not supported
        try:
            if not automl_settings.enable_streaming:
                graph_json_dict = _transform_graph(fit_output.fitted_pipeline)  # type: Any
                files_to_save[constants.PIPELINE_GRAPH_PATH] = json.dumps(graph_json_dict, indent=4)
        except Exception as e:
            ex = ClientException.from_exception(e, target="SaveArtifact",
                                                reference_code=ReferenceCodes._FIT_PIPELINE_TRANSFORM_PIPELINE_GRAPH)\
                .with_generic_msg("Failed to transform graph and get pipeline graph file.")
            fit_output.add_error(constants.ARTIFACT_TAG, ex)
            raise ex

        try:
            automl_run_context.batch_save_artifacts(working_dir, files_to_save, models_to_save)
        except (AutoMLException, AzureMLServiceException, AzureMLException) as e:
            logging_utilities.log_traceback(e, logger)
            logger.error("Encountered an error on the service while uploading artifacts to the run.")
            fit_output.add_error(constants.ARTIFACT_TAG, e)
            raise e
        except Exception as e:
            ex = ServiceException.from_exception(e, target="SaveArtifact",
                                                 reference_code=ReferenceCodes._FIT_PIPELINE_ARTIFACT_BATCH_SAVE)\
                .with_generic_msg("Failed to batch save artifacts")
            logging_utilities.log_traceback(e, logger)
            logger.error("Encountered an error while uploading artifacts to the run. Exception type: {}".
                         format(e.__class__.__name__))
            fit_output.add_error(constants.ARTIFACT_TAG, ex)
            raise ex

        # Save artifact ids as run properties
        properties_to_add = automl_run_context._get_artifact_id_run_properties()
        properties_to_add.update({
            # This property signals to AutoML components (the SDK, JOS, and UI) whether the model is explainable.
            # The property was added because in the past, some AutoML models were not explainable.
            # We're keeping the property / plumbing around instead of deleting in case it ever needs to be used again.
            ModelExpSupportStr: str(True),

            inference.AutoMLInferenceArtifactIDs.PipelineGraphVersion: constants.PIPELINE_GRAPH_VERSION
        })
        if model_name:
            properties_to_add[inference.AutoMLInferenceArtifactIDs.ModelName] = model_name
        logger.info("Updating child run properties with model name {} and size {} bytes.".format(
            model_name, properties_to_add[inference.AutoMLInferenceArtifactIDs.ModelSizeOnDisk]))
        run.add_properties(properties_to_add)


def _mark_run_as_complete(run: RunType, run_id: str, delay: int = 5) -> None:
    logger.info("Marking the Run {} as Completed.".format(run_id))

    @retry_with_backoff(retries=3, delay=delay, backoff=2, logger=logger)
    def _complete():
        run._mark_run_as_complete()
        # If the run is not marked as Completed, (e.g. Network problems) raise an exception and retry
        # Note that get_status() will not result in an additional network call if the status was updated in the
        # previous call to complete(), in which case the cached result is returned
        current_status = run.get_status()
        if current_status != 'Completed':
            error_msg = "Failed to mark the Run {} as Completed. Last known status: {}".format(run_id, current_status)
            raise RunStateChangeException(error_msg, target="MarkRunComplete", has_pii=False)

    with logging_utilities.log_activity(logger=logger, activity_name="SetRunStatusToComplete"):
        _complete()


def _extract_data(fit_iteration_parameters_dict: Optional[Dict[str, Any]] = None,
                  transformed_data_context: Optional[TransformedDataContext] = None) -> \
        Tuple[Any, Any, Any, Any, Any, Any, Any, Any]:
    # if transformed_data_context is not None, then use data in transformed_data_context. If None, then to
    # use data in fit_iteration_parameters_dict.
    if transformed_data_context is not None:
        X = transformed_data_context.X
        y = transformed_data_context.y
        X_valid = transformed_data_context.X_valid
        y_valid = transformed_data_context.y_valid
        sample_weight = transformed_data_context.sample_weight
        sample_weight_valid = transformed_data_context.sample_weight_valid
        cv_splits_indices = transformed_data_context.cv_splits_indices
        x_raw_column_names = transformed_data_context.x_raw_column_names
    elif fit_iteration_parameters_dict is not None:
        X = fit_iteration_parameters_dict.get('X')
        y = fit_iteration_parameters_dict.get('y')
        X_valid = fit_iteration_parameters_dict.get('X_valid')
        y_valid = fit_iteration_parameters_dict.get('y_valid')
        sample_weight = fit_iteration_parameters_dict.get('sample_weight')
        sample_weight_valid = fit_iteration_parameters_dict.get('sample_weight_valid')
        cv_splits_indices = fit_iteration_parameters_dict.get('cv_splits_indices')
        x_raw_column_names = fit_iteration_parameters_dict.get('x_raw_column_names')
    else:
        raise PipelineRunException(
            "Either a transformed data context or parameters dict is required to extract data.",
            target=PipelineRunException.PIPELINE_RUN_REQUIREMENTS,
            has_pii=False)
    return X, y, X_valid, y_valid, sample_weight, sample_weight_valid, cv_splits_indices, x_raw_column_names


# helper function to create edges
def edge_helper(source_node_id: Optional[str],
                source_node_name: Optional[str],
                source_name: Optional[str],
                target_name: Optional[str],
                dst_node_id: Optional[str],
                dst_node_name: Optional[str],
                graph_json_dict: Dict[str, Any]) -> None:
    edge = {}  # type: Dict[str, Any]
    edge['source_node_id'] = source_node_id
    edge['source_node_name'] = source_node_name
    edge['source_name'] = source_name
    edge['target_name'] = target_name
    edge['dst_node_id'] = dst_node_id
    edge['dst_node_name'] = dst_node_name
    graph_json_dict['edges'].append(edge)


def _transform_graph(fitted_model: sklearn.pipeline.Pipeline) -> Any:
    feature_summary_dict = defaultdict()  # type: Any

    # check preprocess is set to True by the user
    is_preprocess = False
    for step in fitted_model.steps:
        if step[0] == 'datatransformer' or step[0] == 'timeseriestransformer':
            is_preprocess = True
            break
    if not is_preprocess:
        # TODO returned the datasource node
        # along with the fitted_pipeline nodes (scaler + final estimator)
        return {}

    model_lst = []
    # append schema_name and version to differenciate different json files in the future
    # initialize the keys
    complete_graph_json_dict = defaultdict()  # type: Any
    complete_graph_json_dict["schema_name"] = "pipeline_graph"
    complete_graph_json_dict["schema_version"] = "1.0.0"
    graph_json_dict = defaultdict()  # type: Any
    graph_json_dict['module_nodes'] = {}
    graph_json_dict['edges'] = []
    graph_json_dict['child_runs'] = []

    for step in fitted_model.steps:
        if step[0] == 'datatransformer' or step[0] == 'timeseriestransformer':
            total_col = 0
            for summary in step[1].get_featurization_summary():
                total_col += 1
                feature_count = str(summary['EngineeredFeatureCount'])
                if summary['TypeDetected'] in feature_summary_dict:
                    tf = ' '.join(summary['Transformations'])
                    feature_summary_dict[summary['TypeDetected']][tf].append(summary['RawFeatureName'])
                    feature_summary_dict[summary['TypeDetected']]['EngineeredFeatureCount'] = [feature_count]
                else:
                    transformation_col_dict = defaultdict(list)  # type: Any
                    tf = ' '.join(summary['Transformations'])
                    transformation_col_dict[tf].append(summary['RawFeatureName'])
                    transformation_col_dict['EngineeredFeatureCount'] = [feature_count]
                    feature_summary_dict[summary['TypeDetected']] = transformation_col_dict

        else:
            md_id = uuid.uuid4().hex[:8]
            model = {'node_id': md_id, 'model_name': step[0]}
            graph_json_dict['module_nodes'][md_id] = {
                'node_id': md_id,
                'name': step[0],
                'status': 'model'
            }
            model_lst.append(model)

    name = 'data_source - ' + str(total_col) + " col"
    src_id = uuid.uuid4().hex[:8]
    graph_json_dict['datasource_nodes'] = {src_id: {'node_id': src_id, 'name': name}}

    # Each run will have a graph_json_dict that contains the information of data_source_nodes,
    # module_nodes, edges

    for i in range(len(model_lst) - 1):
        edge_helper(model_lst[i]['node_id'], "", "",
                    "", model_lst[i + 1]['node_id'], "",
                    graph_json_dict)

    for i, data_type in enumerate(feature_summary_dict):
        ds_id = uuid.uuid4().hex[:8]
        graph_json_dict['module_nodes'][ds_id] = {
            'node_id': ds_id,
            'name': data_type,
            'status': 'dataType'
        }
        # connect the data source to all the data types, display incoming col number and outgoing col number
        # calculate number of cols that go into every data type
        num_col_per_type = 0
        for key, val in feature_summary_dict[data_type].items():
            if key != 'EngineeredFeatureCount':
                num_col_per_type += len(val)
        target_name = str(num_col_per_type) + " col"
        edge_helper(src_id, 'data_source', "", target_name, ds_id, data_type, graph_json_dict)
        # connect each operation with the model, data type and chain up the models
        for key, val in feature_summary_dict[data_type].items():
            operation_id_lst = []
            if key != '' and key != 'EngineeredFeatureCount':
                operation_lst = key.split()
                for j, op in enumerate(operation_lst):
                    op_id = uuid.uuid4().hex[:8]
                    operation_dict = {'node_id': op_id, 'op_name': op}
                    operation_id_lst.append(operation_dict)
                    graph_json_dict['module_nodes'][op_id] = {
                        'node_id': op_id,
                        'name': op,
                        'status': 'operation'
                    }
                    # chain up the operation
                    # first operation, connect with feature_summary_dict type nodes
                    if j == 0:
                        edge_helper(ds_id, "", "", "", op_id, "", graph_json_dict)
                    # last operation connect with model node
                    if j == len(operation_lst) - 1:
                        if (len(model_lst) > 0):
                            output_name = feature_summary_dict[data_type]['EngineeredFeatureCount'][0] + " col"
                            edge_helper(op_id, "", "", output_name, model_lst[0]['node_id'],
                                        "", graph_json_dict)
                    # inbetween operations
                    if j > 0:
                        edge_helper(operation_id_lst[j - 1]['node_id'], "",
                                    "", "", op_id, "", graph_json_dict)

    complete_graph_json_dict['data'] = graph_json_dict
    return complete_graph_json_dict


def _check_iteration_time(automl_settings: AutoMLBaseSettings,
                          component_name: str,
                          start_time: datetime.datetime,
                          is_ensemble_pipeline: bool = False,
                          elapsed_time: Optional[int] = None,
                          raise_exception: Optional[bool] = True) -> Optional[int]:
    # Check Time Spent So Far for the Component
    running_min = (datetime.datetime.now() - start_time).total_seconds() / 60.
    logger.info("Component {} finished after {} minutes.".format(component_name, running_min))

    # Check Iteration Time
    iteration_timeout_min = automl_settings.iteration_timeout_minutes
    if iteration_timeout_min is not None:
        iteration_timeout_min = math.ceil(iteration_timeout_min - running_min)
        if iteration_timeout_min <= 0 and raise_exception:
            raise TimeoutException(
                "Iteration ran for {min} minutes. {err_msg}".format(
                    min=math.floor(running_min),
                    err_msg=constants.ClientErrors.EXCEEDED_ITERATION_TIMEOUT_MINUTES),
                target="CheckIterationTime",
                reference_code=ReferenceCodes._FIT_PIPELINE_ITERATION_TIMEOUT,
                has_pii=False)

    # Check Experiment Time
    # If experiment is already over and in Voting/Stack Ensemble, then skip this check
    if not is_ensemble_pipeline:
        if automl_settings.experiment_timeout_minutes is not None and elapsed_time is not None:
            remaining_experiment_min = math.ceil(
                int(automl_settings.experiment_timeout_minutes) - elapsed_time - running_min
            )
            if remaining_experiment_min <= 0 and raise_exception:
                raise TimeoutException(
                    "Experiment ran for {min} minutes. {err_msg}".format(
                        min=math.floor(elapsed_time + running_min),
                        err_msg=constants.ClientErrors.EXCEEDED_EXPERIMENT_TIMEOUT_MINUTES),
                    target="CheckIterationTime",
                    reference_code=ReferenceCodes._FIT_PIPELINE_EXPERIMENT_TIMEOUT,
                    has_pii=False)
            # Update iteration timeout if remaining experiment min is smaller
            if iteration_timeout_min is None or remaining_experiment_min < iteration_timeout_min:
                iteration_timeout_min = remaining_experiment_min

    return iteration_timeout_min


def _log_metrics_info(scores, pipeline_id=None, run_id=None):
    reduced_scores = _get_reduced_scores(scores)
    log_fmt = "run_id:{}, pipeline_id:{},The following metrics have been logged for the child run: {}."
    logger.info(log_fmt.format(run_id, pipeline_id, reduced_scores))


def _get_reduced_scores(scores):
    reduced_scores = dict()
    for name, score in scores.items():
        is_score_NoneOrNumeric = score is None or isinstance(score, int) or isinstance(score, float)
        if name in constants.Metric.SCALAR_FULL_SET or is_score_NoneOrNumeric:
            reduced_scores[name] = score
        else:
            reduced_scores[name] = type(score)
    return reduced_scores


def _log_metric_failure_warning(metric_name: str, metric_value: str) -> None:
    logger.warning("Failed to log the metric {} with value {}.".format(metric_name, metric_value))


def _log_metrics(child_run, scores):
    # First, log all scalar metrics. Scalar metrics are batched to RH servers,
    # so logging them all at once can lead to more optimal batches
    non_scalar_metrics = {}
    for name, score in scores.items():
        try:
            if name in constants.Metric.SCALAR_FULL_SET:
                child_run.log(name, score)
            else:
                non_scalar_metrics[name] = score
        except Exception:
            _log_metric_failure_warning(name, score)

    # Log the non-scalar metrics. (Currently, these are all artifact-based.)
    for name, score in non_scalar_metrics.items():
        try:
            if name == constants.Metric.AccuracyTable:
                child_run.log_accuracy_table(name, score)
            elif name == constants.Metric.ConfusionMatrix:
                child_run.log_confusion_matrix(name, score)
            elif name == constants.Metric.Residuals:
                child_run.log_residuals(name, score)
            elif name == constants.Metric.PredictedTrue:
                child_run.log_predictions(name, score)
            # TODO support these schemas before logging them:
            # elif name == constants.Metric.ForecastResiduals:
            #     child_run.log_residuals(name, score)
            # elif name == constants.Metric.ForecastMAPE:
            #     child_run.log_mape(name, score)
            else:
                logger.warning(
                    "Did not recognize metric: {}. Will not log.".format(name))
        except Exception:
            _log_metric_failure_warning(name, score)


def _check_fit_output_result(fit_output: FitOutput) -> None:
    """Check the run results."""
    if fit_output.score is None or np.isnan(fit_output.score) \
            or fit_output.score == constants.Defaults.DEFAULT_PIPELINE_SCORE:
        raise PipelineRunException(
            "Primary metric {} is not available.".format(fit_output.primary_metric),
            target=PipelineRunException.PIPELINE_OUTPUT).with_generic_msg("Primary metric is not available.")

    if fit_output.fitted_pipeline == constants.Defaults.INVALID_PIPELINE_OBJECT:
        raise PipelineRunException(
            "Fitted model is empty.", target=PipelineRunException.PIPELINE_OUTPUT, has_pii=False)
