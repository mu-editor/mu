"""
Mu - a "micro" Python editor for everyone.

Copyright (c) 2015-2016 Nicholas H.Tollervey and others (see the AUTHORS file).

Based upon work done for Puppy IDE by Dan Pope, Nicholas Tollervey and Damien
George.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import gettext
import os
import sys
import platform
import logging
from logging.handlers import TimedRotatingFileHandler
from PyQt5.QtWidgets import QApplication, QSplashScreen
from mu import __version__
from mu.logic import Editor, LOG_FILE, LOG_DIR
from mu.interface import Window
from mu.resources import load_pixmap
from mu.modes import PythonMode, AdafruitMode, MicrobitMode


gettext.install('mu', 'locale')
_ = gettext.gettext


def setup_logging():
    """
    Configure logging.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_fmt = ('%(asctime)s - %(name)s:%(lineno)d(%(funcName)s) '
               '%(levelname)s: %(message)s')
    formatter = logging.Formatter(log_fmt)
    handler = TimedRotatingFileHandler(LOG_FILE, when='midnight',
                                       backupCount=5, delay=0)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    sys.excepthook = excepthook
    print(_('Logging to {}').format(LOG_FILE))


def setup_modes(editor, view):
    """
    Create a simple dictionary to hold instances of the available modes.

    *PREMATURE OPTIMIZATION ALERT* This may become more complex in future so
    splitting things out here to contain the mess. ;-)
    """
    return {
        'python': PythonMode(editor, view),
        'adafruit': AdafruitMode(editor, view),
        'microbit': MicrobitMode(editor, view),
    }


def excepthook(*exc_args):
    """
    Log exception and exit cleanly.
    """
    logging.error('Unrecoverable error', exc_info=(exc_args))
    sys.__excepthook__(*exc_args)
    sys.exit(1)


def run():
    """
    Creates all the top-level assets for the application, sets things up and
    then runs the application.
    """
    setup_logging()
    logging.info('\n\n-----------------\n\nStarting Mu {}'.format(__version__))
    logging.info(platform.uname())
    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    # Display a friendly "splash" icon.
    splash = QSplashScreen(load_pixmap('icon'))
    splash.show()
    # Create the "window" we'll be looking at.
    editor_window = Window()
    # Create the "editor" that'll control the "window".
    editor = Editor(view=editor_window)
    editor.setup(setup_modes(editor, editor_window))
    # Setup the window.
    editor_window.closeEvent = editor.quit
    editor_window.setup(editor.theme)
    # capture the filename passed by the os, if there was one
    passed_filename = sys.argv[1] if len(sys.argv) > 1 else None
    editor.restore_session(passed_filename)
    # Connect the various UI elements in the window to the editor.
    status_bar = editor_window.status_bar
    status_bar.connect_logs(editor.show_logs)
    status_bar.connect_mode(editor.select_mode)
    # Finished starting up the application, so hide the splash icon.
    splash.finish(editor_window)
    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
