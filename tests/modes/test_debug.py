# -*- coding: utf-8 -*-
"""
Tests for the debug mode.
"""
from mu.modes.debugger import DebugMode
from unittest import mock


def test_debug_mode():
    """
    Sanity check for setting up of the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = DebugMode(editor, view)
    assert pm.name == 'Graphical Debugger'
    assert pm.description is not None
    assert pm.icon == 'python'
    assert pm.runner is None
    assert pm.is_debugger is True
    assert pm.editor == editor
    assert pm.view == view

    actions = pm.actions()
    assert len(actions) == 5
    assert actions[0]['name'] == 'stop'
    assert actions[0]['handler'] == pm.button_stop
    assert actions[1]['name'] == 'run'
    assert actions[1]['handler'] == pm.button_continue
    assert actions[2]['name'] == 'step-over'
    assert actions[2]['handler'] == pm.button_step_over
    assert actions[3]['name'] == 'step-in'
    assert actions[3]['handler'] == pm.button_step_in
    assert actions[4]['name'] == 'step-out'
    assert actions[4]['handler'] == pm.button_step_out


def test_debug_run():
    """
    Ensure the run handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = '/foo'
    view.current_tab.isModified.return_value = True
    mock_runner = mock.MagicMock()
    view.add_python3_runner.return_value = mock_runner
    pm = DebugMode(editor, view)
    pm.workspace_dir = mock.MagicMock(return_value='/bar')
    with mock.patch('mu.modes.python3.open_atomic') as oa:
        pm.run()
        oa.assert_called_once_with('/foo', 'w', newline='')
    view.add_python3_runner.assert_called_once_with('/foo', '/bar')
    assert pm.runner == mock_runner


def test_debug_run_no_tab():
    """
    If there's no active tab, there can be no runner either.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = DebugMode(editor, view)
    pm.run()
    assert pm.runner is None


def test_debug_run_prompt_for_unsaved_file():
    """
    If the file hasn't been saved yet (it's unnamed), prompt the user to save
    it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = None
    pm = DebugMode(editor, view)
    pm.run()
    editor.save.assert_called_once_with()
    assert pm.runner is None


def test_debug_stop():
    """
    Ensure the script runner is cleaned up properly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = DebugMode(editor, view)
    mock_runner = mock.MagicMock()
    pm.runner = mock_runner
    pm.stop()
    assert pm.runner is None
    mock_runner.process.kill.assert_called_once_with()
