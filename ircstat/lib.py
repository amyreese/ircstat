# Copyright 2013 John Reese
# Licensed under the MIT license

import re

from functools import lru_cache

config = None
def push_config(new_config):
    """Update the configuration being used by all the library functions.
    This should not be used by anything but core."""
    global config
    config = new_config

def is_bot(nick):
    """Determine if a nick a bot based on a configurable list of bots."""
    return nick in config.bots

@lru_cache()
def canonical(nick):
    """Determine the canonical representation for nick based on a configurable
    set of aliases, using regex matching, with cached results."""
    global _aliases
    nick = nick.lower()

    if _aliases is None:
        _aliases = {re.compile(k + '$'): v.lower()
                    for k, v in config.aliases.items()}

    for regex in _aliases:
        if regex.match(nick):
            return _aliases[regex]

    return nick

_aliases = None
