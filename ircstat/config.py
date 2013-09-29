# Copyright 2013 John Reese
# Licensed under the MIT license

import ircstat
from ircstat.ent import Config

from os import path

from .plugins import Plugin

log = ircstat.log.logger(__name__)


def read_config_file(filepath, defaults=None):
    """Read configuration from a given file path, by executing the contents as
    python code within a sandboxed set of globals.  Default values may be
    passed in as a dictionary to pre-populate the set of locals.  The returned
    value is the resulting dictionary of local values after executing the
    configuration file."""

    filepath = path.realpath(filepath)

    if not path.isfile(filepath):
        raise ValueError('config path "%s" does not exist' % filepath)

    log.debug('loading configuration from %s', filepath)

    g = {"__builtins__": {}}
    config = {'plugins': Config({p.name: Config()
                                for p in Plugin.subclasses()})}

    if defaults is not None:
        if isinstance(defaults, Config):
            config.update(defaults.__dict__)
        elif isinstance(defaults, dict):
            config.update(defaults)
        else:
            raise ValueError('defaults must be of type Config or dict')

    with open(filepath) as fh:
        data = fh.read()

    data = compile(data, filepath, 'exec')
    exec(data, g, config)

    return Config(config)


def read_default_config():
    """Read in the default configuration file (part of the ircstat module)."""
    here = path.dirname(path.realpath(__file__))
    filepath = path.join(here, 'defaults.py')

    return read_config_file(filepath)


def load_config(filepath=None):
    """Read in the given configuration file, overwriting the default values."""
    defaults = read_default_config()

    if filepath is not None:
        return read_config_file(filepath, defaults=defaults)
    else:
        return defaults
