# Copyright 2013 John Reese
# Licensed under the MIT license

import logging

logging.addLevelName(logging.DEBUG, 'DBG')
logging.addLevelName(logging.INFO, 'INF')
logging.addLevelName(logging.WARNING, 'WRN')
logging.addLevelName(logging.ERROR, 'ERR')

sh = None


def logger(name=None):
    """Create and return a logger that will print to terminal, by default
    at info level or higher."""
    global sh

    if sh is None:
        root_log = logging.getLogger()
        root_log.setLevel(logging.DEBUG)

        fm = logging.Formatter('%(message)s')

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(fm)

        root_log.addHandler(sh)

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    return log


def enable_debug():
    """Modify the shared StreamHandler to increase logging to debug level, and
    update the formatting to include the message level and module name."""
    fm = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(fm)
