# -*- coding: utf-8 -*-
"""
Tests for the debug runner.
"""
import json
import pytest
import os.path
import mu.debugger.runner
from unittest import mock


def test_command_buffer_break_loop():
    """
    Ensure if the command_buffer receives None from the socket then break out
    of the loop end end with a close instruction to the client.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger.client.recv.return_value = None
    mu.debugger.runner.command_buffer(mock_debugger)
    mock_debugger.client.recv.assert_called_once_with(1024)
    mock_debugger.commands.put.assert_called_once_with(('close', {}))


def test_command_buffer_message():
    """
    Make sure that the command buffer of bytes received with a terminated
    message results in the expected command, associated arguments and the
    remainder is correctly populated.
    """
    raw = ["enable", {'bpnum': '1'}]
    msg = json.dumps(raw).encode('utf-8')
    msg += mu.debugger.runner.Debugger.ETX
    # Splitting the message in two ensures remainder handling is exercised.
    pos = len(msg) // 2
    msg1 = msg[:pos]
    msg2 = msg[pos:]
    mock_debugger = mock.MagicMock()
    mock_debugger.ETX = mu.debugger.runner.Debugger.ETX
    mock_debugger.client.recv.side_effect = [msg1, msg2, None]
    mu.debugger.runner.command_buffer(mock_debugger)
    assert mock_debugger.client.recv.call_count == 3
    assert mock_debugger.commands.put.call_count == 2
    assert mock_debugger.commands.put.call_args_list[0][0][0] == raw
    assert mock_debugger.commands.put.call_args_list[1][0][0] == ('close', {})


def test_Debugger_init():
    """
    Ensure the runner's Debugger class initialises as expected.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    assert db._run_state == mu.debugger.runner.DebugState.NOT_STARTED
    assert db.socket == mock_socket
    assert db.host == 'localhost'
    assert db.port == 9999
    assert db.mainpyfile == ''
    assert db.client is None
    assert db.command_thread is None
    assert db.commands is None
    assert db.quitting is None
    assert db.botframe is None
    assert db.stopframe is None


def test_Debugger_output():
    """
    Ensure the "good case" call for output works (there appears to be a working
    socket connection).
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.client = mock.MagicMock()
    db.output('test', foo='bar')
    db.client.sendall.assert_called_once_with(b'["test", {"foo": "bar"}]\x03')


def test_Debugger_output_client_error():
    """
    Ensure that any debug client error is logged.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.client = mock.MagicMock()
    db.client.sendall.side_effect = OSError('bang!')
    with mock.patch('mu.debugger.runner.logger.debug') as mock_logger:
        db.output('test', foo='bar')
        assert mock_logger.call_count == 2
        mock_logger.call_args_list[0][0] == 'Debugger client error.'
        mock_logger.call_args_list[1][0] == OSError('bang!')


def test_Debugger_output_no_client_connection():
    """
    Ensure that if output is attempted via a disconnected client, it's logged
    for further information.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.client = mock.MagicMock()
    db.client.sendall.side_effect = AttributeError('bang!')
    with mock.patch('mu.debugger.runner.logger.debug') as mock_logger:
        db.output('test', foo='bar')
        assert mock_logger.call_count == 2
        mock_logger.call_args_list[0][0] == ('Debugger client not connected '
                                             'to runner.')
        mock_logger.call_args_list[1][0] == AttributeError('bang!')


def test_Debugger_output_stack_normal():
    """
    Ensure that outputting the stack uses the correct frame in a normal
    situation (the top two frames are always BDB and the runner executing the
    program being debugged - these should be ignored).
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    frame1 = mock.MagicMock()
    frame1.f_code.co_filename = '<string>'
    frame2 = mock.MagicMock()
    frame2.f_code.co_filename = 'filename.py'
    frame2.f_locals = {'locals': 'foo'}
    frame2.f_globals = {'globals': 'bar'}
    frame2.f_builtins = {'builtins': 'baz'}
    frame2.f_restricted = 'f_restricted'
    frame2.f_lasti = 'f_lasti'
    frame2.f_exc_type = 'f_exc_type'
    frame2.f_exc_value = 'f_exc_value'
    frame2.f_exc_traceback = 'f_exc_traceback'
    db.stack = [
        (None, 1),
        (frame1, 2),
        (frame2, 3),
    ]
    db.curframe = None
    db.output_stack()
    expected_stack = [(
        3,
        {
            'filename': 'filename.py',
            'locals': {'locals': "'foo'"},
            'globals': {'globals': "'bar'"},
            'builtins': {'builtins': "'baz'"},
            'restricted': 'f_restricted',
            'lasti': "'f_lasti'",
            'exc_type': "'f_exc_type'",
            'exc_value': "'f_exc_value'",
            'exc_traceback': "'f_exc_traceback'",
            'current': False,
        }
    )]
    db.output.assert_called_once_with('stack', stack=expected_stack)


