import os

import appdirs

# The default directory for application data (i.e., configuration).
DATA_DIR = appdirs.user_data_dir(appname="mu", appauthor="python")

# The name of the default virtual environment used by Mu.
VENV_NAME = "mu_venv"

# The directory containing default virtual environment.
VENV_DIR = os.path.join(DATA_DIR, VENV_NAME)
