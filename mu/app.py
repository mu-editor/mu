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
import time
import platform
import traceback
import sys
import urllib
import webbrowser
import base64

from PyQt5.QtCore import (
    Qt,
    QEventLoop,
    QThread,
    QObject,
    pyqtSignal,
)
from PyQt5.QtWidgets import QApplication, QSplashScreen

from . import i18n
from .virtual_environment import venv, logger as vlogger
from . import __version__
from .logic import Editor, LOG_FILE, LOG_DIR, ENCODING
from .interface import Window
from .resources import load_icon, load_movie, load_pixmap
from .modes import (
    PythonMode,
    CircuitPythonMode,
    MicrobitMode,
    DebugMode,
    PyGameZeroMode,
    ESPMode,
    WebMode,
    PyboardMode,
    LegoMode,
    PicoMode,
)
from .interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE
from . import settings


class AnimatedSplash(QSplashScreen):
    """
    An animated splash screen for gifs. Includes a text area for logging
    output.
    """

    def __init__(self, animation, parent=None):
        """
        Ensure signals are connected and start the animation.
        """
        self.log_lines = 4
        # To hold only number of log_lines of logs to display.
        self.log = []
        self.animation = animation
        self.animation.frameChanged.connect(self.set_frame)
        # Always on top.
        super().__init__(
            self.animation.currentPixmap(), Qt.WindowStaysOnTopHint
        )
        # Disable clicks.
        self.setEnabled(False)
        self.animation.start()

    def set_frame(self):
        """
        Update the splash screen with the next frame of the animation.
        """
        pixmap = self.animation.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

    def draw_log(self, text):
        """
        Draw the log entries onto the splash screen. Will only display the last
        self.log_lines number of log entries. The logs will be displayed at the
        bottom of the splash screen, justified left.
        """
        self.log.append(text)
        self.log = self.log[-self.log_lines :]
        if self.log:
            self.draw_text("\n".join(self.log))

    def draw_text(self, text):
        """
        Draw text into splash screen.
        """
        if text:
            self.showMessage(text, Qt.AlignBottom | Qt.AlignLeft)

    def failed(self, text):
        """
        Something has gone wrong during start-up, so signal this, display a
        helpful message along with instructions for what to do.
        """
        self.animation.stop()
        pixmap = load_pixmap("splash_fail.png")
        self.setPixmap(pixmap)
        lines = text.split("\n")
        lines.append(
            "This screen will close in a few seconds. "
            "Then a crash report tool will open in your browser."
        )
        lines = lines[-12:]
        self.draw_text("\n".join(lines))


class StartupWorker(QObject):
    """
    A worker class for running blocking tasks on a separate thread during
    application start-up.

    The animated splash screen will be shown until this thread is finished.
    """

    finished = pyqtSignal()  # emitted when successfully finished.
    failed = pyqtSignal(str)  # emitted if finished with an error.
    display_text = pyqtSignal(str)  # emitted to update the splash text.

    def run(self):
        """
        Blocking and long running tasks for application startup should be
        called from here.
        """
        try:
            venv.ensure_and_create(self.display_text)
            self.finished.emit()  # Always called last.
        except Exception as ex:
            # Catch all exceptions just in case.
            # Report the failure, along with a summary to show the user.
            stack = traceback.extract_stack()[:-1]
            msg = "\n".join(traceback.format_list(stack))
            msg += "\n\n" + traceback.format_exc()
            self.failed.emit(msg)
            # Sleep a while in the thread so the user sees something is wrong.
            time.sleep(7)
            self.finished.emit()
            # Re-raise for crash handler to kick in.
            raise ex
        finally:
            # Always clean up the startup splash/venv logging handlers.
            if vlogger.handlers:
                handler = vlogger.handlers[0]
                vlogger.removeHandler(handler)


def excepthook(*exc_args):
    """
    Log exception and exit cleanly.
    """
    logging.error("Unrecoverable error", exc_info=(exc_args))
    try:
        log_file = base64.standard_b64encode(LOG_FILE.encode("utf-8"))
        error = base64.standard_b64encode(
            "".join(traceback.format_exception(*exc_args)).encode("utf-8")
        )
        p = platform.uname()
        params = {
            "v": __version__,  # version
            "l": str(i18n.language_code),  # locale
            "p": base64.standard_b64encode(
                " ".join([p.system, p.release, p.version, p.machine]).encode(
                    "utf-8"
                )
            ),  # platform
            "f": log_file,  # location of log file
            "e": error,  # error message
        }
        args = urllib.parse.urlencode(params)
        webbrowser.open("https://codewith.mu/crash/?" + args)
    except Exception as e:  # The Alamo of crash handling.
        logging.error("Failed to report crash", exc_info=e)
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

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)

    # set up primary log
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.addHandler(stdout_handler)
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
        "lego": LegoMode(editor, view),
        "pico": PicoMode(editor, view),
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

    #
    # Load settings from known locations and register them for
    # autosave
    #
    settings.init()

    # Images (such as toolbar icons) aren't scaled nicely on retina/4k displays
    # unless this flag is set
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # An issue in PyQt5 v5.13.2 to v5.15.1 makes PyQt5 application
    # hang on Mac OS 11 (Big Sur)
    # Setting this environment variable fixes the problem.
    # See issue #1147 for more information
    os.environ["QT_MAC_WANTS_LAYER"] = "1"

    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    # By default PyQt uses the script name (run.py)
    app.setApplicationName("mu")
    # Set hint as to the .desktop files name
    app.setDesktopFileName("mu.codewith.editor")
    app.setApplicationVersion(__version__)
    app.setAttribute(Qt.AA_DontShowIconsInMenus)

    def splash_context():
        """
        Function context (to ensure garbage collection) for displaying the
        splash screen.
        """
        # Display a friendly "splash" icon.
        splash = AnimatedSplash(load_movie("splash_screen"))
        splash.show()

        # Create a blocking thread upon which to run the StartupWorker and which
        # will process the events for animating the splash screen.
        initLoop = QEventLoop()
        thread = QThread()
        worker = StartupWorker()
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        worker.display_text.connect(splash.draw_log)
        worker.failed.connect(splash.failed)
        # Stop the blocking event loop when the thread is finished.
        thread.finished.connect(initLoop.quit)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        initLoop.exec()  # start processing the pending StartupWorker.
        splash.close()
        splash.deleteLater()

    splash_context()

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
    # Connect find again both forward and backward ('Shift+F3')
    find_again_handlers = (editor.find_again, editor.find_again_backward)
    editor_window.connect_find_again(find_again_handlers, "F3")
    editor_window.connect_toggle_comments(editor.toggle_comments, "Ctrl+K")
    editor.connect_to_status_bar(editor_window.status_bar)

    # Restore the previous session along with files passed by the os
    editor.restore_session(sys.argv[1:])

    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
