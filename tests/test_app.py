# -*- coding: utf-8 -*-
"""
Tests for the app script.
"""
from unittest import mock
from mu.app import run


def test_run():
    """
    Ensure the run function sets things up in the expected way.

    Why check this?

    We need to know if something fundamental has inadvertently changed and
    these tests highlight such a case.

    Testing the call_count and mock_calls allows us to measure the expected
    number of instantiations and method calls.
    """
    with mock.patch('mu.app.QApplication') as qa, \
            mock.patch('mu.app.QSplashScreen') as qsp, \
            mock.patch('mu.app.Editor') as ed, \
            mock.patch('mu.app.load_pixmap'), \
            mock.patch('mu.app.Window') as win, \
            mock.patch('sys.exit') as ex:
        run()
        # foo.call_count is instantiating the class
        assert qa.call_count == 1
        # foo.mock_calls are method calls on the object
        assert len(qa.mock_calls) == 2
        assert qsp.call_count == 1
        assert len(qsp.mock_calls) == 3
        assert ed.call_count == 1
        assert len(ed.mock_calls) == 2
        assert win.call_count == 1
        assert len(win.mock_calls) == 11
        assert ex.call_count == 1
