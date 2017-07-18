# -*- coding: utf-8 -*-
"""
Tests for the app script.
"""
import sys
from unittest import mock
from mu.app import excepthook, run, setup_logging
from mu.logic import LOG_FILE, LOG_DIR


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
                                         backupCount=5, delay=0)
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
    with mock.patch('mu.app.setup_logging') as set_log, \
            mock.patch('mu.app.QApplication') as qa, \
            mock.patch('mu.app.QSplashScreen') as qsp, \
            mock.patch('mu.app.Editor') as ed, \
            mock.patch('mu.app.load_pixmap'), \
            mock.patch('mu.app.Window') as win, \
            mock.patch('sys.exit') as ex:
        run()
        assert set_log.call_count == 1
        # foo.call_count is instantiating the class
        assert qa.call_count == 1
        # foo.mock_calls are method calls on the object
        assert len(qa.mock_calls) == 2
        assert qsp.call_count == 1
        assert len(qsp.mock_calls) == 3
        assert ed.call_count == 1
        assert len(ed.mock_calls) == 3
        assert win.call_count == 1
        assert len(win.mock_calls) == 4
        assert ex.call_count == 1


def test_excepthook():
    """
    Test that custom excepthook logs error and calls sys.exit.
    """
    ex = Exception('BANG')
    exc_args = (type(ex), ex, ex.__traceback__)

    with mock.patch('mu.app.logging.error') as error, \
            mock.patch('mu.app.sys.exit') as exit:
        sys.excepthook(*exc_args)
        error.assert_called_once_with('Unrecoverable error', exc_info=exc_args)
        exit.assert_called_once_with(1)
