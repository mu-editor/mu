#!/usr/bin/env python3
import os
import sys
from mu.debugger.config import DEBUGGER_PORT
import mu.debugger.runner

if sys.platform == "win32" and "pythonw.exe" in sys.executable:
    # Add the python**.zip path to sys.path if running from the version of Mu
    # installed via the official Windows installer.
    # See: #612 and #581 for context.
    py_dir = os.path.dirname(sys.executable)
    version = "{}{}".format(*sys.version_info[:2])
    zip_file = "python{}.zip".format(version)
    path_to_add = os.path.normcase(os.path.join(py_dir, zip_file))
    if os.path.exists(path_to_add):
        sys.path.append(path_to_add)


def debug(filename=None, *args):
    """
    Create a debug runner in a new process.

    This is what the Mu debugger will drive. Uses the filename and associated
    args found in sys.argv.
    """
    if filename is None:
        print("Debugger requires a Python script filename to run.")
    else:
        filepath = os.path.normcase(os.path.abspath(filename))
        mu.debugger.runner.run("localhost", DEBUGGER_PORT, filepath, args)


if __name__ == "__main__":
    debug(*sys.argv[1:])
