# -*- coding: utf-8 -*-
"""
Tests for the debug mode.
"""
from mu.debugger.config import DEBUGGER_PORT
from mu.modes.debugger import DebugMode
from mu.virtual_environment import venv
from unittest import mock


def test_debug_mode():
    """
    Sanity check for setting up of the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    assert dm.name == "Graphical Debugger"
    assert dm.description is not None
    assert dm.icon == "python"
    assert dm.runner is None
    assert dm.is_debugger is True
    assert dm.editor == editor
    assert dm.view == view

    assert dm.api() == []

    actions = dm.actions()
    assert len(actions) == 5
    assert actions[0]["name"] == "stop"
    assert actions[0]["handler"] == dm.button_stop
    assert actions[1]["name"] == "run"
    assert actions[1]["handler"] == dm.button_continue
    assert actions[2]["name"] == "step-over"
    assert actions[2]["handler"] == dm.button_step_over
    assert actions[3]["name"] == "step-in"
    assert actions[3]["handler"] == dm.button_step_in
    assert actions[4]["name"] == "step-out"
    assert actions[4]["handler"] == dm.button_step_out


def test_debug_start():
    """
    Ensure the handling of starting the debugger works as expected.
    """
    editor = mock.MagicMock()
    editor.envars = [["name", "value"]]
    view = mock.MagicMock()
    view.current_tab.path = "/foo/bar"
    view.current_tab.isModified.return_value = True
    mock_runner = mock.MagicMock()
    view.add_python3_runner.return_value = mock_runner
    mock_debugger = mock.MagicMock()
    mock_debugger_class = mock.MagicMock(return_value=mock_debugger)
    dm = DebugMode(editor, view)
    with mock.patch(
        "mu.modes.debugger.Debugger", mock_debugger_class
    ), mock.patch.object(venv, "interpreter", "interpreter"):
        dm.start()
    editor.save_tab_to_file.assert_called_once_with(view.current_tab)
    view.add_python3_runner.assert_called_once_with(
        "interpreter",
        "/foo/bar",
        "/foo",
        debugger=True,
        envars=[["name", "value"]],
    )
    mock_runner.process.waitForStarted.assert_called_once_with()
    mock_runner.process.finished.connect.assert_called_once_with(dm.finished)
    view.add_debug_inspector.assert_called_once_with()
    view.set_read_only.assert_called_once_with(True)
    mock_debugger_class.assert_called_once_with(
        "localhost", DEBUGGER_PORT, proc=mock_runner.process
    )
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
    mock_runner.stop_process.assert_called_once_with()
    view.remove_python_runner.assert_called_once_with()
    view.remove_debug_inspector.assert_called_once_with()
    editor.change_mode.assert_called_once_with("python")
    assert editor.mode == "python"
    view.set_read_only.assert_called_once_with(False)


def test_debug_finished():
    """
    Ensure the end-state of the mode is enacted when the running script has
    finished executing.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {
        "stop": mock.MagicMock(),
        "run": mock.MagicMock(),
        "step-over": mock.MagicMock(),
        "step-in": mock.MagicMock(),
        "step-out": mock.MagicMock(),
    }
    dm = DebugMode(editor, view)
    mock_debugger = mock.MagicMock()
    dm.debugger = mock_debugger
    mock_debugger.bp_index = []
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.enabled = True
    mock_debugger.breakpoints.side_effect = [{1: mock_breakpoint}, {}]
    tab1 = mock.MagicMock()
    tab1.path = "foo"
    tab2 = mock.MagicMock()
    view.widgets = [tab1, tab2]
    dm.finished()
    # Buttons are set to the right state.
    assert view.button_bar.slots["stop"].setEnabled.call_count == 0
    view.button_bar.slots["run"].setEnabled.assert_called_once_with(False)
    view.button_bar.slots["step-over"].setEnabled.assert_called_once_with(
        False
    )
    view.button_bar.slots["step-in"].setEnabled.assert_called_once_with(False)
    view.button_bar.slots["step-out"].setEnabled.assert_called_once_with(False)
    # Tabs are set to the right state.
    tab1.setSelection.assert_called_once_with(0, 0, 0, 0)
    tab1.reset_debugger_highlight.assert_called_once_with()
    tab2.setSelection.assert_called_once_with(0, 0, 0, 0)
    tab2.reset_debugger_highlight.assert_called_once_with()


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
    assert view.current_tab.reset_debugger_highlight.call_count == 1


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
    assert view.current_tab.reset_debugger_highlight.call_count == 1


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
    assert view.current_tab.reset_debugger_highlight.call_count == 1


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
    assert view.current_tab.reset_debugger_highlight.call_count == 1


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
    mock_debugger.breakpoints.side_effect = [{1: mock_breakpoint}]
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
    mock_tab.markersAtLine.return_value = True
    dm.toggle_breakpoint(0, mock_tab)
    mock_debugger.breakpoints.assert_called_once_with(mock_tab.path)
    mock_tab.markersAtLine.assert_called_once_with(0)
    mock_debugger.disable_breakpoint.assert_called_once_with(mock_breakpoint)
    mock_tab.markerDelete.assert_called_once_with(
        0, mock_tab.BREAKPOINT_MARKER
    )


