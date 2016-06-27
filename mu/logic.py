"""
Copyright (c) 2015-2016 Nicholas H.Tollervey and others (see the AUTHORS file).

Based upon work done for Puppy IDE by Dan Pope, Nicholas Tollervey and Damien
George.

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
import os.path
import sys
import json
import logging
import webbrowser
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSerialPort import QSerialPortInfo
from mu.contrib import uflash, appdirs
from mu import __version__


#: USB product ID.
MICROBIT_PID = 516
#: USB vendor ID.
MICROBIT_VID = 3368
#: The user's home directory.
HOME_DIRECTORY = os.path.expanduser('~')
#: The default directory for Python scripts.
PYTHON_DIRECTORY = os.path.join(HOME_DIRECTORY, 'python')
#: The default directory for application data.
DATA_DIR = appdirs.user_data_dir('mu', 'python')
#: The default directory for application logs.
LOG_DIR = appdirs.user_log_dir('mu', 'python')
#: The path to the JSON file containing application settings.
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')
#: The path to the log file for the application.
LOG_FILE = os.path.join(LOG_DIR, 'mu.log')


logger = logging.getLogger(__name__)


def find_microbit():
    """
    Returns the port for the first microbit it finds connected to the host
    computer. If no microbit is found, returns None.
    """
    available_ports = QSerialPortInfo.availablePorts()
    for port in available_ports:
        pid = port.productIdentifier()
        vid = port.vendorIdentifier()
        if pid == MICROBIT_PID and vid == MICROBIT_VID:
            port_name = port.portName()
            logger.info('Found micro:bit with portName: {}'.format(port_name))
            return port_name
    logger.warning('Could not find micro:bit.')
    logger.debug('Available ports:')
    logger.debug(['PID:{} VID:{} PORT:{}'.format(p.productIdentifier(),
                                                 p.vendorIdentifier(),
                                                 p.portName())
                 for p in available_ports])
    return None


class REPL:
    """
    Read, Evaluate, Print, Loop.

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
            raise NotImplementedError('OS not supported.')
        logger.info('Created new REPL object with port: {}'.format(self.port))


