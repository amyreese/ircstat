# Copyright 2013 John Reese
# Licensed under the MIT license

from collections import defaultdict

class Struct(object):
    """A basic object type that, given a dictionary or keyword arguments,
    converts the key/value pairs into object attributes."""
    def __init__(self, data=None, **kwargs):
        if data is not None:
            self.__dict__.update(data)
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__dict__)


class UserStat(Struct):
    """Store key/value pairs for a single user."""
    def __init__(self, nick):
        Struct.__init__(self,
                        nick=nick,
                        stats=defaultdict(int))


class DailyStat(Struct):
    """Store key/value pairs for the day, and for a set of users."""
    def __init__(self, date):
        Struct.__init__(self,
                        date=date,
                        users=defaultdict(UserStat),
                        stats=defaultdict(int))


class ChannelStat(Struct):
    """Store key/value pairs for a given channel, a set of days, and for
    a set of users."""
    def __init__(self, channel):
        Struct.__init__(self,
                        channel=channel,
                        users=defaultdict(UserStat),
                        days=defaultdict(DailyStat),
                        stats=defaultdict(int))


class NetworkStat(Struct):
    """Store key/value pairs for a network, a set of channels, and for
    a set of users."""
    def __init__(self):
        Struct.__init__(self,
                        channels=defaultdict(ChannelStat),
                        users=defaultdict(UserStat),
                        stats=defaultdict(int))