def test_debug_toggle_breakpoint_off_no_breakpoint():
    """
    If a breakpoint appears on a line, but it's not actually been created in
    the debug runner process (perhaps because the breakpoint was created after
    the process finished but before the stop button was created) then it's
    toggled off with no further side-effects.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    mock_debugger = mock.MagicMock()
    dm.debugger = mock_debugger
    mock_debugger.breakpoints.side_effect = [{}]
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
    mock_tab.markersAtLine.return_value = True
    dm.toggle_breakpoint(0, mock_tab)
    mock_debugger.breakpoints.assert_called_once_with(mock_tab.path)
    mock_tab.markersAtLine.assert_called_once_with(0)
    assert mock_debugger.disable_breakpoint.call_count == 0
    mock_tab.markerDelete.assert_called_once_with(
        0, mock_tab.BREAKPOINT_MARKER
    )


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
    mock_debugger.breakpoints.side_effect = [{1: mock_breakpoint}]
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
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
    mock_tab.path = "foo"
    mock_tab.markersAtLine.return_value = False
    dm.toggle_breakpoint(0, mock_tab)
    dm.debugger.create_breakpoint.assert_called_once_with(mock_tab.path, 1)


def test_debug_on_fail():
    """
    Ensure an appropriate message is shown to the user and the UI is put into
    the correct state if the debug client calls this function because it can't
    connect to the runner.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.finished = mock.MagicMock()
    dm.debug_on_fail("This is a useful message")
    assert view.process_runner.append.call_count == 1  # message shown.
    dm.finished.assert_called_once_with()
    view.process_runner.finished.assert_called_once_with(1, -1)


def test_debug_on_bootstrap():
    """
    Ensure all the current breakpoints are set and the script is run.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
    mock_tab.text.return_value = "print('Hello')"
    mock_tab.breakpoint_handles = set([0])
    mock_tab.markerLine.return_value = 0
    view.widgets = [mock_tab]
    dm.debug_on_bootstrap()
    dm.debugger.create_breakpoint.assert_called_once_with(mock_tab.path, 1)
    dm.debugger.do_run.assert_called_once_with()


def test_debug_on_bootstrap_remove_missing_marker_handles():
    """
    Ensure all marker handles that are not currently associated with a line
    are removed from the breakpoint_handles set.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
    mock_tab.breakpoint_handles = set([0])
    mock_tab.markerLine.return_value = -1
    view.widgets = [mock_tab]
    dm.debug_on_bootstrap()
    assert dm.debugger.create_breakpoint.call_count == 0
    assert 0 not in mock_tab.breakpoint_handles


def test_debug_on_bootstrap_ignore_duplicate_handles():
    """
    Sometimes it's possible for two different handles to be found on a single
    line due to how Scintilla moves markers around as lines are concatenated.
    This ensures only one breakpoint is created per marker.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
    mock_tab.text.return_value = "print('Hello')"
    mock_tab.breakpoint_handles = set([0, 1])
    mock_tab.markerLine.side_effect = [1, 1]
    view.widgets = [mock_tab]
    dm.debug_on_bootstrap()
    assert dm.debugger.create_breakpoint.call_count == 1


def test_debug_on_bootstrap_remove_invalid_breaks():
    """
    Sometimes it's possible for a marker to end up on a line that is eventually
    an in-valid breakpoint line. This checks that such markers don't end up
    with an attempt to set a breakpoint and are ultimately discarded so the
    visual state of the markers matches the breakpoint state of the debugger.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.path = "foo"
    mock_tab.breakpoint_handles = set([0])
    mock_tab.markerLine.return_value = 1
    view.widgets = [mock_tab]
    with mock.patch(
        "mu.modes.debugger.is_breakpoint_line", return_value=False
    ):
        dm.debug_on_bootstrap()
    assert 0 not in mock_tab.breakpoint_handles
    mock_tab.markerDelete.assert_called_once_with(1, -1)


def test_debug_on_breakpoint_enable():
    """
    Handle the signal that shows the debug runner has created a breakpoint.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.markersAtLine.return_value = False
    mock_tab.path = "foo"
    view.current_tab = mock_tab
    dm = DebugMode(editor, view)
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.filename = "foo"
    mock_breakpoint.line = 1
    dm.debug_on_breakpoint_enable(mock_breakpoint)
    mock_tab.markerAdd.assert_called_once_with(
        mock_breakpoint.line - 1, mock_tab.BREAKPOINT_MARKER
    )


def test_debug_on_breakpoint_enable_different_tab():
    """
    When the breakpoints are set on bootstrap, some of them may be for tabs
    that are not the currently visible tab. In any case, when breakpoints are
    set "on_breakpoint_enable" is called. This check ensures the marker is only
    created IF the current tab has the same path as the filename associated
    with the newly created breakpoint.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.markersAtLine.return_value = False
    mock_tab.path = "foo"
    view.current_tab = mock_tab
    dm = DebugMode(editor, view)
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.filename = "bar"
    mock_breakpoint.line = 1
    dm.debug_on_breakpoint_enable(mock_breakpoint)
    assert mock_tab.markerAdd.call_count == 0


