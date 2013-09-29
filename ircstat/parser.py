# Copyright 2013 John Reese
# Licensed under the MIT license

import os
import re

from collections import defaultdict, OrderedDict
from datetime import datetime
from os import path

from .ent import Struct, Conversation, Message
from .log import logger
from .lib import canonical, ignore

log = logger(__name__)


class LogParser(Struct):
    """Parse a set of logs, and generate statistics for the entire set of logs,
    a set of channels, and a set of users."""
    def __init__(self, config):
        message_types = OrderedDict([
            (Message.MESSAGE, re.compile(config.log_message_regex)),
            (Message.ACTION, re.compile(config.log_action_regex)),
            (Message.JOIN, re.compile(config.log_join_regex)),
            (Message.PART, re.compile(config.log_part_regex)),
            (Message.QUIT, re.compile(config.log_quit_regex)),
        ])
        Struct.__init__(self,
                        config=config,
                        message_types=message_types,
                        matched=0,
                        unmatched=0,
                        )

    def parse_log(self, file_path):
        """Given a single path to a log file, parse the file and return a list
        of messages from the conversation."""

        messages = []

        log.debug('parsing log file "%s"', file_path)

        with open(file_path, encoding=self.config.log_encoding) as logfile:
            lineno = 1
            for line in logfile:
                for message_type, message_regex in self.message_types.items():
                    match = message_regex.match(line)
                    if match:
                        content = match.groupdict()

                        content['nick'] = canonical(content['nick'])
                        if ignore(content['nick']):
                            break

                        content['time'] = datetime.strptime(
                            content['time'],
                            self.config.log_timestamp_format,
                            ).time()
                        messages.append(Message(message_type,
                                                **content))
                        self.matched += 1
                        break

                if not match:
                    log.debug('line %d did not match anything', lineno)
                    self.unmatched += 1

                lineno += 1

        return messages

    def parse_logs(self, input_paths):
        """Given a list of directories, search those directories for log files
        matching the configured filename regex, and then send each file for
        individual parsing."""

        conversations = defaultdict(lambda: defaultdict(bool))

        filename_regex = re.compile(self.config.filename_regex)

        for input_path in input_paths:
            input_path = path.realpath(input_path)

            if not path.isdir(input_path):
                log.warning('input path "%s" does not exist, skipping',
                            input_path)
                continue

            log.debug('walking input directory "%s"', input_path)

            for dir_path, subdirs, filenames in os.walk(input_path):
                log.debug((dir_path, filenames, subdirs))

                for filename in filenames:
                    match = filename_regex.search(filename)

                    if not match:
                        log.debug('skipping file "%s"', filename)
                        continue

                    file_path = path.join(dir_path, filename)
                    channel = match.group('channel')
                    datestr = match.group('date')
                    date = datetime.strptime(datestr,
                                             self.config.filename_date_format,
                                             ).date()

                    messages = self.parse_log(file_path)
                    conversation = Conversation(channel, date, messages)
                    conversations[channel][date] = conversation

        log.debug('parsing all input paths complete')
        log.debug('%d log lines matched regexes', self.matched)
        log.debug('%d log lines unmatched', self.unmatched)

        return conversations
