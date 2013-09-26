# Copyright 2013 John Reese
# Licensed under the MIT license

from collections import defaultdict
from ircstat import Struct, NetworkStat

class LogParser(Struct):
    """Parse a set of logs, and generate statistics for the entire set of logs,
    a set of channels, and a set of users."""
    def __init__(self, config):
        Struct.__init__(self,
                        config=config,
                        stats=NetworkStat())
