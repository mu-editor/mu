# -*- coding: utf-8 -*-
"""
Tests for the app script.
"""
import sys
import os.path
from unittest import mock
from mu.app import (
    excepthook,
    run,
    setup_logging,
    AnimatedSplash,
    StartupWorker,
)
from mu.debugger.config import DEBUGGER_PORT

# ~ from mu.debugger import runner as debugger_runner
from mu.interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE
from mu.logic import LOG_FILE, LOG_DIR, ENCODING
from mu import mu_debug
from PyQt5.QtCore import Qt


class DumSig:
    """
    Fake signal for mocking purposes

    Only supports a signal callback
    """

    def __init__(self):
        """
        Setup the signal
        """

        # Setup a fallback handled
        @self.connect
        def default(*args):
            # ... and throw an exception because it still exists
            raise Exception("No signal handler connected")

    def connect(self, func):
        """
        Set the callback function
        """
        self.func = func
        return func

    def emit(self, *args):
        """
        Proxy the callback function
        """
        self.func(*args)


def test_animated_splash_init():
    """
    Ensure the AnimatedSplash class uses the passed in animation.
    """
    mock_gif = mock.MagicMock()
    asplash = AnimatedSplash(mock_gif)
    assert asplash.animation == mock_gif
    asplash.animation.frameChanged.connect.assert_called_once_with(
        asplash.set_frame
    )
    asplash.animation.start.assert_called_once_with()


def test_animated_splash_set_frame():
    """
    Ensure the splash screen's pixmap is updated with the animation's current
    pixmap.
    """
    mock_gif = mock.MagicMock()
    asplash = AnimatedSplash(mock_gif)
    asplash.setPixmap = mock.MagicMock()
    asplash.setMask = mock.MagicMock()
    asplash.set_frame()
    asplash.animation.currentPixmap.assert_called_once_with()
    pixmap = asplash.animation.currentPixmap()
    asplash.setPixmap.assert_called_once_with(pixmap)
    asplash.setMask.assert_called_once_with(pixmap.mask())


def test_worker_run():
    """
    Ensure the finished signal is called when the tasks called in the run
    method are completed.
    """
    w = StartupWorker()
    w.finished = mock.MagicMock()
    with mock.patch("mu.app.venv.ensure") as mock_ensure:
        w.run()
        mock_ensure.assert_called_once_with()
        w.finished.emit.assert_called_once_with()


def test_setup_logging():
    """
    Ensure that logging is set up in some way.
    """
    with mock.patch("mu.app.TimedRotatingFileHandler") as log_conf, mock.patch(
        "mu.app.os.path.exists", return_value=False
    ), mock.patch("mu.app.logging") as logging, mock.patch(
        "mu.app.os.makedirs", return_value=None
    ) as mkdir:
        setup_logging()
        mkdir.assert_called_once_with(LOG_DIR)
        log_conf.assert_called_once_with(
            LOG_FILE,
            when="midnight",
            backupCount=5,
            delay=0,
            encoding=ENCODING,
        )
        logging.getLogger.assert_called_once_with()
        assert sys.excepthook == excepthook


def test_run():
    """
    Ensure the run function sets things up in the expected way.

    Why check this?

    We need to know if something fundamental has inadvertently changed and
    these tests highlight such a case.

    Testing the call_count and mock_calls allows us to measure the expected
    number of instantiations and method calls.
    """

    class Win(mock.MagicMock):
        load_theme = DumSig()
        icon = "icon"

    window = Win()

    with mock.patch("mu.app.setup_logging") as set_log, mock.patch(
        "mu.app.QApplication"
    ) as qa, mock.patch("mu.app.AnimatedSplash") as qsp, mock.patch(
        "mu.app.Editor"
    ) as ed, mock.patch(
        "mu.app.load_movie"
    ), mock.patch(
        "mu.app.Window", window
    ) as win, mock.patch(
        "sys.argv", ["mu"]
    ), mock.patch(
        "sys.exit"
    ) as ex:
        run()
        assert set_log.call_count == 1
        # foo.call_count is instantiating the class
        assert qa.call_count == 1
        # foo.mock_calls are method calls on the object
        if hasattr(Qt, "AA_EnableHighDpiScaling"):
            assert len(qa.mock_calls) == 10
        else:
            assert len(qa.mock_calls) == 9
        assert qsp.call_count == 1
        assert len(qsp.mock_calls) == 3
        assert ed.call_count == 1
        assert len(ed.mock_calls) == 4
        assert win.call_count == 1
        assert len(win.mock_calls) == 6
        assert ex.call_count == 1
        window.load_theme.emit("day")
        qa.assert_has_calls([mock.call().setStyleSheet(DAY_STYLE)])
        window.load_theme.emit("night")
        qa.assert_has_calls([mock.call().setStyleSheet(NIGHT_STYLE)])
        window.load_theme.emit("contrast")
        qa.assert_has_calls([mock.call().setStyleSheet(CONTRAST_STYLE)])


def test_close_splash_screen():
    """
    Test that the splash screen is closed.
    """

    # Create a dummy window
    class Win(mock.MagicMock):
        load_theme = DumSig()
        icon = "icon"

    window = Win()

    # Create a dummy timer class
    class DummyTimer:
        def __init__(self):
            self.callback = lambda x: None
            self.stop = lambda: None
            self.setSingleShot = lambda x: None

            def set_callback(fun):
                self.callback = fun

            class Object(object):
                pass

            self.timeout = Object()
            self.timeout.connect = set_callback

        def start(self, t):
            # Just call the callback immediately
            self.callback()

    # Mock Splash screen
    splash = mock.MagicMock()

    # Mock QTimer, QApplication, Window, Editor, sys.exit
    with mock.patch("mu.app.Window", window), mock.patch(
        "mu.app.QApplication"
    ), mock.patch("sys.exit"), mock.patch("mu.app.Editor"), mock.patch(
        "mu.app.AnimatedSplash", return_value=splash
    ):
        run()
        assert splash.finish.call_count == 1


def test_excepthook():
    """
    Test that custom excepthook logs error and calls sys.exit.
    """
    ex = Exception("BANG")
    exc_args = (type(ex), ex, ex.__traceback__)

    with mock.patch("mu.app.logging.error") as error, mock.patch(
        "mu.app.sys.exit"
    ) as exit:
        excepthook(*exc_args)
        error.assert_called_once_with("Unrecoverable error", exc_info=exc_args)
        exit.assert_called_once_with(1)


def test_debug():
    """
    Ensure the debugger is run with the expected arguments given the filename
    and other arguments passed in via sys.argv.
    """
    args = ("foo", "bar", "baz")
    filename = "foo.py"
    expected_filename = os.path.normcase(os.path.abspath(filename))
    mock_runner = mock.MagicMock()
    with mock.patch("mu.debugger.runner.run", mock_runner):
        mu_debug.debug(filename, *args)
        mock_runner.assert_called_once_with(
            "localhost", DEBUGGER_PORT, expected_filename, args
        )


def test_debug_no_args():
    """
    If the debugger is accidentally started with no filename and/or associated
    args, then emit a friendly message to indicate the problem.
    """
    expected_msg = "Debugger requires a Python script filename to run."
    mock_print = mock.MagicMock()
    with mock.patch("builtins.print", mock_print):
        mu_debug.debug()
        mock_print.assert_called_once_with(expected_msg)
