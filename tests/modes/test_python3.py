# -*- coding: utf-8 -*-
"""
Tests for the Python3 mode.
"""
from mu.modes.python3 import PythonMode
from unittest import mock


def test_python_mode():
    """
    Sanity check for setting up of the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    assert pm.name == 'Python 3'
    assert pm.description is not None
    assert pm.icon == 'python'
    assert pm.debugger is True
    assert pm.editor == editor
    assert pm.view == view

    actions = pm.actions()
    assert len(actions) == 2
    assert actions[0]['name'] == 'run'
    assert actions[0]['handler'] == pm.toggle_run
    assert actions[1]['name'] == 'repl'
    assert actions[1]['handler'] == pm.toggle_repl

    assert pm.apis() == NotImplemented


def test_python_run():
    """
    Ensure the run handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    assert pm.run() is None


def test_python_repl():
    """
    Ensure the REPL handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    assert pm.toggle_repl(None) is None
