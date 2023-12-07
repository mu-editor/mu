"""
A mode for working with Snek boards. https://keithp.com/snek

Copyright © 2019 Keith Packard

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
from .base import MicroPythonMode, REPLConnection
from .api import SNEK_APIS
from mu.interface.panes import CHARTS
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer

logger = logging.getLogger(__name__)

snek_bauds = [115200, 57600]


class SnekREPLConnection(REPLConnection):
    """
    Handle Snek serial connection, including flow control
    """

    def __init__(
        self,
        port,
        baudrate=115200,
        flowcontrol=False,
        chunk=16,
        wait_for_data=False,
    ):
        super().__init__(port, baudrate)
        self.flowcontrol = flowcontrol
        self.sent = 0
        self.chunk = chunk
        self.data = b""
        self.waiting = False
        self.ready = False
        self.pending = b""
        self.wait_for_data = wait_for_data
        self.got_dc4 = False

    def set_ready(self):
        """
        Device is ready, detect baud rate, then send any pending output
        """
        if self.ready:
            return
        self.ready = True
        if self.flowcontrol:
            for self._baudrate in snek_bauds:
                logger.info("Try baudrate %d" % self._baudrate)
                self.serial.setBaudRate(self._baudrate)
                self.serial.write(b"\x14\n")
                self.serial.waitForReadyRead(250)
                if self.got_dc4:
                    logger.info("Autobaud response detected")
                    break
                logger.info("No autobaud response")
            else:
                self._baudrate = snek_bauds[0]
                logger.info("Using default baudrate %d" % self._baudrate)
                self.serial.setBaudRate(self._baudrate)
        self.write(self.pending)
        self.pending = b""

    def open(self):
        super().open()

        # If the device will reset on open, wait for it to send
        # something before talking to it. Don't wait more than three
        # seconds, in case it doesn't actually reset, or uses a
        # non-default baud rate

        if self.wait_for_data:
            ready_func = lambda: self.set_ready()
            QTimer.singleShot(3000, ready_func)
        else:
            self.set_ready()

    # Flow control: every 'chunk' bytes, send an ENQ character and
    # block until the matching ACK is received

    def send_enq(self):
        super().write(b"\x05")
        self.waiting = True

    # Called when an ACK is received. Restart transmission.

    def recv_ack(self):
        self.sent = 0
        self.waiting = False
        self.send_data()

    def _on_serial_read(self):
        data = bytes(self.serial.readAll())

        # when we receive an ACK, restart transmission
        if b"\x06" in data:
            self.recv_ack()
            data = data.replace(b"\x06", b"")

        # we receive DC4 during startup for autobaud
        if b"\x14" in data:
            self.got_dc4 = True
            data = data.replace(b"\x14", b"")

        self.data_received.emit(data)

        # if we were waiting for reset, we know the device is now
        # ready, so start transmitting
        if not self.ready and b"W" in data:
            ready_func = lambda: self.set_ready()
            # give it 200ms to finish starting up
            QTimer.singleShot(200, ready_func)

    def send_data(self):
        while not self.waiting and self.data:
            amt = self.chunk - self.sent
            if amt > len(self.data):
                amt = len(self.data)
            part = self.data[:amt]
            self.data = self.data[amt:]
            super().write(part)
            self.sent += amt
            if self.sent >= self.chunk:
                self.send_enq()

    # Overload write method to handle flow control when needed

    def write(self, data):
        if not self.ready:
            self.pending += data
            return
        if self.flowcontrol:
            if b"\x03" in data:
                self.data = data
                self.sent = 0
                self.waiting = False
            else:
                self.data += data
            self.send_data()
        else:
            super().write(data)

    def send_interrupt(self):
        # Send a Control-O / exit raw mode.
        # Send a Control-C / keyboard interrupt.
        self.write(b"\x0f\x03")


class SnekMode(MicroPythonMode):
    """
    Represents the functionality required by the Snek mode.
    """

    name = _("Snek")
    short_name = "snek"
    description = _("Write code for boards running Snek.")
    icon = "snek"
    save_timeout = 0  #: No auto-save on CP boards. Will restart.
    connected = True  #: is the board connected.
    force_interrupt = True  #: keyboard interrupt on serial connection.
    valid_boards = [
        # VID  , PID   , manufact., device name
        (0xFFFE, None, None, "Altus Metrum"),
        (0x239A, 0x8022, None, "Adafruit Feather M0 Express"),
        (0x239A, 0x8011, None, "Adafruit ItsyBitsy M0"),
        (0x239A, 0x8013, None, "Adafruit Metro M0 Express"),
        (0x239A, 0x8018, None, "Circuit Playground Express M0"),
        (0x239A, 0x804D, None, "Snekboard"),
        (0x1366, 0x1051, None, "SiFive Hifive1 Revb"),
        (0x2341, 0x8057, None, "Arduino SA Nano 33 IoT"),
        (0x2341, 0x0010, None, "Arduino Mega 2560"),
        (0x2341, 0x0058, None, "Arduino Nano Every"),
        (0x2341, 0x0043, None, "Arduino Uno"),
        (0x03EB, 0x204B, None, "Arduino Mega with LUFA"),
        (0x2886, 0x002E, None, "Seeed Xiao"),
    ]
    # These boards don't need flow control
    usb_boards = [
        (0xFFFE, None),
        (0x239A, 0x8022),
        (0x239A, 0x8011),
        (0x239A, 0x8013),
        (0x239A, 0x8018),
        (0x239A, 0x804D),
    ]
    # These boards get reset when we connect, wait before talking
    reset_boards = [
        (0x0403, 0x6001),  # Duemilanove with FT232
        (0x03EB, 0x204B),  # Arduino Mega with LUFA
        (0x10C4, 0xEA60),  # Seeed Grove with CP210x
        (0x2341, 0x0010),  # Arduino Mega 2560
        (0x2341, 0x0058),  # Arduino Nano Every
        (0x2341, 0x0043),  # Arduino Uno
        (0x1A86, 0x7523),  # Pandauino Narrow 1284
    ]
    # Modules built into Snek which mustn't be used as file names
    # for source code.
    module_names = {"time", "random", "math"}
    builtins = (
        "A0",
        "A1",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "BUTTONA",
        "BUTTONB",
        "CAP1",
        "CAP2",
        "CAP3",
        "CAP4",
        "D0",
        "D1",
        "D10",
        "D11",
        "D12",
        "D13",
        "D14",
        "D15",
        "D16",
        "D17",
        "D18",
        "D19",
        "D2",
        "D20",
        "D21",
        "D22",
        "D23",
        "D24",
        "D25",
        "D26",
        "D27",
        "D28",
        "D29",
        "D3",
        "D30",
        "D31",
        "D32",
        "D33",
        "D34",
        "D35",
        "D36",
        "D37",
        "D38",
        "D39",
        "D4",
        "D40",
        "D41",
        "D42",
        "D43",
        "D44",
        "D45",
        "D46",
        "D47",
        "D48",
        "D49",
        "D5",
        "D50",
        "D51",
        "D52",
        "D53",
        "D6",
        "D7",
        "D8",
        "D9",
        "DRIVE1",
        "DRIVE2",
        "DRIVE3",
        "DRIVE4",
        "FLASHCS",
        "FLASHMISO",
        "FLASHMOSI",
        "FLASHSCK",
        "I2SCK",
        "I2SDO",
        "LED",
        "LIGHT",
        "LISIRQ",
        "LISSCL",
        "LISSDA",
        "M1",
        "M2",
        "M3",
        "M4",
        "MISO",
        "MOSI",
        "MOTOR1",
        "MOTOR2",
        "NEOPIXEL",
        "NEOPIXEL1",
        "REMOTEIN",
        "REMOTEOUT",
        "RX",
        "SCK",
        "SCL",
        "SDA",
        "SERVO1",
        "SERVO2",
        "SERVO3",
        "SERVO4",
        "SIGNAL1",
        "SIGNAL2",
        "SIGNAL3",
        "SIGNAL4",
        "SIGNAL5",
        "SIGNAL6",
        "SIGNAL7",
        "SIGNAL8",
        "SWITCH",
        "TEMP",
        "TX",
        "abs_tol",
        "curses",
        "eeprom",
        "exit",
        "math",
        "neopixel",
        "off",
        "on",
        "onfor",
        "pulldown",
        "pullnone",
        "pullup",
        "random",
        "read",
        "rel_tol",
        "reset",
        "round",
        "setleft",
        "setpower",
        "setright",
        "stdscr",
        "stopall",
        "sys",
        "talkto",
        "temperature",
        "time",
    )

    def stop(self):
        self.remove_repl()

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                "name": "serial",
                "display_name": _("Serial"),
                "description": _("Open a serial connection to your device."),
                "handler": self.toggle_repl,
                "shortcut": "CTRL+Shift+U",
            },
            {
                "name": "flash",
                "display_name": _("Put"),
                "description": _("Put the current program to the device."),
                "handler": self.put,
                "shortcut": "CTRL+Shift+P",
            },
            {
                "name": "getflash",
                "display_name": _("Get"),
                "description": _("Get the current program from the device."),
                "handler": self.get,
                "shortcut": "CTRL+Shift+G",
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

    def put(self):
        """
        Put the current program into the device memory.
        """
        logger.info("Downloading code to target device.")
        # Grab the Python script.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor.
            message = _("Cannot run anything without any active editor tabs.")
            information = _(
                "Running transfers the content of the current tab"
                " onto the device. It seems like you don't have "
                " any tabs open."
            )
            self.view.show_message(message, information)
            return
        python_script = tab.text()
        if not python_script or python_script[-1] != "\n":
            python_script += "\n"
        if not self.repl:
            self.toggle_repl(None)
        command = ("eeprom.write()\n" + python_script + "\x04" + "reset()\n",)
        if self.repl:
            self.view.repl_pane.send_commands(command)

    def get_tab(self):
        for tab in self.view.widgets:
            if not tab.path:
                return tab
        return None

    def recv_text(self, text):
        target_tab = self.get_tab()
        if target_tab:
            target_tab.setText(text)
            target_tab.setModified(False)
        else:
            view = self.view
            editor = self.editor
            view.add_tab(None, text, editor.modes[editor.mode].api(), "\n")

    def get(self):
        """
        Get the current program from device memory.
        """
        target_tab = self.get_tab()
        if target_tab and target_tab.isModified():
            msg = _(
                "There is un-saved work, 'get' will cause you " "to lose it."
            )
            window = target_tab.nativeParentWidget()
            if window.show_confirmation(msg) == QMessageBox.Cancel:
                return

        command = ("eeprom.show(1)\n",)
        if not self.repl:
            self.toggle_repl(None)
        if self.repl:
            self.view.repl_pane.text_recv = self
            self.view.repl_pane.send_commands(command)

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SNEK_APIS

    def add_repl(self):
        """
        Detect a connected Snek based device and, if found, connect to
        the REPL and display it to the user.
        """
        device = self.editor.current_device
        if device:
            baudrate = snek_bauds[0]
            try:
                if not self.connection:
                    flowcontrol = not (
                        (device.vid, device.pid) in self.usb_boards
                        or (device.vid, None) in self.usb_boards
                    )

                    # If the board is going to get rebooted when we open it,
                    # wait for it to say something before trying to talk to it
                    wait_for_data = (
                        device.vid,
                        device.pid,
                    ) in self.reset_boards

                    self.connection = SnekREPLConnection(
                        device.port,
                        baudrate=baudrate,
                        flowcontrol=flowcontrol,
                        wait_for_data=wait_for_data,
                    )

                    self.connection.open()

                    if self.force_interrupt:
                        self.connection.send_interrupt()

                self.view.add_snek_repl(self.name, self.connection)

                logger.info("Started REPL on port: {}".format(device.port))
                self.repl = True
            except IOError as ex:
                logger.error(ex)
                self.repl = False
                info = _(
                    "Click on the device's reset button, wait a few"
                    " seconds and then try again."
                )
                self.view.show_message(str(ex), info)
            except Exception as ex:
                logger.error(ex)
        else:
            message = _("Could not find an attached device.")
            information = _(
                "Please make sure the device is plugged into this"
                " computer.\n\nIt must have a version of"
                " Snek flashed onto it before the REPL will work.\n\n"
                "Finally, press the device's reset button and wait a"
                " few seconds before trying again."
            )
            self.view.show_message(message, information)

    def device_changed(self, new_device):
        """
        Invoked when the user changes device.
        """
        # Reconnect REPL, Plotter and send interrupt
        if self.repl:
            self.remove_repl()
            self.add_repl()
        if self.plotter:
            self.remove_plotter()
            self.add_plotter()
        if self.connection:
            self.connection.send_interrupt()
