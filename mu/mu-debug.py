#!/usr/bin/env python3
import os
import sys
from mu.app import debug


if sys.platform == 'win32' and 'pythonw.exe' in sys.executable:
    # Add the python**.zip path to sys.path if running from the version of Mu
    # installed via the official Windows installer.
    # See: #612 and #581 for context.
    py_dir = os.path.dirname(sys.executable)
    version = '{}{}'.format(*sys.version_info[:2])
    zip_file = 'python{}.zip'.format(version)
    path_to_add = os.path.normcase(os.path.join(py_dir, zip_file))
    if os.path.exists(path_to_add):
        sys.path.append(path_to_add)


if __name__ == "__main__":
    debug()
