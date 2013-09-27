# Copyright 2013 John Reese
# Licensed under the MIT license

import re

from ..ent import Struct, NetworkStat
from ..log import logger

log = logger(__name__)

class Plugin(Struct):
    """A pluggable class for generating and displaying message statistics."""
    def __init__(self, config):
        Struct.__init__(self,
                        config=config,
                        **config.plugins.__dict__[self.name].__dict__)

    def process(self, conversations):
        """Process a list of conversations and return a NetworkStat object."""
        network = NetworkStat()

        for channel in conversations:
            channel_stats = network.channels[channel]

            for date, conversation in conversations[channel].items():
                daily_stats = channel_stats.days[date]

                self.process_conversation(conversation,
                                          network, channel_stats, daily_stats)

        return network

    def process_conversation(self, conversation, network, channel, day):
        """Process a single conversation, with the given network, channel, and
        daily statistics objects."""

        for message in conversation.messages:
            self.process_message(message, network, channel, day)

    def process_message(self, message, network, channel, day):
        """Process an individual message, with the given network, channel, and
        daily statistics objects."""
        raise NotImplementedError()
