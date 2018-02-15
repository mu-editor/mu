"""
The PyGameZero mode for the Mu editor.

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
import os
import logging
from mu.modes.base import BaseMode
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, PYGAMEZERO_APIS
from mu.logic import write_and_flush
from mu.resources import load_icon
from PyQt5.QtCore import QProcess


logger = logging.getLogger(__name__)


class PyGameZeroMode(BaseMode):
    """
    Represents the functionality required by the PyGameZero mode.
    """

    name = _('PyGame Zero')
    description = _('Make games with PyGame Zero.')
    icon = 'pygamezero'
    runner = None

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                'name': 'play',
                'display_name': _('Play'),
                'description': _('Play your PyGame Zero game.'),
                'handler': self.play_toggle,
                'shortcut': 'F5',
            },
        ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + PYTHON3_APIS + PYGAMEZERO_APIS

    def play_toggle(self, event):
        """
        Handles the toggling of the run button to start/stop a script.
        """
        if self.runner:
            self.stop_game()
            play_slot = self.view.button_bar.slots['play']
            play_slot.setIcon(load_icon('play'))
            play_slot.setText(_('Play'))
            play_slot.setToolTip(_('Play your PyGame Zero game.'))
        else:
            self.run_game()
            if self.runner:
                play_slot = self.view.button_bar.slots['play']
                play_slot.setIcon(load_icon('stop'))
                play_slot.setText(_('Stop'))
                play_slot.setToolTip(_('Stop your PyGame Zero game.'))

    def run_game(self):
        """
        Run the current game.
        """
        # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            logger.debug('There is no active text editor.')
            self.stop_script()
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            # If needed, save the script.
            if tab.isModified():
                with open(tab.path, 'w', newline='') as f:
                    logger.info('Saving script to: {}'.format(tab.path))
                    logger.debug(tab.text())
                    write_and_flush(f, tab.text())
                    tab.setModified(False)
            logger.debug(tab.text())
            self.runner = QProcess(self.view)
            self.runner.setProcessChannelMode(QProcess.MergedChannels)
            logger.info('Working directory: {}'.format(self.workspace_dir()))
            self.runner.setWorkingDirectory(self.workspace_dir())
            script = os.path.abspath(os.path.normcase(tab.path))
            self.runner.start('pgzrun', [script, ])
            self.runner.waitForStarted()

    def stop_game(self):
        """
        Stop the currently running game.
        """
        logger.debug('Stopping script.')
        if self.runner:
            self.runner.kill()
            self.runner.waitForFinished()
            self.runner = None
