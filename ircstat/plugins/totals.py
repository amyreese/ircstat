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
                                 style='bar',
                                 keys={k: k
                                       for k in Message.type_names.values()},
                                 ),
            NetworkUserComparison(title='Channel Joins',
                                  style='pie',
                                  key=Message.type_to_name(Message.JOIN),
                                  ),
            NetworkUserComparison(title='Messages Sent',
                                  style='pie',
                                  key=Message.type_to_name(Message.MESSAGE)
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

    def generate_graphs(self):
        transform = lambda nick, v, net: (
            v / net.users[nick].stats['word_count_messages'])

        return [
            NetworkUserComparison(title='Words Spoken',
                                  style='pie',
                                  key='word_count_total',
                                  ),
            NetworkUserComparison(title='Average Word Count',
                                  style='bar',
                                  key='word_count_total',
                                  transform=transform,
                                  ),
        ]
