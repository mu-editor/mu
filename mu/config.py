import os

import appdirs

# The default directory for application data (i.e., configuration).
DATA_DIR = appdirs.user_data_dir(appname="mu", appauthor="python")

# The name of the default virtual environment used by Mu.
VENV_NAME = "mu_venv"

# The directory containing default virtual environment.
VENV_DIR = os.path.join(DATA_DIR, VENV_NAME)

# Maximum line length for using both in Check and Tidy
MAX_LINE_LENGTH = 88

# The user's home directory.
HOME_DIRECTORY = os.path.expanduser("~")

# Name of the directory within the home folder to use by default
WORKSPACE_NAME = "mu_code"
