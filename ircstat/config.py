# Copyright 2013 John Reese
# Licensed under the MIT license

import json

from os import path

def read_config(filepath, defaults=None):
    """Read configuration from a given file path, by executing the contents as
    python code within a sandboxed set of globals.  Default values may be
    passed in as a dictionary to pre-populate the set of locals.  The returned
    value is the resulting dictionary of local values after executing the
    configuration file."""

    filepath = path.realpath(filepath)

    if not path.isfile(filepath):
        raise ValueError('config path "%s" does not exist' % filepath)

    g = {"__builtins__": {}}
    config = {}

    if defaults is not None:
        config.update(defaults)

    with open(filepath) as fh:
        data = fh.read()

    data = compile(data, filepath, 'exec')
    exec(data, g, config)

    return config
