# Copyright 2013 John Reese
# Licensed under the MIT license

import re

from ..lib import is_bot
from ..graphs import NetworkKeyComparison, NetworkUserComparison
from .base import Plugin


class Highbrow(Plugin):
    """Gathers metrics related to how intelligent the conversation (or users)
    may be, like swear words used, etc."""

    # a mapping of swears to regexes that match the variants of the word
    swears = {
        'ass': r'ass(es|hole)?',
        'crap': r'crap(s|py|ped)?',
        'shit': r'shits?',
        'fuck': r'fuck(s?|ing|ed)?',
        'damn': r'(god)?damn(n?it|ed)?',
        'hell': r'hell',
    }

    # this regex fragment wraps every swear regex
    swear_regex = r'\b%s\b'

    def process_message(self, message):
        if is_bot(message) or not message.content:
            return

        nick = message.nick
        content = message.content.lower()

        if self._swears is None:
            self._swears = {swear: re.compile(self.swear_regex % regex)
                            for swear, regex in self.swears.items()}

        swears = {swear: len(regex.findall(content))
                  for swear, regex in self._swears.items()}
        swears['total'] = sum(swears.values())

        self.inc_shared_stats(nick, **swears)

    def generate_graphs(self):
        return [
            NetworkKeyComparison(title='Swears Used',
                                 style='bar',
                                 keys={k: k for k in self.swears},
                                 ),
            NetworkUserComparison(title='Potty Mouths',
                                  style='bar',
                                  key='total',
                                  ),
        ]

    # cache compiled regexes
    _swears = None
