# -*- coding: utf-8 -*-
"""
Tests for the app script.
"""
import sys
import os.path
from unittest import mock
from mu.app import excepthook, run, setup_logging, debug, setup_modes
from mu.logic import LOG_FILE, LOG_DIR, DEBUGGER_PORT, ENCODING
from mu.interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE


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
            raise Exception('No signal handler connected')

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


def test_setup_logging():
    """
    Ensure that logging is set up in some way.
    """
    with mock.patch('mu.app.TimedRotatingFileHandler') as log_conf, \
            mock.patch('mu.app.os.path.exists', return_value=False),\
            mock.patch('mu.app.logging') as logging, \
            mock.patch('mu.app.os.makedirs', return_value=None) as mkdir:
        setup_logging()
        mkdir.assert_called_once_with(LOG_DIR)
        log_conf.assert_called_once_with(LOG_FILE, when='midnight',
                                         backupCount=5, delay=0,
                                         encoding=ENCODING)
        logging.getLogger.assert_called_once_with()
        assert sys.excepthook == excepthook


def test_setup_modes_with_pgzero():
    """
    If pgzero is installed, allow Pygame Zero mode.
    """
    with mock.patch('mu.app.pkgutil.iter_modules', return_value=['pgzero', ]):
        mock_editor = mock.MagicMock()
        mock_view = mock.MagicMock()
        modes = setup_modes(mock_editor, mock_view)
        assert 'pygamezero' in modes


def test_setup_modes_without_pgzero():
    """
    If pgzero is NOT installed, do not add Pygame Zero mode to the list of
    available modes.
    """
    with mock.patch('mu.app.pkgutil.iter_modules', return_value=['foo', ]):
        mock_editor = mock.MagicMock()
        mock_view = mock.MagicMock()
        modes = setup_modes(mock_editor, mock_view)
        assert 'pygamezero' not in modes


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
        icon = 'icon'

    window = Win()

    with mock.patch('mu.app.setup_logging') as set_log, \
            mock.patch('mu.app.QApplication') as qa, \
            mock.patch('mu.app.QSplashScreen') as qsp, \
            mock.patch('mu.app.Editor') as ed, \
            mock.patch('mu.app.load_pixmap'), \
            mock.patch('mu.app.Window', window) as win, \
            mock.patch('mu.app.QTimer') as timer, \
            mock.patch('sys.argv', ['mu']), \
            mock.patch('sys.exit') as ex:
        run()
        assert set_log.call_count == 1
        # foo.call_count is instantiating the class
        assert qa.call_count == 1
        # foo.mock_calls are method calls on the object
        assert len(qa.mock_calls) == 8
        assert qsp.call_count == 1
        assert len(qsp.mock_calls) == 2
        assert timer.call_count == 1
        assert len(timer.mock_calls) == 4
        assert ed.call_count == 1
        assert len(ed.mock_calls) == 3
        assert win.call_count == 1
        assert len(win.mock_calls) == 6
        assert ex.call_count == 1
        window.load_theme.emit('day')
        qa.assert_has_calls([mock.call().setStyleSheet(DAY_STYLE)])
        window.load_theme.emit('night')
        qa.assert_has_calls([mock.call().setStyleSheet(NIGHT_STYLE)])
        window.load_theme.emit('contrast')
        qa.assert_has_calls([mock.call().setStyleSheet(CONTRAST_STYLE)])


def test_excepthook():
    """
    Test that custom excepthook logs error and calls sys.exit.
    """
    ex = Exception('BANG')
    exc_args = (type(ex), ex, ex.__traceback__)

    with mock.patch('mu.app.logging.error') as error, \
            mock.patch('mu.app.sys.exit') as exit:
        excepthook(*exc_args)
        error.assert_called_once_with('Unrecoverable error', exc_info=exc_args)
        exit.assert_called_once_with(1)


def test_debug():
    """
    Ensure the debugger is run with the expected arguments given the filename
    and other arguments passed in via sys.argv.
    """
    mock_sys = mock.MagicMock()
    mock_sys.argv = [None, 'foo.py', 'foo', 'bar', 'baz']
    mock_runner = mock.MagicMock()
    with mock.patch('mu.app.sys', mock_sys), \
            mock.patch('mu.app.run_debugger', mock_runner):
        debug()
    expected_filename = os.path.normcase(os.path.abspath('foo.py'))
    mock_runner.assert_called_once_with('localhost', DEBUGGER_PORT,
                                        expected_filename,
                                        ['foo', 'bar', 'baz', ])


def test_debug_no_args():
    """
    If the debugger is accidentally started with no filename and/or associated
    args, then emit a friendly message to indicate the problem.
    """
    mock_sys = mock.MagicMock()
    mock_sys.argv = [None, ]
    mock_print = mock.MagicMock()
    with mock.patch('mu.app.sys', mock_sys), \
            mock.patch('builtins.print', mock_print):
        debug()
    msg = "Debugger requires a Python script filename to run."
    mock_print.assert_called_once_with(msg)
