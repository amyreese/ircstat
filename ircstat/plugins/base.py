# Copyright 2013 John Reese
# Licensed under the MIT license

from ..ent import Struct
from ..log import logger

log = logger(__name__)

class Plugin(Struct):
    """A pluggable class for generating and displaying message statistics."""
    def __init__(self, config):
        Struct.__init__(self,
                        config=config,
                        **config.plugins.__dict__[self.name].__dict__)
