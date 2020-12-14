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
import sys

from PyQt5.QtCore import QTimer, Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QSplashScreen

from . import i18n
from .virtual_environment import venv
from . import __version__
from .logic import Editor, LOG_FILE, LOG_DIR, ENCODING
from .interface import Window
from .resources import load_pixmap, load_icon
from .modes import (
    PythonMode,
    CircuitPythonMode,
    MicrobitMode,
    DebugMode,
    PyGameZeroMode,
    ESPMode,
    WebMode,
    PyboardMode,
)
from .interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE


def excepthook(*exc_args):
    """
    Log exception and exit cleanly.
    """
    logging.error("Unrecoverable error", exc_info=(exc_args))
    sys.__excepthook__(*exc_args)
    sys.exit(1)


def setup_logging():
    """
    Configure logging.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # set logging format
    log_fmt = (
        "%(asctime)s - %(name)s:%(lineno)d(%(funcName)s) "
        "%(levelname)s: %(message)s"
    )
    formatter = logging.Formatter(log_fmt)

    # define log handlers such as for rotating log files
    handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight", backupCount=5, delay=0, encoding=ENCODING
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    # set up primary log
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    sys.excepthook = excepthook


def setup_modes(editor, view):
    """
    Create a simple dictionary to hold instances of the available modes.

    *PREMATURE OPTIMIZATION ALERT* This may become more complex in future so
    splitting things out here to contain the mess. ;-)
    """
    return {
        "python": PythonMode(editor, view),
        "circuitpython": CircuitPythonMode(editor, view),
        "microbit": MicrobitMode(editor, view),
        "esp": ESPMode(editor, view),
        "web": WebMode(editor, view),
        "pyboard": PyboardMode(editor, view),
        "debugger": DebugMode(editor, view),
        "pygamezero": PyGameZeroMode(editor, view),
    }


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
    logging.info("\n\n-----------------\n\nStarting Mu {}".format(__version__))
    logging.info(platform.uname())
    logging.info("Python path: {}".format(sys.path))
    logging.info("Language code: {}".format(i18n.language_code))

    # Images (such as toolbar icons) aren't scaled nicely on retina/4k displays
    # unless this flag is set
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    # By default PyQt uses the script name (run.py)
    app.setApplicationName("mu")
    # Set hint as to the .desktop files name
    app.setDesktopFileName("mu.codewith.editor")
    app.setApplicationVersion(__version__)
    app.setAttribute(Qt.AA_DontShowIconsInMenus)

    #
    # FIXME -- look at the possiblity of tying ensure completion
    # into Splash screen finish below...
    #
    venv.ensure()

    # Create the "window" we'll be looking at.
    editor_window = Window()

    @editor_window.load_theme.connect
    def load_theme(theme):
        if theme == "contrast":
            app.setStyleSheet(CONTRAST_STYLE)
        elif theme == "night":
            app.setStyleSheet(NIGHT_STYLE)
        else:
            app.setStyleSheet(DAY_STYLE)

    # Display a friendly "splash" icon.
    splash = QSplashScreen(load_pixmap("splash-screen"))
    splash.show()

    def raise_and_process_events():
        # Make sure the splash screen stays on top while
        # the mode selection dialog might open
        splash.raise_()

        # Make sure splash screen reacts to mouse clicks, even when
        # the event loop is not yet started
        QCoreApplication.processEvents()

    raise_splash = QTimer()
    raise_splash.timeout.connect(raise_and_process_events)
    raise_splash.start(10)

    # Hide the splash icon.
    def remove_splash():
        splash.finish(editor_window)
        raise_splash.stop()

    splash_be_gone = QTimer()
    splash_be_gone.timeout.connect(remove_splash)
    splash_be_gone.setSingleShot(True)
    splash_be_gone.start(2000)

    # Make sure all windows have the Mu icon as a fallback
    app.setWindowIcon(load_icon(editor_window.icon))
    # Create the "editor" that'll control the "window".
    editor = Editor(view=editor_window)
    editor.setup(setup_modes(editor, editor_window))
    # Setup the window.
    editor_window.closeEvent = editor.quit
    editor_window.setup(editor.debug_toggle_breakpoint, editor.theme)
    # Connect the various UI elements in the window to the editor.
    editor_window.connect_tab_rename(editor.rename_tab, "Ctrl+Shift+S")
    editor_window.connect_find_replace(editor.find_replace, "Ctrl+F")
    editor_window.connect_toggle_comments(editor.toggle_comments, "Ctrl+K")
    editor.connect_to_status_bar(editor_window.status_bar)

    # Restore the previous session along with files passed by the os
    editor.restore_session(sys.argv[1:])

    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
