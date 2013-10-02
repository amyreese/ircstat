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

    # a mapping of phrases to regexes that match the variants of the phrase
    phrases = {
        'lol': r'(lol|l\.o\.l)',
        'rofl': r'rofl',
        'haha': r'(ha|(ha|he)(ha|he)*)',
        'nice': r'^nice$',
        'hi': r'hi',
        'howdy': r'howdy',
        'morning': r'morning',
    }

    # this regex fragment wraps every regex
    word_regex = r'\b%s\b'

    def process_message(self, message):
        if is_bot(message) or not message.content:
            return

        nick = message.nick
        content = message.content.lower()

        if self._swears is None:
            self._swears = {swear: re.compile(self.word_regex % regex)
                            for swear, regex in self.swears.items()}
            self._phrases = {phrase: re.compile(self.word_regex % regex)
                             for phrase, regex in self.phrases.items()}

        swears = {swear: len(regex.findall(content))
                  for swear, regex in self._swears.items()}
        swears['total_swears'] = sum(swears.values())

        phrases = {phrase: len(regex.findall(content))
                   for phrase, regex in self._phrases.items()}
        phrases['total_phrases'] = sum(phrases.values())

        self.inc_shared_stats(nick, **swears)
        self.inc_shared_stats(nick, **phrases)

    def generate_graphs(self):
        return [
            NetworkKeyComparison(title='Swears Used',
                                 style='bar',
                                 keys={k: k for k in self.swears},
                                 ),
            NetworkUserComparison(title='Potty Mouths',
                                  style='bar',
                                  key='total_swears',
                                  ),
            NetworkKeyComparison(title='Phrases Used',
                                 style='bar',
                                 keys={k: k for k in self.phrases},
                                 ),
            NetworkUserComparison(title='Broken Records',
                                  style='bar',
                                  key='total_phrases',
                                  ),
        ]

    # cache compiled regexes
    _swears = None
    _phrases = None
