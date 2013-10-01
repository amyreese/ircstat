# Copyright 2013 John Reese
# Licensed under the MIT license

from ..ent import Struct, NetworkStat
from ..log import logger
from ..lib import month, week

log = logger(__name__)


class Plugin(Struct):
    """A pluggable class for generating and displaying message statistics."""
    def __init__(self, config):
        Struct.__init__(self,
                        config=config,
                        **config.plugins.__dict__[self.name].__dict__)

    def process(self, conversations):
        """Process a list of conversations and return a NetworkStat object."""
        self.network = NetworkStat()

        for channel in conversations:
            self.channel = self.network.channels[channel]

            for date, conversation in conversations[channel].items():
                self.day = self.channel.days[date]
                self.week = self.channel.weeks[week(date)]
                self.month = self.channel.months[month(date)]
                self.process_conversation(conversation)

        return self.network

    def process_conversation(self, conversation):
        """Process a single conversation, with the given network, channel, and
        daily statistics objects."""

        for message in conversation.messages:
            self.process_message(message)

    def process_message(self, message):
        """Process an individual message, with the given network, channel, and
        daily statistics objects."""
        raise NotImplementedError()

    def inc_user_stats(self, nick, **kwargs):
        """Increment user stat counters for the given key/value pairs."""
        for key, value in kwargs.items():
            self.network.users[nick].stats[key] += value
            self.channel.users[nick].stats[key] += value
            self.day.users[nick].stats[key] += value
            self.week.users[nick].stats[key] += value
            self.month.users[nick].stats[key] += value

    def inc_network_stats(self, **kwargs):
        """Increment aggregate stat counters for the given key/value pairs."""
        for key, value in kwargs.items():
            self.network.stats[key] += value
            self.channel.stats[key] += value
            self.day.stats[key] += value
            self.week.stats[key] += value
            self.month.stats[key] += value

    def inc_shared_stats(self, nick, **kwargs):
        """Increment shared user/aggregate stat counters."""
        self.inc_user_stats(nick, **kwargs)
        self.inc_network_stats(**kwargs)

    def generate_graphs(self):
        """Return a list of Graph objects."""

        return []
