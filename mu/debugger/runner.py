"""
A debug runner for the Mu editor.

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
import sys
import os
import socket
import json
import bdb
import linecache
import logging
import traceback
from enum import Enum
from queue import Queue
from threading import Thread
from mu.debugger.utils import is_breakpoint_line


logger = logging.getLogger(__name__)


class Restart(Exception):
    """
    Cause the debugger to restart for the target Python program.
    """

    pass


class ClientClose(Exception):
    """
    Cause the debugger to wait for a new client to connect.
    """

    pass


class DebugState(Enum):
    """
    Enumerates the three possible states of a debugging session.
    """

    NOT_STARTED = 0
    STARTING = 1
    STARTED = 2


def command_buffer(debugger):
    """
    Buffer input from a socket, yield complete debugger commands.
    """
    remainder = b""
    while True:
        new_buffer = debugger.client.recv(1024)
        if new_buffer:
            if new_buffer.endswith(debugger.ETX):
                terminator = debugger.ETX
                pos = new_buffer.rfind(debugger.ETX)
                full_buffer = remainder + new_buffer[:pos]
            else:
                terminator = None
                full_buffer = remainder + new_buffer

            commands = full_buffer.split(debugger.ETX)
            if terminator is None:
                remainder = commands.pop()
            else:
                remainder = b""
            for command in commands:
                command = command.decode("utf-8")
                command_data = json.loads(command)
                logging.debug(command_data)
                debugger.commands.put(command_data)
        else:
            # If recv() returns None, the socket is closed.
            logger.debug("Closing debugger socket.")
            break
    debugger.commands.put(("close", {}))


class Debugger(bdb.Bdb):
    """
    Instances of this class represent and drive the debugging process.
    """

    ETX = b"\x03"  # End transmission token.

    def __init__(self, socket, host, port, skip=None):
        super().__init__(skip=skip)
        self._run_state = DebugState.NOT_STARTED
        self.socket = socket
        self.host = host
        self.port = port
        self.mainpyfile = ""
        self.client = None
        self.command_thread = None
        self.commands = None
        self.quitting = None
        self.botframe = None
        self.stopframe = None
        # A flag to indicate that set_trace was called once, instead of
        # set_continue, in the absence of breakpoints at script start. The
        # flag indicates that continue means set_continue from now on.
        self.continue_flag = False

    def output(self, event, **data):
        """
        Dumps data related to a referenced event to the socket.
        """
        try:
            dumped = json.dumps((event, data)).encode("utf-8")
            logging.debug(dumped)
            self.client.sendall(dumped + Debugger.ETX)
        except OSError as e:
            logger.debug("Debugger client error.")
            logger.debug(e)
        except AttributeError as e:
            logger.debug("Debugger client not connected to runner.")
            logger.debug(e)

    def output_stack(self):
        """
        Dump the current stack.

        If this is a normal situation, the top two frames are BDB and the
        runner executing the program. If there is an exception, there are two
        further extra frames. All these frames can be ignored.
        """
        str_index = 0
        sl = len(self.stack)  # Bound check for stack length.
        if sl > 1 and self.stack[1][0].f_code.co_filename == "<string>":
            str_index = 2
        elif sl > 3 and self.stack[3][0].f_code.co_filename == "<string>":
            str_index = 4
        stack_data = []
        if str_index > 0:
            for frame, line_no in self.stack[str_index:]:
                frame_data = (
                    line_no,
                    {
                        "filename": frame.f_code.co_filename,
                        "locals": {
                            k: repr(v) for k, v in frame.f_locals.items()
                        },
                        "globals": {
                            k: repr(v) for k, v in frame.f_globals.items()
                        },
                        "builtins": {
                            k: repr(v) for k, v in frame.f_builtins.items()
                        },
                        "restricted": getattr(frame, "f_restricted", ""),
                        "lasti": repr(frame.f_lasti),
                        "exc_type": repr(getattr(frame, "f_exc_type", "")),
                        "exc_value": repr(getattr(frame, "f_exc_value", "")),
                        "exc_traceback": repr(
                            getattr(frame, "f_exc_traceback", "")
                        ),
                        "current": frame is self.curframe,
                    },
                )
                stack_data.append(frame_data)
        self.output("stack", stack=stack_data)

    def reset(self):
        """
        Reset state.
        """
        self.line = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

    def setup(self, frame, traceback):
        """
        Start state should be set correctly.
        """
        self.reset()
        self.stack, self.curindex = self.get_stack(frame, traceback)
        self.curframe = self.stack[self.curindex][0]

    def interact(self, frame, traceback):
        """
        Contains the loop processing interactions with the debugger.
        """
        self.setup(frame, traceback)
        self.output_stack()
        while True:
            try:
                command, args = self.commands.get(block=True)
                if hasattr(self, "do_{}".format(command)):
                    try:
                        resume = getattr(self, "do_{}".format(command))(**args)
                        if resume:
                            # Resume running the program after the interaction.
                            break
                    except (ClientClose, Restart):
                        raise
                    except Exception as ex:
                        msg = 'Unhandled error with command "{}": {}'.format(
                            command, ex
                        )
                        self.output("error", message=msg)
                else:
                    self.output(
                        "error", message="Unknown command: {}".format(command)
                    )
            except (OSError, AttributeError, ClientClose):
                # Connection problem; try listening for new connection.
                client, addr = self.socket.accept()
                self.client = client
                self.commands = Queue()
                self.command_thread = Thread(
                    target=command_buffer, args=(self,)
                )
                self.command_thread.daemon = True
                self.command_thread.start()
                self.output(
                    "bootstrap",
                    breakpoints=[
                        {
                            "bpnum": bp.number,
                            "filename": bp.file,
                            "line": bp.line,
                            "temporary": bp.temporary,
                            "enabled": bp.enabled,
                            "funcname": bp.funcname,
                        }
                        for bp in bdb.Breakpoint.bpbynumber[1:]
                    ],
                )
                self.output_stack()
        # End
        self.reset()

    # Overridden Bdb methods
    # See https://docs.python.org/3.6/library/bdb.html#bdb.Bdb.user_call

    def user_call(self, frame, argument_list):
        """
        This method is called from dispatch_call() when there is the
        possibility that a break might be necessary anywhere inside the called
        function.
        """
        if self._run_state == DebugState.STARTING:
            return
        if self.stop_here(frame):
            self.output("call", args=argument_list)
            self.interact(frame, None)

    def user_line(self, frame):
        """
        This method is called from dispatch_line() when either stop_here() or
        break_here() yields True.

        For when we stop or break at this line.
        """
        if self._run_state == DebugState.STARTING:
            self._run_state = DebugState.STARTED
        self.output(
            "line",
            filename=self.canonic(frame.f_code.co_filename),
            line=frame.f_lineno,
        )
        self.interact(frame, None)

    def user_return(self, frame, return_value):
        """
        This method is called from dispatch_return() when stop_here() yields
        True.

        For when a return trap is set here.
        """
        if self._run_state == DebugState.STARTING:
            return
        frame.f_locals["__return__"] = return_value
        self.output("return", retval=repr(return_value))
        self.interact(frame, None)

    def user_exception(self, frame, exc_info):
        """
        This method is called from dispatch_exception() when stop_here()
        yields True.

        For when an exception occurs, but only if we are to stop at or just
        below this level.
        """
        if self._run_state == DebugState.STARTING:
            return
        exc_type, exc_value, exc_traceback = exc_info
        frame.f_locals["__exception__"] = exc_type, exc_value
        if isinstance(exc_type, str):
            exc_type_name = exc_type
        else:
            exc_type_name = exc_type.__name__
        self.output("exception", name=exc_type_name, value=repr(exc_value))
        self.interact(frame, exc_traceback)

    # Debug command handlers.

    def do_break(self, filename, line, temporary=False):
        """
        Set a breakpoint.
        """
        globs = self.curframe.f_globals if hasattr(self, "curframe") else None
        code = linecache.getline(filename, line, globs)
        if is_breakpoint_line(code):
            err = self.set_break(filename, line, temporary, None, None)
            if err:
                self.output("error", message=err)
            else:
                bp = self.get_breaks(filename, line)[-1]
                self.output(
                    "breakpoint_create",
                    bpnum=bp.number,
                    filename=bp.file,
                    line=bp.line,
                    temporary=bp.temporary,
                    funcname=bp.funcname,
                )
        else:
            self.output(
                "error",
                message="{}:{} is not executable".format(filename, line),
            )

    def do_enable(self, bpnum):
        """
        Enables the breakpoint referenced by its breakpoint number (bpnum).
        """
        bpnum = int(bpnum)
        if not (0 <= bpnum < len(bdb.Breakpoint.bpbynumber)):
            self.output(
                "error", message="No breakpoint numbered {}".format(bpnum)
            )
        else:
            bp = bdb.Breakpoint.bpbynumber[bpnum]
            bp.enable()
            self.output("breakpoint_enable", bpnum=bpnum)

    def do_disable(self, bpnum):
        """
        Disable the breakpoint referenced by its breakpoint number (bpnum).
        """
        bpnum = int(bpnum)
        if not (0 <= bpnum < len(bdb.Breakpoint.bpbynumber)):
            self.output(
                "error", message="No breakpoint numbered {}".format(bpnum)
            )
        else:
            bp = bdb.Breakpoint.bpbynumber[bpnum]
            bp.disable()
            self.output("breakpoint_disable", bpnum=bpnum)

    def do_ignore(self, bpnum, count):
        """
        Ignore the breakpoint referenced by its breakpoint number (bpnum),
        count number of times.
        """
        try:
            count = int(count)
        except ValueError:
            count = 0
        if not (0 <= bpnum < len(bdb.Breakpoint.bpbynumber)):
            self.output(
                "error", message="No breakpoint numbered {}".format(bpnum)
            )
        else:
            bp = bdb.Breakpoint.bpbynumber[bpnum]
            bp.ignore = count
            if count > 0:
                self.output("breakpoint_ignore", bpnum=bpnum, count=count)
            else:
                self.output("breakpoint_enable", bpnum=bpnum)

    def do_clear(self, bpnum):
        """
        Handle how a breakpoint must be removed when it is a temporary one.
        """
        bpnum = int(bpnum)
        if not (0 <= bpnum < len(bdb.Breakpoint.bpbynumber)):
            self.output("error", message="No breakpoint numbered %s" % bpnum)
        else:
            err = self.clear_bpbynumber(bpnum)
            if err:
                self.output("error", message=err)
            else:
                self.output("breakpoint_clear", bpnum=bpnum)

    def do_step(self):
        """
        Stop after one line of code.
        """
        self.set_step()
        return True

    def do_next(self):
        """
        Stop on the next line in or below the given frame.
        """
        self.set_next(self.curframe)
        return True

    def do_restart(self):
        """
        Restart the program by raising an exception to be caught by the
        debugger.
        """
        raise Restart

    def do_return(self):
        """
        Stop when returning from the current frame.
        """
        self.set_return(self.curframe)
        return True

    def do_continue(self):
        """
        Stop only at breakpoints or when finished. If there are no breakpoints
        on script start, do a set_trace to stop at the first available line.
        However, use the continue_flag to ensure set_continue is always called
        thereafter.
        """
        if self.continue_flag or self.get_all_breaks():
            self.set_continue()
        else:
            self.set_step()
            self.continue_flag = True
        return True

    def do_quit(self):
        """
        Set the quitting attribute to True. This raises BdbQuit in the next
        call to one of the dispatch_*() methods.
        """
        self._user_requested_quit = True
        self.set_quit()
        return True

    def do_close(self):
        """
        Respond to a closed socket (not a user commend, but needs handling).
        """
        self.client = None
        self.command_thread.join()
        self.commands = None
        raise ClientClose

    def _runscript(self, filename):
        """
        Start a debugging session with the Python script in the referenced
        filename.
        """
        # Clean __main__
        import __main__

        __main__.__dict__.clear()
        __main__.__dict__.update(
            {
                "__name__": "__main__",
                "__file__": filename,
                "__builtins__": __builtins__,
            }
        )
        # When bdb sets tracing, a number of call and line events happen BEFORE
        # we get to the user's code. The following measures avoid stopping
        # before we get to the target script (see user_line and user_call for
        # details).
        self._run_state = DebugState.STARTING
        self.mainpyfile = self.canonic(filename)
        self._user_requested_quit = True  # End the process once completed.
        e = (
            '__debug_script__ = open(r"{filename}", "rb");'
            "__debug_code__ = compile(__debug_script__.read(),"
            ' r"{filename}", "exec");'
            "exec(__debug_code__);"
            "__debug_script__.close();".format(filename=filename)
        )
        self.run(e)


def run(hostname, port, filename, args):
    """
    Run a Python script identified by "filename" with the specified arguments
    in a debugger session that's listening at hostname/port.
    """
    logger.debug("runner.run %s:%s %s %r", hostname, port, filename, args)
    # Create the correct context for the target Python script.
    sys.argv[0] = filename
    sys.argv[1:] = args
    sys.path[0] = os.path.dirname(filename)

    # Socket to which the client debugger connects.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.bind((hostname, port))
    s.listen(1)

    debugger = Debugger(s, hostname, port)
    debugger.reset()

    print(
        "Running in debug mode. Use the Stop, Continue, and Step toolbar"
        " buttons to debug the script",
        file=sys.stderr,
    )

    while True:
        try:
            debugger._runscript(filename)
            if debugger._user_requested_quit:
                debugger.output("finished")
                break
        except Restart:
            # TODO: Log restart.
            debugger.output("restart")
        except (KeyboardInterrupt, SystemExit, OSError):
            debugger.client = None
            break
        except Exception:
            msg = traceback.format_exc()
            debugger.output("postmortem", exception=msg)
            debugger.client = None
            break
    # Close connection in a tidy manner.
    if debugger.client:
        debugger.client.shutdown(socket.SHUT_WR)