def test_Debugger_output_stack_exception():
    """
    Ensure that outputting the stack uses the currect frame in an exception
    condition (in addition to BDB and the runner, there are two further frames
    that should be ignored).
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    frame1 = mock.MagicMock()
    frame1.f_code.co_filename = ''
    frame3 = mock.MagicMock()
    frame3.f_code.co_filename = '<string>'
    frame4 = mock.MagicMock()
    frame4.f_code.co_filename = 'filename.py'
    frame4.f_locals = {'locals': 'foo'}
    frame4.f_globals = {'globals': 'bar'}
    frame4.f_builtins = {'builtins': 'baz'}
    frame4.f_restricted = 'f_restricted'
    frame4.f_lasti = 'f_lasti'
    frame4.f_exc_type = 'f_exc_type'
    frame4.f_exc_value = 'f_exc_value'
    frame4.f_exc_traceback = 'f_exc_traceback'
    db.stack = [
        (None, 1),
        (frame1, 2),
        (None, 3),
        (frame3, 4),
        (frame4, 5),
    ]
    db.curframe = None
    db.output_stack()
    expected_stack = [(
        5,
        {
            'filename': 'filename.py',
            'locals': {'locals': "'foo'"},
            'globals': {'globals': "'bar'"},
            'builtins': {'builtins': "'baz'"},
            'restricted': 'f_restricted',
            'lasti': "'f_lasti'",
            'exc_type': "'f_exc_type'",
            'exc_value': "'f_exc_value'",
            'exc_traceback': "'f_exc_traceback'",
            'current': False,
        }
    )]
    db.output.assert_called_once_with('stack', stack=expected_stack)


def test_Debugger_reset():
    """
    Check reset brings about the correct states in certain attributes.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.reset()
    assert db.line is None  # No known line number (yet)
    assert db.stack == []  # No stack (yet)
    assert db.curindex == 0  # Current stack index
    assert db.curframe is None  # No current frame (yet)


def test_Debugger_setup():
    """
    Make sure setup resets state and grabs details about the current stack.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.reset = mock.MagicMock()
    mock_curframe = mock.MagicMock()
    mock_stack = [
        None,
        (mock_curframe, 1),
    ]
    db.get_stack = mock.MagicMock(return_value=(mock_stack, 1))
    mock_frame = mock.MagicMock()
    mock_traceback = mock.MagicMock()
    db.setup(mock_frame, mock_traceback)
    db.reset.assert_called_once_with()
    db.get_stack.assert_called_once_with(mock_frame, mock_traceback)
    assert db.stack == mock_stack
    assert db.curindex == 1
    assert db.curframe == mock_curframe


def test_Debugger_interact_good_case():
    """
    Ensure a good command from the client to interact with the runner is
    handled correctly with the arguments passed as expected.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.setup = mock.MagicMock()
    db.output_stack = mock.MagicMock()
    db.reset = mock.MagicMock()
    db.commands = mock.MagicMock()
    db.commands.get.return_value = ('quit', {'foo': 'bar'})
    db.do_quit = mock.MagicMock(return_value=True)
    db.interact(None, None)
    db.commands.get.assert_called_once_with(block=True)
    db.do_quit.assert_called_once_with(foo='bar')


