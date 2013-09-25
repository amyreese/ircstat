# Copyright 2013 John Reese
# Licensed under the MIT license

import logging

logging.addLevelName(logging.DEBUG, 'DBG')
logging.addLevelName(logging.INFO, 'INF')
logging.addLevelName(logging.WARNING, 'WRN')
logging.addLevelName(logging.ERROR, 'ERR')

def logger(name=None):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    fm = logging.Formatter('%(levelname)s %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fm)

    log.addHandler(sh)

    return log
