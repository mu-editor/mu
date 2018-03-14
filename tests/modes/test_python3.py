# -*- coding: utf-8 -*-
"""
Tests for the Python3 mode.
"""
from mu.modes.python3 import PythonMode, KernelRunner
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, PI_APIS
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
    assert len(actions) == 3
    assert actions[0]['name'] == 'run'
    assert actions[0]['handler'] == pm.run_toggle
    assert actions[1]['name'] == 'debug'
    assert actions[1]['handler'] == pm.debug
    assert actions[2]['name'] == 'repl'
    assert actions[2]['handler'] == pm.toggle_repl


def test_python_api():
    """
    Make sure the API definition is as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    result = pm.api()
    assert result == SHARED_APIS + PYTHON3_APIS + PI_APIS


def test_python_run_toggle_on():
    """
    Check the handler for clicking run starts the new process and updates the
    UI state.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {
        'debug': mock.MagicMock(),
        'modes': mock.MagicMock(),
        'run': mock.MagicMock(),
    }
    pm = PythonMode(editor, view)
    pm.runner = None

    def runner(pm=pm):
        pm.runner = True

    pm.run_script = mock.MagicMock(side_effect=runner)
    pm.run_toggle(None)
    pm.run_script.assert_called_once_with()
    slot = pm.view.button_bar.slots['run']
    assert slot.setIcon.call_count == 1
    slot.setText.assert_called_once_with('Stop')
    slot.setToolTip.assert_called_once_with('Stop your Python script.')
    pm.view.button_bar.slots['debug'].setEnabled.assert_called_once_with(False)
    pm.view.button_bar.slots['modes'].setEnabled.assert_called_once_with(False)


def test_python_run_toggle_on_cancelled():
    """
    Ensure the button states are correct if running an unsaved script is
    cancelled before the process is allowed to start. See issue #338.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.runner = None
    pm.run_script = mock.MagicMock()
    pm.run_toggle(None)
    pm.run_script.assert_called_once_with()
    slot = pm.view.button_bar.slots['run']
    assert slot.setIcon.call_count == 0


def test_python_run_toggle_off():
    """
    Check the handler for clicking run stops the process and reverts the UI
    state.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {
        'debug': mock.MagicMock(),
        'modes': mock.MagicMock(),
        'run': mock.MagicMock(),
    }
    pm = PythonMode(editor, view)
    pm.runner = True
    pm.stop_script = mock.MagicMock()
    pm.run_toggle(None)
    pm.stop_script.assert_called_once_with()
    slot = pm.view.button_bar.slots['run']
    assert slot.setIcon.call_count == 1
    slot.setText.assert_called_once_with('Run')
    slot.setToolTip.assert_called_once_with('Run your Python script.')
    pm.view.button_bar.slots['debug'].setEnabled.assert_called_once_with(True)
    pm.view.button_bar.slots['modes'].setEnabled.assert_called_once_with(True)


def test_python_run_script():
    """
    Ensure that running the script launches the process as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = '/foo'
    view.current_tab.isModified.return_value = True
    mock_runner = mock.MagicMock()
    view.add_python3_runner.return_value = mock_runner
    pm = PythonMode(editor, view)
    pm.workspace_dir = mock.MagicMock(return_value='/bar')
    with mock.patch('builtins.open') as oa, \
            mock.patch('mu.modes.python3.write_and_flush'):
        pm.run_script()
        oa.assert_called_once_with('/foo', 'w', newline='')
    view.add_python3_runner.assert_called_once_with('/foo', '/bar',
                                                    interactive=True)
    mock_runner.process.waitForStarted.assert_called_once_with()


def test_python_run_script_no_editor():
    """
    If there's no active tab, there can be no runner either.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PythonMode(editor, view)
    pm.stop_script = mock.MagicMock()
    pm.run_script()
    assert pm.runner is None
    pm.stop_script.assert_called_once_with()


def test_python_run_script_needs_saving():
    """
    If the file hasn't been saved yet (it's unnamed), prompt the user to save
    it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = None
    pm = PythonMode(editor, view)
    pm.stop_script = mock.MagicMock()
    pm.run_script()
    editor.save.assert_called_once_with()


def test_python_stop_script():
    """
    Check that the child process is killed, the runner cleaned up and UI
    is reset.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    mock_runner = mock.MagicMock()
    pm.runner = mock_runner
    pm.stop_script()
    mock_runner.process.kill.assert_called_once_with()
    mock_runner.process.waitForFinished.assert_called_once_with()
    assert pm.runner is None
    view.remove_python_runner.assert_called_once_with()


def test_python_stop_script_no_runner():
    """
    If the script is cancelled before the child process is created ensure
    nothing breaks and the UI is reset.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.runner = None
    pm.stop_script()
    view.remove_python_runner.assert_called_once_with()


def test_python_debug():
    """
    Ensure Python3 mode hands over running of the script to the debug mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PythonMode(editor, view)
    pm.debug(None)
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
