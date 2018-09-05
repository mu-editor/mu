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

import logging
from argparse import Namespace
import tempfile
import urllib.request
import tarfile
from PyQt5.QtCore import QThread, pyqtSignal
import esptool

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
            self.on_flash_fail.emit("Unknown firmware type: {0}".format(self.firmware_type))

    def get_addr_filename(self, values):
        if len(values) % 2 != 0:
            raise Exception('Values must come in pairs')
        addr_filename = []
        for i in range(0, len(values), 2):
            addr = int(values[i], 0)
            file = open(values[i+1], 'rb')
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
            esp32loader = esptool.ESPLoader.detect_chip(self.port, 115200, False)
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
        url = "http://micropython.org/resources/firmware/esp32-20180511-v1.9.4.bin"
        f = tempfile.NamedTemporaryFile()
        f.close()
        try:
            urllib.request.urlretrieve(url, f.name)
            # TODO: Checksum the firmware
            logger.info("Downloaded MicroPython firmware to: {0}".format(f.name))
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
        members = tar.getmembers()
        tar.extractall(path=tmpdir.name)
        values = [
            "0x1000", "{0}/RPK_Bootloader_V1_0_2.bin".format(tmpdir.name),
            "0x10000", "{0}/RPK_App_V1_0_2.bin".format(tmpdir.name),
            "0x8000", "{0}/RPK_Partitions_V1_0_2.bin".format(tmpdir.name)
        ]
        addr_filename = self.get_addr_filename(values)
        self.write_flash(addr_filename)
