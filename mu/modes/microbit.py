"""
The mode for working with the BBC micro:bit. Conatains most of the origial
functionality from Mu when it was only a micro:bit related editor.

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
import os
import os.path
import logging
from mu.logic import get_settings_path, HOME_DIRECTORY
from mu.contrib import uflash, microfs
from mu.modes.api import MICROBIT_APIS, SHARED_APIS
from mu.modes.base import MicroPythonMode
from PyQt5.QtCore import QObject, QThread, pyqtSignal


logger = logging.getLogger(__name__)


class FileManager(QObject):
    """
    Used to manage micro:bit filesystem operations in a manner such that the
    UI remains responsive.

    Provides an FTP-ish API. Emits signals on success or failure of different
    operations.
    """

    # Emitted when the tuple of files on the micro:bit is known.
    on_list_files = pyqtSignal(tuple)
    # Emitted when the file with referenced filename is got from the micro:bit.
    on_get_file = pyqtSignal(str)
    # Emitted when the file with referenced filename is put onto the micro:bit.
    on_put_file = pyqtSignal(str)
    # Emitted when the file with referenced filename is deleted from the
    # micro:bit.
    on_delete_file = pyqtSignal(str)
    # Emitted when Mu is unable to list the files on the micro:bit.
    on_list_fail = pyqtSignal()
    # Emitted when the referenced file fails to be got from the micro:bit.
    on_get_fail = pyqtSignal(str)
    # Emitted when the referenced file fails to be put onto the micro:bit.
    on_put_fail = pyqtSignal(str)
    # Emitted when the referenced file fails to be deleted from the micro:bit.
    on_delete_fail = pyqtSignal(str)

    def on_start(self):
        """
        Run when the thread containing this object's instance is started so
        it can emit the list of files found on the connected micro:bit.
        """
        self.ls()

    def ls(self):
        """
        List the files on the micro:bit. Emit the resulting tuple of filenames
        or emit a failure signal.
        """
        try:
            result = tuple(microfs.ls(microfs.get_serial()))
            self.on_list_files.emit(result)
        except Exception as ex:
            logger.exception(ex)
            self.on_list_fail.emit()

    def get(self, microbit_filename, local_filename):
        """
        Get the referenced micro:bit filename and save it to the local
        filename. Emit the name of the filename when complete or emit a
        failure signal.
        """
        try:
            with microfs.get_serial() as serial:
                microfs.get(microbit_filename, local_filename, serial)
            self.on_get_file.emit(microbit_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_get_fail.emit(microbit_filename)

    def put(self, local_filename):
        """
        Put the referenced local file onto the filesystem on the micro:bit.
        Emit the name of the file on the micro:bit when complete, or emit
        a failure signal.
        """
        try:
            with microfs.get_serial() as serial:
                microfs.put(local_filename, serial)
            self.on_put_file.emit(os.path.basename(local_filename))
        except Exception as ex:
            logger.error(ex)
            self.on_put_fail.emit(local_filename)

    def delete(self, microbit_filename):
        """
        Delete the referenced file on the micro:bit's filesystem. Emit the name
        of the file when complete, or emit a failure signal.
        """
        try:
            with microfs.get_serial() as serial:
                microfs.rm(microbit_filename, serial)
            self.on_delete_file.emit(microbit_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_delete_fail.emit(microbit_filename)


class MicrobitMode(MicroPythonMode):
    """
    Represents the functionality required by the micro:bit mode.
    """
    name = _('BBC micro:bit')
    description = _("Write MicroPython for the BBC micro:bit.")
    icon = 'microbit'
    fs = None  #: Reference to filesystem navigator.

    valid_boards = [
        (0x0D28, 0x0204),  # micro:bit USB VID, PID
    ]

    user_defined_microbit_path = None

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                'name': 'flash',
                'display_name': _('Flash'),
                'description': _('Flash your code onto the micro:bit.'),
                'handler': self.flash,
                'shortcut': 'F3',
            },
            {
                'name': 'files',
                'display_name': _('Files'),
                'description': _('Access the file system on the micro:bit.'),
                'handler': self.toggle_files,
                'shortcut': 'F4',
            },
            {
                'name': 'repl',
                'display_name': _('REPL'),
                'description': _('Use the REPL to live-code on the '
                                 'micro:bit.'),
                'handler': self.toggle_repl,
                'shortcut': 'Ctrl+Shift+I',
            },
        ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + MICROBIT_APIS

    def flash(self):
        """
        Takes the currently active tab, compiles the Python script therein into
        a hex file and flashes it all onto the connected device.
        """
        logger.info('Flashing script.')
        # Grab the Python script.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor.
            return
        python_script = tab.text().encode('utf-8')
        logger.debug('Python script:')
        logger.debug(python_script)
        if len(python_script) >= 8192:
            message = _('Unable to flash "{}"').format(tab.label)
            information = _("Your script is too long!")
            self.view.show_message(message, information, 'Warning')
            return
        # Determine the location of the BBC micro:bit. If it can't be found
        # fall back to asking the user to locate it.
        path_to_microbit = uflash.find_microbit()
        if path_to_microbit is None:
            # Has the path to the device already been specified?
            if self.user_defined_microbit_path:
                path_to_microbit = self.user_defined_microbit_path
            else:
                # Ask the user to locate the device.
                path_to_microbit = self.view.get_microbit_path(HOME_DIRECTORY)
                # Store the user's specification of the path for future use.
                self.user_defined_microbit_path = path_to_microbit
                logger.debug('User defined path to micro:bit: {}'.format(
                             self.user_defined_microbit_path))
        # Check the path and that it exists simply because the path maybe based
        # on stale data.
        logger.debug('Path to micro:bit: {}'.format(path_to_microbit))
        if path_to_microbit and os.path.exists(path_to_microbit):
            logger.debug('Flashing to device.')
            # Flash the microbit
            rt_hex_path = self.get_hex_path()
            uflash.flash(paths_to_microbits=[path_to_microbit],
                         python_script=python_script,
                         path_to_runtime=rt_hex_path)
            message = _('Flashing "{}" onto the micro:bit.').format(tab.label)
            if (rt_hex_path is not None and os.path.exists(rt_hex_path)):
                message = message + _(" Runtime: {}").format(rt_hex_path)
            self.editor.show_status_message(message, 10)
        else:
            # Reset user defined path since it's incorrect.
            self.user_defined_microbit_path = None
            # Try to be helpful... essentially there is nothing Mu can do but
            # prompt for patience while the device is mounted and/or do the
            # classic "have you tried switching it off and on again?" trick.
            # This one's for James at the Raspberry Pi Foundation. ;-)
            message = _('Could not find an attached BBC micro:bit.')
            information = _("Please ensure you leave enough time for the BBC"
                            " micro:bit to be attached and configured"
                            " correctly by your computer. This may take"
                            " several seconds."
                            " Alternatively, try removing and re-attaching the"
                            " device or saving your work and restarting Mu if"
                            " the device remains unfound.")
            self.view.show_message(message, information)

    def toggle_repl(self, event):
        """
        Check for the existence of the file dialog before toggling REPL.
        """
        if self.fs is None:
            super().toggle_repl(event)
        else:
            message = _("REPL and file system cannot work at the same time.")
            information = _("The REPL and file system both use the same USB "
                            "serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def toggle_files(self, event):
        """
        Check for the existence of the REPL before toggling the file system
        navigator for the micro:bit on or off.
        """
        if self.repl is None:
            if self.fs is None:
                self.add_fs()
                logger.info('Toggle filesystem on.')
            else:
                self.remove_fs()
                logger.info('Toggle filesystem off.')
        else:
            message = _("File system and REPL cannot work at the same time.")
            information = _("The file system and REPL both use the same USB "
                            "serial connection. Only one can be active "
                            "at any time. Toggle the REPL off and try again.")
            self.view.show_message(message, information)

    def add_fs(self):
        """
        If the REPL is not active, add the file system navigator to the UI.
        """
        if self.repl is None and self.fs is None:
            # Check for micro:bit
            try:
                microfs.get_serial()
            except IOError:
                # abort
                message = _('Could not find an attached BBC micro:bit.')
                information = _("Please make sure the device is plugged "
                                "into this computer.\n\nThe device must "
                                "have MicroPython flashed onto it before "
                                "the file system will work.\n\n"
                                "Finally, press the device's reset button "
                                "and wait a few seconds before trying "
                                "again.")
                self.view.show_message(message, information)
                return
            self.file_manager_thread = QThread(self)
            self.file_manager = FileManager()
            self.file_manager.moveToThread(self.file_manager_thread)
            self.file_manager_thread.started.\
                connect(self.file_manager.on_start)
            self.fs = self.view.add_filesystem(self.workspace_dir(),
                                               self.file_manager)
            self.fs.set_message.connect(self.editor.show_status_message)
            self.fs.set_warning.connect(self.view.show_message)
            self.file_manager_thread.start()

    def remove_fs(self):
        """
        If the REPL is not active, remove the file system navigator from
        the UI.
        """
        if self.fs is None:
            raise RuntimeError("File system not running")
        self.view.remove_filesystem()
        self.file_manager = None
        self.file_manager_thread = None
        self.fs = None

    def get_hex_path(self):
        """
        Returns the path to the hex runtime file - if this has been
        specified under element 'microbit_runtime_hex' in settings.json.
        This can be a fully-qualified file path, or just a file name
        in which case the file should be located in the workspace directory.
        Returns None if no path is specified or if the file is not present.
        """
        runtime_hex_path = None
        sp = get_settings_path()
        settings = {}
        try:
            with open(sp) as f:
                settings = json.load(f)
        except FileNotFoundError:
            logger.error('Settings file {} does not exist.'.format(sp))
        except ValueError:
            logger.error('Settings file {} could not be parsed.'.format(sp))
        else:
            if 'microbit_runtime_hex' in settings and \
                    settings['microbit_runtime_hex'] is not None:
                if os.path.exists(settings['microbit_runtime_hex']):
                    runtime_hex_path = settings['microbit_runtime_hex']
                else:
                    expected_path = settings['microbit_runtime_hex']
                    runtime_hex_path = os.path.join(self.workspace_dir(),
                                                    expected_path)
                    if not os.path.exists(runtime_hex_path):
                        runtime_hex_path = None
        return runtime_hex_path
