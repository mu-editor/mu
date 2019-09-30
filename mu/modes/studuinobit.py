"""
A mode for working with Studuino:bit running MicroPython.

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
import os
import time
from mu.modes.base import MicroPythonMode, StuduinoBitFileManager
from mu.modes.api import STUDUINOBIT_APIS, SHARED_APIS
from mu.interface.panes import CHARTS
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import (QDialog, QGridLayout, QPushButton,
                             QHBoxLayout, QGroupBox, QLabel)
from mu.contrib import microfs
from mu.logic import HOME_DIRECTORY, WORKSPACE_NAME, save_and_encode
from serial import Serial

logger = logging.getLogger(__name__)


class StuduinoBitMode(MicroPythonMode):
    """
    Represents the functionality required for running
    MicroPython on Studuino:bit
    """
    name = _('Artec Studuino:Bit MicroPython')
    description = _("Write MicroPython on Studuino:bit.")
    icon = 'studuinobit'
    fs = None

    # There are many boards which use ESP microcontrollers but they often use
    # the same USB / serial chips (which actually define the Vendor ID and
    # Product ID for the connected devices.
    valid_boards = [
        # VID  , PID
        (0x20A0, 0x4269),   # Studuion:bit VID, PID
    ]

    def __init__(self, editor, view):
        super().__init__(editor, view)

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                'name': 'run',
                'display_name': _('Run'),
                'description': _('Run your code directly on the Studuino:bit'
                                 ' via the REPL.'),
                'handler': self.run,
                'shortcut': 'F5',
            },
            {
                'name': 'flash_sb',
                'display_name': _('Flash'),
                'description': _('Flash your code onto the Studuino:bit.'),
                'handler': self.toggle_flash,
                'shortcut': 'F3',
            },
            {
                'name': 'files_sb',
                'display_name': _('Files'),
                'description': _('Access the file system on Studuino:bit.'),
                'handler': self.toggle_files,
                'shortcut': 'F4',
            },
            {
                'name': 'repl',
                'display_name': _('REPL'),
                'description': _('Use the REPL to live-code on the '
                                 'Studuino:bit.'),
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
        return SHARED_APIS + STUDUINOBIT_APIS

    def toggle_repl(self, event):
        if self.fs is None:
            if self.repl:
                # Remove REPL
                super().toggle_repl(event)
                self.set_buttons(files_sb=True, flash_sb=True)
            elif not (self.repl):
                # Add REPL
                time.sleep(1)
                super().toggle_repl(event)
                if self.repl:
                    self.set_buttons(files_sb=False, flash_sb=False)
        else:
            message = _("REPL and file system cannot work at the same time.")
            information = _("The REPL and file system both use the same USB "
                            "serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def toggle_flash(self, event):
        """
        Display the folder to regist script. Return a dictionary of the
        settings that may have been changed by the admin dialog.
        """
        regist_box = RegisterWindow(self.view)
        result = regist_box.exec()
        if (result == 0):
            return

        # Display sending message
        self.editor.show_status_message(_("Updating..."))

        # Display sending message
        reg_info = regist_box.get_register_info()
        reg_num = reg_info[0]

        tab = self.view.current_tab
        usr_file = HOME_DIRECTORY + '\\' + WORKSPACE_NAME + \
            '\\studuinobit\\usr' + reg_num + '.py'
        save_and_encode(tab.text(), usr_file, tab.newline)

        # Send script
        device_port, serial_number = self.find_device()
        serial = None
        try:
            serial = Serial(device_port, 115200, timeout=1, parity='N')
            filename = os.path.basename(usr_file)
            microfs.put(usr_file, 'usr/' + filename, serial)
            microfs.execute([
                'import machine',
                'machine.nvs_setint("lastSelected", {0})'.format(reg_num),
            ], serial)
            time.sleep(0.1)
            serial.write(b'\x04')
        except Exception as e:
            logger.error(e)
        finally:
            if serial is not None:
                serial.dtr = True
                serial.close()

        self.toggle_repl(None)
        self.toggle_repl(None)

        # dlg_msg.close()
        self.editor.show_status_message(_("Finished transfer. \
            Press the reset button on the Studuino:bit"))

    def toggle_plotter(self, event):
        """
        Check for the existence of the file pane before toggling plotter.
        """
        if self.fs is None:
            super().toggle_plotter(event)
            if self.plotter:
                self.set_buttons(files_sb=False, flash_sb=False)
            elif not (self.repl or self.plotter):
                self.set_buttons(files_sb=True, flash_sb=True)
        else:
            message = _("The plotter and file system cannot work at the same "
                        "time.")
            information = _("The plotter and file system both use the same "
                            "USB serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def run(self):
        """
        Takes the currently active tab, compiles the Python script therein into
        a hex file and flashes it all onto the connected device.
        """

        if not self.repl:
            device_port, serial_number = self.find_device()
            try:
                serial = Serial(device_port, 115200, timeout=1, parity='N')
            except Exception as e:
                logger.error(e)
                return

            try:
                microfs.execute([
                    'import machine',
                    'machine.nvs_setint("lastSelected", 99)',
                ], serial)
            except IOError as e:
                self.editor.\
                    show_status_message(_('Please REST Button'))
                logger.error(e)
                serial.close()
                return

            serial.close()

        logger.info('Running script.')
        # Grab the Python script.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor.
            message = _("Cannot run anything without any active editor tabs.")
            information = _("Running transfers the content of the current tab"
                            " onto the device. It seems like you don't have "
                            " any tabs open.")
            self.view.show_message(message, information)
            return
        python_script = tab.text().split('\n')
        if not self.repl:
            self.toggle_repl(None)
        if self.repl:
            self.view.repl_pane.send_commands(python_script)

    def toggle_files(self, event):
        """
        Check for the existence of the REPL or plotter before toggling the file
        system navigator for the MicroPython device on or off.
        """
        if self.repl:
            message = _("File system cannot work at the same time as the "
                        "REPL or plotter.")
            information = _("The file system and the REPL and plotter "
                            "use the same USB serial connection. Toggle the "
                            "REPL and plotter off and try again.")
            self.view.show_message(message, information)
        else:
            if self.fs is None:
                time.sleep(1)
                self.add_fs()
                if self.fs:
                    logger.info('Toggle filesystem on.')
                    self.set_buttons(run=False, repl=False,
                                     plotter=False, flash_sb=False)
            else:
                self.remove_fs()
                logger.info('Toggle filesystem off.')
                self.set_buttons(run=True, repl=True,
                                 plotter=True, flash_sb=True)

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """

        # Find serial port the ESP8266/ESP32 is connected to
        device_port, serial_number = self.find_device()

        # Check for MicroPython device
        if not device_port:
            message = _('Could not find an attached Studuino:bit.')
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
        self.file_manager = StuduinoBitFileManager(device_port)
        self.file_manager.moveToThread(self.file_manager_thread)
        self.file_manager_thread.started.\
            connect(self.file_manager.on_start)
        self.fs = self.view.add_studuinobit_filesystem(self.workspace_dir(),
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
        self.set_buttons(files_sb=True)
        super().on_data_flood()

    def add_repl(self):
        """
        Detect a connected MicroPython based device and, if found, connect to
        the REPL and display it to the user.
        """
        device_port, serial_number = self.find_device()
        if device_port:
            try:
                self.view.add_studuionbit_repl(device_port, self.name,
                                               self.force_interrupt)
                logger.info('Started REPL on port: {}'.format(device_port))
                self.repl = True
            except IOError as ex:
                logger.error(ex)
                self.repl = False
                info = _("Click on the device's reset button, wait a few"
                         " seconds and then try again.")
                self.view.show_message(str(ex), info)
            except Exception as ex:
                logger.error(ex)
        else:
            message = _('Could not find an attached device.')
            information = _('Please make sure the device is plugged into this'
                            ' computer.\n\nIt must have a version of'
                            ' MicroPython (or CircuitPython) flashed onto it'
                            ' before the REPL will work.\n\nFinally, press the'
                            " device's reset button and wait a few seconds"
                            ' before trying again.')
            self.view.show_message(message, information)


class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.register_info = []

        grid = QGridLayout()
        grid.setSpacing(10)

        offset_v = 5
        offset_h = 3
        for i in range(10):
            reg_fname = QLabel('usr' + str(i) + '.py')
            button = QPushButton('Transfer')
            button.clicked.connect(self.on_click)
            hbox = QHBoxLayout()
            group_box = QGroupBox()
            group_box.setTitle(str(i))

            hbox.addWidget(reg_fname)
            hbox.addWidget(button)
            group_box.setLayout(hbox)

            if i > 4:
                grid.addWidget(group_box, i - offset_v, offset_h)
            else:
                grid.addWidget(group_box, i, 0)

        self.setLayout(grid)
        self.setWindowTitle('Select a slot to transfer.')

        self.parent = parent

    def on_click(self):
        sender = self.sender()
        reg_number = sender.parent().title()
        self.register_info.append(reg_number)
        self.accept()

    def get_register_info(self):
        """
        Return a selected slot number
        """
        return self.register_info
