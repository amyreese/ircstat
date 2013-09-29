# Copyright 2013 John Reese
# Licensed under the MIT license

from ..lib import is_bot
from ..ent import Message
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
