# -*- coding: utf-8 -*-
"""
Tests for the debug mode.
"""
from mu.logic import DEBUGGER_PORT
from mu.modes.debugger import DebugMode
from unittest import mock


def test_debug_mode():
    """
    Sanity check for setting up of the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    assert dm.name == 'Graphical Debugger'
    assert dm.description is not None
    assert dm.icon == 'python'
    assert dm.runner is None
    assert dm.is_debugger is True
    assert dm.editor == editor
    assert dm.view == view

    assert dm.api() == []

    actions = dm.actions()
    assert len(actions) == 5
    assert actions[0]['name'] == 'stop'
    assert actions[0]['handler'] == dm.button_stop
    assert actions[1]['name'] == 'run'
    assert actions[1]['handler'] == dm.button_continue
    assert actions[2]['name'] == 'step-over'
    assert actions[2]['handler'] == dm.button_step_over
    assert actions[3]['name'] == 'step-in'
    assert actions[3]['handler'] == dm.button_step_in
    assert actions[4]['name'] == 'step-out'
    assert actions[4]['handler'] == dm.button_step_out


def test_debug_start():
    """
    Ensure the handling of starting the debugger works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = '/foo'
    view.current_tab.isModified.return_value = True
    mock_runner = mock.MagicMock()
    view.add_python3_runner.return_value = mock_runner
    mock_debugger = mock.MagicMock()
    mock_debugger_class = mock.MagicMock(return_value=mock_debugger)
    dm = DebugMode(editor, view)
    dm.workspace_dir = mock.MagicMock(return_value='/bar')
    with mock.patch('mu.modes.debugger.open') as oa, \
            mock.patch('mu.modes.debugger.Debugger', mock_debugger_class), \
            mock.patch('mu.modes.debugger.write_and_flush'):
        dm.start()
        oa.assert_called_once_with('/foo', 'w', newline='')
    view.add_python3_runner.assert_called_once_with('/foo', '/bar')
    mock_runner.process.waitForStarted.assert_called_once_with()
    mock_runner.process.finished.connect.assert_called_once_with(dm.finished)
    view.add_debug_inspector.assert_called_once_with()
    view.set_read_only.assert_called_once_with(True)
    mock_debugger_class.assert_called_once_with('localhost', DEBUGGER_PORT,
                                                proc=mock_runner.process)
    assert dm.runner == mock_runner
    assert dm.debugger == mock_debugger
    assert mock_debugger.view == dm
    mock_debugger.start.assert_called_once_with()


def test_debug_start_no_tab():
    """
    If there's no active tab, there can be no runner either.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    dm = DebugMode(editor, view)
    dm.start()
    assert dm.runner is None


def test_debug_start_prompt_for_unsaved_file():
    """
    If the file hasn't been saved yet (it's unnamed), prompt the user to save
    it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = None
    dm = DebugMode(editor, view)
    dm.stop = mock.MagicMock()
    dm.start()
    editor.save.assert_called_once_with()
    assert dm.runner is None
    dm.stop.assert_called_once_with()


def test_debug_stop():
    """
    Ensure the script runner is cleaned up properly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    mock_runner = mock.MagicMock()
    dm.runner = mock_runner
    dm.stop()
    assert dm.runner is None
    assert dm.debugger is None
    mock_runner.process.kill.assert_called_once_with()
    mock_runner.process.waitForFinished.assert_called_once_with()
    view.remove_python_runner.assert_called_once_with()
    view.remove_debug_inspector.assert_called_once_with()
    editor.change_mode.assert_called_once_with('python')
    assert editor.mode == 'python'
    view.set_read_only.assert_called_once_with(False)


def test_debug_finished():
    """
    Ensure the end-state of the mode is enacted when the running script has
    finished executing.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {
        'stop': mock.MagicMock(),
        'run': mock.MagicMock(),
        'step-over': mock.MagicMock(),
        'step-in': mock.MagicMock(),
        'step-out': mock.MagicMock(),
    }
    dm = DebugMode(editor, view)
    mock_debugger = mock.MagicMock()
    dm.debugger = mock_debugger
    mock_debugger.bp_index = []
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.enabled = True
    mock_debugger.breakpoints.side_effect = [
        {
            1: mock_breakpoint,
        },
        {},
    ]
    tab1 = mock.MagicMock()
    tab1.path = 'foo'
    tab2 = mock.MagicMock()
    view.widgets = [tab1, tab2]
    dm.finished(None, None)
    # Buttons are set to the right state.
    assert view.button_bar.slots['stop'].setEnabled.call_count == 0
    view.button_bar.slots['run'].setEnabled.assert_called_once_with(False)
    view.button_bar.slots['step-over'].\
        setEnabled.assert_called_once_with(False)
    view.button_bar.slots['step-in'].setEnabled.assert_called_once_with(False)
    view.button_bar.slots['step-out'].setEnabled.assert_called_once_with(False)
    # Tabs are set to the right state.
    tab1.markerDeleteAll.assert_called_once_with()
    tab1.breakpoint_lines == set([1, ])
    tab1.setSelection.assert_called_once_with(0, 0, 0, 0)
    tab1.markerAdd(0, tab1.BREAKPOINT_MARKER)
    tab2.markerDeleteAll.assert_called_once_with()
    tab2.breakpoint_lines == set()
    tab2.setSelection.assert_called_once_with(0, 0, 0, 0)


