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
import json
import os
import logging
from PyQt5.QtSerialPort import QSerialPortInfo
from PyQt5.QtCore import QObject
from mu.logic import HOME_DIRECTORY, WORKSPACE_NAME, get_settings_path


logger = logging.getLogger(__name__)


# List of supported board USB IDs.  Each board is a tuple of unique USB vendor
# ID, USB product ID.
BOARD_IDS = set([
    (0x0D28, 0x0204),  # micro:bit USB VID, PID
    (0x239A, 0x800B),  # Adafruit Feather M0 CDC only USB VID, PID
    (0x239A, 0x8016),  # Adafruit Feather M0 CDC + MSC USB VID, PID
    (0x239A, 0x8014),  # metro m0 PID
    (0x239A, 0x8019),  # circuitplayground m0 PID
    (0x239A, 0x8015),  # circuitplayground m0 PID prototype
    (0x239A, 0x801B),  # feather m0 express PID
])


class BaseMode(QObject):
    """
    Represents the common aspects of a mode.
    """

    name = 'UNNAMED MODE'
    description = 'DESCRIPTION NOT AVAILABLE.'
    icon = 'help'
    repl = None
    is_debugger = False
    has_debugger = False
    save_timeout = 5  #: Number of seconds to wait before saving work.

    def __init__(self, editor, view):
        self.editor = editor
        self.view = view
        super().__init__()

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
        sp = get_settings_path()
        workspace_dir = os.path.join(HOME_DIRECTORY, WORKSPACE_NAME)
        settings = {}
        try:
            with open(sp) as f:
                settings = json.load(f)
        except FileNotFoundError:
            logger.error('Settings file {} does not exist.'.format(sp))
        except ValueError:
            logger.error('Settings file {} could not be parsed.'.format(sp))
        else:
            if 'workspace' in settings:
                if os.path.isdir(settings['workspace']):
                    workspace_dir = settings['workspace']
                else:
                    logger.error(
                        'Workspace value in the settings file is not a valid'
                        'directory: {}'.format(settings['workspace']))
        return workspace_dir

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return NotImplemented


class MicroPythonMode(BaseMode):
    """
    Includes functionality that works with a USB serial based REPL.
    """
    valid_boards = BOARD_IDS

    def find_device(self, with_logging=True):
        """
        Returns the port for the first MicroPython-ish device found connected
        to the host computer. If no device is found, returns None.
        """
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            pid = port.productIdentifier()
            vid = port.vendorIdentifier()
            # Look for the port VID & PID in the list of know board IDs
            if (vid, pid) in self.valid_boards:
                port_name = port.portName()
                logger.info('Found device on port: {}'.format(port_name))
                return port_name
        if with_logging:
            logger.warning('Could not find device.')
            logger.debug('Available ports:')
            logger.debug(['PID:{} VID:{} PORT:{}'.format(p.productIdentifier(),
                                                         p.vendorIdentifier(),
                                                         p.portName())
                         for p in available_ports])
        return None

    def toggle_repl(self, event):
        """
        Toggles the REPL on and off.
        """
        if self.repl is None:
            self.add_repl()
            logger.info('Toggle REPL on.')
        else:
            self.remove_repl()
            logger.info('Toggle REPL off.')

    def remove_repl(self):
        """
        If there's an active REPL, disconnect and hide it.
        """
        if self.repl is None:
            raise RuntimeError('REPL not running.')
        self.view.remove_repl()
        self.repl = None

    def add_repl(self):
        """
        Detect a connected MicroPython based device and, if found, connect to
        the REPL and display it to the user.
        """
        if self.repl is not None:
            raise RuntimeError('REPL already running')
        device_port = self.find_device()
        if device_port:
            try:
                self.repl = REPL(port=device_port)
                self.view.add_micropython_repl(self.repl, self.name)
                logger.info('Started REPL on port: {}'.format(device_port))
            except IOError as ex:
                logger.error(ex)
                self.repl = None
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


class REPL:
    """
    A USB serial Read, Evaluate, Print, Loop.

    Represents the REPL. Since the logic for the REPL is simply a USB/serial
    based widget this class only contains a reference to the associated port.
    """

    def __init__(self, port):
        if os.name == 'posix':
            # If we're on Linux or OSX reference the port is like this...
            self.port = "/dev/{}".format(port)
        elif os.name == 'nt':
            # On Windows simply return the port (e.g. COM0).
            self.port = port
        else:
            # No idea how to deal with other OS's so fail.
            raise NotImplementedError('OS "{}" not supported.'.format(os.name))
        logger.info('Created new REPL object with port: {}'.format(self.port))
