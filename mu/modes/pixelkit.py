"""
The mode for working with the Kano Retail Pixel Kit. Conatains most of the
origial functionality from the BBC micro:bit related editor.

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
from argparse import Namespace
import esptool
import tempfile
import tarfile
import urllib.request
from time import sleep
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from mu.modes.base import MicroPythonMode
from mu.modes.api import SHARED_APIS
from mu.contrib import pixelfs

logger = logging.getLogger(__name__)


class DeviceFlasher(QThread):
    """
    Used to flash the Pixel Kit in a non-blocking manner.
    """
    # Emitted when flashing the Pixel Kit fails for any reason.
    on_flash_fail = pyqtSignal(str)
    # Emitted when flasher outputs data
    on_data = pyqtSignal(str)
    # Serial port to flash
    port = None
    # What kind of firmware to flash
    firmware_type = "micropython"

    def __init__(self, port, firmware_type="micropython"):
        QThread.__init__(self)
        self.port = port
        self.firmware_type = firmware_type

    def run(self):
        """
        Flash the device.
        """
        if self.firmware_type == "micropython":
            self.flash_micropython()
        elif self.firmware_type == "kanocode":
            self.flash_kanocode()
        else:
            msg = "Unknown firmware type: {0}".format(self.firmware_type)
            self.on_flash_fail.emit(msg)

    def get_addr_filename(self, values):
        if len(values) % 2 != 0:
            raise Exception('Values must come in pairs')
        addr_filename = []
        for i in range(0, len(values), 2):
            addr = int(values[i], 0)
            file = open(values[i + 1], 'rb')
            addr_filename.append([addr, file])
        return addr_filename

    def write_flash(self, addr_filename):
        self.on_data.emit(_("Writing firmware to flash memory"))
        logger.info("Writing firmware to flash memory")
        args = Namespace()
        args.flash_freq = "40m"
        args.flash_mode = "dio"
        args.flash_size = "detect"
        args.no_progress = False
        args.compress = False
        args.no_stub = False
        args.trace = False
        args.verify = False
        args.addr_filename = addr_filename
        try:
            esp32loader = esptool.ESPLoader.detect_chip(
                self.port, 115200, False
            )
            esp = esp32loader.run_stub()
            esp.change_baud(921600)
            esptool.detect_flash_size(esp, args)
            esp.flash_set_parameters(esptool.flash_size_bytes(args.flash_size))
            esptool.erase_flash(esp, args)
            esptool.write_flash(esp, args)
            esp.hard_reset()
        except Exception as ex:
            logger.error(ex)
            self.on_flash_fail.emit("Could not write to flash memory")

    def download_micropython(self):
        self.on_data.emit(_("Downloading MicroPython firmware"))
        logger.info("Downloading MicroPython firmware")
        url = "http://micropython.org/resources/firmware/" + \
              "esp32-20180511-v1.9.4.bin"
        f = tempfile.NamedTemporaryFile()
        f.close()
        try:
            urllib.request.urlretrieve(url, f.name)
            # TODO: Checksum the firmware
            msg = "Downloaded MicroPython firmware to: {0}".format(f.name)
            logger.info(msg)
            return f.name
        except Exception as ex:
            logger.error(ex)
            self.on_flash_fail.emit("Could not download MicroPython firmware")

    def flash_micropython(self):
        firmware_path = self.download_micropython()
        addr_filename = self.get_addr_filename(["0x1000", firmware_path])
        self.write_flash(addr_filename)

    def download_kanocode(self):
        self.on_data.emit(_("Downloading Kano Code firmware"))
        logger.info("Downloading Kano Code firmware")
        url = "https://releases.kano.me/rpk/offline/rpk_1.0.2.tar.gz.disabled"
        f = tempfile.NamedTemporaryFile()
        f.close()
        try:
            urllib.request.urlretrieve(url, f.name)
            logger.info("Downloaded Kano Code firmware to: {0}".format(f.name))
            return f.name
        except Exception as ex:
            logger.error(ex)
            self.on_flash_fail.emit("Could not download Kano Code firmware")

    def flash_kanocode(self):
        firmware_path = self.download_kanocode()
        tar = tarfile.open(firmware_path)
        tmpdir = tempfile.TemporaryDirectory()
        tar.extractall(path=tmpdir.name)
        values = [
            "0x1000", "{0}/RPK_Bootloader_V1_0_2.bin".format(tmpdir.name),
            "0x10000", "{0}/RPK_App_V1_0_2.bin".format(tmpdir.name),
            "0x8000", "{0}/RPK_Partitions_V1_0_2.bin".format(tmpdir.name)
        ]
        addr_filename = self.get_addr_filename(values)
        self.write_flash(addr_filename)


class FileManager(QObject):
    """
    Used to manage Pixel Kit filesystem operations in a manner such that the
    UI remains responsive.
    Provides an FTP-ish API. Emits signals on success or failure of different
    operations.
    """

    # Emitted when the tuple of files on the Pixel Kit is known.
    on_list_files = pyqtSignal(tuple)
    # Emitted when the file with referenced filename is got from the Pixel Kit.
    on_get_file = pyqtSignal(str)
    # Emitted when the file with referenced filename is put onto the Pixel Kit.
    on_put_file = pyqtSignal(str)
    # Emitted when the file with referenced filename is deleted from the
    # Pixel Kit.
    on_delete_file = pyqtSignal(str)
    # Emitted when Mu is unable to list the files on the Pixel Kit.
    on_list_fail = pyqtSignal()
    # Emitted when the referenced file fails to be got from the Pixel Kit.
    on_get_fail = pyqtSignal(str)
    # Emitted when the referenced file fails to be put onto the Pixel Kit.
    on_put_fail = pyqtSignal(str)
    # Emitted when the referenced file fails to be deleted from the Pixel Kit.
    on_delete_fail = pyqtSignal(str)

    def on_start(self):
        """
        Run when the thread containing this object's instance is started so
        it can emit the list of files found on the connected Pixel Kit.
        """
        self.ls()

    def ls(self):
        """
        List the files on the Pixel Kit. Emit the resulting tuple of filenames
        or emit a failure signal.
        """
        try:
            result = tuple(pixelfs.ls())
            self.on_list_files.emit(result)
        except Exception as ex:
            logger.exception(ex)
            self.on_list_fail.emit()

    def get(self, board_filename, local_filename):
        """
        Get the referenced Pixel Kit filename and save it to the local
        filename. Emit the name of the filename when complete or emit a
        failure signal.
        """
        try:
            pixelfs.get(board_filename, local_filename)
            self.on_get_file.emit(board_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_get_fail.emit(board_filename)

    def put(self, local_filename):
        """
        Put the referenced local file onto the filesystem on the Pixel Kit.
        Emit the name of the file on the Pixel Kit when complete, or emit
        a failure signal.
        """
        try:
            pixelfs.put(local_filename, target=None)
            self.on_put_file.emit(os.path.basename(local_filename))
        except Exception as ex:
            logger.error(ex)
            self.on_put_fail.emit(local_filename)

    def delete(self, board_filename):
        """
        Delete the referenced file on the Pixel Kit's filesystem. Emit the name
        of the file when complete, or emit a failure signal.
        """
        try:
            pixelfs.rm(board_filename)
            self.on_delete_file.emit(board_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_delete_fail.emit(board_filename)


class PixelKitMode(MicroPythonMode):
    """
    Represents the functionality required by the Kano Pixel Kit mode.
    """
    name = _("Kano Pixel Kit")
    description = _("Write MicroPython on the Kano Pixel Kit.")
    icon = "pixelkit"
    fs = None  #: Reference to filesystem navigator.
    flash_thread = None
    flash_timer = None

    valid_boards = [
        (0x0403, 0x6015),  # Kano Pixel Kit USB VID, PID
    ]

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                'name': 'run',
                'display_name': _('Run'),
                'description': _('Execute code from active tab.'),
                'handler': self.run,
                'shortcut': '',
            },
            {
                'name': 'stop',
                'display_name': _('Stop'),
                'description': _('Interrupts running code.'),
                'handler': self.stop,
                'shortcut': '',
            },
            {
                'name': 'mpfiles',
                'display_name': _('Files'),
                'description': _('Access the file system on the Pixel Kit.'),
                'handler': self.toggle_files,
                'shortcut': 'F4',
            },
            {
                'name': 'repl',
                'display_name': _('REPL'),
                'description': _('Use the REPL to live-code on the '
                                 'Pixel Kit.'),
                'handler': self.toggle_repl,
                'shortcut': 'Ctrl+Shift+I',
            },
            {
                'name': 'mpflash',
                'display_name': _('Flash'),
                'description': _('Flash your Pixel Kit with MicroPython'),
                'handler': self.flash,
                'shortcut': 'Ctrl+Shift+I',
            }, ]
        return buttons

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS

    def run(self):
        """
        Run code on current tab.
        """
        port, serial_number = self.find_device()
        if not port or not serial_number:
            message = _('Could not find an attached Pixel Kit.')
            information = _("Please make sure the device is plugged "
                            "into this computer and turned on.\n\n"
                            "If it's already on, try reseting it and waiting "
                            "a few seconds before trying again.")
            self.view.show_message(message, information)
            return
        if not self.repl:
            self.toggle_repl(self)
        serial = self.view.serial
        if serial and self.view.current_tab and self.view.current_tab.text():
            code = self.view.current_tab.text()
            self.enter_raw_repl()
            serial.write(bytes(code, 'ascii'))
            sleep(0.01)
            self.exit_raw_repl()

    def enter_raw_repl(self):
        self.view.serial.write(b'\x01')
        sleep(0.01)

    def exit_raw_repl(self):
        self.view.serial.write(b'\x04')  # CTRL-D
        sleep(0.01)
        self.view.serial.write(b'\x02')  # CTRL-B
        sleep(0.01)

    def stop(self):
        """
        Send keyboard interrupt.
        """
        port, serial_number = self.find_device()
        if not port or not serial_number:
            message = _('Could not find an attached Pixel Kit.')
            information = _("Please make sure the device is plugged "
                            "into this computer and turned on.\n\n"
                            "If it's already on, try reseting it and waiting "
                            "a few seconds before trying again.")
            self.view.show_message(message, information)
            return
        if not self.repl:
            self.toggle_repl(self)
        if self.view.serial:
            self.view.serial.write(b'\x03')  # CTRL-C

    def flash(self):
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor. Exit.
            return
        port, serial_number = self.find_device()
        if not port or not serial_number:
            message = _('Could not find an attached Pixel Kit.')
            information = _("Please make sure the device is plugged "
                            "into this computer and turned on.\n\n"
                            "If it's already on, try reseting it and waiting "
                            "a few seconds before trying again.")
            self.view.show_message(message, information)
            return
        message = _("Flash your Pixel Kit with MicroPython.")
        informaton = _("Make sure you have internet connection and don't "
                       "disconnect your device during the process. It "
                       "might take a minute or two but you will only need"
                       "to do it once.")
        confirmation = self.view.show_confirmation(message, informaton)
        if confirmation != QMessageBox.Cancel:
            self.set_buttons(
                mpflash=False, mpfiles=False, run=False, stop=False, repl=False
            )
            self.flash_thread = DeviceFlasher(port)

            self.flash_thread.finished.connect(self.flash_finished)
            self.flash_thread.on_flash_fail.connect(self.flash_failed)
            self.flash_thread.on_data.connect(self.on_flash_data)
            self.flash_thread.start()

    def flash_finished(self):
        self.set_buttons(
            mpflash=True, mpfiles=True, run=True, stop=True, repl=True
        )
        self.editor.show_status_message(_('Pixel Kit was flashed. Have fun!'))
        message = _("Pixel Kit was flashed. Have fun!")
        information = _("Your Pixel Kit now has MicroPython on it. Restart it "
                        "to start using!")
        self.view.show_message(message, information, 'Warning')
        logger.info('Flash finished.')
        self.flash_thread = None
        self.flash_timer = None

    def flash_failed(self, error):
        self.set_buttons(
            mpflash=True, mpfiles=True, run=True, stop=True, repl=True
        )
        logger.info('Flash failed.')
        logger.error(error)
        message = _("There was a problem flashing the Pixel Kit.")
        information = _("Please do not disconnect the device until flashing"
                        " has completed. Please check the logs for more"
                        " information.")
        self.view.show_message(message, information, 'Warning')
        self.editor.show_status_message(_("Pixel Kit could not be flashed. "
                                          "Please restart the Pixel Kit and "
                                          "try again."))
        if self.flash_timer:
            self.flash_timer.stop()
            self.flash_timer = None
        self.flash_thread = None

    def on_flash_data(self, message):
        self.editor.show_status_message(message)

    def toggle_repl(self, event):
        """
        Check for the existence of the file pane before toggling REPL.
        """
        if self.fs is None:
            super().toggle_repl(event)
            if self.repl:
                self.set_buttons(
                    mpflash=False, mpfiles=False, run=True, stop=True,
                )
            elif not (self.repl or self.plotter):
                self.set_buttons(
                    mpflash=True, mpfiles=True, run=True, stop=True,
                )
        else:
            message = _("REPL and file system cannot work at the same time.")
            information = _("The REPL and file system both use the same USB "
                            "serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def toggle_files(self, event):
        """
        Check for the existence of the REPL or plotter before toggling the file
        system navigator for the Pixel Kit on or off.
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
                    self.set_buttons(
                        mpflash=False, repl=False, run=False, stop=False,
                        plotter=False,
                    )
            else:
                self.remove_fs()
                logger.info('Toggle filesystem off.')
                self.set_buttons(
                    mpflash=True, repl=True, run=True, stop=True, plotter=True,
                )

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """
        # Check for Pixel Kit
        port, serial_number = self.find_device()
        if not port:
            message = _('Could not find an attached Pixel Kit.')
            information = _("Please make sure the device is plugged "
                            "into this computer.\n\nThe device must "
                            "have MicroPython flashed onto it before "
                            "the file system will work.\n\n"
                            "Finally, reset it and wait a few seconds "
                            "before trying again.")
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
        self.set_buttons(mpfiles=True)
        super().on_data_flood()
