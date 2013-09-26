# Copyright 2013 John Reese
# Licensed under the MIT license

import logging

logging.addLevelName(logging.DEBUG, 'DBG')
logging.addLevelName(logging.INFO, 'INF')
logging.addLevelName(logging.WARNING, 'WRN')
logging.addLevelName(logging.ERROR, 'ERR')

sh = None

def logger(name=None):
    global sh

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    if sh is None:
        fm = logging.Formatter('%(message)s')

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(fm)

    log.addHandler(sh)

    return log

def enable_debug():
    fm = logging.Formatter('%(levelname)s %(message)s')
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fm)
