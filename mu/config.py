import os
import sys
import tempfile

import platformdirs


# The default directory for application data (i.e., configuration).
def get_data_dir():
    path = platformdirs.user_data_dir(appname="mu", appauthor="python")
    if sys.platform == "win32":
        # Locate the actual path for Windows by making a temporary file
        # then resolving the real path. Solves a bug in the Windows store
        # distribution of Python 3.8+
        # See https://github.com/mu-editor/mu/issues/2293
        os.makedirs(path, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=path)
        realpath = os.path.dirname(os.path.realpath(tmp))
        os.close(fd)
        os.remove(tmp)
        return realpath
    else:
        return path


# The name of the default virtual environment used by Mu.
VENV_NAME = "mu_venv"

# The directory containing default virtual environment.
def get_venv_dir():
    return os.path.join(get_data_dir(), VENV_NAME)


# Maximum line length for using both in Check and Tidy
MAX_LINE_LENGTH = 88

# The user's home directory.
HOME_DIRECTORY = os.path.expanduser("~")

# Name of the directory within the home folder to use by default
WORKSPACE_NAME = "mu_code"
