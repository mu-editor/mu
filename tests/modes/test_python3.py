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


def test_python_api():
    """
    Make sure the API definition is as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    result = pm.api()
    assert isinstance(result, list)


def test_python_toggle_run():
    """
    Ensure the toggle method toggles!
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.run = mock.MagicMock()
    pm.stop = mock.MagicMock()
    pm.toggle_run(None)
    pm.run.assert_called_once_with()
    pm.runner = True
    pm.toggle_run(None)
    pm.stop.assert_called_once_with()


def test_python_run():
    """
    Ensure the run handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = '/foo'
    view.current_tab.isModified.return_value = True
    mock_runner = mock.MagicMock()
    view.add_python3_runner.return_value = mock_runner
    pm = PythonMode(editor, view)
    pm.workspace_dir = mock.MagicMock(return_value='/bar')
    with mock.patch('mu.modes.python3.open_atomic') as oa:
        pm.run()
        oa.assert_called_once_with('/foo', 'w', newline='')
    view.add_python3_runner.assert_called_once_with('/foo', '/bar')
    assert pm.runner == mock_runner


def test_python_run_no_tab():
    """
    If there's no active tab, there can be no runner either.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PythonMode(editor, view)
    pm.run()
    assert pm.runner is None


def test_python_run_prompt_for_unsaved_file():
    """
    If the file hasn't been saved yet (it's unnamed), prompt the user to save
    it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = None
    pm = PythonMode(editor, view)
    pm.run()
    editor.save.assert_called_once_with()
    assert pm.runner is None


def test_python_stop():
    """
    Ensure the script runner is cleaned up properly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    mock_runner = mock.MagicMock()
    pm.runner = mock_runner
    pm.stop()
    assert pm.runner is None
    mock_runner.process.kill.assert_called_once_with()


def test_python_toggle_repl():
    """
    Ensure the REPL handling works as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.add_repl = mock.MagicMock()
    pm.remove_repl = mock.MagicMock()
    pm.toggle_repl(None)
    pm.add_repl.assert_called_once_with()
    pm.repl = True
    pm.toggle_repl(None)
    pm.remove_repl.assert_called_once_with()


def test_python_add_repl():
    """
    Check the REPL's kernal manager is configured correctly before being handed
    to the Jupyter widget in the view.
    """
    mock_kernel_manager = mock.MagicMock()
    mock_manager_class = mock.MagicMock(return_value=mock_kernel_manager)
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    with mock.patch('mu.modes.python3.QtInProcessKernelManager',
                    mock_manager_class):
        pm.add_repl()
    mock_kernel_manager.start_kernel.assert_called_once_with(show_banner=False)
    view.add_jupyter_repl.assert_called_once_with(mock_kernel_manager)
    assert pm.repl == mock_kernel_manager


def test_python_remove_repl():
    """
    Make sure the REPL is removed properly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.repl = True
    pm.remove_repl()
    assert pm.repl is None
    view.remove_repl.assert_called_once_with()
