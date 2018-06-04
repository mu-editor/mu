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
import os
import sys
import os.path
import logging
from tokenize import TokenError
from mu.logic import HOME_DIRECTORY
from mu.contrib import uflash, microfs
from mu.modes.api import MICROBIT_APIS, SHARED_APIS
from mu.modes.base import MicroPythonMode
from mu.interface.panes import CHARTS
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer

# We can run without nudatus
can_minify = True
try:
    import nudatus
except ImportError:  # pragma: no cover
    can_minify = False

logger = logging.getLogger(__name__)


class DeviceFlasher(QThread):
    """
    Used to flash the micro:bit in a non-blocking manner.
    """
    # Emitted when flashing the micro:bit fails for any reason.
    on_flash_fail = pyqtSignal(str)

    def __init__(self, paths_to_microbits, python_script, path_to_runtime):
        """
        The paths_to_microbits should be a list containing filesystem paths to
        attached micro:bits to flash. The python_script should be the text of
        the script to flash onto the device. The path_to_runtime should be the
        path of the hex file for the MicroPython runtime to use. If the
        path_to_runtime is None, the default MicroPython runtime is used by
        default.
        """
        QThread.__init__(self)
        self.paths_to_microbits = paths_to_microbits
        self.python_script = python_script
        self.path_to_runtime = path_to_runtime

    def run(self):
        """
        Flash the device.
        """
        try:
            uflash.flash(paths_to_microbits=self.paths_to_microbits,
                         python_script=self.python_script,
                         path_to_runtime=self.path_to_runtime)
        except Exception as ex:
            # Catch everything so Mu can recover from all of the wide variety
            # of possible exceptions that could happen at this point.
            self.on_flash_fail.emit(str(ex))


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
            result = tuple(microfs.ls())
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
            microfs.get(microbit_filename, local_filename)
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
            microfs.put(local_filename, target=None)
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
            microfs.rm(microbit_filename)
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
    flash_thread = None
    flash_timer = None
    file_extensions = ['hex']

    valid_boards = [
        (0x0D28, 0x0204),  # micro:bit USB VID, PID
    ]

    user_defined_microbit_path = None

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
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
            }, ]
        if CHARTS:
            buttons.append({
                'name': 'plotter',
                'display_name': _('Plotter'),
                'description': _('Plot incoming REPL data.'),
                'handler': self.toggle_plotter,
                'shortcut': 'CTRL+Shift+P',
            })
        return buttons

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
        # Check minification status.
        minify = False
        if uflash.get_minifier():
            minify = self.editor.minify
        if len(python_script) >= 8192:
            message = _('Unable to flash "{}"').format(tab.label)
            if minify and can_minify:
                orginal = len(python_script)
                script = python_script.decode('utf-8')
                try:
                    mangled = nudatus.mangle(script).encode('utf-8')
                except TokenError as e:
                    msg, (line, col) = e.args
                    logger.debug('Minify failed')
                    logger.exception(e)
                    message = _("Problem with script")
                    information = _("{} [{}:{}]").format(msg, line, col)
                    self.view.show_message(message, information, 'Warning')
                    return
                saved = orginal - len(mangled)
                percent = saved / orginal * 100
                logger.debug('Script minified, {} bytes ({:.2f}%) saved:'
                             .format(saved, percent))
                logger.debug(mangled)
                python_script = mangled
                if len(python_script) >= 8192:
                    information = _("Our minifier tried but your "
                                    "script is too long!")
                    self.view.show_message(message, information, 'Warning')
                    return
            elif minify and not can_minify:
                information = _("Your script is too long and the minifier"
                                " isn't available")
                self.view.show_message(message, information, 'Warning')
                return
            else:
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
            # Check use of custom runtime.
            rt_hex_path = self.editor.microbit_runtime.strip()
            message = _('Flashing "{}" onto the micro:bit.').format(tab.label)
            if (rt_hex_path and os.path.exists(rt_hex_path)):
                message = message + _(" Runtime: {}").format(rt_hex_path)
            else:
                rt_hex_path = None
                self.editor.microbit_runtime = ''
            self.editor.show_status_message(message, 10)
            self.set_buttons(flash=False)
            self.flash_thread = DeviceFlasher([path_to_microbit],
                                              python_script, rt_hex_path)
            if sys.platform == 'win32':
                # Windows blocks on write.
                self.flash_thread.finished.connect(self.flash_finished)
            else:
                # Other platforms don't block, so schedule the finish call
                # for 10 seconds (approximately how long flashing the device
                # takes).
                self.flash_timer = QTimer()
                self.flash_timer.timeout.connect(self.flash_finished)
                self.flash_timer.setSingleShot(True)
                self.flash_timer.start(10000)
            self.flash_thread.on_flash_fail.connect(self.flash_failed)
            self.flash_thread.start()
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

    def flash_finished(self):
        """
        Called when the thread used to flash the micro:bit has finished.
        """
        self.set_buttons(flash=True)
        self.editor.show_status_message(_("Finished flashing."))
        self.flash_thread = None
        self.flash_timer = None

    def flash_failed(self, error):
        """
        Called when the thread used to flash the micro:bit encounters a
        problem.
        """
        logger.error(error)
        message = _("There was a problem flashing the micro:bit.")
        information = _("Please do not disconnect the device until flashing"
                        " has completed.")
        self.view.show_message(message, information, 'Warning')
        if self.flash_timer:
            self.flash_timer.stop()
            self.flash_timer = None
        self.set_buttons(flash=True)
        self.flash_thread = None

    def toggle_repl(self, event):
        """
        Check for the existence of the file pane before toggling REPL.
        """
        if self.fs is None:
            super().toggle_repl(event)
            if self.repl:
                self.set_buttons(files=False)
            elif not (self.repl or self.plotter):
                self.set_buttons(files=True)
        else:
            message = _("REPL and file system cannot work at the same time.")
            information = _("The REPL and file system both use the same USB "
                            "serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def toggle_plotter(self, event):
        """
        Check for the existence of the file pane before toggling plotter.
        """
        if self.fs is None:
            super().toggle_plotter(event)
            if self.plotter:
                self.set_buttons(files=False)
            elif not (self.repl or self.plotter):
                self.set_buttons(files=True)
        else:
            message = _("The plotter and file system cannot work at the same "
                        "time.")
            information = _("The plotter and file system both use the same "
                            "USB serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def toggle_files(self, event):
        """
        Check for the existence of the REPL or plotter before toggling the file
        system navigator for the micro:bit on or off.
        """
        if (self.repl or self.plotter):
            message = _("File system cannot work at the same time as the "
                        "REPL or plotter.")
            information = _("The file system and the REPL and plotter "
                            "use the same USB serial connection. Toggle the "
                            "REPL and plotter off and try again.")
            self.view.show_message(message, information)
        else:
            if self.fs is None:
                self.add_fs()
                if self.fs:
                    logger.info('Toggle filesystem on.')
                    self.set_buttons(repl=False, plotter=False)
            else:
                self.remove_fs()
                logger.info('Toggle filesystem off.')
                self.set_buttons(repl=True, plotter=True)

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """
        # Check for micro:bit
        if not microfs.find_microbit():
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
        Remove the file system navigator from the UI.
        """
        if self.fs is None:
            raise RuntimeError("File system not running")
        self.view.remove_filesystem()
        self.file_manager = None
        self.file_manager_thread = None
        self.fs = None

    def on_data_flood(self):
        """
        Ensure the Files button is active before the REPL is killed off when
        a data flood of the plotter is detected.
        """
        self.set_buttons(files=True)
        super().on_data_flood()

    def open_file(self, path):
        """
        Tries to open a MicroPython hex file with an embedded Python script.
        """
        text = None
        if path.lower().endswith('.hex'):
            # Try to open the hex and extract the Python script
            try:
                with open(path, newline='') as f:
                    text = uflash.extract_script(f.read())
            except Exception:
                return None
        return text
