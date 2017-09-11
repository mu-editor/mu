# -*- coding: utf-8 -*-
"""
Tests for the debug client.
"""
import socket
import pytest
import json
import mu.debugger.client
from unittest import mock
from PyQt5.QtCore import pyqtBoundSignal


def test_Breakpoint_init():
    """
    Ensure the Breakpoint class is initialised as expected.
    """
    bp = mu.debugger.client.Breakpoint(1, 'filename.py', 10)
    assert bp.bpnum == 1
    assert bp.filename == 'filename.py'
    assert bp.line == 10
    assert bp.enabled is True
    assert bp.temporary is False
    assert bp.funcname is None


def test_Breakpoint_str():
    """
    Ensure a string representation of a Breakpoint is meaningful.
    """
    bp = mu.debugger.client.Breakpoint(1, 'filename.py', 10)
    assert str(bp) == 'filename.py:10'


def test_CommandBufferHandler_init():
    """
    Check the CommandBufferHandler initialises as expected: with two signals
    and a reference to the debugger client instance.
    """
    mock_debugger = mock.MagicMock()
    cbh = mu.debugger.client.CommandBufferHandler(mock_debugger)
    assert isinstance(cbh.on_command, pyqtBoundSignal)
    assert isinstance(cbh.on_fail, pyqtBoundSignal)
    assert cbh.debugger == mock_debugger


def test_CommandBufferHandler_worker_with_error():
    """
    Check that the connection will try up to 10 times before emitting an
    on_fail signal.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger.host = 'localhost'
    mock_debugger.port = 9999
    mock_socket_factory = mock.MagicMock()
    mock_socket = mock.MagicMock()
    mock_socket.connect.side_effect = ConnectionRefusedError()
    mock_socket_factory.socket.return_value = mock_socket
    mock_time = mock.MagicMock()
    mock_debugger = mock.MagicMock()
    cbh = mu.debugger.client.CommandBufferHandler(mock_debugger)
    cbh.on_fail = mock.MagicMock()
    with mock.patch('mu.debugger.client.socket', mock_socket_factory), \
            mock.patch('mu.debugger.client.time', mock_time):
        cbh.worker()
    msg = 'Could not connect to debug runner.'
    cbh.on_fail.emit.assert_called_once_with(msg)
    assert mock_socket.connect.call_count == 10
    assert mock_time.sleep.call_count == 9


def test_CommandBufferHandler_worker_break_loop():
    """
    Ensure if the worker receives None from the socket then break out of the
    loop to end the thread.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger.host = 'localhost'
    mock_debugger.port = 9999
    mock_socket_factory = mock.MagicMock()
    mock_socket = mock.MagicMock()
    mock_socket.recv.return_value = None
    mock_socket_factory.socket.return_value = mock_socket
    cbh = mu.debugger.client.CommandBufferHandler(mock_debugger)
    with mock.patch('mu.debugger.client.socket', mock_socket_factory):
        cbh.worker()
    mock_socket.recv.assert_called_once_with(1024)


def test_command_buffer_message():
    """
    Make sure that the command buffer of bytes received with a terminated
    message results in the expected command, associated arguments and the
    remainder is correctly populated.
    """
    msg = json.dumps(["bootstrap", {'arg': 'value'}]).encode('utf-8')
    msg += mu.debugger.client.Debugger.ETX
    # Splitting the message in two ensures remainder handling is exercised.
    pos = len(msg) // 2
    msg1 = msg[:pos]
    msg2 = msg[pos:]
    mock_debugger = mock.MagicMock()
    mock_debugger.ETX = mu.debugger.client.Debugger.ETX
    mock_debugger.host = 'localhost'
    mock_debugger.port = 9999
    mock_socket_factory = mock.MagicMock()
    mock_socket = mock.MagicMock()
    mock_socket_factory.socket.return_value = mock_socket
    mock_socket.recv.side_effect = [msg1, msg2, None]
    cbh = mu.debugger.client.CommandBufferHandler(mock_debugger)
    cbh.on_command = mock.MagicMock()
    with mock.patch('mu.debugger.client.socket', mock_socket_factory):
        cbh.worker()
    assert mock_debugger.socket.recv.call_count == 3
    expected = msg.replace(mu.debugger.client.Debugger.ETX,
                           b'').decode('utf-8')
    cbh.on_command.emit.assert_called_once_with(expected)


