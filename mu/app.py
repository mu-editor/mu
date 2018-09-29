"""
Mu - a "micro" Python editor for beginner programmers.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

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
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import platform
import pkgutil
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QSplashScreen

from mu import __version__, language_code
from mu.logic import Editor, LOG_FILE, LOG_DIR, DEBUGGER_PORT, ENCODING
from mu.interface import Window
from mu.resources import load_pixmap, load_icon
from mu.modes import (PythonMode, AdafruitMode, MicrobitMode, DebugMode,
                      PyGameZeroMode)
from mu.debugger.runner import run as run_debugger
from mu.interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE


def setup_logging():
    """
    Configure logging.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # set logging format
    log_fmt = ('%(asctime)s - %(name)s:%(lineno)d(%(funcName)s) '
               '%(levelname)s: %(message)s')
    formatter = logging.Formatter(log_fmt)

    # define log handlers such as for rotating log files
    handler = TimedRotatingFileHandler(LOG_FILE, when='midnight',
                                       backupCount=5, delay=0,
                                       encoding=ENCODING)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    # set up primary log
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
    modes = {
        'python': PythonMode(editor, view),
        'adafruit': AdafruitMode(editor, view),
        'microbit': MicrobitMode(editor, view),
        'debugger': DebugMode(editor, view),
    }

    # Check if pgzero is available (without importing it)
    if any([m for m in pkgutil.iter_modules() if 'pgzero' in m]):
        modes['pygamezero'] = PyGameZeroMode(editor, view)

    # return available modes
    return modes


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
    then runs the application. Specific tasks include:

    - set up logging
    - create an application object
    - create an editor window and status bar
    - display a splash screen while starting
    - close the splash screen after startup timer ends
    """
    setup_logging()
    logging.info('\n\n-----------------\n\nStarting Mu {}'.format(__version__))
    logging.info(platform.uname())
    logging.info('Python path: {}'.format(sys.path))
    logging.info('Language code: {}'.format(language_code))

    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    # By default PyQt uses the script name (run.py)
    app.setApplicationName('mu')
    # Set hint as to the .desktop files name
    app.setDesktopFileName('mu.codewith.editor')
    app.setApplicationVersion(__version__)
    app.setAttribute(Qt.AA_DontShowIconsInMenus)
    # Images (such as toolbar icons) aren't scaled nicely on retina/4k displays
    # unless this flag is set
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Create the "window" we'll be looking at.
    editor_window = Window()

    @editor_window.load_theme.connect
    def load_theme(theme):
        if theme == 'contrast':
            app.setStyleSheet(CONTRAST_STYLE)
        elif theme == 'night':
            app.setStyleSheet(NIGHT_STYLE)
        else:
            app.setStyleSheet(DAY_STYLE)

    # Make sure all windows have the Mu icon as a fallback
    app.setWindowIcon(load_icon(editor_window.icon))
    # Create the "editor" that'll control the "window".
    editor = Editor(view=editor_window)
    editor.setup(setup_modes(editor, editor_window))
    # Setup the window.
    editor_window.closeEvent = editor.quit
    editor_window.setup(editor.debug_toggle_breakpoint, editor.theme)
    # Restore the previous session along with files passed by the os
    editor.restore_session(sys.argv[1:])
    # Connect the various UI elements in the window to the editor.
    editor_window.connect_tab_rename(editor.rename_tab, 'Ctrl+Shift+S')
    editor_window.connect_find_replace(editor.find_replace, 'Ctrl+F')
    editor_window.connect_toggle_comments(editor.toggle_comments, 'Ctrl+K')
    status_bar = editor_window.status_bar
    status_bar.connect_logs(editor.show_admin, 'Ctrl+Shift+D')

    # Display a friendly "splash" icon.
    splash = QSplashScreen(load_pixmap('splash-screen'))
    splash.show()

    # Hide the splash icon.
    splash_be_gone = QTimer()
    splash_be_gone.timeout.connect(lambda: splash.finish(editor_window))
    splash_be_gone.setSingleShot(True)
    splash_be_gone.start(2000)

    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())


def debug():
    """
    Create a debug runner in a new process.

    This is what the Mu debugger will drive. Uses the filename and associated
    args found in sys.argv.
    """
    if len(sys.argv) > 1:
        filename = os.path.normcase(os.path.abspath(sys.argv[1]))
        args = sys.argv[2:]
        run_debugger('localhost', DEBUGGER_PORT, filename, args)
    else:
        print(_("Debugger requires a Python script filename to run."))
