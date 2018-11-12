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
import semver
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
            logger.error(ex)
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

    valid_serial_numbers = [9900, 9901]  # Serial numbers of supported boards.

    python_script = ''

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

        WARNING: This method is getting more complex due to several edge
        cases. Ergo, it's a target for refactoring.
        """
        user_defined_microbit_path = None
        self.python_script = ''
        logger.info('Preparing to flash script.')
        # The first thing to do is check the script is valid and of the
        # expected length.
        # Grab the Python script.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor. Exit.
            return
        # Check the script's contents.
        python_script = tab.text().encode('utf-8')
        logger.debug('Python script:')
        logger.debug(python_script)
        # Check minification status.
        minify = False
        if uflash.get_minifier():
            minify = self.editor.minify
        # Attempt and handle minification.
        if len(python_script) >= uflash._MAX_SIZE:
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
        # By this point, there's a valid Python script in "python_script".
        # Assign this to an attribute for later processing in a different
        # method.
        self.python_script = python_script
        # Next step: find the microbit port and serial number.
        path_to_microbit = uflash.find_microbit()
        logger.info('Path to micro:bit: {}'.format(path_to_microbit))
        port = None
        serial_number = None
        try:
            port, serial_number = self.find_device()
            logger.info('Serial port: {}'.format(port))
            logger.info('Device serial number: {}'.format(serial_number))
        except Exception as ex:
            logger.warning('Unable to make serial connection to micro:bit.')
            logger.warning(ex)
        # Determine the location of the BBC micro:bit. If it can't be found
        # fall back to asking the user to locate it.
        if path_to_microbit is None:
            # Ask the user to locate the device.
            path_to_microbit = self.view.get_microbit_path(HOME_DIRECTORY)
            user_defined_microbit_path = path_to_microbit
            logger.debug('User defined path to micro:bit: {}'.format(
                         user_defined_microbit_path))
        # Check the path and that it exists simply because the path maybe based
        # on stale data.
        if path_to_microbit and os.path.exists(path_to_microbit):
            force_flash = False  # If set to true, fully flash the device.
            # If there's no port but there's a path_to_microbit, then we're
            # probably running on Windows with an old device, so force flash.
            if not port:
                force_flash = True
            if not self.python_script.strip():
                # If the script is empty, this is a signal to simply force a
                # flash.
                logger.info("Python script empty. Forcing flash.")
                force_flash = True
            logger.info("Checking target device.")
            # Get the version of MicroPython on the device.
            try:
                version_info = microfs.version()
                logger.info(version_info)
                board_info = version_info['version'].split()
                if (board_info[0] == 'micro:bit' and
                        board_info[1].startswith('v')):
                    # New style versions, so the correct information will be
                    # in the "release" field.
                    try:
                        # Check the release is a correct semantic version.
                        semver.parse(version_info['release'])
                        board_version = version_info['release']
                    except ValueError:
                        # If it's an invalid semver, set to unknown version to
                        # force flash.
                        board_version = '0.0.1'
                else:
                    # 0.0.1 indicates an old unknown version. This is just a
                    # valid arbitrary flag for semver comparison a couple of
                    # lines below.
                    board_version = '0.0.1'
                logger.info('Board MicroPython: {}'.format(board_version))
                logger.info(
                    'Mu MicroPython: {}'.format(uflash.MICROPYTHON_VERSION))
                # If there's an older version of MicroPython on the device,
                # update it with the one packaged with Mu.
                if semver.compare(board_version,
                                  uflash.MICROPYTHON_VERSION) < 0:
                    force_flash = True
            except Exception:
                # Could not get version of MicroPython. This means either the
                # device has a really old version of MicroPython or is running
                # something else. In any case, flash MicroPython onto the
                # device.
                logger.warning('Could not detect version of MicroPython.')
                force_flash = True
            # Check use of custom runtime.
            rt_hex_path = self.editor.microbit_runtime.strip()
            message = _('Flashing "{}" onto the micro:bit.').format(tab.label)
            if (rt_hex_path and os.path.exists(rt_hex_path)):
                message = message + _(" Runtime: {}").format(rt_hex_path)
                force_flash = True  # Using a custom runtime, so flash it.
            else:
                rt_hex_path = None
                self.editor.microbit_runtime = ''
            # Check for use of user defined path (to save hex onto local
            # file system.
            if user_defined_microbit_path:
                force_flash = True
            # If we need to flash the device with a clean hex, do so now.
            if force_flash:
                logger.info('Flashing new MicroPython runtime onto device')
                self.editor.show_status_message(message, 10)
                self.set_buttons(flash=False)
                if user_defined_microbit_path or not port:
                    # The user has provided a path to a location on the
                    # filesystem. In this case save the combined hex/script
                    # in the specified path_to_microbit.
                    # Or... Mu has a path to a micro:bit but can't establish
                    # a serial connection, so use the combined hex/script
                    # to flash the device.
                    self.flash_thread = DeviceFlasher([path_to_microbit],
                                                      self.python_script,
                                                      rt_hex_path)
                    # Reset python_script so Mu doesn't try to copy it as the
                    # main.py file.
                    self.python_script = ''
                else:
                    # We appear to need to flash a connected micro:bit device,
                    # so just flash the Python hex with no embedded Python
                    # script, since this will be copied over when the
                    # flashing operation has finished.
                    model_serial_number = int(serial_number[:4])
                    if rt_hex_path:
                        # If the user has specified a bespoke runtime hex file
                        # assume they know what they're doing and hope for the
                        # best.
                        self.flash_thread = DeviceFlasher([path_to_microbit],
                                                          b'', rt_hex_path)
                    elif model_serial_number in self.valid_serial_numbers:
                        # The connected board has a serial number that
                        # indicates the MicroPython hex bundled with Mu
                        # supports it. In which case, flash it.
                        self.flash_thread = DeviceFlasher([path_to_microbit],
                                                          b'', None)
                    else:
                        message = _('Unsupported BBC micro:bit.')
                        information = _("Your device is newer than this "
                                        "version of Mu. Please update Mu "
                                        "to the latest version to support "
                                        "this device.\n\n"
                                        "https://codewith.mu/")
                        self.view.show_message(message, information)
                        return
                if sys.platform == 'win32':
                    # Windows blocks on write.
                    self.flash_thread.finished.connect(self.flash_finished)
                else:
                    if user_defined_microbit_path:
                        # Call the flash_finished immediately the thread
                        # finishes if Mu is writing the hex file to a user
                        # defined location on the local filesystem.
                        self.flash_thread.finished.connect(self.flash_finished)
                    else:
                        # Other platforms don't block, so schedule the finish
                        # call for 10 seconds (approximately how long flashing
                        # the connected device takes).
                        self.flash_timer = QTimer()
                        self.flash_timer.timeout.connect(self.flash_finished)
                        self.flash_timer.setSingleShot(True)
                        self.flash_timer.start(10000)
                self.flash_thread.on_flash_fail.connect(self.flash_failed)
                self.flash_thread.start()
            else:
                try:
                    self.copy_main()
                except IOError as ioex:
                    # There was a problem with the serial communication with
                    # the device, so revert to forced flash... "old style".
                    # THIS IS A HACK! :-(
                    logger.warning('Could not copy file to device.')
                    logger.error(ioex)
                    logger.info('Falling back to old-style flashing.')
                    self.flash_thread = DeviceFlasher([path_to_microbit],
                                                      self.python_script,
                                                      rt_hex_path)
                    self.python_script = ''
                    if sys.platform == 'win32':
                        # Windows blocks on write.
                        self.flash_thread.finished.connect(self.flash_finished)
                    else:
                        self.flash_timer = QTimer()
                        self.flash_timer.timeout.connect(self.flash_finished)
                        self.flash_timer.setSingleShot(True)
                        self.flash_timer.start(10000)
                    self.flash_thread.on_flash_fail.connect(self.flash_failed)
                    self.flash_thread.start()
                except Exception as ex:
                    self.flash_failed(ex)
        else:
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
        if self.python_script:
            try:
                self.copy_main()
            except Exception as ex:
                self.flash_failed(ex)

    def copy_main(self):
        """
        If the attribute self.python_script contains any code, copy it onto the
        connected micro:bit as main.py, then restart the board (CTRL-D).
        """
        if self.python_script.strip():
            script = self.python_script
            logger.info('Copying main.py onto device')
            commands = [
                "fd = open('main.py', 'wb')",
                "f = fd.write",
            ]
            while script:
                line = script[:64]
                commands.append('f(' + repr(line) + ')')
                script = script[64:]
            commands.append('fd.close()')
            logger.info(commands)
            serial = microfs.get_serial()
            out, err = microfs.execute(commands, serial)
            logger.info((out, err))
            if err:
                raise IOError(microfs.clean_error(err))
            # Reset the device.
            serial.write(b'import microbit\r\n')
            serial.write(b'microbit.reset()\r\n')
            self.editor.show_status_message(_('Copied code onto micro:bit.'))
        self.python_script = ''

    def flash_failed(self, error):
        """
        Called when the thread used to flash the micro:bit encounters a
        problem.
        """
        logger.error(error)
        message = _("There was a problem flashing the micro:bit.")
        information = _("Please do not disconnect the device until flashing"
                        " has completed. Please check the logs for more"
                        " information.")
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
                self.set_buttons(flash=False, files=False)
            elif not (self.repl or self.plotter):
                self.set_buttons(flash=True, files=True)
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
                self.set_buttons(flash=False, files=False)
            elif not (self.repl or self.plotter):
                self.set_buttons(flash=True, files=True)
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
                    self.set_buttons(flash=False, repl=False, plotter=False)
            else:
                self.remove_fs()
                logger.info('Toggle filesystem off.')
                self.set_buttons(flash=True, repl=True, plotter=True)

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """
        # Check for micro:bit
        port, serial_number = self.find_device()
        if not port:
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
