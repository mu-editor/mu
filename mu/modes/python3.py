"""
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
from gettext import gettext as _
from mu.modes.base import BaseMode
from mu.resources import load_icon
from mu.contrib.atomicfile import open_atomic
from qtconsole.inprocess import QtInProcessKernelManager


logger = logging.getLogger(__name__)


class PythonMode(BaseMode):
    """
    Represents the functionality required by the Python 3 mode.
    """

    name = _('Python 3')
    description = _('Create code using standard Python 3.')
    icon = 'python'
    runner = None
    debugger = True

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                'name': 'run',
                'display_name': _('Run'),
                'description': _('Run your Python script.'),
                'handler': self.toggle_run,
            },
            {
                'name': 'repl',
                'display_name': _('REPL'),
                'description': _('Use the REPL for live coding.'),
                'handler': self.toggle_repl,
            },
        ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return []

    def toggle_run(self, event):
        """
        Run or stop the current script.
        """
        if self.runner is None:
            logger.info('Start RUN.')
            self.run()
        else:
            logger.info('Stop RUN.')
            self.stop()

    def run(self):
        """
        Run the current script
        """
        # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor.
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            logger.debug('Running script.')
            # If needed, save the script.
            if tab.isModified():
                with open_atomic(tab.path, 'w', newline='') as f:
                    logger.info('Saving script to: {}'.format(tab.path))
                    logger.debug(tab.text())
                    f.write(tab.text())
                    tab.setModified(False)
            logger.debug('Python script: {}'.format(tab.path))
            logger.debug('Working directory: {}'.format(self.workspace_dir()))
            logger.debug(tab.text())
            self.view.button_bar.slots['run'].setIcon(load_icon('stop'))
            self.view.button_bar.slots['run'].setText(_('Stop'))
            self.view.button_bar.slots['run'].setToolTip(
                _('Quit the running code.'))
            self.runner = self.view.add_python3_runner(tab.path,
                                                       self.workspace_dir())

    def stop(self):
        """
        Stop the currently running script.
        """
        logger.debug('Stopping script runner.')
        self.runner.process.kill()
        self.runner = None
        self.view.remove_python_runner()
        self.view.button_bar.slots['run'].setIcon(load_icon('run'))
        self.view.button_bar.slots['run'].setText(_('Run'))
        self.view.button_bar.slots['run'].setToolTip(_('Run your Python '
                                                       'script.'))

    def toggle_repl(self, event):
        """
        Toggles the REPL on and off
        """
        if self.repl is None:
            logger.info('Toggle REPL on.')
            self.add_repl()
        else:
            logger.info('Toggle REPL off.')
            self.remove_repl()

    def add_repl(self,):
        """
        Create a new Jupyter REPL session.
        """
        self.repl = QtInProcessKernelManager()
        self.repl.start_kernel(show_banner=False)
        self.view.add_jupyter_repl(self.repl)

    def remove_repl(self):
        """
        Remove the Jupyter REPL session.
        """
        self.view.remove_repl()
        self.repl = None
