# Copyright 2013 John Reese
# Licensed under the MIT license

import calendar
import datetime
import re

from functools import lru_cache

from .ent import Message

config = None


def push_config(new_config):
    """Update the configuration being used by all the library functions.
    This should not be used by anything but core."""
    global config
    config = new_config


def today():
    """Return a date object representing today."""
    return datetime.date.today()


def ago(**kwargs):
    """Return a day object from the past based on the given arguments,
    which are passed to datetime.timedelta()."""
    return today() - datetime.timedelta(**kwargs)


def week(date):
    """Given a date object, return a new date object representing the
    beginning of the week in which the date took place."""
    return date - datetime.timedelta(days=date.isoweekday())


def month(date):
    """Given a date object, return a new date object representing the
    last day of the month in which the date took place."""
    return datetime.date(date.year, date.month, days_in_month(date))


def days_in_month(date):
    """Return the number of days in the month for the given date."""
    weekday, numdays = calendar.monthrange(date.year, date.month)
    return numdays


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
