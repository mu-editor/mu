# -*- coding: utf-8 -*-
"""
Tests for the app script.
"""
import sys
import os.path
import pytest
import subprocess

from unittest import mock
from mu.app import (
    excepthook,
    run,
    setup_logging,
    AnimatedSplash,
    StartupWorker,
    vlogger,
    check_only_running_once,
)
from mu.debugger.config import DEBUGGER_PORT

from mu.interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE
from mu.logic import LOG_FILE, LOG_DIR, ENCODING
from mu.resources import load_movie
from mu import mu_debug
from mu.virtual_environment import VirtualEnvironment as VE, SplashLogHandler
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
    test_animation = load_movie("splash_screen")
    test_animation.frameChanged = mock.MagicMock()
    test_animation.start = mock.MagicMock()
    asplash = AnimatedSplash(test_animation)
    assert asplash.animation == test_animation
    asplash.animation.frameChanged.connect.assert_called_once_with(
        asplash.set_frame
    )
    asplash.animation.start.assert_called_once_with()


def test_animated_splash_set_frame():
    """
    Ensure the splash screen's pixmap is updated with the animation's current
    pixmap.
    """
    test_animation = load_movie("splash_screen")
    test_animation.frameChanged = mock.MagicMock()
    test_animation.start = mock.MagicMock()
    asplash = AnimatedSplash(test_animation)
    asplash.setPixmap = mock.MagicMock()
    asplash.setMask = mock.MagicMock()
    test_animation.currentPixmap = mock.MagicMock()
    asplash.set_frame()
    asplash.animation.currentPixmap.assert_called_once_with()
    pixmap = asplash.animation.currentPixmap()
    asplash.setPixmap.assert_called_once_with(pixmap)
    asplash.setMask.assert_called_once_with(pixmap.mask())


def test_animated_splash_draw_log():
    """
    Ensure the scrolling updates from the log handler are sliced properly and
    the expected text is shown in the right place on the splash screen.
    """
    test_animation = load_movie("splash_screen")
    asplash = AnimatedSplash(test_animation)
    asplash.log = [
        "1st line of the log",
        "2nd line of the log",
        "3rd line of the log",
        "4th line of the log",
        "5th line of the log",
    ]
    asplash.showMessage = mock.MagicMock()
    msg = "A new line of the log"
    expected = asplash.log[-3:]
    expected.append(msg)
    expected = "\n".join(expected)
    asplash.draw_log(msg)
    asplash.showMessage.assert_called_once_with(
        expected, Qt.AlignBottom | Qt.AlignLeft
    )


def test_animated_splash_failed():
    """
    When instructed to transition to a failed state, ensure the correct image
    is displayed along with the correct message.
    """
    test_animation = load_movie("splash_screen")
    asplash = AnimatedSplash(test_animation)
    asplash.setPixmap = mock.MagicMock()
    asplash.draw_text = mock.MagicMock()
    error = (
        "Something went boom!\n"
        "This is an error message...\n"
        "In real life, this would include a stack trace.\n"
        "It will also include details about the exception.\n"
    )
    with mock.patch("mu.app.load_pixmap") as load_pix:
        asplash.failed(error)
        load_pix.assert_called_once_with("splash_fail.png")
    asplash.draw_text.assert_called_once_with(
        error
        + "\nThis screen will close in a few seconds. "
        + "Then a crash report tool will open in your browser."
    )
    assert asplash.setPixmap.call_count == 1


def test_worker_run():
    """
    Ensure the finished signal is called when the tasks called in the run
    method are completed.
    """
    w = StartupWorker()
    slh = SplashLogHandler(w.display_text)
    vlogger.addHandler(slh)
    w.finished = mock.MagicMock()
    with mock.patch("mu.app.venv.ensure_and_create") as mock_ensure:
        w.run()
        assert mock_ensure.call_count == 1
        w.finished.emit.assert_called_once_with()
    # Ensure the splash related logger handler has been removed.
    while vlogger.hasHandlers() and vlogger.handlers:
        handler = vlogger.handlers[0]
        assert not isinstance(handler, SplashLogHandler)


def test_worker_fail():
    """
    Ensure that exceptions encountered during Mu's start-up are handled in the
    expected manner.
    """
    w = StartupWorker()
    w.finished = mock.MagicMock()
    w.failed = mock.MagicMock()
    mock_ensure = mock.MagicMock()
    ex = RuntimeError("Boom")
    mock_ensure.side_effect = ex
    with pytest.raises(RuntimeError):
        with mock.patch(
            "mu.app.venv.ensure_and_create", mock_ensure
        ), mock.patch("mu.app.time") as mock_time:
            w.run()
    assert mock_ensure.call_count == 1
    assert w.failed.emit.call_count == 1
    mock_time.sleep.assert_called_once_with(7)
    w.finished.emit.assert_called_once_with()


