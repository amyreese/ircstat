# Copyright 2013 John Reese
# Licensed under the MIT license

from collections import defaultdict

safe_types = (bool, int, float, str, tuple, list, dict, set)


class Struct(object):
    """A basic object type that, given a dictionary or keyword arguments,
    converts the key/value pairs into object attributes."""
    def __init__(self, data=None, **kwargs):
        if data is None:
            data = {}
        data.update(kwargs)

        # prevent overwriting values with unsafe callables
        for key, value in list(data.items()):
            if (key in self.__class__.__dict__ and
                    type(value) not in safe_types):
                data.pop(key)

        self.__dict__.update(data)

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
    MESSAGE = 1
    ACTION = 2
    JOIN = 3
    PART = 4
    QUIT = 5

    type_names = {
        MESSAGE: 'message',
        ACTION: 'action',
        JOIN: 'join',
        PART: 'part',
        QUIT: 'quit',
    }

    @staticmethod
    def type_to_name(message_type):
        return Message.type_names[message_type]

    def __init__(self, type, time=None, nick=None,
                 content=None, reason=None, hostmask=None):
        Struct.__init__(self,
                        type=type,
                        time=time,
                        nick=nick,
                        content=content,
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
    def __init__(self):
        Struct.__init__(self,
                        stats=defaultdict(int))


class DailyStat(Struct):
    """Store key/value pairs for the day, and for a set of users."""
    def __init__(self):
        Struct.__init__(self,
                        users=defaultdict(UserStat),
                        stats=defaultdict(int))


class WeeklyStat(Struct):
    """Store key/value pairs for a week, and for a set of users."""
    def __init__(self):
        Struct.__init__(self,
                        users=defaultdict(UserStat),
                        stats=defaultdict(int))


class MonthlyStat(Struct):
    """Store key/value pairs for a month, and for a set of users."""
    def __init__(self):
        Struct.__init__(self,
                        users=defaultdict(UserStat),
                        stats=defaultdict(int))


class ChannelStat(Struct):
    """Store key/value pairs for a given channel, a set of days, and for
    a set of users."""
    def __init__(self):
        Struct.__init__(self,
                        users=defaultdict(UserStat),
                        days=defaultdict(DailyStat),
                        weeks=defaultdict(WeeklyStat),
                        months=defaultdict(MonthlyStat),
                        stats=defaultdict(int))


class NetworkStat(Struct):
    """Store key/value pairs for a network, a set of channels, and for
    a set of users."""
    def __init__(self):
        Struct.__init__(self,
                        channels=defaultdict(ChannelStat),
                        users=defaultdict(UserStat),
                        stats=defaultdict(int))
