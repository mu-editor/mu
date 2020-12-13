"""
The mode Mu is is when it's debugging a Python 3 script.

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
import logging
import os

from .base import BaseMode
from ..debugger.config import DEBUGGER_PORT
from ..debugger.client import Debugger
from ..debugger.utils import is_breakpoint_line
from ..virtual_environment import venv

from PyQt5.QtCore import QTimer


logger = logging.getLogger(__name__)


class DebugMode(BaseMode):
    """
    Represents the functionality required by the Python 3 visual debugger.
    """

    name = _("Graphical Debugger")
    short_name = "debugger"
    description = _("Debug your Python 3 code.")
    icon = "python"
    runner = None
    is_debugger = True
    save_timeout = 0  # No need to auto-save when in read-only debug mode.

    def __init__(self, editor, view):
        super().__init__(editor, view)
        self._button_disable_timer = QTimer()
        self._button_disable_timer.setSingleShot(True)
        self._button_disable_timer.timeout.connect(self.disable_buttons)

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                "name": "stop",
                "display_name": _("Stop"),
                "description": _("Stop the running code."),
                "handler": self.button_stop,
                "shortcut": "Shift+F5",
            },
            {
                "name": "run",
                "display_name": _("Continue"),
                "description": _("Continue to run your Python script."),
                "handler": self.button_continue,
                "shortcut": "F5",
            },
            {
                "name": "step-over",
                "display_name": _("Step Over"),
                "description": _("Step over a line of code."),
                "handler": self.button_step_over,
                "shortcut": "F10",
            },
            {
                "name": "step-in",
                "display_name": _("Step In"),
                "description": _("Step into a function."),
                "handler": self.button_step_in,
                "shortcut": "F11",
            },
            {
                "name": "step-out",
                "display_name": _("Step Out"),
                "description": _("Step out of a function."),
                "handler": self.button_step_out,
                "shortcut": "Shift+F11",
            },
        ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return []

    def start(self):
        """
        Start debugging the current script.
        """
        # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            logger.debug("There is no active text editor.")
            self.stop()
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            # If needed, save the script.
            if tab.isModified():
                self.editor.save_tab_to_file(tab)
            logger.debug(tab.text())
            self.set_buttons(modes=False)
            envars = self.editor.envars
            cwd = os.path.dirname(tab.path)
            self.runner = self.view.add_python3_runner(
                venv.interpreter,
                tab.path,
                cwd,
                debugger=True,
                envars=envars,
            )
            self.runner.process.waitForStarted()
            self.runner.process.finished.connect(self.finished)
            self.view.add_debug_inspector()
            self.view.set_read_only(True)
            self.debugger = Debugger(
                "localhost", DEBUGGER_PORT, proc=self.runner.process
            )
            self.debugger.view = self
            self.debugger.start()
        else:
            logger.debug("Current script has not been saved. Aborting debug.")
            self.stop()

    def stop(self):
        """
        Stop the debug runner and reset the UI.
        """
        logger.debug("Stopping debugger.")
        if self.runner:
            self.runner.process.kill()
            self.runner.process.waitForFinished()
            self.runner = None
            self.debugger = None
            self.view.remove_python_runner()
            self.view.remove_debug_inspector()
        self.set_buttons(modes=True)
        self.editor.change_mode("python")
        self.editor.mode = "python"
        self.view.set_read_only(False)

    def finished(self):
        """
        Called when the debugged Python process is finished.
        """
        self.disable_buttons()
        self.editor.show_status_message(_("Your script has finished running."))
        for tab in self.view.widgets:
            tab.setSelection(0, 0, 0, 0)
            tab.reset_debugger_highlight()

    def _enable_buttons(self, *, enable):
        """
        Enable/disable all debug control buttons except 'stop'.
        """
        buttons = {
            action["name"]: enable
            for action in self.actions()
            if action["name"] != "stop"
        }
        self.set_buttons(**buttons)

    def disable_buttons(self):
        """
        Disable all debug control buttons except 'stop'.
        """
        self._enable_buttons(enable=False)

    def disable_buttons_later(self, *, milliseconds=100):
        """
        Set a timer to disable all debug control buttons except 'stop'.
        """
        self._button_disable_timer.start(milliseconds)

    def enable_buttons(self):
        """
        Enable all debug control buttons except 'stop': if the timer started
        in `disable_buttons_later` is active, stops it and does nothing else.
        """
        if self._button_disable_timer.isActive():
            self._button_disable_timer.stop()
            return
        self._enable_buttons(enable=True)

    def button_stop(self, event):
        """
        Button clicked to stop the current script and return to Python3 mode.
        """
        self.stop()

    def button_continue(self, event):
        """
        Button clicked to continue running the script.
        """
        self.disable_buttons_later()
        self.view.current_tab.reset_debugger_highlight()
        self.debugger.do_run()

    def button_step_over(self, event):
        """
        Button clicked to step over the current line of code.
        """
        self.disable_buttons_later()
        self.view.current_tab.reset_debugger_highlight()
        self.debugger.do_next()

    def button_step_in(self, event):
        """
        Button clicked to step into the current block of code.
        """
        self.disable_buttons_later()
        self.view.current_tab.reset_debugger_highlight()
        self.debugger.do_step()

    def button_step_out(self, event):
        """
        Button clicked to step out of the current block of code.
        """
        self.disable_buttons_later()
        self.view.current_tab.reset_debugger_highlight()
        self.debugger.do_return()

    def toggle_breakpoint(self, line, tab):
        """
        Toggle a breakpoint in the debugger.
        """
        bps = self.debugger.breakpoints(tab.path)
        breakpoint = bps.get(line + 1, None)
        if tab.markersAtLine(line):
            if breakpoint:
                self.debugger.disable_breakpoint(breakpoint)
            tab.markerDelete(line, tab.BREAKPOINT_MARKER)
        else:
            handle = tab.markerAdd(line, tab.BREAKPOINT_MARKER)
            tab.breakpoint_handles.add(handle)
            if breakpoint:
                self.debugger.enable_breakpoint(breakpoint)
            else:
                self.debugger.create_breakpoint(tab.path, line + 1)

    def debug_on_fail(self, message):
        """
        Called when, for any reason, the debug client was unable to connect to
        the debug runner. On a Raspberry Pi this is usually because it's an
        underpowereed machine and it takes time to start the debug runner
        process. (However, the debug client waits for 10 seconds for the
        runner to start.)
        """
        # Report the problem.
        process_runner = self.view.process_runner
        if process_runner:
            msg = _("Unable to connect to the Python debugger.\n\n") + message
            process_runner.append(msg.encode("utf-8"))
            # Set the state to finished.
            self.finished()
            process_runner.finished(1, -1)

    def debug_on_bootstrap(self):
        """
        Once the debugger is bootstrapped ensure all the current breakpoints
        are set. Do not set breakpoints (and remove the marker) if:

        * The marker is not visible (the line is -1)
        * The marker is not a duplicate of an existing line.
        * The line with the marker is not a valid breakpoint line.
        """
        for tab in self.view.widgets:
            break_lines = set()
            for handle in list(tab.breakpoint_handles):
                line = tab.markerLine(handle)
                code = tab.text(line)
                if (
                    line > -1
                    and line not in break_lines
                    and is_breakpoint_line(code)
                ):
                    self.debugger.create_breakpoint(tab.path, line + 1)
                    break_lines.add(line)
                else:
                    tab.breakpoint_handles.remove(handle)
                    tab.markerDelete(line, -1)
        # Start the script running.
        self.debugger.do_run()

    def debug_on_breakpoint_enable(self, breakpoint):
        """
        Handle when a breakpoint is enabled.
        """
        tab = self.view.current_tab
        if tab.path == breakpoint.filename and not tab.markersAtLine(
            breakpoint.line - 1
        ):
            tab.markerAdd(breakpoint.line - 1, tab.BREAKPOINT_MARKER)

    def debug_on_breakpoint_disable(self, breakpoint):
        """
        Handle when a breakpoint is disabled.
        """
        tab = self.view.current_tab
        tab.markerDelete(breakpoint.line - 1, tab.BREAKPOINT_MARKER)

    def debug_on_line(self, filename, line):
        """
        Handle when the debugger has moved to the referenced line in the file.
        """
        self.enable_buttons()
        ignored = ["bdb.py"]  # Files the debugger should ignore.
        if os.path.basename(filename) in ignored:
            self.debugger.do_return()
            return
        self.view.current_tab.setSelection(0, 0, 0, 0)
        tab = self.editor.get_tab(filename)
        tab.debugger_at_line(line - 1)

    def debug_on_stack(self, stack):
        """
        Handle when the debugger sends an updated stack.
        """
        if stack:
            locals_dict = {}
            for frame in stack:
                for k, v in frame[1]["locals"].items():
                    locals_dict[k] = v
            self.view.update_debug_inspector(locals_dict)

    def debug_on_postmortem(self, args, kwargs):
        """
        Handle when something catastrophic happens to the debugger.
        """
        process_runner = self.view.process_runner
        for item in args:
            process_runner.append(item.encode("utf-8"))
        for k, v in kwargs.items():
            msg = "{}: {}".format(k, v)
            process_runner.append(msg.encode("utf-8"))

    def debug_on_info(self, message):
        """
        Handle when the debugger sends an informative textual message.
        """
        self.editor.show_status_message(_("Debugger info: {}").format(message))

    def debug_on_warning(self, message):
        """
        Handle when the debugger sends a warning message.
        """
        self.editor.show_status_message(
            _("Debugger warning: {}").format(message)
        )

    def debug_on_error(self, message):
        """
        Handle when the debugger sends an error message.
        """
        self.editor.show_status_message(
            _("Debugger error: {}").format(message)
        )

    def debug_on_call(self, args):
        """
        Handle when the debugger has called a function with the referenced
        args. Make sure the debugger steps into the function.
        """
        self.debugger.do_step()

    def debug_on_return(self, return_value):
        """
        Handle when the debugger returns from a function call with the
        referenced return value. Make sure the debugger steps out of the
        function to the caller.
        """
        self.debugger.do_step()

    def debug_on_finished(self):
        """
        Called when the runner has completed running the script to be
        debugged.
        """
        self.finished()

    def debug_on_breakpoint_ignore(self, breakpoint, count):
        """
        Handle when a breakpoint is to be ignored by the debugger. Currently
        an unimplemented extra feature.
        """
        pass

    def debug_on_breakpoint_clear(self, breakpoint):
        """
        Handle the clearing of the referenced breakpoint. Currently an
        unimplemented extra feature.
        """
        pass

    def debug_on_restart(self):
        """
        Handle when the debugger restarts. Currenty an unimplemented extra
        feature.
        """
        pass

    def debug_on_exception(self, name, value):
        """
        Handle when the debugger encounters a named exception with an
        associated value. Clear the highlighted line and allow the script to
        run until the end so the error message is printed to stdout.
        """
        self.view.current_tab.reset_debugger_highlight()
        self.debugger.do_run()