def test_Debugger_interact_unknown_command():
    """
    If the runner receives an unknown command it should respond with an error.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.setup = mock.MagicMock()
    db.output_stack = mock.MagicMock()
    db.reset = mock.MagicMock()
    db.commands = mock.MagicMock()
    db.commands.get.side_effect = [('foo', {'bar': 'baz'}),
                                   ('quit', {'foo': 'bar'})]
    db.do_quit = mock.MagicMock(return_value=True)
    db.output = mock.MagicMock()
    db.interact(None, None)
    db.output.assert_called_once_with('error', message='Unknown command: foo')


def test_Debugger_interact_client_close():
    """
    If there's a ClientClose exception just raise and handle reconnection to
    the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.setup = mock.MagicMock()
    db.output_stack = mock.MagicMock()
    db.reset = mock.MagicMock()
    db.commands = mock.MagicMock()
    db.commands.get.side_effect = mu.debugger.runner.ClientClose()
    db.do_quit = mock.MagicMock(return_value=True)
    db.socket = mock.MagicMock()
    mock_client = mock.MagicMock
    db.socket.accept.return_value = (mock_client, '127.0.0.1')
    mock_thread_instance = mock.MagicMock()
    mock_thread = mock.MagicMock(return_value=mock_thread_instance)
    db.output = mock.MagicMock()
    mock_queue = mock.MagicMock()
    mock_queue.get.side_effect = [('quit', {'foo': 'bar'}), ]
    mock_queue_class = mock.MagicMock(return_value=mock_queue)
    with mock.patch('mu.debugger.runner.Thread', mock_thread), \
            mock.patch('mu.debugger.runner.Queue', mock_queue_class):
        db.interact(None, None)
    db.output.assert_called_once_with('bootstrap', breakpoints=[])
    assert db.output_stack.call_count == 2


def test_Debugger_interact_restart():
    """
    If there's a Restart exception, just raise and let the process fail.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.setup = mock.MagicMock()
    db.output_stack = mock.MagicMock()
    db.reset = mock.MagicMock()
    db.commands = mock.MagicMock()
    db.commands.get.side_effect = [('next', {}), ]
    db.do_next = mock.MagicMock(side_effect=mu.debugger.runner.Restart())
    with pytest.raises(mu.debugger.runner.Restart):
        db.interact(None, None)


def test_Debugger_interact_exception_encountered():
    """
    If there's a generic exception encountered make sure the runner responds
    with an appropriate catch-all error message.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.setup = mock.MagicMock()
    db.output_stack = mock.MagicMock()
    db.reset = mock.MagicMock()
    db.commands = mock.MagicMock()
    db.commands.get.side_effect = [('next', {}),
                                   ('quit', {'foo': 'bar'}), ]
    db.do_next = mock.MagicMock(side_effect=Exception('boom!'))
    db.do_quit = mock.MagicMock()
    db.output = mock.MagicMock()
    db.interact(None, None)
    expected = 'Unhandled error with command "next": boom!'
    db.output.assert_called_once_with('error', message=expected)


def test_Debugger_user_call_starting():
    """
    If user_call is called while the runner is still starting, just return
    None.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db._run_state = mu.debugger.runner.DebugState.STARTING
    assert db.user_call(None, None) is None


def test_Debugger_user_call_started():
    """
    Assuming the runner has started, ensure the passed in frame and argument
    list are output and an interact is called.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.stop_here = mock.MagicMock(return_value=True)
    db.output = mock.MagicMock()
    db.interact = mock.MagicMock()
    mock_frame = mock.MagicMock()
    db.user_call(mock_frame, ['foo', 'bar', 'baz'])
    db.stop_here.assert_called_once_with(mock_frame)
    db.output.assert_called_once_with('call', args=['foo', 'bar', 'baz'])
    db.interact.assert_called_once_with(mock_frame, None)


