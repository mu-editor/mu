# -*- coding: utf-8 -*-
"""
Tests for the Adafruit mode.
"""
from mu.modes.adafruit import AdafruitMode
from unittest import mock


def test_adafruit_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = AdafruitMode(editor, view)
    assert am.name == 'Adafruit'
    assert am.description is not None
    assert am.icon == 'adafruit'
    assert am.editor == editor
    assert am.view == view

    actions = am.actions()
    assert len(actions) == 1
    assert actions[0]['name'] == 'repl'
    assert actions[0]['handler'] == am.repl

    assert am.workspace_dir() == NotImplemented
    assert am.apis() == NotImplemented


def test_adafruit_repl():
    """
    Ensure the REPL handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = AdafruitMode(editor, view)
    assert am.repl(None) is None