def test_debug_button_stop():
    """
    Ensure the stop method is called when the stop button is clicked.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.stop = mock.MagicMock()
    dm.button_stop(None)
    dm.stop.assert_called_once_with()


def test_debug_button_continue():
    """
    Ensure the do_run method is called when the continue button is clicked.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.button_continue(None)
    dm.debugger.do_run.assert_called_once_with()


def test_debug_button_step_over():
    """
    Ensure the do_next method is called when the step-over button is clicked.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.button_step_over(None)
    dm.debugger.do_next.assert_called_once_with()


def test_debug_button_step_in():
    """
    Ensure the do_step method is called when the step-in button is clicked.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.button_step_in(None)
    dm.debugger.do_step.assert_called_once_with()


def test_debug_button_step_out():
    """
    Ensure the do_return method is called when the step-out button is clicked.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.button_step_out(None)
    dm.debugger.do_return.assert_called_once_with()


def test_debug_toggle_breakpoint_off():
    """
    If a breakpoint is on, it's toggled off.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    mock_debugger = mock.MagicMock()
    dm.debugger = mock_debugger
    mock_breakpoint = mock.MagicMock()
    mock_debugger.breakpoints.side_effect = [
        {
            1: mock_breakpoint,
        },
    ]
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    mock_tab.markersAtLine.return_value = True
    dm.toggle_breakpoint(0, mock_tab)
    mock_debugger.breakpoints.assert_called_once_with(mock_tab.path)
    mock_tab.markersAtLine.assert_called_once_with(0)
    mock_debugger.disable_breakpoint(mock_breakpoint)
    mock_tab.markerDelete.assert_called_once_with(0,
                                                  mock_tab.BREAKPOINT_MARKER)


def test_debug_toggle_breakpoint_on_new():
    """
    If the breakpoint is off but disabled, enable it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    mock_debugger = mock.MagicMock()
    dm.debugger = mock_debugger
    mock_breakpoint = mock.MagicMock()
    mock_debugger.breakpoints.side_effect = [
        {
            1: mock_breakpoint,
        },
    ]
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    mock_tab.markersAtLine.return_value = False
    dm.toggle_breakpoint(0, mock_tab)
    dm.debugger.enable_breakpoint.assert_called_once_with(mock_breakpoint)


def test_debug_toggle_breakpoint_on_existing():
    """
    If the breakpoint doesn't exist, create it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    mock_debugger = mock.MagicMock()
    dm.debugger = mock_debugger
    mock_debugger.breakpoints.return_value = {}
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    mock_tab.markersAtLine.return_value = False
    dm.toggle_breakpoint(0, mock_tab)
    dm.debugger.create_breakpoint.assert_called_once_with(mock_tab.path, 1)


def test_debug_on_bootstrap():
    """
    Ensure all the current breakpoints are set and the script is run.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = 'foo'
    mock_tab.breakpoint_lines = set([0, ])
    view.widgets = [mock_tab, ]
    dm.debug_on_bootstrap()
    dm.debugger.create_breakpoint.assert_called_once_with(mock_tab.path, 1)
    dm.debugger.do_run.assert_called_once_with()


def test_debug_on_breakpoint_enable():
    """
    Handle the signal that shows the debug runner has created a breakpoint.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    view.current_tab = mock_tab
    dm = DebugMode(editor, view)
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.line = 1
    dm.debug_on_breakpoint_enable(mock_breakpoint)
    mock_tab.markerAdd.assert_called_once_with(mock_breakpoint.line - 1,
                                               mock_tab.BREAKPOINT_MARKER)


def test_debug_on_breakpoint_disable():
    """
    Handle the signal that shows the debug runner has disabled a breakpoint.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    view.current_tab = mock_tab
    dm = DebugMode(editor, view)
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.line = 1
    dm.debug_on_breakpoint_disable(mock_breakpoint)
    mock_tab.markerDelete.assert_called_once_with(mock_breakpoint.line - 1,
                                                  mock_tab.BREAKPOINT_MARKER)
