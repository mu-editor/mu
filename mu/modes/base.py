"""
Contains the base classes for Mu editor modes.

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
import sys
import os
import os.path
import csv
import time
import logging
import pkgutil
from serial import Serial
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QObject, pyqtSignal, QIODevice, QTimer
from mu.logic import Device
from mu.contrib import microfs
from .. import config, settings

ENTER_RAW_MODE = b"\x01"  # CTRL-A
EXIT_RAW_MODE = b"\x02"  # CTRL-B
KEYBOARD_INTERRUPT = b"\x03"  # CTRL-C
SOFT_REBOOT = b"\x04"  # CTRL-C


logger = logging.getLogger(__name__)


# Cache module names for filename shadow checking later.
MODULE_NAMES = set([name for _, name, _ in pkgutil.iter_modules()])
MODULE_NAMES.add("sys")
MODULE_NAMES.add("builtins")


def get_default_workspace():
    """
    Return the location on the filesystem for opening and closing files.

    The default is to use a directory in the users home folder, however
    in some network systems this in inaccessible. This allows a key in the
    settings file to be used to set a custom path.
    """
    workspace_dir = os.path.join(config.HOME_DIRECTORY, config.WORKSPACE_NAME)
    settings_workspace = settings.settings.get("workspace")

    if settings_workspace:
        if os.path.isdir(settings_workspace):
            logger.info(
                "Using workspace {} from settings file".format(
                    settings_workspace
                )
            )
            workspace_dir = settings_workspace
        else:
            logger.warn(
                "Workspace {} in the settings file is not a valid "
                "directory; using default {}".format(
                    settings_workspace, workspace_dir
                )
            )

    return workspace_dir


class REPLConnection(QObject):
    serial = None
    data_received = pyqtSignal(bytes)
    connection_error = pyqtSignal(str)

    def __init__(self, port, baudrate=115200):
        super().__init__()
        self.serial = QSerialPort()
        self._port = port
        self._baudrate = baudrate
        self.serial.setPortName(port)
        self.serial.setBaudRate(baudrate)

    @property
    def port(self):
        if self.serial:
            # perhaps return self.serial.portName()?
            return self._port
        else:
            return None

    @property
    def baudrate(self):
        if self.serial:
            # perhaps return self.serial.baudRate()
            return self._baudrate
        else:
            return None

    def open(self):
        """
        Open the serial link
        """

        logger.info("Connecting to REPL on port: {}".format(self.port))

        if not self.serial.open(QIODevice.ReadWrite):
            msg = _("Cannot connect to device on port {}").format(self.port)
            raise IOError(msg)

        self.serial.setDataTerminalReady(True)
        if not self.serial.isDataTerminalReady():
            # Using pyserial as a 'hack' to open the port and set DTR
            # as QtSerial does not seem to work on some Windows :(
            # See issues #281 and #302 for details.
            self.serial.close()
            pyser = Serial(self.port)  # open serial port w/pyserial
            pyser.dtr = True
            pyser.close()
            self.serial.open(QIODevice.ReadWrite)
        self.serial.readyRead.connect(self._on_serial_read)

        logger.info("Connected to REPL on port: {}".format(self.port))

    def close(self):
        """
        Close and clean up the currently open serial link.
        """
        logger.info("Closing connection to REPL on port: {}".format(self.port))
        if self.serial:
            self.serial.close()
            self.serial = None

    def _on_serial_read(self):
        """
        Called when data is ready to be send from the device
        """
        data = bytes(self.serial.readAll())
        self.data_received.emit(data)

    def write(self, data):
        self.serial.write(data)

    def send_interrupt(self):
        self.write(EXIT_RAW_MODE)  # CTRL-B
        self.write(KEYBOARD_INTERRUPT)  # CTRL-C

    def execute(self, commands):
        """
        Execute a series of commands over a period of time (scheduling
        remaining commands to be run in the next iteration of the event loop).
        """
        if commands:
            command = commands[0]
            logger.info("Sending command {}".format(command))
            self.write(command)
            remainder = commands[1:]
            remaining_task = lambda commands=remainder: self.execute(commands)
            QTimer.singleShot(2, remaining_task)

    def send_commands(self, commands):
        """
        Send commands to the REPL via raw mode.
        """
        # Sequence of commands to get into raw mode (From pyboard.py).
        raw_on = [
            KEYBOARD_INTERRUPT,
            KEYBOARD_INTERRUPT,
            ENTER_RAW_MODE,
            SOFT_REBOOT,
            KEYBOARD_INTERRUPT,
            KEYBOARD_INTERRUPT,
        ]

        newline = [b'print("\\n");']
        commands = [c.encode("utf-8") + b"\r" for c in commands]
        commands.append(b"\r")
        commands.append(SOFT_REBOOT)
        raw_off = [EXIT_RAW_MODE]
        command_sequence = raw_on + newline + commands + raw_off
        logger.info(command_sequence)
        self.execute(command_sequence)


class BaseMode(QObject):
    """
    Represents the common aspects of a mode.
    """

    name = "UNNAMED MODE"
    short_name = "UNDEFINED_MODE"
    description = "DESCRIPTION NOT AVAILABLE."
    icon = "help"
    repl = False
    plotter = False
    is_debugger = False
    has_debugger = False
    save_timeout = 5  #: Number of seconds to wait before saving work.
    builtins = None  #: Symbols to assume as builtins when checking code style.
    file_extensions = []
    module_names = MODULE_NAMES
    code_template = _("# Write your code here :-)")

    def __init__(self, editor, view):
        self.editor = editor
        self.view = view
        super().__init__()

    def stop(self):
        """
        Called if/when the editor quits when in this mode. Override in child
        classes to clean up state, stop child processes etc.
        """
        pass  # Default is to do nothing

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return NotImplemented

    def workspace_dir(self):
        """
        Return the location on the filesystem for opening and closing files.

        The default is to use a directory in the users home folder, however
        in some network systems this in inaccessible. This allows a key in the
        settings file to be used to set a custom path.
        """
        return get_default_workspace()

    def assets_dir(self, asset_type):
        """
        Determine (and create) the directory for a set of assets

        This supports the [Images] and [Sounds] &c. buttons in pygamezero
        mode and possibly other modes, too.

        If a tab is current and has an active file, the assets directory
        is looked for under that path; otherwise the workspace directory
        is used.

        If the assets directory does not exist it is created
        """
        if self.view.current_tab and self.view.current_tab.path:
            base_dir = os.path.dirname(self.view.current_tab.path)
        else:
            base_dir = self.workspace_dir()
        assets_dir = os.path.join(base_dir, asset_type)
        os.makedirs(assets_dir, exist_ok=True)
        return assets_dir

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return NotImplemented

    def set_buttons(self, **kwargs):
        """
        Given the names and boolean settings of buttons associated with actions
        for the current mode, toggles them into the boolean enabled state.
        """
        for k, v in kwargs.items():
            if k in self.view.button_bar.slots:
                self.view.button_bar.slots[k].setEnabled(bool(v))

    def return_focus_to_current_tab(self):
        """
        After, eg, stopping the plotter or closing the REPL return the focus
        to the currently-active tab is there is one.
        """
        if self.view.current_tab:
            self.view.current_tab.setFocus()

    def add_plotter(self):
        """
        Mode specific implementation of adding and connecting a plotter to
        incoming streams of data tuples.
        """
        return NotImplemented

    def write_plotter_data_to_csv(self, csv_filepath):
        """Write any plotter data out to a CSV file when the
        plotter is closed
        """
        with open(csv_filepath, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(self.view.plotter_pane.raw_data)

    def remove_plotter(self):
        """
        If there's an active plotter, hide it.

        Save any data captured while the plotter was active into a directory
        called 'data_capture' in the workspace directory. The file contains
        CSV data and is named with a timestamp for easy identification.
        """
        # Save the raw data as CSV
        data_dir = os.path.join(get_default_workspace(), "data_capture")
        if not os.path.exists(data_dir):
            logger.debug("Creating directory: {}".format(data_dir))
            os.makedirs(data_dir)
        filename = "{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))
        filepath = os.path.join(data_dir, filename)
        self.write_plotter_data_to_csv(filepath)
        self.view.remove_plotter()
        self.plotter = False
        logger.info("Removing plotter")
        self.return_focus_to_current_tab()

    def on_data_flood(self):
        """
        Handle when the plotter is being flooded by data (which usually causes
        Mu to become unresponsive). In this case, remove the plotter and
        display a warning dialog to explain what's happened and how to fix
        things (usually, put a time.sleep(x) into the code generating the
        data).
        """
        logger.error("Plotting data flood detected.")
        self.view.remove_plotter()
        self.plotter = False
        msg = _("Data Flood Detected!")
        info = _(
            "The plotter is flooded with data which will make Mu "
            "unresponsive and freeze. As a safeguard, the plotter has "
            "been stopped.\n\n"
            "Flooding is when chunks of data of more than 1024 bytes are "
            "repeatedly sent to the plotter.\n\n"
            "To fix this, make sure your code prints small tuples of "
            "data between calls to 'sleep' for a very short period of "
            "time."
        )
        self.view.show_message(msg, info)

    def open_file(self, path):
        """
        Some files are not plain text and each mode can attempt to decode them.

        When overridden, should return the text and newline convention for the
        file.
        """
        return None, None

    def activate(self):
        """
        Executed when the mode is activated
        """
        pass  # Default is to do nothing

    def deactivate(self):
        """
        Executed when the mode is activated
        """
        pass  # Default is to do nothing

    def device_changed(self, new_device):
        """
        Invoked when the user changes device.
        """
        pass


class MicroPythonMode(BaseMode):
    """
    Includes functionality that works with a USB serial based REPL.
    """

    valid_boards = []
    force_interrupt = True
    connection = None
    baudrate = 115200
    builtins = ["const"]

    def compatible_board(self, port):
        """
        A compatible board must match on vendor ID, but only needs to
        match on product ID or manufacturer ID, if they are supplied
        in the list of valid boards (aren't None).
        """
        pid = port.productIdentifier()
        vid = port.vendorIdentifier()
        manufacturer = port.manufacturer()
        serial_number = port.serialNumber()
        port_name = self.port_path(port.portName())

        for v, p, m, device_name in self.valid_boards:
            if (
                v == vid
                and (p == pid or p is None)
                and (m == manufacturer or m is None)
            ):
                return Device(
                    vid,
                    pid,
                    port_name,
                    serial_number,
                    manufacturer,
                    self.name,
                    self.short_name,
                    device_name,
                )
        return None

    def find_devices(self, with_logging=True):
        """
        Returns the port and serial number, and name for the first
        MicroPython-ish device found connected to the host computer.
        If no device is found, returns the tuple (None, None, None).
        """
        available_ports = QSerialPortInfo.availablePorts()
        devices = []
        for port in available_ports:
            device = self.compatible_board(port)
            if device:
                # On OS X devices show up with two different port
                # numbers (/dev/tty.usbserial-xxx and
                # /dev/cu.usbserial-xxx) we only want to display the
                # ones on ports names /dev/cu.usbserial-xxx to users
                if sys.platform == "darwin" and device.port[:7] != "/dev/cu":
                    continue
                if with_logging:
                    logger.info("Found device on port: {}".format(device.port))
                    logger.info(
                        "Serial number: {}".format(device.serial_number)
                    )
                    if device.board_name:
                        logger.info("Board type: {}".format(device.board_name))
                devices.append(device)
        if not devices and with_logging:
            logger.warning("Could not find device.")
            logger.debug("Available ports:")
            logger.debug(
                [
                    "PID:0x{:04x} VID:0x{:04x} PORT:{}".format(
                        p.productIdentifier(),
                        p.vendorIdentifier(),
                        p.portName(),
                    )
                    for p in available_ports
                ]
            )
        return devices

    def port_path(self, port_name):
        if os.name == "posix":
            # If we're on Linux or OSX reference the port is like this...
            return "/dev/{}".format(port_name)
        elif os.name == "nt":
            # On Windows simply return the port (e.g. COM0).
            return port_name
        else:
            # No idea how to deal with other OS's so fail.
            raise NotImplementedError('OS "{}" not supported.'.format(os.name))

    def toggle_repl(self, event):
        """
        Toggles the REPL on and off.
        """
        if self.repl:
            self.remove_repl()
            logger.info("Toggle REPL off.")
        else:
            self.add_repl()
            logger.info("Toggle REPL on.")

    def remove_repl(self):
        """
        If there's an active REPL, disconnect and hide it.
        """
        if not self.plotter and self.connection:
            self.connection.close()
            self.connection = None
        self.view.remove_repl()
        self.repl = False

    def add_repl(self):
        """
        Detect a connected MicroPython based device and, if found, connect to
        the REPL and display it to the user.
        """
        device = self.editor.current_device
        if device:
            try:
                if not self.connection:
                    self.connection = REPLConnection(
                        device.port, self.baudrate
                    )
                    self.connection.open()
                    if self.force_interrupt:
                        self.connection.send_interrupt()

                self.view.add_micropython_repl(self.name, self.connection)
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
                " MicroPython (or CircuitPython) flashed onto it"
                " before the REPL will work.\n\nFinally, press the"
                " device's reset button and wait a few seconds"
                " before trying again."
            )
            self.view.show_message(message, information)

    def toggle_plotter(self, event):
        """
        Toggles the plotter on and off.
        """
        if self.plotter:
            self.remove_plotter()
            logger.info("Toggle plotter off.")
        else:
            self.add_plotter()
            logger.info("Toggle plotter on.")

    def add_plotter(self):
        """
        Check if REPL exists, and if so, enable the plotter pane!
        """
        device = self.editor.current_device
        if device:
            try:
                if not self.connection:
                    self.connection = REPLConnection(
                        device.port, self.baudrate
                    )
                    self.connection.open()
                self.view.add_micropython_plotter(
                    self.name, self.connection, self.on_data_flood
                )
                logger.info("Started plotter")
                self.plotter = True
            except IOError as ex:
                logger.error(ex)
                self.plotter = False
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
                " MicroPython (or CircuitPython) flashed onto it"
                " before the Plotter will work.\n\nFinally, press"
                " the device's reset button and wait a few seconds"
                " before trying again."
            )
            self.view.show_message(message, information)

    def on_data_flood(self):
        """
        Ensure the REPL is stopped if there is data flooding of the plotter.
        """
        self.remove_repl()
        super().on_data_flood()

    def remove_plotter(self):
        """
        Remove plotter pane. Disconnects serial connection to device.
        """
        if not self.repl and self.connection:
            self.connection.close()
            self.connection = None
        super().remove_plotter()

    def activate(self):
        """
        Invoked whenever the mode is activated.
        """
        self.view.show_device_selector()

    def deactivate(self):
        """
        Invoked whenever the mode is deactivated.
        """
        # Remove REPL/Plotter if they are active
        self.view.hide_device_selector()
        if self.plotter:
            self.remove_plotter()
        if self.repl:
            self.remove_repl()

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


class FileManager(QObject):
    """
    Used to manage filesystem operations on connected MicroPython devices in a
    manner such that the UI remains responsive.

    Provides an FTP-ish API. Emits signals on success or failure of different
    operations.
    """

    # Emitted when the tuple of files on the device is known.
    on_list_files = pyqtSignal(tuple)
    # Emitted when the file with referenced filename is got from the device.
    on_get_file = pyqtSignal(str)
    # Emitted when the file with referenced filename is put onto the device.
    on_put_file = pyqtSignal(str)
    # Emitted when the file with referenced filename is deleted from the
    # device.
    on_delete_file = pyqtSignal(str)
    # Emitted when Mu is unable to list the files on the device.
    on_list_fail = pyqtSignal()
    # Emitted when the referenced file fails to be got from the device.
    on_get_fail = pyqtSignal(str)
    # Emitted when the referenced file fails to be put onto the device.
    on_put_fail = pyqtSignal(str)
    # Emitted when the referenced file fails to be deleted from the device.
    on_delete_fail = pyqtSignal(str)

    def __init__(self, port):
        """
        Initialise with a port.
        """
        super().__init__()
        self.port = port

    def on_start(self):
        """
        Run when the thread containing this object's instance is started so
        it can emit the list of files found on the connected device.
        """
        # Create a new serial connection.
        try:
            self.serial = Serial(
                self.port,
                115200,
                timeout=settings.settings.get("serial_timeout", 2),
                parity="N",
            )
            self.ls()
        except Exception as ex:
            logger.exception(ex)
            self.on_list_fail.emit()

    def ls(self):
        """
        List the files on the micro:bit. Emit the resulting tuple of filenames
        or emit a failure signal.
        """
        try:
            result = tuple(microfs.ls(self.serial))
            self.on_list_files.emit(result)
        except Exception as ex:
            logger.exception(ex)
            self.on_list_fail.emit()

    def get(self, device_filename, local_filename):
        """
        Get the referenced device filename and save it to the local
        filename. Emit the name of the filename when complete or emit a
        failure signal.
        """
        try:
            microfs.get(device_filename, local_filename, serial=self.serial)
            self.on_get_file.emit(device_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_get_fail.emit(device_filename)

    def put(self, local_filename, target=None):
        """
        Put the referenced local file onto the filesystem on the micro:bit.
        Emit the name of the file on the micro:bit when complete, or emit
        a failure signal.
        """
        try:
            microfs.put(local_filename, target=target, serial=self.serial)
            self.on_put_file.emit(os.path.basename(local_filename))
        except Exception as ex:
            logger.error(ex)
            self.on_put_fail.emit(local_filename)

    def delete(self, device_filename):
        """
        Delete the referenced file on the device's filesystem. Emit the name
        of the file when complete, or emit a failure signal.
        """
        try:
            microfs.rm(device_filename, serial=self.serial)
            self.on_delete_file.emit(device_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_delete_fail.emit(device_filename)
