# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Functionality to execute a function in a child process created using "spawn".

This file contains the server portion.
"""
import dill
import logging
import sys

from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.fake_traceback import FakeTraceback


def run_server(config_file_name, input_file_name, output_file_name):
    """Run the server."""
    try:
        # Deserialize the configuration object using dill.
        with open(config_file_name, 'rb') as f:
            config = dill.load(f)

        # Initialize system path to match parent process configuration.
        sys.path = config['path']

        # Deserialize the input file using dill.
        with open(input_file_name, 'rb') as f:
            obj = dill.load(f)

        # Set verbosity after loading function, since deserialization can cause dependencies to set the log level.
        log_server.set_verbosity(config['log_verbosity'])

        # Deconstruct the input into function, arguments, keywords arguments.
        fn, args, kwargs = obj

        # Invoke the function and store the result in a (value, error) pair.
        # TODO: Currently this code assumes that the called function will already return such a pair. Need to fix.
        ret, ex = fn(*args, **kwargs)
    except BaseException as e:
        ret = None
        ex = e

    res = (ret, ex, FakeTraceback.serialize_exception_tb(ex))

    # Write the result to the output file using dill.
    with open(output_file_name, 'wb') as f:
        dill.dump(res, f)


if __name__ == "__main__":
    # Check command-line arguments.
    if len(sys.argv) != 4:
        print("Usage: spawn_server config_file input_file output_file")
        exit(2)

    # Extract configuration, input, and output file names.
    config_file_name = sys.argv[1]
    input_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    try:
        run_server(config_file_name, input_file_name, output_file_name)
    except Exception as e:
        sys.stderr.write('{}\n'.format(e))
        exit(2)
