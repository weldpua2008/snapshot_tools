import logging


__author__ = 'weldpua2008@gmail.com'


def debug(msg="", logger=None):
    if logger:
        logger.debug(msg)
    else:
        logging.debug(msg)


def info(msg="", logger=None):
    if logger:
        logger.info(msg)
    else:
        logging.info(msg)


def warn(msg="", logger=None):
    if logger:
        logger.warn(msg)
    else:
        logging.warn(msg)


def error(msg="", logger=None):
    if logger:
        logger.error(msg)
    else:
        logging.error(msg)