def test_Debugger_user_line_starting_no_line():
    """
    Do nothing (return None) if the runner is starting and there's no valid
    line set in the frame.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db._run_state = mu.debugger.runner.DebugState.STARTING
    mock_frame = mock.MagicMock()
    mock_frame.f_code.co_filename = db.canonic('foo')
    db.mainpyfile = mock_frame.f_code.co_filename
    mock_frame.f_lineno = 0
    assert db.user_line(mock_frame) is None


def test_Debugger_user_line_starting_valid_line():
    """
    If the runner is starting and there's a valid line set in the frame change
    state to STARTED, emit details of the line to the client and do an interact
    on the frame.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.interact = mock.MagicMock()
    db._run_state = mu.debugger.runner.DebugState.STARTING
    mock_frame = mock.MagicMock()
    mock_frame.f_code.co_filename = db.canonic('foo')
    db.mainpyfile = mock_frame.f_code.co_filename
    mock_frame.f_lineno = 1
    db.user_line(mock_frame)
    assert db._run_state == mu.debugger.runner.DebugState.STARTED
    db.output.assert_called_once_with('line', filename=db.canonic('foo'),
                                      line=1)
    db.interact.assert_called_once_with(mock_frame, None)


def test_Debugger_user_return_starting():
    """
    If the runner is starting return None.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db._run_state = mu.debugger.runner.DebugState.STARTING
    assert db.user_return(None, None) is None


def test_Debugger_user_return():
    """
    If there is a return value associate it with the referenced frame, signal
    to the client the value of the return and interact with the frame.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.interact = mock.MagicMock()
    mock_frame = mock.MagicMock()
    mock_frame.f_locals = {}
    return_value = 'foo'
    db.user_return(mock_frame, return_value)
    assert mock_frame.f_locals['__return__'] == return_value
    db.output.assert_called_once_with('return', retval=repr(return_value))
    db.interact.assert_called_once_with(mock_frame, None)


def test_Debugger_user_exception_starting():
    """
    If the runner is startig return None.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db._run_state = mu.debugger.runner.DebugState.STARTING
    assert db.user_exception(None, None) is None


def test_Debugger_user_exception_string_exc_type():
    """
    Given details of the exception, with a exc_type that's a string, update the
    frame, signal to the client and interact with the frame.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.interact = mock.MagicMock()
    exc_info = ('type', 'value', 'traceback')
    mock_frame = mock.MagicMock()
    mock_frame.f_locals = {}
    db.user_exception(mock_frame, exc_info)
    assert mock_frame.f_locals['__exception__'] == ('type', 'value')
    db.output.assert_called_once_with('exception', name='type',
                                      value=repr('value'))
    db.interact.assert_called_once_with(mock_frame, 'traceback')


def test_Debugger_user_exception_other_exc_type():
    """
    Given details of the exception, with a exc_type that's a string, update the
    frame, signal to the client and interact with the frame.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.interact = mock.MagicMock()
    mock_type = mock.MagicMock()
    mock_type.__name__ = 'type'
    exc_info = (mock_type, 'value', 'traceback')
    mock_frame = mock.MagicMock()
    mock_frame.f_locals = {}
    db.user_exception(mock_frame, exc_info)
    assert mock_frame.f_locals['__exception__'] == (mock_type, 'value')
    db.output.assert_called_once_with('exception', name='type',
                                      value=repr('value'))
    db.interact.assert_called_once_with(mock_frame, 'traceback')


def test_Debugger_do_break_non_executable_line():
    """
    If the referenced file and line are not a executable line, output an error
    message to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.is_executable_line = mock.MagicMock(return_value=False)
    db.do_break('foo.py', 10)
    db.output.assert_called_once_with('error',
                                      message='foo.py:10 is not executable')


