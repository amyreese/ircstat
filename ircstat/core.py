# Copyright 2013 John Reese
# Licensed under the MIT license

VERSION = '0.1.0'

import os

from os import path

from .log import logger
from .lib import push_config
from .parser import LogParser
from .plugins import load_plugins

log = logger(__name__)


def do_everything(input_paths, output_path, config):
    """One entry point to rule them all."""
    push_config(config)

    parser = LogParser(config)
    conversations = parser.parse_logs(input_paths)

    log.info('found %d channels', len(conversations))
    for channel in conversations:
        log.info('channel %s has %d conversations', channel,
                 len(conversations[channel]))

    if not path.exists(output_path):
        os.makedirs(output_path)

    plugins = load_plugins(config)
    plugin_stats = {}

    for plugin in plugins:
        result = plugin.process(conversations)
        plugin_stats[plugin] = result

        for graph in plugin.generate_graphs():
            log.debug(graph)
            graph.prep(plugin, config, result)
            graph.render(output_path)