def test_Debugger_init():
    """
    Ensure a the Debugger client class initialises properly.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    assert db.host == 'localhost'
    assert db.port == 1908
    assert db.proc is None
    assert db.view is None


def test_Debugger_start():
    """
    Ensure the Debugger client starts a session correctly.
    """
    mock_thread_instance = mock.MagicMock()
    mock_thread = mock.MagicMock(return_value=mock_thread_instance)
    mock_handler_instance = mock.MagicMock()
    mock_handler = mock.MagicMock(return_value=mock_handler_instance)
    with mock.patch('mu.debugger.client.QThread', mock_thread), \
            mock.patch('mu.debugger.client.CommandBufferHandler',
                       mock_handler):
        db = mu.debugger.client.Debugger('localhost', 1908)
        db.start()
    mock_thread.assert_called_once_with()
    mock_thread_instance.started.connect.assert_called_once_with(
        mock_handler_instance.worker)
    mock_thread_instance.start.assert_called_once_with()
    mock_handler.assert_called_once_with(db)
    mock_handler_instance.moveToThread.\
        assert_called_once_with(mock_thread_instance)
    mock_handler_instance.on_command.connect.\
        assert_called_once_with(db.on_command)
    mock_handler_instance.on_fail.connect.assert_called_once_with(db.on_fail)


def test_Debugger_on_command():
    """
    Ensure the debug client handles command messages sent from the
    CommandBufferHandler thread.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.on_bootstrap = mock.MagicMock()
    msg = json.dumps(["bootstrap", {'arg': 'value'}])
    db.on_command(msg)
    db.on_bootstrap.assert_called_once_with(arg='value')


def test_Debugger_on_fail():
    """
    If a failure is emitted ensure it's logged.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    with mock.patch('mu.debugger.client.logger.error') as mock_log:
        db.on_fail('bang')
        mock_log.assert_called_once_with('bang')


def test_Debugger_stop():
    """
    Ensure the debugger client stops gracefully.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.proc = mock.MagicMock()
    db.output = mock.MagicMock()
    db.socket = mock.MagicMock()
    db.stop()
    db.proc.wait.assert_called_once_with()
    db.socket.shutdown.assert_called_once_with(socket.SHUT_WR)


def test_Debugger_output():
    """
    Ensure the "good case" call for output works (there appears to be a working
    socket connection).
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.socket = mock.MagicMock()
    db.output('test', foo='bar')
    db.socket.sendall.assert_called_once_with(b'["test", {"foo": "bar"}]\x03')


def test_Debugger_output_client_error():
    """
    Ensure that any debug client error is logged.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.socket = mock.MagicMock()
    db.socket.sendall.side_effect = OSError('bang!')
    with mock.patch('mu.debugger.client.logger.debug') as mock_logger:
        db.output('test', foo='bar')
        assert mock_logger.call_count == 2
        mock_logger.call_args_list[0][0] == 'Debugger client error.'
        mock_logger.call_args_list[1][0] == OSError('bang!')


def test_Debugger_output_no_client_connection():
    """
    Ensure that if output is attempted via a disconnected client, it's logged
    for further information.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.socket = mock.MagicMock()
    db.socket.sendall.side_effect = AttributeError('bang!')
    with mock.patch('mu.debugger.client.logger.debug') as mock_logger:
        db.output('test', foo='bar')
        assert mock_logger.call_count == 2
        mock_logger.call_args_list[0][0] == ('Debugger client not connected '
                                             'to runner.')
        mock_logger.call_args_list[1][0] == AttributeError('bang!')


def test_Debugger_breakpoint_as_tuple():
    """
    Given a tuple of (filename, line), check the breakpoint method returns an
    object representing the referenced breakpoint.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    mock_breakpoint = mock.MagicMock()
    db.bp_index = {
        'file.py': {
            666: mock_breakpoint,
        }
    }
    assert db.breakpoint(('file.py', 666)) == mock_breakpoint


def test_Debugger_breakpoint_as_breakpoint_number():
    """
    Given a breakpoint number, check the breakpoint method returns an object
    representing the referenced breakpoint.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    mock_breakpoint = mock.MagicMock()
    db.bp_list = {
        123: mock_breakpoint,
    }
    assert db.breakpoint(123) == mock_breakpoint


def test_Debugger_breakpoint_unknown():
    """
    Ensure the breakpoint method raises an UnknownBreakpoint exception if the
    referenced breakpoint is, you've guessed it, unknown.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    mock_breakpoint = mock.MagicMock()
    db.bp_list = {
        123: mock_breakpoint,
    }
    with pytest.raises(mu.debugger.client.UnknownBreakpoint):
        db.breakpoint(321)