def test_Debugger_do_break_causes_error():
    """
    If any error is encountered while calling set_break, output an error
    message to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.is_executable_line = mock.MagicMock(return_value=True)
    db.set_break = mock.MagicMock(return_value='bang!')
    db.do_break('foo.py', 10)
    db.output.assert_called_once_with('error',
                                      message='bang!')


def test_Debugger_do_break():
    """
    Assuming all is well while setting the breakpoint, ensure the client is
    informed of the details of the new breakpoint.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.is_executable_line = mock.MagicMock(return_value=True)
    db.set_break = mock.MagicMock(return_value=None)
    mock_bp = mock.MagicMock()
    mock_bp.number = 123
    mock_bp.file = 'foo.py'
    mock_bp.line = 10
    mock_bp.temporary = False
    mock_bp.funcname = 'bar'
    db.get_breaks = mock.MagicMock(return_value=[mock_bp, ])
    db.do_break('foo.py', 10)
    db.output.assert_called_once_with('breakpoint_create',
                                      bpnum=mock_bp.number,
                                      filename=mock_bp.file,
                                      line=mock_bp.line,
                                      temporary=mock_bp.temporary,
                                      funcname=mock_bp.funcname)


def test_Debugger_is_executable_line_true():
    """
    If the line is executable, return True.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.curframe = mock.MagicMock()
    db.curframe.f_globals = mock.MagicMock()
    mock_linecache = mock.MagicMock()
    mock_linecache.getline.return_value = "print('Hello, world')"
    with mock.patch('mu.debugger.runner.linecache', mock_linecache):
        assert db.is_executable_line('foo.py', 10)


def test_Debugger_is_executable_line_false():
    """
    If the line is NOT executable, return False.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.curframe = mock.MagicMock()
    db.curframe.f_globals = mock.MagicMock()
    mock_linecache = mock.MagicMock()
    mock_linecache.getline.return_value = "    # This is a comment"
    with mock.patch('mu.debugger.runner.linecache', mock_linecache):
        assert not db.is_executable_line('foo.py', 10)


def test_Debugger_is_executable_line_no_valid_line():
    """
    If the referenced line does not exist, return False.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.curframe = mock.MagicMock()
    db.curframe.f_globals = mock.MagicMock()
    mock_linecache = mock.MagicMock()
    mock_linecache.getline.return_value = False
    with mock.patch('mu.debugger.runner.linecache', mock_linecache):
        assert not db.is_executable_line('foo.py', 10)


def test_Debugger_do_enable_no_such_breakpoint():
    """
    If the referenced breakpoint number does not exist send an error message
    back to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: 1, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_enable('4')
    db.output.assert_called_once_with('error',
                                      message='No breakpoint numbered 4')


def test_Debugger_do_enable():
    """
    Ensure the referenced breakpoint is enabled and a message is sent back to
    the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_enable('1')
    mock_breakpoint.enable.assert_called_once_with()
    db.output.assert_called_once_with('breakpoint_enable',
                                      bpnum=1)


def test_Debugger_do_disable_no_such_breakpoint():
    """
    If the referenced breakpoint number does not exist send an error message
    back to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: 1, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_disable('4')
    db.output.assert_called_once_with('error',
                                      message='No breakpoint numbered 4')


def test_Debugger_do_disable():
    """
    Ensure the referenced breakpoint is disabled and a message is sent back to
    the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_disable('1')
    mock_breakpoint.disable.assert_called_once_with()
    db.output.assert_called_once_with('breakpoint_disable',
                                      bpnum=1)


def test_Debugger_do_ignore_bad_count():
    """
    If the referenced count value cannot be cast to an integer, ensure just
    breakpoint_enable is actioned.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_ignore(1, "hello")
    assert mock_breakpoint.ignore == 0
    db.output.assert_called_once_with('breakpoint_enable', bpnum=1)


