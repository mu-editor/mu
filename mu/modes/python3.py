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

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                'name': 'run',
                'display_name': _('Run'),
                'description': _('Run and debug your Python script.'),
                'handler': self.run,
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

    def run(self, event):
        """
        Run and debug the script using the debug mode.
        """
        logger.info("Starting debug mode.")
        self.editor.change_mode('debugger')
        self.editor.mode = 'debugger'
        self.editor.modes['debugger'].start()

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