def test_debug_on_breakpoint_enable_marker_already_exists():
    """
    Handle the signal that shows the debug runner has created a breakpoint
    during the bootstrapping of the debug runner, so it doesn't add a second
    marker at the same location as the pre-existing one that caused the
    breakpoint to be created during bootstrapping.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.markersAtLine.return_value = True
    view.current_tab = mock_tab
    dm = DebugMode(editor, view)
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.line = 1
    dm.debug_on_breakpoint_enable(mock_breakpoint)
    mock_tab.markerAdd.call_count == 0


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
    mock_tab.markerDelete.assert_called_once_with(
        mock_breakpoint.line - 1, mock_tab.BREAKPOINT_MARKER
    )


def test_debug_on_line_ignore_file():
    """
    If the filename is in the ignored bucket, do a return.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.debug_on_line("bdb.py", 100)
    dm.debugger.do_return.assert_called_once_with()


def test_debug_on_line():
    """
    Ensure the view is updated to the expected tab and the correct line is
    selected therein.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    mock_tab = mock.MagicMock()
    editor.get_tab.return_value = mock_tab
    dm.debug_on_line("foo.py", 100)
    view.current_tab.setSelection.assert_called_once_with(0, 0, 0, 0)
    mock_tab.setSelection(99, 0, 100, 0)


def test_debug_on_stack_no_stack():
    """
    In certain rare situations the runner could send an empty stack.

    ToDo: Look into this.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debug_on_stack([])
    assert view.update_debug_inspector.call_count == 0


def test_debug_on_stack():
    """
    Ensure the expected locals dict is passed to the view so the object
    inspector is updated properly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    stack = [
        (1, {"locals": {"a": "frame1", "b": "frame1"}}),
        (2, {"locals": {"b": "frame2", "c": "frame2"}}),
    ]
    dm.debug_on_stack(stack)
    view.update_debug_inspector.assert_called_once_with(
        {"a": "frame1", "b": "frame2", "c": "frame2"}
    )


def test_debug_on_postmortem():
    """
    Ensure that the args and kwargs passed as a context for postmortem and
    appended to the text area displaying stdout from the Python process.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    args = ["foo", "bar"]
    kwargs = {"baz": "qux"}
    dm.debug_on_postmortem(args, kwargs)
    assert view.process_runner.append.call_count == 3


def test_debug_on_info():
    """
    Information messages result in a status message being shown by the editor.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debug_on_info("message")
    expected = "Debugger info: message"
    editor.show_status_message.assert_called_once_with(expected)


def test_debug_on_warning():
    """
    Warning messages result in a status message being shown by the editor.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debug_on_warning("message")
    expected = "Debugger warning: message"
    editor.show_status_message.assert_called_once_with(expected)


def test_debug_on_error():
    """
    Error messages result in a status message being shown by the editor.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debug_on_error("message")
    expected = "Debugger error: message"
    editor.show_status_message.assert_called_once_with(expected)


def test_debug_on_call():
    """
    Calling a function causes the debugger to step into the function.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.debug_on_call(None)
    dm.debugger.do_step.assert_called_once_with()


def test_debug_on_return():
    """
    Returning from a function causes the debugger to step out of the function.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.debug_on_return(None)
    dm.debugger.do_step.assert_called_once_with()


def test_debug_on_finished():
    """
    When the debugger is finished, the view is reset.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.finished = mock.MagicMock()
    dm.debug_on_finished()
    dm.finished.assert_called_once_with()


def test_debug_on_breakpoint_ignore():
    """
    Should do nothing.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    assert dm.debug_on_breakpoint_ignore(None, None) is None


def test_debug_on_breakpoint_clear():
    """
    Should do nothing.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    assert dm.debug_on_breakpoint_clear(None) is None


def test_debug_on_restart():
    """
    Should do nothing.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    assert dm.debug_on_restart() is None


def test_debug_on_exception():
    """
    Since an exception has been signalled, allow the script to run to the
    end of life so the error is correctly reported via stdout.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)
    dm.debugger = mock.MagicMock()
    dm.debug_on_exception("Exception", "Exception information")
    dm.debugger.do_run.assert_called_once_with()
    assert view.current_tab.reset_debugger_highlight.call_count == 1


def test_enable_buttons_before_delayed_disable_buttons():
    """
    Calling `enable_buttons` before the disable button timer fires i) cancels
    that timer and, ii) does not call the code that actually enables buttons.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    dm = DebugMode(editor, view)

    # Mocked active timer.
    timer_mock = mock.MagicMock()
    timer_mock.isActive.return_value = True
    dm._button_disable_timer = timer_mock

    # Mocked underlying _enable_buttons method.
    real_enable_method_mock = mock.MagicMock()
    dm._enable_buttons = real_enable_method_mock

    # Call enable_buttons to check behaviour.
    dm.enable_buttons()

    # Timer should have been stopped.
    timer_mock.stop.assert_called_once_with()

    # Underlying _enable_buttons method should not have been called.
    assert real_enable_method_mock.call_count == 0
