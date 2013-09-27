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

    @classmethod
    def subclasses(cls):
        """Return a set of all subclasses, recursively."""
        seen = set()
        queue = set([cls])

        while queue:
            c = queue.pop()
            seen.add(c)

            sc = c.__subclasses__()
            for c in sc:
                if c not in seen:
                    queue.add(c)

        seen.remove(cls)
        return seen


class Config(Struct):
    """A configuration subclass of Struct that isn't noisy."""
    def __repr__(self):
        return '<Config>'


class Message(Struct):
    """A single timestamped message."""
    MESSAGE=1
    ACTION=2
    JOIN=3
    PART=4
    QUIT=5

    def __init__(self, message_type, time=None, nick=None,
                 action=None, message=None, reason=None, hostmask=None):
        Struct.__init__(self,
                        message_type=message_type,
                        time=time,
                        nick=nick,
                        action=action,
                        message=message,
                        reason=reason,
                        hostmask=hostmask)


class Conversation(Struct):
    """Store an ordered list of messages for a single day and channel."""
    def __init__(self, channel, date, messages=None):
        if messages is None:
            messages = []
        Struct.__init__(self,
                        channel=channel,
                        date=date,
                        messages=messages)


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
