import logging
import sys

from . import logger, download

#
# If run from the command line (eg python -m mu.wheels)
# make sure all logging goes to stdout
#
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# A single flag is accepted to trigger a `pip download` using flag to increase
# compatibility with older operating system versions.
# As there is a single option available sys.argv is used for simplicity,
# if more options are added in the future we should start using argparse
os_old_compat = sys.argv[1] == "--package"

download(os_old_compat=os_old_compat)
