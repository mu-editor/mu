# -*- coding: utf-8 -*-
"""
Tests for the micro:bit mode.
"""
from mu.modes.microbit import MicrobitMode
from unittest import mock


def test_microbit_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    assert mm.name == 'BBC micro:bit'
    assert mm.description is not None
    assert mm.icon == 'microbit'
    assert mm.editor == editor
    assert mm.view == view

    actions = mm.actions()
    assert len(actions) == 3
    assert actions[0]['name'] == 'flash'
    assert actions[0]['handler'] == mm.flash
    assert actions[1]['name'] == 'files'
    assert actions[1]['handler'] == mm.files
    assert actions[2]['name'] == 'repl'
    assert actions[2]['handler'] == mm.repl

    assert mm.workspace_dir() == NotImplemented
    assert mm.apis() == NotImplemented


def test_microbit_flash():
    """
    Ensure the flash handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    assert mm.flash(None) is None


def test_microbit_files():
    """
    Ensure the files handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    assert mm.files(None) is None


def test_microbit_repl():
    """
    Ensure the REPL handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicrobitMode(editor, view)
    assert mm.repl(None) is None
