#!/usr/bin/env python3
import os
import sys
from mu.debugger import DEBUGGER_PORT
from mu.debugger.runner import run as run_debugger

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

def debug():
    """
    Create a debug runner in a new process.

    This is what the Mu debugger will drive. Uses the filename and associated
    args found in sys.argv.
    """
    if len(sys.argv) > 1:
        filename = os.path.normcase(os.path.abspath(sys.argv[1]))
        args = sys.argv[2:]
        run_debugger("localhost", DEBUGGER_PORT, filename, args)
    else:
        # See https://github.com/mu-editor/mu/issues/743
        print("Debugger requires a Python script filename to run.")


if __name__ == "__main__":
    debug()