def test_setup_logging_without_envvar():
    """
    Ensure that logging is set up in some way.

    Resetting the MU_LOG_TO_STDOUT env var ensures that the crash handler
    will be enabled and stdout logging not
    """
    os.environ.pop("MU_LOG_TO_STDOUT", "")
    with mock.patch("mu.app.TimedRotatingFileHandler") as log_conf, mock.patch(
        "mu.app.os.path.exists", return_value=False
    ), mock.patch("mu.app.logging") as logging, mock.patch(
        "mu.app.os.makedirs", return_value=None
    ) as mkdir:
        setup_logging()
        mkdir.assert_called_once_with(LOG_DIR, exist_ok=True)
        log_conf.assert_called_once_with(
            LOG_FILE,
            when="midnight",
            backupCount=5,
            delay=0,
            encoding=ENCODING,
        )
        logging.getLogger.assert_called_once_with()
        assert sys.excepthook == excepthook


def test_setup_logging_with_envvar():
    """
    Ensure that logging is set up in some way.

    Setting the MU_LOG_TO_STDOUT env var ensures that the crash handler
    will not be enabled and stdout logging will
    """
    os.environ["MU_LOG_TO_STDOUT"] = "1"
    with mock.patch("mu.app.TimedRotatingFileHandler") as log_conf, mock.patch(
        "mu.app.os.path.exists", return_value=False
    ), mock.patch("mu.app.logging") as logging, mock.patch(
        "mu.app.os.makedirs", return_value=None
    ) as mkdir:
        setup_logging()
        mkdir.assert_called_once_with(LOG_DIR, exist_ok=True)
        log_conf.assert_called_once_with(
            LOG_FILE,
            when="midnight",
            backupCount=5,
            delay=0,
            encoding=ENCODING,
        )
        logging.getLogger.assert_called_once_with()
        # ~ assert sys.excepthook == excepthook


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
    ) as ex, mock.patch(
        "mu.app.QEventLoop"
    ) as mock_event_loop, mock.patch(
        "mu.app.QThread"
    ), mock.patch(
        "mu.app.StartupWorker"
    ) as mock_worker:
        run()
        assert set_log.call_count == 1
        # foo.call_count is instantiating the class
        assert qa.call_count == 1
        # foo.mock_calls are method calls on the object
        if hasattr(Qt, "AA_EnableHighDpiScaling"):
            assert len(qa.mock_calls) == 9
        else:
            assert len(qa.mock_calls) == 8
        assert qsp.call_count == 1
        assert len(qsp.mock_calls) == 4
        assert ed.call_count == 1
        assert len(ed.mock_calls) == 4
        assert win.call_count == 1
        assert len(win.mock_calls) == 6
        assert ex.call_count == 1
        assert mock_event_loop.call_count == 1
        assert mock_worker.call_count == 1
        window.load_theme.emit("day")
        qa.assert_has_calls([mock.call().setStyleSheet(DAY_STYLE)])
        window.load_theme.emit("night")
        qa.assert_has_calls([mock.call().setStyleSheet(NIGHT_STYLE)])
        window.load_theme.emit("contrast")
        qa.assert_has_calls([mock.call().setStyleSheet(CONTRAST_STYLE)])


@pytest.mark.skip("Possibly hanging...")
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
    ), mock.patch.object(
        VE, "ensure_and_create"
    ):
        run()
        assert splash.close.call_count == 1


def test_excepthook():
    """
    Test that custom excepthook logs error and calls sys.exit.
    """
    ex = Exception("BANG")
    exc_args = (type(ex), ex, ex.__traceback__)

    with mock.patch("mu.app.logging.error") as error, mock.patch(
        "mu.app.sys.exit"
    ) as exit, mock.patch("mu.app.webbrowser") as browser:
        excepthook(*exc_args)
        error.assert_called_once_with("Unrecoverable error", exc_info=exc_args)
        exit.assert_called_once_with(1)
        assert browser.open.call_count == 1


def test_excepthook_alamo():
    """
    If the crash reporting code itself encounters an error, then ensure this
    is logged before exiting.
    """
    ex = Exception("BANG")
    exc_args = (type(ex), ex, ex.__traceback__)

    mock_browser = mock.MagicMock()
    mock_browser.open.side_effect = RuntimeError("BROWSER BANG")

    with mock.patch("mu.app.logging.error") as error, mock.patch(
        "mu.app.sys.exit"
    ) as exit, mock.patch("mu.app.webbrowser", mock_browser):
        excepthook(*exc_args)
        assert error.call_count == 2
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


def test_only_running_once():
    """
    If we are the first to acquire the application lock we should succeed
    """
    check_only_running_once()
    assert True


def test_running_twice():
    """
    If we attempt to acquire the application lock when it's already held
    we should fail
    """
    #
    # It's important that the two competing processes are not part of the same
    # process tree; otherwise the second attempt to acquire the mutex will
    # succeed (which we don't want to happen for our purposes)
    #
    cmd1 = "import time;"
    "from mu import app;"
    "app.check_only_running_once();"
    "time.sleep(2)"
    cmd2 = "import time;"
    "from mu import app;"
    "app.check_only_running_once()"
    subprocess.Popen([sys.executable, cmd1])
    result = subprocess.run([sys.executable, cmd2])
    assert result.returncode == 2
