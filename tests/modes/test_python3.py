# -*- coding: utf-8 -*-
"""
Tests for the Python3 mode.
"""
from mu.modes.python3 import PythonMode, KernelRunner
from mu.modes.api import PYTHON3_APIS, SHARED_APIS
from unittest import mock


def test_kernel_runner_start_kernel():
    """
    Ensure the start_kernel method eventually emits the kernel_started signal
    with the associated kernel manager and kernel client objects for
    subsequent use.
    """
    mock_kernel_manager = mock.MagicMock()
    mock_client = mock.MagicMock()
    mock_kernel_manager.client.return_value = mock_client
    kr = KernelRunner(cwd='/a/path/to/mu_code')
    kr.kernel_started = mock.MagicMock()
    mock_os = mock.MagicMock()
    with mock.patch('mu.modes.python3.os', mock_os), \
            mock.patch('mu.modes.python3.QtKernelManager',
                       return_value=mock_kernel_manager):
        kr.start_kernel()
    mock_os.chdir.assert_called_once_with('/a/path/to/mu_code')
    assert kr.repl_kernel_manager == mock_kernel_manager
    mock_kernel_manager.start_kernel.assert_called_once_with()
    assert kr.repl_kernel_client == mock_client
    kr.kernel_started.emit.assert_called_once_with(mock_kernel_manager,
                                                   mock_client)


def test_kernel_runner_stop_kernel():
    """
    Ensure the stop_kernel method eventually emits the kernel_finished
    signal once it has stopped the client communication channels and shutdown
    the kernel in the quickest way possible.
    """
    kr = KernelRunner(cwd='/a/path/to/mu_code')
    kr.repl_kernel_client = mock.MagicMock()
    kr.repl_kernel_manager = mock.MagicMock()
    kr.kernel_finished = mock.MagicMock()
    kr.stop_kernel()
    kr.repl_kernel_client.stop_channels.assert_called_once_with()
    kr.repl_kernel_manager.shutdown_kernel.assert_called_once_with(now=True)
    kr.kernel_finished.emit.assert_called_once_with()


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
    assert pm.is_debugger is False
    assert pm.editor == editor
    assert pm.view == view

    actions = pm.actions()
    assert len(actions) == 2
    assert actions[0]['name'] == 'run'
    assert actions[0]['handler'] == pm.run
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
    assert result == SHARED_APIS + PYTHON3_APIS


def test_python_run():
    """
    Ensure Python3 mode hands over running of the script to the debug mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.run(None)
    editor.change_mode.assert_called_once_with('debugger')
    assert editor.mode == 'debugger'
    editor.modes['debugger'].start.assert_called_once_with()


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
    pm.kernel_runner = True
    pm.toggle_repl(None)
    pm.remove_repl.assert_called_once_with()


def test_python_add_repl():
    """
    Check the REPL's kernal manager is configured correctly before being handed
    to the Jupyter widget in the view.
    """
    mock_qthread = mock.MagicMock()
    mock_kernel_runner = mock.MagicMock()
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.stop_kernel = mock.MagicMock()
    with mock.patch('mu.modes.python3.QThread', mock_qthread), \
            mock.patch('mu.modes.python3.KernelRunner', mock_kernel_runner):
        pm.add_repl()
    mock_qthread.assert_called_once_with()
    mock_kernel_runner.assert_called_once_with(cwd=pm.workspace_dir())
    assert pm.kernel_thread == mock_qthread()
    assert pm.kernel_runner == mock_kernel_runner()
    view.button_bar.slots['repl'].setEnabled.assert_called_once_with(False)
    pm.kernel_runner.moveToThread.assert_called_once_with(pm.kernel_thread)
    pm.kernel_runner.kernel_started.connect.\
        assert_called_once_with(pm.on_kernel_start)
    pm.kernel_runner.kernel_finished.connect.\
        assert_called_once_with(pm.kernel_thread.quit)
    pm.stop_kernel.connect.\
        assert_called_once_with(pm.kernel_runner.stop_kernel)
    pm.kernel_thread.started.connect.\
        assert_called_once_with(pm.kernel_runner.start_kernel)
    pm.kernel_thread.finished.connect.\
        assert_called_once_with(pm.on_kernel_stop)
    pm.kernel_thread.start.assert_called_once_with()


def test_python_remove_repl():
    """
    Make sure the REPL is removed properly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.stop_kernel = mock.MagicMock()
    pm.remove_repl()
    pm.stop_kernel.emit.assert_called_once_with()
    view.button_bar.slots['repl'].setEnabled.assert_called_once_with(False)


def test_python_on_kernel_start():
    """
    Ensure the handler for when the kernel has started updates the UI such that
    the kernel manager and kernel client are used to add the Jupyter widget to
    the UI, the REPL button is re-enabled and a status update is shown.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    mock_kernel_manager = mock.MagicMock()
    mock_client = mock.MagicMock()
    pm.on_kernel_start(mock_kernel_manager, mock_client)
    view.add_jupyter_repl.assert_called_once_with(mock_kernel_manager,
                                                  mock_client)
    view.button_bar.slots['repl'].setEnabled.assert_called_once_with(True)
    editor.show_status_message.assert_called_once_with('REPL started.')


def test_python_on_kernel_stop():
    """
    Ensure everything REPL based is cleaned up when this handler is called.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {
        'repl': mock.MagicMock(),
    }
    pm = PythonMode(editor, view)
    pm.on_kernel_stop()
    assert pm.repl_kernel_manager is None
    view.button_bar.slots['repl'].setEnabled.assert_called_once_with(True)
    editor.show_status_message.assert_called_once_with('REPL stopped.')
    assert pm.kernel_runner is None
    assert pm.kernel_thread is None
