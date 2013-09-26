# Copyright 2013 John Reese
# Licensed under the MIT license

class Struct(object):
    """A basic object type that, given a dictionary or keyword arguments,
    converts the key/value pairs into object attributes."""
    def __init__(self, data=None, **kwargs):
        if data is not None:
            self.__dict__.update(data)
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__dict__)
