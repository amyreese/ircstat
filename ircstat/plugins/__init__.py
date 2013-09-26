# Copyright 2013 John Reese
# Licensed under the MIT license

import importlib
import os

from functools import lru_cache
from os import path

from .base import Plugin

@lru_cache()
def load_plugins(config):
    """Import all the plugins, and return a set of plugin instances, filtering
    out any plugin whose name appears in the configurable blacklist."""

    cwd = path.abspath(path.dirname(__file__))
    files = os.listdir(cwd)

    for filename in files:
        name, ext = path.splitext(filename)

        if name.startswith('_'):
            continue

        if ext == '.py':
            importlib.import_module('ircstat.plugins.' + name)

    plugins = set(plugin() for plugin in Plugin.subclasses())

    for plugin in plugins:
        if plugin.name in config.plugin_blacklist:
            plugins.remove(plugin)

    return plugins