class Editor:
    """
    Application logic for the editor itself.
    """

    def __init__(self, view):
        logger.info('Setting up editor.')
        self._view = view
        self.repl = None
        self.theme = 'day'
        self.user_defined_microbit_path = None
        if not os.path.exists(PYTHON_DIRECTORY):
            logger.debug('Creating directory: {}'.format(PYTHON_DIRECTORY))
            os.makedirs(PYTHON_DIRECTORY)
        if not os.path.exists(DATA_DIR):
            logger.debug('Creating directory: {}'.format(DATA_DIR))
            os.makedirs(DATA_DIR)

    def restore_session(self):
        """
        Attempts to recreate the tab state from the last time the editor was
        run.
        """
        if os.path.exists(SETTINGS_FILE):
            logger.info('Restoring session from: {}'.format(SETTINGS_FILE))
            with open(SETTINGS_FILE) as f:
                old_session = json.load(f)
                logger.debug(old_session)
                if 'theme' in old_session:
                    self.theme = old_session['theme']
                if 'paths' in old_session:
                    for path in old_session['paths']:
                        try:
                            with open(path) as f:
                                text = f.read()
                        except FileNotFoundError:
                            pass
                        else:
                            self._view.add_tab(path, text)
        if not self._view.tab_count:
            py = 'from microbit import *\n\n# Write your code here :-)'
            self._view.add_tab(None, py)
        self._view.set_theme(self.theme)

    def flash(self):
        """
        Takes the currently active tab, compiles the Python script therein into
        a hex file and flashes it all onto the connected device.
        """
        logger.info('Flashing script')
        # Grab the Python script.
        tab = self._view.current_tab
        if tab is None:
            # There is no active text editor.
            return
        python_script = tab.text().encode('utf-8')
        logger.debug('Python script:')
        logger.debug(python_script)
        # Generate a hex file.
        python_hex = uflash.hexlify(python_script)
        logger.debug('Python hex:')
        logger.debug(python_hex)
        micropython_hex = uflash.embed_hex(uflash._RUNTIME, python_hex)
        # Determine the location of the BBC micro:bit. If it can't be found
        # fall back to asking the user to locate it.
        path_to_microbit = uflash.find_microbit()
        if path_to_microbit is None:
            # Has the path to the device already been specified?
            if self.user_defined_microbit_path:
                path_to_microbit = self.user_defined_microbit_path
            else:
                # Ask the user to locate the device.
                path_to_microbit = self._view.get_microbit_path(HOME_DIRECTORY)
                # Store the user's specification of the path for future use.
                self.user_defined_microbit_path = path_to_microbit
                logger.debug('User defined path to micro:bit: {}'.format(
                             self.user_defined_microbit_path))
        # Check the path and that it exists simply because the path maybe based
        # on stale data.
        logger.debug('Path to micro:bit: {}'.format(path_to_microbit))
        if path_to_microbit and os.path.exists(path_to_microbit):
            logger.debug('Flashing to device.')
            hex_file = os.path.join(path_to_microbit, 'micropython.hex')
            uflash.save_hex(micropython_hex, hex_file)
            message = 'Flashing "{}" onto the micro:bit.'.format(tab.label)
            information = ("When the yellow LED stops flashing the device"
                           " will restart and your script will run. If there"
                           " is an error, you'll see a helpful message scroll"
                           " across the device's display.")
            self._view.show_message(message, information, 'Information')
        else:
            # Reset user defined path since it's incorrect.
            self.user_defined_microbit_path = None
            # Try to be helpful... essentially there is nothing Mu can do but
            # prompt for patience while the device is mounted and/or do the
            # classic "have you tried switching it off and on again?" trick.
            # This one's for James at the Raspberry Pi Foundation. ;-)
            message = 'Could not find an attached BBC micro:bit.'
            information = ("Please ensure you leave enough time for the BBC"
                           " micro:bit to be attached and configured correctly"
                           " by your computer. This may take several seconds."
                           " Alternatively, try removing and re-attaching the"
                           " device or saving your work and restarting Mu if"
                           " the device remains unfound.")
            self._view.show_message(message, information)

    def add_repl(self):
        """
        Detect a connected BBC micro:bit and if found, connect to the
        MicroPython REPL and display it to the user.
        """
        logger.info('Starting REPL in UI.')
        if self.repl is not None:
            raise RuntimeError("REPL already running")
        mb_port = find_microbit()
        if mb_port:
            try:
                self.repl = REPL(port=mb_port)
                self._view.add_repl(self.repl)
                logger.info('REPL on port: {}'.format(mb_port))
            except IOError as ex:
                logger.error(ex)
                self.repl = None
                information = ("Click the device's reset button, wait a few"
                               " seconds and then try again.")
                self._view.show_message(str(ex), information)
            except Exception as ex:
                logger.error(ex)
        else:
            message = 'Could not find an attached BBC micro:bit.'
            information = ("Please make sure the device is plugged into this"
                           " computer.\n\nThe device must have MicroPython"
                           " flashed onto it before the REPL will work.\n\n"
                           "Finally, press the device's reset button and wait"
                           " a few seconds before trying again.")
            self._view.show_message(message, information)

    def remove_repl(self):
        """
        If there's an active REPL, disconnect and hide it.
        """
        if self.repl is None:
            raise RuntimeError("REPL not running")
        self._view.remove_repl()
        self.repl = None

    def toggle_repl(self):
        """
        If the REPL is active, close it; otherwise open the REPL.
        """
        if self.repl is None:
            self.add_repl()
        else:
            self.remove_repl()

    def toggle_theme(self):
        """
        Switches between themes (night or day).
        """
        if self.theme == 'day':
            self.theme = 'night'
        else:
            self.theme = 'day'
        logger.info('Toggle theme to: {}'.format(self.theme))
        self._view.set_theme(self.theme)

    def new(self):
        """
        Adds a new tab to the editor.
        """
        self._view.add_tab(None, '')

    def load(self):
        """
        Loads a Python file from the file system or extracts a Python sccript
        from a hex file.
        """
        path = self._view.get_load_path(PYTHON_DIRECTORY)
        logger.info('Loading script from: {}'.format(path))
        try:
            if path.endswith('.py'):
                # Open the file, read the textual content and set the name as
                # the path to the file.
                with open(path) as f:
                    text = f.read()
                name = path
            else:
                # Open the hex, extract the Python script therein and set the
                # name to None, thus forcing the user to work out what to name
                # the recovered script.
                with open(path) as f:
                    text = uflash.extract_script(f.read())
                name = None
        except FileNotFoundError:
            pass
        else:
            logger.debug(text)
            self._view.add_tab(name, text)

    def save(self):
        """
        Save the content of the currently active editor tab.
        """
        tab = self._view.current_tab
        if tab is None:
            # There is no active text editor so abort.
            return
        if tab.path is None:
            # Unsaved file.
            tab.path = self._view.get_save_path(PYTHON_DIRECTORY)
        if tab.path:
            # The user specified a path to a file.
            if not os.path.basename(tab.path).endswith('.py'):
                # No extension given, default to .py
                tab.path += '.py'
            with open(tab.path, 'w') as f:
                logger.info('Saving script to: {}'.format(tab.path))
                logger.debug(tab.text())
                f.write(tab.text())
            tab.setModified(False)
        else:
            # The user cancelled the filename selection.
            tab.path = None

    def zoom_in(self):
        """
        Make the editor's text bigger
        """
        self._view.zoom_in()

    def zoom_out(self):
        """
        Make the editor's text smaller.
        """
        self._view.zoom_out()

    def show_help(self):
        """
        Display browser based help about Mu.
        """
        webbrowser.open_new('http://codewith.mu/help/{}'.format(__version__))

    def quit(self, *args, **kwargs):
        """
        Exit the application.
        """
        logger.info('Quitting')
        if self._view.modified:
            # Alert the user to handle unsaved work.
            msg = ('There is un-saved work, exiting the application will'
                   ' cause you to lose it.')
            result = self._view.show_confirmation(msg)
            if result == QMessageBox.Cancel:
                if args and hasattr(args[0], 'ignore'):
                    # The function is handling an event, so ignore it.
                    args[0].ignore()
                return
        paths = []
        for widget in self._view.widgets:
            if widget.path:
                paths.append(widget.path)
        session = {
            'theme': self.theme,
            'paths': paths
        }
        logger.debug(session)
        with open(SETTINGS_FILE, 'w') as out:
            logger.debug('Saving session to: {}'.format(SETTINGS_FILE))
            json.dump(session, out, indent=2)
        sys.exit(0)