def test_Debugger_do_ignore_no_breakpoint():
    """
    If the referenced breakpoint number does not exist send an error message
    back to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_ignore(4, 1)
    db.output.assert_called_once_with('error',
                                      message='No breakpoint numbered 4')


def test_Debugger_do_ignore():
    """
    In a valid situation, the breakpoint_ignore message is sent to the client
    and the breakpoint has the ignore value updated.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_ignore(1, 5)
    assert mock_breakpoint.ignore == 5
    db.output.assert_called_once_with('breakpoint_ignore', bpnum=1, count=5)


def test_Debugger_do_clear_no_breakpoint():
    """
    If the referenced breakpoint number does not exist send an error message
    back to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_clear(4)
    db.output.assert_called_once_with('error',
                                      message='No breakpoint numbered 4')


def test_Debugger_do_clear_error_encountered():
    """
    If an error is encountered while trying to clear the breakpoint, report
    the error back to the client.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.clear_bpbynumber = mock.MagicMock(return_value='bang!')
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_clear('1')
    db.output.assert_called_once_with('error',
                                      message='bang!')


def test_Debugger_do_clear():
    """
    In a successful situation, the breakpoint_clear message is sent to the
    client and the clear_bpbynumber is called with the expected value.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.output = mock.MagicMock()
    db.clear_bpbynumber = mock.MagicMock(return_value='')
    mock_breakpoint = mock.MagicMock()
    mock_bdb = mock.MagicMock()
    mock_bdb.Breakpoint.bpbynumber = {1: mock_breakpoint, 2: 2, 3: 3, }
    with mock.patch('mu.debugger.runner.bdb', mock_bdb):
        db.do_clear('1')
    db.clear_bpbynumber.assert_called_once_with(1)
    db.output.assert_called_once_with('breakpoint_clear',
                                      bpnum=1)


def test_Debugger_do_step():
    """
    Calls set_step and returns True.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.set_step = mock.MagicMock()
    assert db.do_step()
    db.set_step.assert_called_once_with()


def test_Debugger_do_next():
    """
    Calls set_next and return True.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.curframe = mock.MagicMock()
    db.set_next = mock.MagicMock()
    assert db.do_next()
    db.set_next.assert_called_once_with(db.curframe)


def test_Debugger_do_restart():
    """
    Raises Restart
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    with pytest.raises(mu.debugger.runner.Restart):
        db.do_restart()


def test_Debugger_do_return():
    """
    Calls set_return and returns True
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.curframe = mock.MagicMock()
    db.set_return = mock.MagicMock()
    assert db.do_return()
    db.set_return.assert_called_once_with(db.curframe)


def test_Debugger_do_continue():
    """
    Calls set_continue and returns True
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.set_continue = mock.MagicMock()
    assert db.do_continue()
    db.set_continue.assert_called_once_with()


def test_Debugger_do_quit():
    """
    Sets _user_requested_quit to True, calles set_quit and returns True.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.set_quit = mock.MagicMock()
    assert db.do_quit()
    assert db._user_requested_quit
    db.set_quit.assert_called_once_with()


def test_Debugger_do_close():
    """
    Tidy up on client close.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.command_thread = mock.MagicMock()
    with pytest.raises(mu.debugger.runner.ClientClose):
        db.do_close()
    assert db.client is None
    assert db.commands is None
    db.command_thread.join.assert_called_once_with()


def test_Debugger_runscript():
    """
    Ensure the context for running the script to be debugged is created
    correctly.
    """
    mock_socket = mock.MagicMock()
    db = mu.debugger.runner.Debugger(mock_socket, 'localhost', 9999)
    db.run = mock.MagicMock()
    db._runscript('x.py')
    assert db._run_state == mu.debugger.runner.DebugState.STARTING
    assert db.mainpyfile == db.canonic('x.py')
    assert db._user_requested_quit
    db.run.assert_called_once_with('__debug_script__ = open("x.py", "rb");'
                                   '__debug_code__ = compile(__debug_script__'
                                   '.read(), "x.py", "exec");'
                                   'exec(__debug_code__);'
                                   '__debug_script__.close();')


