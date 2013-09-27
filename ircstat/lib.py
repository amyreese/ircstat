# Copyright 2013 John Reese
# Licensed under the MIT license

import re

from functools import lru_cache

from .ent import Message

config = None
def push_config(new_config):
    """Update the configuration being used by all the library functions.
    This should not be used by anything but core."""
    global config
    config = new_config

def is_bot(nick):
    """Determine if a nick a bot based on a configurable list of bots."""
    if type(nick) == Message:
        nick = nick.nick
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

@lru_cache()
def ignore(nick):
    """Determine if the nick should be ignored.  Assumes the nick has already
    been canonicalized before being passed here."""
    global _ignores

    if _ignores is None:
        _ignores = [re.compile(v + '$') for v in config.ignore]

    return any(regex.match(nick) for regex in _ignores)


_aliases = None
_ignores = None
