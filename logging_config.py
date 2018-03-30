'''
Configure global logging
'''

import logging
from logging.handlers import RotatingFileHandler


def configure_logging(level=logging.DEBUG, path="log.txt"):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    handler = RotatingFileHandler(path, maxBytes=20000, backupCount=5)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(name)s %(levelname)-8s %(message)s',
        '%a, %d %b %Y %H:%M:%S'))
    root_logger.addHandler(handler)
