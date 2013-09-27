# Copyright 2013 John Reese
# Licensed under the MIT license

VERSION = '0.1.0'

from collections import Counter, OrderedDict

from .ent import Message
from .log import logger
from .parser import LogParser
from .plugins import load_plugins

log = logger(__name__)

def do_everything(input_paths, output_path, config):
    """One entry point to rule them all."""

    parser = LogParser(config)
    conversations = parser.parse_logs(input_paths)

    log.info('found %d channels', len(conversations))
    for channel in conversations:
        log.info('channel %s has %d conversations', channel,
                 len(conversations[channel]))

    plugins = load_plugins(config)
    plugin_stats = {}

    for plugin in plugins:
        result = plugin.process(conversations)
        plugin_stats[plugin] = result

        log.debug(sorted(result.users.keys()))
