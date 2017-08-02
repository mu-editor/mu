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
    assert am.name == 'Adafruit CircuitPython'
    assert am.description is not None
    assert am.icon == 'adafruit'
    assert am.editor == editor
    assert am.view == view

    actions = am.actions()
    assert len(actions) == 1
    assert actions[0]['name'] == 'repl'
    assert actions[0]['handler'] == am.toggle_repl

    assert am.apis() == NotImplemented
