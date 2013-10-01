# Copyright 2013 John Reese
# Licensed under the MIT license

from ..lib import is_bot
from ..ent import Message
from ..graphs import NetworkKeyComparison, NetworkUserComparison
from .base import Plugin


class Totals(Plugin):
    """Gathers total message type statistics, broken down by channel, day
    and user."""

    def process_message(self, message):
        nick = message.nick
        mtype = Message.type_to_name(message.type)
        kwargs = {
            mtype: 1,
        }

        self.inc_shared_stats(nick, **kwargs)

    def generate_graphs(self):
        return [
            NetworkKeyComparison(title='Logged Events',
                                 network=self.network,
                                 bars=True,
                                 keys={k: k
                                    for k in Message.type_names.values()},
                                 ),
            NetworkUserComparison(title='Channel Joins',
                                  network=self.network,
                                  bars=True,
                                  key=Message.type_to_name(Message.JOIN),
                                  log=True,
                                  ),
        ]


class Wordcount(Plugin):
    """Tracks the average word count of messages."""
    def process_message(self, message):
        if is_bot(message) or not message.content:
            return

        nick = message.nick
        word_count = len(message.content.split())

        self.inc_shared_stats(nick,
                              word_count_total=word_count,
                              word_count_messages=1,
                              )
