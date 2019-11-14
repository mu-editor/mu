"""
A debug client for the Mu editor.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import socket
import time
import logging
import os.path
from PyQt5.QtCore import QObject, QThread, pyqtSignal


logger = logging.getLogger(__name__)


class UnknownBreakpoint(Exception):
    """
    The client encountered an unknown breakpoint.
    """

    pass


class ConnectionNotBootstrapped(Exception):
    """
    The connection to the runner hasn't been completed.
    """

    pass


class Breakpoint:
    """
    Represents a breakpoint, identified by a breakpoint number (bpnum). Users
    set breakpoints to stop the debugger at a certain line (potentially in a
    named function) in a file.
    """

    def __init__(
        self,
        bpnum,
        filename,
        line,
        enabled=True,
        temporary=False,
        funcname=None,
    ):
        self.bpnum = bpnum
        self.filename = filename
        self.line = line
        self.enabled = enabled
        self.temporary = temporary
        self.funcname = funcname

    def __str__(self):
        return "{}:{}".format(self.filename, self.line)


class CommandBufferHandler(QObject):
    """
    Represents the work to be done on a separate thread for connecting and
    processing incoming messages.

    Emits signals to indicate when messages are receievd or the connection
    fails at appropriate moments during the lifetime of a debug session.
    """

    on_command = pyqtSignal(str)  #: Signal emitted when a command is received.
    on_fail = pyqtSignal(str)  #: Emitted when there was a connection failure.

    def __init__(self, debugger):
        """
        Receive the debugger object containing the configuration attributes and
        socket for inter-process communication with the debug runner.
        """
        super().__init__()
        self.debugger = debugger
        self.stopped = False

    def worker(self):
        """
        Buffer input from a socket, emit complete debugger commands as signals.
        """
        connected = False
        tries = 0
        connection_attempts = 50  # Translates to 10 seconds.
        pause_between_attempts = 0.2
        while not connected:
            try:
                self.debugger.socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                )
                self.debugger.socket.connect(
                    (self.debugger.host, self.debugger.port)
                )
                connected = True
            except ConnectionRefusedError:
                # Allow up to connection_attempts attempts to connect.
                # The Raspberry Pi is quite slow, so Mu needs to give the
                # debug runner enough time to start up and start listening.
                tries += 1
                if tries >= connection_attempts:
                    self.on_fail.emit(
                        _(
                            "Connection timed out. Is your "
                            "machine slow or busy? Free up some "
                            "of the machine's resources and try "
                            "again."
                        )
                    )
                    return
                time.sleep(pause_between_attempts)
            except OSError:
                # This will catch address related errors. Especially on OSX
                # this is usually solved by adding "127.0.0.1 localhost" to
                # /etc/hosts.
                self.on_fail.emit(
                    _(
                        "Could not find localhost.\n"
                        "Ensure you have '127.0.0.1 localhost' in "
                        "your /etc/hosts file."
                    )
                )
                return
        # Getting here means the connection has been established, so handle all
        # incoming data from the debug runner process.
        remainder = b""
        while not self.stopped:
            new_buffer = None
            try:
                new_buffer = self.debugger.socket.recv(1024)
            except Exception:
                # Stop if there's any failure in receiving data from the
                # runner.
                self.stopped = True
            if new_buffer:
                if new_buffer.endswith(self.debugger.ETX):
                    terminator = self.debugger.ETX
                    pos = new_buffer.rfind(self.debugger.ETX)
                    full_buffer = remainder + new_buffer[:pos]
                else:
                    terminator = None
                    full_buffer = remainder + new_buffer

                commands = full_buffer.split(self.debugger.ETX)
                if terminator is None:
                    remainder = commands.pop()
                else:
                    remainder = b""
                for command in commands:
                    command = command.decode("utf-8")
                    logger.debug(command)
                    self.on_command.emit(command)
            else:
                # If recv() returns None, the socket is closed.
                logger.debug("Debug client closed.")
                break


class Debugger(QObject):
    """
    Represents the networked debugger client.
    """

    ETX = b"\x03"  # End transmission token.

    def __init__(self, host, port, proc=None):
        """
        Instantiate given a host, port and process for the debug runner.
        """
        self.host = host
        self.port = port
        self.proc = proc
        self.view = None  # Set after instantiation.
        super().__init__()

    def start(self):
        """
        Start the debugger session.
        """
        self.listener_thread = QThread(self.view.view)
        self.command_handler = CommandBufferHandler(self)
        self.command_handler.moveToThread(self.listener_thread)
        self.command_handler.on_command.connect(self.on_command)
        self.command_handler.on_fail.connect(self.on_fail)
        self.listener_thread.started.connect(self.command_handler.worker)
        self.listener_thread.start()

    def on_command(self, command):
        """
        Handle a command emitted by the client thread.
        """
        event, data = json.loads(command)
        if hasattr(self, "on_{}".format(event)):
            getattr(self, "on_{}".format(event))(**data)

    def on_fail(self, message):
        """
        Handle if there's a connection failure with the debug runner.
        """
        logger.error(message)
        self.view.debug_on_fail(message)

    def stop(self):
        """
        Shut down the debugger session.
        """
        self.command_handler.stopped = True
        self.listener_thread.quit()
        self.listener_thread.wait()
        if self.proc is not None:
            self.output("quit")
        self.socket.shutdown(socket.SHUT_WR)
        if self.proc is not None:
            # Wait for the runner process to die.
            self.proc.wait()

    def output(self, event, **data):
        """
        Send a command to the debug runner.
        """
        try:
            dumped = json.dumps((event, data)).encode("utf-8")
            self.socket.sendall(dumped + Debugger.ETX)
        except OSError as e:
            logger.debug("Debugger client error.")
            logger.debug(e)
        except AttributeError as e:
            logger.debug("Debugger client not connected to runner.")
            logger.debug(e)

    def breakpoint(self, breakpoint):
        """
        Given a breakpoint number or (filename, line), return an object
        representing the referenced breakpoint.
        """
        try:
            if isinstance(breakpoint, tuple):
                filename, line = breakpoint
                filename = os.path.normcase(os.path.abspath(filename))
                return self.bp_index[filename][line]
            else:
                return self.bp_list[breakpoint]
        except KeyError:
            raise UnknownBreakpoint()

    def breakpoints(self, filename):
        """
        Return all the breakpoints associated with the referenced file.
        """
        normalised = os.path.normcase(os.path.abspath(filename))
        return self.bp_index.get(normalised, {})

    # Commands that can be passed to the debug runner.

    def create_breakpoint(self, filename, line, temporary=False):
        """
        Create a new, enabled breakpoint at the specified line of the given
        file.
        """
        self.output("break", filename=filename, line=line, temporary=temporary)

    def enable_breakpoint(self, breakpoint):
        """
        Enable an existing breakpoint.
        """
        self.output("enable", bpnum=breakpoint.bpnum)

    def disable_breakpoint(self, breakpoint):
        """
        Disable an existing breakpoint.
        """
        self.output("disable", bpnum=breakpoint.bpnum)

    def ignore_breakpoint(self, breakpoint, count):
        """
        Ignore an existing breakpoint for "count" iterations.

        (N.B. Use a count of 0 to restore the breakpoint.
        """
        self.output("ignore", bpnum=breakpoint.bpnum, count=count)

    def clear_breakpoint(self, breakpoint):
        """
        Clear an existing breakpoint.
        """
        self.output("clear", bpnum=breakpoint.bpnum)

    def do_run(self):
        """
        Run the debugger until the next breakpoint.
        """
        self.output("continue")

    def do_step(self):
        """
        Step through one stack frame.
        """
        self.output("step")

    def do_next(self):
        """
        Go to the next line in the current stack frame.
        """
        self.output("next")

    def do_return(self):
        """
        Return to the previous stack frame.
        """
        self.output("return")

    # Handlers for events raised by the debug runner. These generally follow
    # the pattern of updating state in the client object to reflect that of
    # the debug runner, then calling a method in the UI layer to update the
    # GUI to reflect the changed state.

    def on_bootstrap(self, breakpoints):
        """
        The runner has finished setting up.
        """
        self.bp_index = {}
        self.bp_list = list([True])  # Breakpoints count from 1
        for bp_data in breakpoints:
            self.on_breakpoint_create(**bp_data)
        self.view.debug_on_bootstrap()

    def on_breakpoint_create(self, **bp_data):
        """
        The runner has created a breakpoint.
        """
        bp = Breakpoint(**bp_data)
        filename = os.path.normcase(os.path.abspath(bp.filename))
        self.bp_index.setdefault(filename, {}).setdefault(bp.line, bp)
        self.bp_list.append(bp)
        if bp.enabled:
            self.view.debug_on_breakpoint_enable(bp)
        else:
            self.view.debug_on_breakpoint_disable(bp)

    def on_breakpoint_enable(self, bpnum):
        """
        The runner has enabled the breakpoint referenced by breakpoint number.
        """
        bp = self.bp_list[bpnum]
        bp.enabled = True
        self.view.debug_on_breakpoint_enable(bp)

    def on_breakpoint_disable(self, bpnum):
        """
        The runner has disabled a breakpoint referenced by breakpoint number.
        """
        bp = self.bp_list[bpnum]
        bp.enabled = False
        self.view.debug_on_breakpoint_disable(bp)

    def on_breakpoint_ignore(self, bpnum, count):
        """
        The runner will ignore the referenced breakpoint "count" iterations.
        """
        bp = self.bp_list[bpnum]
        bp.ignore = count
        self.view.debug_on_breakpoint_ignore(bp, count)

    def on_breakpoint_clear(self, bpnum):
        """
        The runner has cleared the referenced breakpoint.
        """
        bp = self.bp_list[bpnum]
        self.view.debug_on_breakpoint_clear(bp)

    def on_stack(self, stack):
        """
        The runner has sent an update to the stack.
        """
        self.stack = stack
        self.view.debug_on_stack(stack)

    def on_restart(self):
        """
        The runner has restarted.
        """
        self.view.debug_on_restart()

    def on_finished(self):
        """
        The debug runner has finished running the script to be debugged.
        """
        self.view.debug_on_finished()

    def on_call(self, args):
        """
        The runner has called a function with the specified arguments.
        """
        self.view.debug_on_call(args)

    def on_return(self, retval):
        """
        The runner has returned from a function with the specified return
        value.
        """
        self.view.debug_on_return(retval)

    def on_line(self, filename, line):
        """
        The runner has moved to the specified line in the referenced file.
        """
        self.view.debug_on_line(filename, line)

    def on_exception(self, name, value):
        """
        The runner has encountered a named exception with an associated value.
        """
        msg = "Exception encountered in user's code: {} - {}"
        logger.info(msg.format(name, value))
        self.view.debug_on_exception(name, value)

    def on_postmortem(self, *args, **kwargs):
        """
        The runner encountered a fatal error and has died.
        """
        self.view.debug_on_postmortem(args, kwargs)

    def on_info(self, message):
        """
        The runner has sent an informative message.
        """
        logger.info("Debug runner says: {}".format(message))
        self.view.debug_on_info(message)

    def on_warning(self, message):
        """
        The runner has sent a warning message.
        """
        logger.warning("Debug runner says: {}".format(message))
        self.view.debug_on_warning(message)

    def on_error(self, message):
        """
        The runner has sent an error message.
        """
        logger.error("Debug runner says: {}".format(message))
        self.view.debug_on_error(message)