def test_Debugger_breakpoints():
    """
    Given a filename, ensure all the related breakpoints are returned.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    mock_breakpoint = mock.MagicMock()
    db.bp_index = {
        'file.py': {
            666: mock_breakpoint,
        }
    }
    assert db.breakpoints('file.py') == {666: mock_breakpoint, }


def test_Debugger_create_breakpoint():
    """
    Ensure creating a new breakpoint results in the expected output call to the
    debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    db.create_breakpoint('file.py', 123)
    db.output.assert_called_once_with('break', filename='file.py', line=123,
                                      temporary=False)


def test_Debugger_enable_breakpoint():
    """
    Ensure enabling a breakpoint results in the expected output call to the
    debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.bpnum = 123
    db.enable_breakpoint(mock_breakpoint)
    db.output.assert_called_once_with('enable', bpnum=123)


def test_Debugger_disable_breakpoint():
    """
    Ensure disabling a breakpoint results in the expected output call to the
    debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.bpnum = 123
    db.disable_breakpoint(mock_breakpoint)
    db.output.assert_called_once_with('disable', bpnum=123)


def test_Debugger_ignore_breakpoint():
    """
    Ensure ignoring a breakpoint for "count" iterations results in the expected
    output call to the debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.bpnum = 123
    db.ignore_breakpoint(mock_breakpoint, 4)
    db.output.assert_called_once_with('ignore', bpnum=123, count=4)


def test_Debugger_clear_breakpoint():
    """
    Ensure clearing a breakpoint results in the expected output call to the
    debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_breakpoint.bpnum = 123
    db.clear_breakpoint(mock_breakpoint)
    db.output.assert_called_once_with('clear', bpnum=123)


def test_Debugger_do_run():
    """
    Ensure instructing the client to run to the next breakpoint results in the
    expected output call to the debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    db.do_run()
    db.output.assert_called_once_with('continue')


def test_Debugger_do_step():
    """
    Ensure instructing the client to step through one stack frame results in
    the expected output call to the debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    db.do_step()
    db.output.assert_called_once_with('step')


def test_Debugger_do_next():
    """
    Ensure instructing the client to go to the next line in the stack frame
    results in the expected output call to the debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    db.do_next()
    db.output.assert_called_once_with('next')


def test_Debugger_do_return():
    """
    Ensure instructing the client to return to the previous the stack frame
    results in the expected output call to the debug runner.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.output = mock.MagicMock()
    db.do_return()
    db.output.assert_called_once_with('return')


def test_Debugger_on_bootstrap():
    """
    Test the debug client responds correctly to a signal from the runner that
    it has finished setting up. Essentially this just means passing on details
    of breakpoints to on_breakpoint create.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_breakpoint_create = mock.MagicMock()
    breakpoints = [
        {
            'name': 'breakpoint1',
        },
        {
            'name': 'breakpoint2',
        },
    ]
    db.on_bootstrap(breakpoints)
    assert db.bp_index == {}
    assert db.bp_list == [True, ]
    assert db.on_breakpoint_create.call_count == 2
    db.view.debug_on_bootstrap.assert_called_once_with()


def test_Debugger_on_breakpoint_create():
    """
    Test the debug client handles the signal that a breakpoint is created in
    the expected manner, by instantiating a Breakpoint instance and adding it
    to the bp_index and bp_list datastructures before signalling to the view
    to display a visual representation of the breakpoint.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_bootstrap([])
    data = {
        'bpnum': 1,
        'filename': 'file.py',
        'line': 10,
    }
    db.on_breakpoint_create(**data)
    bp = db.bp_index['file.py'][10]
    assert bp.bpnum == 1
    assert bp.filename == 'file.py'
    assert bp.line == 10
    assert bp.enabled is True
    assert bp.temporary is False
    assert bp.funcname is None
    assert bp in db.bp_list
    db.view.debug_on_breakpoint_enable.assert_called_once_with(bp)


def test_Debugger_on_breakpoint_create_disabled():
    """
    As above, but the runner has signalled the breakpoint exists but is
    disabled.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_bootstrap([])
    data = {
        'bpnum': 1,
        'filename': 'file.py',
        'line': 10,
        'enabled': False,
    }
    db.on_breakpoint_create(**data)
    bp = db.bp_index['file.py'][10]
    assert bp.enabled is False
    db.view.debug_on_breakpoint_disable.assert_called_once_with(bp)


def test_Debugger_on_breakpoint_enable():
    """
    Handle when the runner signals that a breakpoint has transitioned to
    enabled.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_bootstrap([])
    data = {
        'bpnum': 1,
        'filename': 'file.py',
        'line': 10,
        'enabled': False,
    }
    db.on_breakpoint_create(**data)
    db.view.reset_mock()
    db.on_breakpoint_enable(1)
    bp = db.bp_index['file.py'][10]
    assert bp.enabled is True
    db.view.debug_on_breakpoint_enable.assert_called_once_with(bp)


