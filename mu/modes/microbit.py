"""
The mode for working with the BBC micro:bit. Contains most of the origial
functionality from Mu when it was only a micro:bit related editor.

Copyright (c) 2015-2021 Nicholas H.Tollervey and others (see the AUTHORS file).

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
import time
from tokenize import TokenError

import semver
from PyQt5.QtCore import QThread, pyqtSignal

from mu.logic import sniff_newline_convention
from mu.contrib import uflash, microfs
from mu.modes.api import MICROBIT_APIS, SHARED_APIS
from mu.modes.base import MicroPythonMode, FileManager
from mu.interface.panes import CHARTS
from .. import config


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

    def __init__(
        self, path_to_microbit, python_script=None, path_to_runtime=None
    ):
        """
        The path_to_microbit should be a filesystem path to an attached
        micro:bit to flash. The python_script should be the text of
        the script to flash onto the device. The path_to_runtime should be the
        path of the hex file for the MicroPython runtime to use. If the
        path_to_runtime is None, the default MicroPython runtime is used by
        default.
        """
        QThread.__init__(self)
        self.path_to_microbit = path_to_microbit
        self.python_script = python_script
        self.path_to_runtime = path_to_runtime

    def run(self):
        """
        Flash the device.
        If we are sending a custom hex we need to manually read it and copy it
        into the micro:bit drive otherwise use uFlash.
        """
        try:
            if self.path_to_runtime:
                if self.python_script:
                    raise Exception(
                        "Cannot flash a custom runtime with a Python script"
                    )
                with open(self.path_to_runtime, "rb") as f_input:
                    rt_bytes = f_input.read()
                with open(
                    os.path.join(self.path_to_microbit, "micropython.hex"),
                    "wb",
                ) as f_output:
                    f_output.write(rt_bytes)
                    f_output.flush()
                    os.fsync(f_output.fileno())
            else:
                uflash.flash(
                    paths_to_microbits=[self.path_to_microbit],
                    python_script=self.python_script,
                )
            # After flash ends DAPLink reboots the MSD, and serial might not
            # be immediately available, so this small delay helps.
            time.sleep(0.5)
        except Exception as ex:
            # Catch everything so Mu can recover from all of the wide variety
            # of possible exceptions that could happen at this point.
            logger.error(ex)
            self.on_flash_fail.emit(str(ex))


class MicrobitMode(MicroPythonMode):
    """
    Represents the functionality required by the micro:bit mode.
    """

    name = _("BBC micro:bit")
    short_name = "microbit"
    description = _("Write MicroPython for the BBC micro:bit.")
    icon = "microbit"
    fs = None  #: Reference to filesystem navigator.
    flash_thread = None
    file_extensions = ["hex"]

    # Device name should only be supplied for modes
    # supporting more than one board, thus None is returned.
    #
    #               VID,     PID,   manufact., device name
    valid_boards = [(0x0D28, 0x0204, None, "BBC micro:bit")]

    # Board IDs of supported boards.
    valid_board_ids = [0x9900, 0x9901, 0x9904]

    python_script = ""

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                "name": "flash",
                "display_name": _("Flash"),
                "description": _("Flash your code onto the micro:bit."),
                "handler": self.flash,
                "shortcut": "F3",
            },
            {
                "name": "files",
                "display_name": _("Files"),
                "description": _("Access the file system on the micro:bit."),
                "handler": self.toggle_files,
                "shortcut": "F4",
            },
            {
                "name": "repl",
                "display_name": _("REPL"),
                "description": _(
                    "Use the REPL to live-code on the " "micro:bit."
                ),
                "handler": self.toggle_repl,
                "shortcut": "Ctrl+Shift+I",
            },
        ]
        if CHARTS:
            buttons.append(
                {
                    "name": "plotter",
                    "display_name": _("Plotter"),
                    "description": _("Plot incoming REPL data."),
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
        return SHARED_APIS + MICROBIT_APIS

    def minify_if_needed(self, python_script_bytes):
        """
        Minify the script if is too large to fit in flash via uFlash appended
        method.
        Raises exceptions if minification fails or cannot be performed.
        """
        if len(python_script_bytes) < uflash._MAX_SIZE:
            # Script will fit without issues, no need to minify
            return python_script_bytes
        if not self.editor.minify:
            raise Exception(
                _("Your script is too long and code minification is disabled")
            )
        if not can_minify:
            raise Exception(
                _("Your script is too long and the minifier isn't available")
            )

        original_length = len(python_script_bytes)
        script = python_script_bytes.decode("utf-8")
        try:
            mangled = nudatus.mangle(script).encode("utf-8")
        except TokenError as e:
            msg, (line, col) = e.args
            logger.debug("Minify failed")
            logger.exception(e)
            raise Exception(
                "{}\n".format(_("Problem minifying script"))
                + "{} [{}:{}]".format(msg, line, col)
            )
        saved = original_length - len(mangled)
        percent = saved / original_length * 100
        logger.debug(
            "Script minified, {} bytes ({:.2f}%) saved:".format(saved, percent)
        )
        logger.debug(mangled)
        if len(mangled) >= uflash._MAX_SIZE:
            logger.debug("Script still too long after minification")
            raise Exception(
                _("Our minifier tried but your script is too long!")
            )
        return mangled

    def find_microbit(self):
        """
        Finds a micro:bit path, serial port and board ID.
        """
        port = None
        board_id = None
        path_to_microbit = uflash.find_microbit()
        logger.info("Path to micro:bit: {}".format(path_to_microbit))
        if self.editor.current_device:
            port = self.editor.current_device.port
            serial_number = self.editor.current_device.serial_number
            # The board ID are the first 4 hex digits for the USB serial number
            board_id = int(serial_number[:4], 16)
            logger.info("Serial port: {}".format(port))
            logger.info("Device serial number: {}".format(serial_number))
            logger.info("Board ID: 0x{:x}".format(board_id))
        return path_to_microbit, port, board_id

    def get_device_micropython_version(self):
        """
        Retrieves the MicroPython version from a micro:bit board.
        Errors bubble up, so caller must catch them.
        """
        version_info = microfs.version()
        logger.info(version_info)
        board_info = version_info["version"].split()
        if board_info[0] == "micro:bit" and board_info[1].startswith("v"):
            # New style versions, so the correct information will be
            # in the "release" field.
            # Check the release is a correct semantic version.
            semver.parse(version_info["release"])
            board_version = version_info["release"]
            logger.info("Board MicroPython: {}".format(board_version))
        else:
            # MicroPython was found, but not with an expected version string.
            # 0.0.1 indicates an old unknown version. This is just a valid
            # arbitrary flag for semver comparison
            board_version = "0.0.1"
        return board_version

    def flash(self):
        """
        Performs multiple checks to see if it needs to flash MicroPython
        into the micro:bit and then sends via serial the Python script from the
        currently active tab.
        In some error cases it attaches the code directly into the MicroPython
        hex and flashes that (this method is much slower and deprecated).

        WARNING: This method is getting more complex due to several edge
        cases. Ergo, it's a target for refactoring.
        """
        logger.info("Preparing to flash script.")
        # The first thing to do is check the tab and script are valid.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor. Exit.
            return
        python_script = tab.text().encode("utf-8")
        logger.debug("Python script from '{}' tab:".format(tab.label))
        logger.debug(python_script)
        try:
            python_script = self.minify_if_needed(python_script)
        except Exception as e:
            logger.debug("Could not minify Python script")
            warn_message = _('Unable to flash "{}"').format(tab.label)
            self.view.show_message(warn_message, "{}".format(e), "Warning")
            return

        # Next step: find the micro:bit path, port, and board ID.
        path_to_microbit, port, board_id = self.find_microbit()
        # If micro:bit path wasn't found ask the user to locate it.
        user_defined_microbit_path = False
        if path_to_microbit is None:
            path_to_microbit = self.view.get_microbit_path(
                config.HOME_DIRECTORY
            )
            user_defined_microbit_path = True
            logger.debug(
                "User defined path to micro:bit: {}".format(path_to_microbit)
            )
        if not path_to_microbit or not os.path.exists(path_to_microbit):
            # Try to be helpful... essentially there is nothing Mu can do but
            # prompt for patience while the device is mounted and/or do the
            # classic "have you tried switching it off and on again?" trick.
            # This one's for James at the Raspberry Pi Foundation. ;-)
            message = _("Could not find an attached BBC micro:bit.")
            information = _(
                "Please ensure you leave enough time for the BBC"
                " micro:bit to be attached and configured"
                " correctly by your computer. This may take"
                " several seconds."
                " Alternatively, try removing and re-attaching the"
                " device or saving your work and restarting Mu if"
                " the device remains unfound."
            )
            self.view.show_message(message, information)
            return

        # Check use of custom runtime.
        rt_hex_path = self.editor.microbit_runtime.strip()
        if rt_hex_path and os.path.isfile(rt_hex_path):
            logger.info("Using custom runtime: {}".format(rt_hex_path))
            if user_defined_microbit_path:
                self.view.show_message(
                    _("Cannot save a custom hex file to a local directory."),
                    _(
                        "When a custom hex file is configured in the settings "
                        "a local directory cannot be used to saved the final "
                        "hex file."
                    ),
                )
                return
            if not port:
                self.view.show_message(
                    _("Cannot use a custom hex file without micro:bit port."),
                    _(
                        "Mu was unable to detect the micro:bit serial port. "
                        "Normally this is okay, as Mu can inject the Python "
                        "code into the hex to flash. "
                        "However, this cannot be done with a custom hex file."
                    ),
                )
                return
            # If the user has specified a bespoke runtime hex file assume they
            # know what they're doing, always flash it, and hope for the best.
            self.flash_and_send(python_script, path_to_microbit, rt_hex_path)
            return
        else:
            self.editor.microbit_runtime = ""
        # Old hex-attach flash method when there's no port (likely Windows<8.1
        # and/or old DAPLink), or when user has selected a PC location.
        if not port or user_defined_microbit_path:
            self.flash_attached(python_script, path_to_microbit)
            return

        # Get the version of MicroPython on the device.
        logger.info("Checking target device.")
        update_micropython = False
        try:
            board_version = self.get_device_micropython_version()
            # MicroPython for micro:bit V2 version starts at 2.x.x.
            if semver.parse(board_version)["major"] < 2:
                uflash_version = uflash.MICROPYTHON_V1_VERSION
            else:
                uflash_version = uflash.MICROPYTHON_V2_VERSION
            logger.info("Mu MicroPython: {}".format(uflash_version))
            # If there's an older version of MicroPython on the device,
            # update it with the one packaged with Mu.
            if semver.compare(board_version, uflash_version) < 0:
                logger.info("Board MicroPython is older than Mu's MicroPython")
                update_micropython = True
        except Exception:
            # Could not get version of MicroPython. This means either the
            # device has a really old version or running something else.
            logger.warning("Could not detect version of MicroPython.")
            update_micropython = True

        if not python_script.strip():
            logger.info("Python script empty. Forcing flash.")
            update_micropython = True

        if update_micropython:
            if board_id in self.valid_board_ids:
                # The connected board has a serial number that indicates the
                # MicroPython hex bundled with Mu supports it, so flash it.
                self.flash_and_send(python_script, path_to_microbit)
                return
            else:
                message = _("Unsupported BBC micro:bit.")
                information = _(
                    "Your device is newer than this version of Mu. Please "
                    "update Mu to the latest version to support this device."
                    "\n\nhttps://codewith.mu/"
                )
                self.view.show_message(message, information)
                return
        else:
            self.set_buttons(
                flash=False, repl=False, files=False, plotter=False
            )
            try:
                self.copy_main(python_script)
            except IOError as ioex:
                # There was a problem with the serial communication with
                # the device, so revert to forced flash... "old style".
                # THIS IS A HACK! :-(
                logger.warning("Could not copy file to device.")
                logger.error(ioex)
                logger.info("Falling back to old-style flashing.")
                self.flash_attached(python_script, path_to_microbit)
                return
            except Exception as ex:
                self.flash_failed(ex)
            self.set_buttons(flash=True, repl=True, files=True, plotter=True)

    def flash_and_send(self, script, microbit_path, rt_path=None):
        """
        Start the MicroPython hex flashing process in a new thread with a
        custom hex file, or the one provided by uFlash.
        Then send the user script via serial.
        """
        logger.info("Flashing new MicroPython runtime onto device")
        self.set_buttons(flash=False, repl=False, files=False, plotter=False)
        status_message = _("Flashing the micro:bit")
        if rt_path:
            status_message += ". {}: {}".format(_("Runtime"), rt_path)
        self.editor.show_status_message(status_message, 10)
        # Store the script to be sent via serial after flashing the runtime
        self.python_script = script
        self.flash_thread = DeviceFlasher(
            microbit_path, python_script=None, path_to_runtime=rt_path
        )
        self.flash_thread.finished.connect(self.flash_finished)
        self.flash_thread.on_flash_fail.connect(self.flash_failed)
        self.flash_thread.start()

    def flash_attached(self, script, microbit_path):
        """
        Start the MicroPython hex flashing process in a new thread with the
        hex file provided by uFlash and the script added to the filesystem
        in the hex.
        """
        logger.info("Flashing new MicroPython runtime onto device")
        self.set_buttons(flash=False, repl=False, files=False, plotter=False)
        self.editor.show_status_message(_("Flashing the micro:bit"), 10)
        # Attach the script to the hex filesystem for flashing
        self.python_script = ""
        self.flash_thread = DeviceFlasher(microbit_path, script)
        self.flash_thread.finished.connect(self.flash_finished)
        self.flash_thread.on_flash_fail.connect(self.flash_failed)
        self.flash_thread.start()

    def flash_finished(self):
        """
        Called when the thread used to flash the micro:bit has finished.
        """
        self.editor.show_status_message(_("Finished flashing."))
        logger.info("Flashing successful.")
        self.flash_thread = None
        if self.python_script:
            try:
                self.copy_main(self.python_script)
            except Exception as ex:
                self.flash_failed(ex)
        self.set_buttons(flash=True, repl=True, files=True, plotter=True)

    def copy_main(self, script):
        """
        If script argument contains any code, copy it onto the
        connected micro:bit as main.py, then restart the board (CTRL-D).
        """
        if script.strip():
            logger.info("Copying main.py onto device")
            commands = ["fd = open('main.py', 'wb')", "f = fd.write"]
            while script:
                line = script[:64]
                commands.append("f(" + repr(line) + ")")
                script = script[64:]
            commands.append("fd.close()")
            logger.info(commands)
            serial = microfs.get_serial()
            out, err = microfs.execute(commands, serial)
            logger.info((out, err))
            if err:
                raise IOError(microfs.clean_error(err))
            # Reset the device.
            serial.write(b"import microbit\r\n")
            serial.write(b"microbit.reset()\r\n")
            self.editor.show_status_message(_("Copied code onto micro:bit."))

    def flash_failed(self, error):
        """
        Called when the thread used to flash the micro:bit encounters a
        problem.
        """
        logger.error(error)
        message = _("There was a problem flashing the micro:bit.")
        information = _(
            "Please do not disconnect the device until flashing"
            " has completed. Please check the logs for more"
            " information."
        )
        self.view.show_message(message, information, "Warning")
        self.set_buttons(flash=True, repl=True, files=True, plotter=True)
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
            information = _(
                "The REPL and file system both use the same USB "
                "serial connection. Only one can be active "
                "at any time. Toggle the file system off and "
                "try again."
            )
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
            message = _(
                "The plotter and file system cannot work at the same " "time."
            )
            information = _(
                "The plotter and file system both use the same "
                "USB serial connection. Only one can be active "
                "at any time. Toggle the file system off and "
                "try again."
            )
            self.view.show_message(message, information)

    def toggle_files(self, event):
        """
        Check for the existence of the REPL or plotter before toggling the file
        system navigator for the micro:bit on or off.
        """
        if self.repl or self.plotter:
            message = _(
                "File system cannot work at the same time as the "
                "REPL or plotter."
            )
            information = _(
                "The file system and the REPL and plotter "
                "use the same USB serial connection. Toggle the "
                "REPL and plotter off and try again."
            )
            self.view.show_message(message, information)
        else:
            if self.fs is None:
                self.add_fs()
                if self.fs:
                    logger.info("Toggle filesystem on.")
                    self.set_buttons(flash=False, repl=False, plotter=False)
            else:
                self.remove_fs()
                logger.info("Toggle filesystem off.")
                self.set_buttons(flash=True, repl=True, plotter=True)

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """
        # Check for micro:bit
        device = self.editor.current_device
        if device is None:
            message = _("Could not find an attached BBC micro:bit.")
            information = _(
                "Please make sure the device is plugged "
                "into this computer.\n\nThe device must "
                "have MicroPython flashed onto it before "
                "the file system will work.\n\n"
                "Finally, press the device's reset button "
                "and wait a few seconds before trying "
                "again."
            )
            self.view.show_message(message, information)
            return
        self.file_manager_thread = QThread(self)
        self.file_manager = FileManager(device.port)
        self.file_manager.moveToThread(self.file_manager_thread)
        self.file_manager_thread.started.connect(self.file_manager.on_start)
        self.fs = self.view.add_filesystem(
            self.workspace_dir(), self.file_manager, _("micro:bit")
        )
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

        Returns the embedded Python script and newline convention.
        """
        text = None
        if path.lower().endswith(".hex"):
            # Try to open the hex and extract the Python script
            try:
                with open(path, newline="") as f:
                    text = uflash.extract_script(f.read())
            except Exception:
                return None, None
            return text, sniff_newline_convention(text)
        else:
            return None, None

    def deactivate(self):
        """
        Invoked whenever the mode is deactivated.
        """
        super().deactivate()
        if self.fs:
            self.remove_fs()

    def device_changed(self, new_device):
        """
        Invoked when the user changes device.
        """
        super().device_changed(new_device)
        if self.fs:
            self.remove_fs()
            self.add_fs()
