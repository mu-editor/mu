"""
A mode for working with ESP8266 and ESP32 boards running MicroPython.

Copyright (c) 2015-2019 Nicholas H.Tollervey and others (see the AUTHORS file).

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
from mu.modes.base import MicroPythonMode, FileManager
from mu.modes.api import ESP_APIS, SHARED_APIS
from mu.interface.panes import CHARTS
from PyQt5.QtCore import QThread
import os


logger = logging.getLogger(__name__)


class ESPMode(MicroPythonMode):
    """
    Represents the functionality required for running MicroPython on ESP8266
    """

    name = _("ESP MicroPython")
    short_name = "esp"
    board_name = "ESP8266/ESP32"
    description = _("Write MicroPython on ESP8266/ESP32 boards.")
    icon = "esp"
    fs = None

    # The below list defines the supported devices, however, many
    # devices are using the exact same FTDI USB-interface, with vendor
    # ID 0x403 without reporting their own VID/PID

    # In some instances we can recognize the device not on VID/PID,
    # but on manufacturer ID, that's what the third column is for.
    # These more specific device specifications, should be listed
    # before the generic FTDI VID/PID's
    valid_boards = [
        # VID  , PID,    Manufacturer string, Device name
        (0x1A86, 0x7523, None, "HL-340"),
        (0x10C4, 0xEA60, None, "CP210x"),
        (0x0403, 0x6001, "M5STACK Inc.", "M5Stack ESP32 device"),
        (0x0403, 0x6001, None, None),  # FT232/FT245 (XinaBox CW01, CW02)
        (0x0403, 0x6010, None, None),  # FT2232C/D/L/HL/Q (ESP-WROVER-KIT)
        (0x0403, 0x6011, None, None),  # FT4232
        (0x0403, 0x6014, None, None),  # FT232H
        (0x0403, 0x6015, None, None),  # FT X-Series (Sparkfun ESP32)
        (0x0403, 0x601C, None, None),  # FT4222H
    ]

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                "name": "run",
                "display_name": _("Run"),
                "description": _(
                    "Run your code directly on the {board_name}"
                    " via the REPL."
                ).format(board_name=self.board_name),
                "handler": self.run,
                "shortcut": "F5",
            },
            {
                "name": "files",
                "display_name": _("Files"),
                "description": _(
                    "Access the file system on {board_name}."
                ).format(board_name=self.board_name),
                "handler": self.toggle_files,
                "shortcut": "F4",
            },
            {
                "name": "repl",
                "display_name": _("REPL"),
                "description": _(
                    "Use the REPL to live-code on the {board_name}."
                ).format(board_name=self.board_name),
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
        return SHARED_APIS + ESP_APIS

    def toggle_repl(self, event):
        if self.fs is None:
            if self.repl:
                # Remove REPL
                super().toggle_repl(event)
                self.set_buttons(files=True)
            elif not (self.repl):
                # Add REPL
                super().toggle_repl(event)
                if self.repl:
                    self.set_buttons(files=False)
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
                self.set_buttons(files=False)
            elif not (self.repl or self.plotter):
                self.set_buttons(files=True)
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

    def run(self):
        """
        Takes the currently active tab, compiles the Python script therein into
        a hex file and flashes it all onto the connected device.
        """
        """
        if self.repl:
            message = _("Flashing cannot be performed at the same time as the "
                        "REPL is active.")
            information = _("File transfers use the same "
                            "USB serial connection as the REPL. Toggle the "
                            "REPL off and try again.")
            self.view.show_message(message, information)
            return
        """
        logger.info("Running script.")
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
        python_script = tab.text().split("\n")
        if not self.repl:
            self.toggle_repl(None)
        if self.repl and self.connection:
            self.connection.send_commands(python_script)

    def toggle_files(self, event):
        """
        Check for the existence of the REPL or plotter before toggling the file
        system navigator for the MicroPython device on or off.
        """
        if self.repl:
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
                    self.set_buttons(run=False, repl=False, plotter=False)
            else:
                self.remove_fs()
                logger.info("Toggle filesystem off.")
                self.set_buttons(run=True, repl=True, plotter=True)

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """

        # Find serial port the ESP8266/ESP32 is connected to
        device = self.editor.current_device

        # Check for MicroPython device
        if not device:
            message = _("Could not find an attached {board_name}").format(
                board_name=self.board_name
            )
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

        # Show directory of the current file in the left pane, if any,
        # otherwise show the default workspace_dir
        if self.view.current_tab and self.view.current_tab.path:
            path = os.path.dirname(os.path.abspath(self.view.current_tab.path))
        else:
            path = self.workspace_dir()
        self.fs = self.view.add_filesystem(
            path,
            self.file_manager,
            _("{board_name} board").format(board_name=self.board_name),
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
