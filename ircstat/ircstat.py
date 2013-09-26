# Copyright 2013 John Reese
# Licensed under the MIT license

VERSION = '0.1.0'

from collections import Counter, OrderedDict

from .ent import Message
from .log import logger
from .parser import LogParser

log = logger(__name__)

def do_everything(input_paths, output_path, config):
    """One entry point to rule them all."""

    parser = LogParser(config)
    conversations = parser.parse_logs(input_paths)

    log.info('found %d channels', len(conversations))
    for channel in conversations:
        log.info('channel %s has %d conversations', channel,
                 len(conversations[channel]))

    counter = Counter()

    for channel in conversations:
        for date, conversation in conversations[channel].items():
            for message in conversation.messages:
                counter[message.message_type] += 1

    counter = OrderedDict([
                          ('message', counter[Message.MESSAGE]),
                          ('action', counter[Message.ACTION]),
                          ('join', counter[Message.JOIN]),
                          ('part', counter[Message.PART]),
                          ('quit', counter[Message.QUIT]),
                          ])

    log.info(counter)
