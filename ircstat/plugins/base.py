# Copyright 2013 John Reese
# Licensed under the MIT license

from ..ent import Struct
from ..log import logger

log = logger(__name__)

class Plugin(Struct):
    """A pluggable class for generating and displaying message statistics."""
    def __init__(self):
        name = self.__class__.__name__
        log.debug('Instantiating plugin %s', name)
        if name.endswith('Plugin'):
            name = name[:-6]
        Struct.__init__(self,
                        name=name)