def test_Debugger_on_breakpoint_disable():
    """
    Handle when the runner signals that a breakpoint has transitioned to
    disabled.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_bootstrap([])
    data = {
        'bpnum': 1,
        'filename': 'file.py',
        'line': 10,
    }
    db.on_breakpoint_create(**data)
    db.view.reset_mock()
    db.on_breakpoint_disable(1)
    bp = db.bp_index['file.py'][10]
    assert bp.enabled is False
    db.view.debug_on_breakpoint_disable.assert_called_once_with(bp)


def test_Debugger_on_breakpoint_ignore():
    """
    Handle when the runner signals that it will ignore a breakpoint "count"
    iterations.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_bootstrap([])
    data = {
        'bpnum': 1,
        'filename': 'file.py',
        'line': 10,
    }
    db.on_breakpoint_create(**data)
    db.view.reset_mock()
    db.on_breakpoint_ignore(1, 5)
    bp = db.bp_index['file.py'][10]
    assert bp.ignore is 5
    db.view.debug_on_breakpoint_ignore.assert_called_once_with(bp, 5)


def test_Debugger_on_breakpoint_clear():
    """
    Ensure handling of clearing a breakpoint is passed to the view.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_bootstrap([])
    data = {
        'bpnum': 1,
        'filename': 'file.py',
        'line': 10,
    }
    db.on_breakpoint_create(**data)
    db.view.reset_mock()
    db.on_breakpoint_clear(1)
    bp = db.bp_index['file.py'][10]
    db.view.debug_on_breakpoint_clear.assert_called_once_with(bp)


def test_Debugger_on_stack():
    """
    Handle the runner sending revised data about the current state of the debug
    stack.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    stack = mock.MagicMock()
    db.on_stack(stack)
    assert db.stack == stack
    db.view.debug_on_stack.assert_called_once_with(stack)


def test_Debugger_on_restart():
    """
    On restart is passed to the view.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_restart()
    db.view.debug_on_restart.assert_called_once_with()


def test_Debugger_on_call():
    """
    On call is passed to the view with the calling args.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_call(args={'foo': 'bar'})
    db.view.debug_on_call.assert_called_once_with({'foo': 'bar'})


def test_Debugger_on_return():
    """
    On return is passed to the view with the return value from the function.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_return(True)
    db.view.debug_on_return.assert_called_once_with(True)


def test_Debugger_on_line():
    """
    Ensure details of the runner moving to the referenced file and line are
    passed to the view.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_line('file.py', 10)
    db.view.debug_on_line.assert_called_once_with('file.py', 10)


def test_Debugger_on_exception():
    """
    Ensure the client passes exception details to the view.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_exception('ValueError', 'foo')
    db.view.debug_on_exception.assert_called_once_with('ValueError', 'foo')


def test_Debugger_on_postmortem():
    """
    Ensure the client passes on the unexpected death of the runner to the view.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    db.on_postmortem()
    db.view.debug_on_postmortem.assert_called_once_with((), {})


def test_Debugger_on_info():
    """
    Handle the runner sending an informative log message to the client.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    with mock.patch('mu.debugger.client.logger.info') as mock_logger:
        db.on_info('info')
        mock_logger.assert_called_once_with('Debug runner says: info')
        db.view.debug_on_info.assert_called_once_with('info')


def test_Debugger_on_warning():
    """
    Handle the runner sending a warning log message to the client.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    with mock.patch('mu.debugger.client.logger.warning') as mock_logger:
        db.on_warning('info')
        mock_logger.assert_called_once_with('Debug runner says: info')
        db.view.debug_on_warning.assert_called_once_with('info')


def test_Debugger_on_error():
    """
    Handle the runner sending an error log message to the client.
    """
    db = mu.debugger.client.Debugger('localhost', 1908)
    db.view = mock.MagicMock()
    with mock.patch('mu.debugger.client.logger.error') as mock_logger:
        db.on_error('info')
        mock_logger.assert_called_once_with('Debug runner says: info')
        db.view.debug_on_error.assert_called_once_with('info')
