# Copyright 2013 John Reese
# Licensed under the MIT license

from ..ent import Message
from .base import Plugin

class Totals(Plugin):
    """Gathers total message type statistics, broken down by channel, day
    and user."""

    def process_message(self, message):
        nick = message.nick
        mtype = Message.type_to_name(message.type)

        self.inc_shared_stats(nick, mtype=1)
