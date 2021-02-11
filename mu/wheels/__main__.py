import logging
from . import logger, download

#
# If run from the command line (eg python -m mu.wheels)
# make sure all logging goes to stdout
#
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

download()
