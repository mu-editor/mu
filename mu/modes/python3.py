"""
The Python3 mode for the Mu editor.

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
import logging
from mu.modes.base import BaseMode
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, PI_APIS
from mu.resources import load_icon
from mu.interface.panes import CHARTS
from ..virtual_environment import venv
from qtconsole.manager import QtKernelManager
from qtconsole.client import QtKernelClient
from PyQt5.QtCore import QObject, QThread, pyqtSignal


logger = logging.getLogger(__name__)


class MuKernelManager(QtKernelManager):
    def start_kernel(self, **kw):
        """Starts a kernel on this host in a separate process.

        Subclassed to allow checking that the kernel uses the same Python as
        Mu itself.
        """
        kernel_cmd, kw = self.pre_start_kernel(**kw)
        cmd_interpreter = kernel_cmd[0]
        if cmd_interpreter != venv.interpreter:
            self.log.debug(
                "Wrong interpreter selected to run REPL: %s", kernel_cmd
            )
            self.log.debug(
                "Using default interpreter to run REPL instead: %s",
                cmd_interpreter,
            )
            cmd_interpreter = venv.interpreter
            kernel_cmd[0] = cmd_interpreter

        # launch the kernel subprocess
        self.log.debug("Starting kernel: %s", kernel_cmd)
        self.kernel = self._launch_kernel(kernel_cmd, **kw)
        self.post_start_kernel(**kw)


class KernelRunner(QObject):
    """
    Used to control the iPython kernel in a non-blocking manner so the UI
    remains responsive.
    """

    kernel_started = pyqtSignal(QtKernelManager, QtKernelClient)
    kernel_finished = pyqtSignal()
    # Used to build context with user defined envars when running the REPL.
    default_envars = os.environ.copy()

    def __init__(self, kernel_name, cwd, envars):
        """
        Initialise the kernel runner with a name of a kernel specification, a
        target current working directory, any user-defined envars and the
        path for the currently active virtualenv's site-packages.
        """
        logger.debug(
            "About to create KernelRunner for %s, %s, %s ",
            kernel_name,
            cwd,
            envars,
        )
        super().__init__()
        self.kernel_name = kernel_name
        self.cwd = cwd
        self.envars = dict(envars)

    def start_kernel(self):
        """
        Create the expected context, start the kernel, obtain a client and
        emit a signal when both are started.
        """
        logger.debug("About to start kernel")
        logger.info(sys.path)
        os.chdir(self.cwd)  # Ensure the kernel runs with the expected CWD.
        # Add user defined envars to os.environ so they can be picked up by
        # the child process running the kernel.
        logger.info(
            "Starting iPython kernel with user defined envars: "
            "{}".format(self.envars)
        )
        for k, v in self.envars.items():
            if k != "PYTHONPATH":
                os.environ[k] = v

        self.repl_kernel_manager = MuKernelManager()
        self.repl_kernel_manager.kernel_name = self.kernel_name
        self.repl_kernel_manager.start_kernel()
        self.repl_kernel_client = self.repl_kernel_manager.client()
        self.kernel_started.emit(
            self.repl_kernel_manager, self.repl_kernel_client
        )

    def stop_kernel(self):
        """
        Clean up the context, stop the client connections to the kernel, affect
        an immediate shutdown of the kernel and emit a "finished" signal.
        """
        os.environ.clear()
        for k, v in self.default_envars.items():
            os.environ[k] = v
        self.repl_kernel_client.stop_channels()
        self.repl_kernel_manager.shutdown_kernel(now=True)
        self.kernel_finished.emit()


class PythonMode(BaseMode):
    """
    Represents the functionality required by the Python 3 mode.
    """

    name = _("Python 3")
    short_name = "python"
    description = _("Create code using standard Python 3.")
    icon = "python"
    runner = None
    has_debugger = True
    kernel_runner = None
    stop_kernel = pyqtSignal()

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                "name": "run",
                "display_name": _("Run"),
                "description": _("Run your Python script."),
                "handler": self.run_toggle,
                "shortcut": "F5",
            },
            {
                "name": "debug",
                "display_name": _("Debug"),
                "description": _("Debug your Python script."),
                "handler": self.debug,
                "shortcut": "F6",
            },
            {
                "name": "repl",
                "display_name": _("REPL"),
                "description": _("Use the REPL for live coding."),
                "handler": self.toggle_repl,
                "shortcut": "Ctrl+Shift+I",
            },
        ]
        if CHARTS:
            buttons.append(
                {
                    "name": "plotter",
                    "display_name": _("Plotter"),
                    "description": _(
                        "Plot data from your script or the REPL."
                    ),
                    "handler": self.toggle_plotter,
                    "shortcut": "CTRL+Shift+P",
                }
            )
        return buttons

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + PYTHON3_APIS + PI_APIS

    def run_toggle(self, event):
        """
        Handles the toggling of the run button to start/stop a script.
        """
        run_slot = self.view.button_bar.slots["run"]
        if self.runner:
            self.stop_script()
            run_slot.setIcon(load_icon("run"))
            run_slot.setText(_("Run"))
            run_slot.setToolTip(_("Run your Python script."))
            self.set_buttons(debug=True, modes=True)
        else:
            self.run_script()
            if self.runner:
                # If the script started, toggle the button state. See #338.
                run_slot.setIcon(load_icon("stop"))
                run_slot.setText(_("Stop"))
                run_slot.setToolTip(_("Stop your Python script."))
                self.set_buttons(debug=False, modes=False)

    def run_script(self):
        """
        Run the current script.
        """
        # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            logger.debug("There is no active text editor.")
            self.stop_script()
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            # If needed, save the script.
            if tab.isModified():
                self.editor.save_tab_to_file(tab)
            envars = self.editor.envars
            cwd = os.path.dirname(tab.path)
            logger.info(
                "About to run script: %s",
                dict(
                    interpreter=venv.interpreter,
                    script_name=tab.path,
                    working_directory=cwd,
                    interactive=True,
                    envars=envars,
                ),
            )
            self.runner = self.view.add_python3_runner(
                interpreter=venv.interpreter,
                script_name=tab.path,
                working_directory=cwd,
                interactive=True,
                envars=envars,
            )
            self.runner.process.waitForStarted()
            if self.kernel_runner:
                self.set_buttons(plotter=False)
            elif self.plotter:
                self.set_buttons(repl=False)

    def stop_script(self):
        """
        Stop the currently running script.
        """
        logger.debug("Stopping script.")
        if self.runner:
            self.runner.process.kill()
            self.runner.process.waitForFinished()
            self.runner = None
        self.view.remove_python_runner()
        self.set_buttons(plotter=True, repl=True)
        self.return_focus_to_current_tab()

    def debug(self, event):
        """
        Debug the script using the debug mode.
        """
        logger.info("Starting debug mode.")
        self.editor.change_mode("debugger")
        self.editor.mode = "debugger"
        self.editor.modes["debugger"].start()

    def toggle_repl(self, event):
        """
        Toggles the REPL on and off
        """
        if self.kernel_runner is None:
            logger.info("Toggle REPL on.")
            self.editor.show_status_message(_("Starting iPython REPL."))
            self.add_repl()
        else:
            logger.info("Toggle REPL off.")
            self.editor.show_status_message(
                _(
                    "Stopping iPython REPL "
                    "(this may take a short amount "
                    "of time)."
                )
            )
            self.remove_repl()

    def add_repl(self):
        """
        Create a new Jupyter REPL session in a non-blocking way.
        """
        self.set_buttons(repl=False)
        self.kernel_thread = QThread()
        self.kernel_runner = KernelRunner(
            kernel_name=venv.name,
            cwd=self.workspace_dir(),
            envars=self.editor.envars,
        )
        self.kernel_runner.moveToThread(self.kernel_thread)
        self.kernel_runner.kernel_started.connect(self.on_kernel_start)
        self.kernel_runner.kernel_finished.connect(self.kernel_thread.quit)
        self.stop_kernel.connect(self.kernel_runner.stop_kernel)
        self.kernel_thread.started.connect(self.kernel_runner.start_kernel)
        self.kernel_thread.finished.connect(self.on_kernel_stop)
        self.kernel_thread.start()

    def remove_repl(self):
        """
        Remove the Jupyter REPL session.
        """
        self.view.remove_repl()
        self.set_buttons(repl=False)
        # Don't block the GUI
        self.stop_kernel.emit()
        self.return_focus_to_current_tab()

    def toggle_plotter(self):
        """
        Toggles the plotter on and off.
        """
        if self.plotter:
            logger.info("Toggle plotter off.")
            self.remove_plotter()
        else:
            logger.info("Toggle plotter on.")
            self.add_plotter()

    def add_plotter(self):
        """
        Add a plotter pane.
        """
        self.view.add_python3_plotter(self)
        logger.info("Started plotter")
        self.plotter = True
        self.set_buttons(debug=False)
        if self.repl:
            self.set_buttons(run=False)
        elif self.runner:
            self.set_buttons(repl=False)

    def remove_plotter(self):
        """
        Remove the plotter pane, dump data and clean things up.
        """
        self.set_buttons(run=True, repl=True, debug=True)
        super().remove_plotter()

    def on_data_flood(self):
        """
        Ensure the process (REPL or runner) causing the data flood is stopped
        *before* the base on_data_flood is called to turn off the plotter and
        tell the user what to fix.
        """
        self.set_buttons(run=True, repl=True, debug=True)
        if self.kernel_runner:
            self.remove_repl()
        elif self.runner:
            self.run_toggle(None)
        super().on_data_flood()

    def on_kernel_start(self, kernel_manager, kernel_client):
        """
        Handles UI update when the kernel runner has started the iPython
        kernel.
        """
        self.view.add_jupyter_repl(kernel_manager, kernel_client)
        self.set_buttons(repl=True)
        if self.runner:
            self.set_buttons(plotter=False)
        elif self.plotter:
            self.set_buttons(run=False, debug=False)
        self.editor.show_status_message(_("REPL started."))

    def on_kernel_stop(self):
        """
        Handles UI updates for when the kernel runner has shut down the running
        iPython kernel.
        """
        self.repl_kernel_manager = None
        self.set_buttons(repl=True, plotter=True, run=True)
        self.editor.show_status_message(_("REPL stopped."))
        self.kernel_runner = None