def test_run_with_user_requested_quit():
    """
    Run the debugger and exit because the user requested it.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger._user_requested_quit = True
    mock_debugger_class = mock.MagicMock(return_value=mock_debugger)
    mock_sys = mock.MagicMock()
    mock_sys.argv = [None, None]
    mock_sys.path = [None]
    mock_socket = mock.MagicMock()
    with mock.patch('mu.debugger.runner.Debugger', mock_debugger_class), \
            mock.patch('mu.debugger.runner.sys', mock_sys), \
            mock.patch('mu.debugger.runner.socket', mock_socket):
        mu.debugger.runner.run('localhost', 1908, 'foo.py', 'bar', 'baz')
    mock_debugger.reset.assert_called_once_with()
    mock_debugger._runscript.assert_called_once_with('foo.py')
    mock_debugger.client.shutdown.assert_called_once_with(mock_socket.SHUT_WR)
    mock_debugger_class.call_args_list[0][0][1] == 'localhost'
    mock_debugger_class.call_args_list[0][0][2] == 1908
    assert mock_sys.argv[0] == 'foo.py'
    assert mock_sys.argv[1:] == ['bar', 'baz', ]
    assert mock_sys.path[0] == os.path.dirname('foo.py')


def test_run_with_restart_exception():
    """
    Ensure the logger is called.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger._runscript.side_effect = [mu.debugger.runner.Restart(), None]
    mock_debugger._user_requested_quit = True
    mock_debugger_class = mock.MagicMock(return_value=mock_debugger)
    mock_sys = mock.MagicMock()
    mock_sys.argv = [None, None]
    mock_sys.path = [None]
    mock_socket = mock.MagicMock()
    with mock.patch('mu.debugger.runner.Debugger', mock_debugger_class), \
            mock.patch('mu.debugger.runner.sys', mock_sys), \
            mock.patch('mu.debugger.runner.socket', mock_socket):
        mu.debugger.runner.run('localhost', 1908, 'foo.py', 'bar', 'baz')
    assert mock_debugger.output.call_count == 2
    assert mock_debugger.output.call_args_list[0][0][0] == 'restart'
    assert mock_debugger.output.call_args_list[1][0][0] == 'finished'


def test_run_with_expected_exception():
    """
    If a handled exception is triggered, set the client to none and stop.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger._runscript.side_effect = SystemExit()
    mock_debugger_class = mock.MagicMock(return_value=mock_debugger)
    mock_sys = mock.MagicMock()
    mock_sys.argv = [None, None]
    mock_sys.path = [None]
    mock_socket = mock.MagicMock()
    with mock.patch('mu.debugger.runner.Debugger', mock_debugger_class), \
            mock.patch('mu.debugger.runner.sys', mock_sys), \
            mock.patch('mu.debugger.runner.socket', mock_socket):
        mu.debugger.runner.run('localhost', 1908, 'foo.py', 'bar', 'baz')
    assert mock_debugger.client is None


def test_run_with_unexpected_exception():
    """
    If an unexpected exception is triggered, report via a postmortem message to
    the client.
    """
    mock_debugger = mock.MagicMock()
    mock_debugger._runscript.side_effect = [Exception('boom'), None]
    mock_debugger._user_requested_quit = True
    mock_debugger_class = mock.MagicMock(return_value=mock_debugger)
    mock_sys = mock.MagicMock()
    mock_sys.argv = [None, None]
    mock_sys.path = [None]
    mock_socket = mock.MagicMock()
    with mock.patch('mu.debugger.runner.Debugger', mock_debugger_class), \
            mock.patch('mu.debugger.runner.sys', mock_sys), \
            mock.patch('mu.debugger.runner.socket', mock_socket):
        mu.debugger.runner.run('localhost', 1908, 'foo.py', 'bar', 'baz')
    assert mock_debugger.output.call_count == 2
    assert mock_debugger.output.call_args_list[0][0][0] == 'postmortem'
    assert mock_debugger.output.call_args_list[1][0][0] == 'finished'
