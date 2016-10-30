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
import io
import re
import json
import logging
import tempfile
import platform
import webbrowser
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSerialPort import QSerialPortInfo
from pyflakes.api import check
# Currently there is no pycodestyle deb packages, so fallback to old name
try:  # pragma: no cover
    from pycodestyle import StyleGuide, Checker
except ImportError:  # pragma: no cover
    from pep8 import StyleGuide, Checker
from mu.contrib import uflash, appdirs, microfs
from mu import __version__


#: USB product ID.
MICROBIT_PID = 516
#: USB vendor ID.
MICROBIT_VID = 3368
#: The user's home directory.
HOME_DIRECTORY = os.path.expanduser('~')
#: The default directory for application data (i.e., configuration).
DATA_DIR = appdirs.user_data_dir(appname='mu', appauthor='python')
#: The default directory for application logs.
LOG_DIR = appdirs.user_log_dir(appname='mu', appauthor='python')
#: The path to the log file for the application.
LOG_FILE = os.path.join(LOG_DIR, 'mu.log')
#: Regex to match pycodestyle (PEP8) output.
STYLE_REGEX = re.compile(r'.*:(\d+):(\d+):\s+(.*)')
#: Regex to match flake8 output.
FLAKE_REGEX = re.compile(r'.*:(\d+):\s+(.*)')
#: Regex to match false positive flake errors if microbit.* is expanded.
EXPAND_FALSE_POSITIVE = re.compile(r"^'microbit\.(\w+)' imported but unused$")
#: The text to which "from microbit import *" should be expanded.
EXPANDED_IMPORT = ("from microbit import pin15, pin2, pin0, pin1, "
                   " pin3, pin6, pin4, i2c, pin5, pin7, pin8, Image, "
                   "pin9, pin14, pin16, reset, pin19, temperature, "
                   "sleep, pin20, button_a, button_b, running_time, "
                   "accelerometer, display, uart, spi, panic, pin13, "
                   "pin12, pin11, pin10, compass")


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


def get_settings_path():
    """
    The settings file default location is the application data directory.
    However, a settings file in  the same directory than the application itself
    takes preference.
    """
    settings_filename = 'settings.json'
    # App location depends on being interpreted by normal Python or bundled
    app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
    app_dir = os.path.dirname(os.path.abspath(app_path))
    # The os x bundled application is placed 3 levels deep in the .app folder
    if platform.system() == 'Darwin' and getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(app_dir)))
    logger.info('Application directory: {}'.format(app_dir))
    settings_dir = os.path.join(app_dir, settings_filename)
    if not os.path.exists(settings_dir):
        settings_dir = os.path.join(DATA_DIR, settings_filename)
        if not os.path.exists(settings_dir):
            with open(settings_dir, 'w') as f:
                logger.debug('Creating settings file: {}'.format(settings_dir))
                json.dump({}, f)
    return settings_dir


def get_python_dir():
    settings_path = get_settings_path()
    with open(settings_path) as f:
        try:
            sets = json.load(f)
            if 'python_dir' in sets:
                return sets['python_dir']
            else:
                return os.path.join(HOME_DIRECTORY, 'mu_code')
        except ValueError:
            logger.error('Settings file {} could not be parsed.'.format(
                             settings_path))
            return os.path.join(HOME_DIRECTORY, 'mu_code')


def check_flake(filename, code):
    """
    Given a filename and some code to be checked, uses the PyFlakesmodule to
    return a dictionary describing issues of code quality per line. See:

    https://github.com/PyCQA/pyflakes
    """
    import_all = "from microbit import *" in code
    if import_all:
        # Massage code so "from microbit import *" is expanded so the symbols
        # are known to flake.
        code = code.replace("from microbit import *", EXPANDED_IMPORT)
    reporter = MuFlakeCodeReporter()
    check(code, filename, reporter)
    feedback = {}
    for log in reporter.log:
        if import_all:
            # Guard to stop unwanted "microbit.* imported but unused" messages.
            message = log['message']
            if EXPAND_FALSE_POSITIVE.match(message):
                continue
        if log['line_no'] not in feedback:
            feedback[log['line_no']] = []
        feedback[log['line_no']].append(log)
    return feedback


def check_pycodestyle(code):
    """
    Given some code, uses the PyCodeStyle module (was PEP8) to return a list
    of items describing issues of coding style. See:

    https://pycodestyle.readthedocs.io/en/latest/intro.html
    """
    # PyCodeStyle reads input from files, so make a temporary file containing
    # the code.
    code_fd, code_filename = tempfile.mkstemp()
    os.close(code_fd)
    with open(code_filename, 'w', newline='') as code_file:
        code_file.write(code)
    # Configure which PEP8 rules to ignore.
    style = StyleGuide(parse_argv=False, config_file=False)
    checker = Checker(code_filename, options=style.options)
    # Re-route stdout to a temporary buffer to be parsed below.
    temp_out = io.StringIO()
    sys.stdout = temp_out
    # Check the code.
    checker.check_all()
    # Put stdout back and read the content of the buffer. Remove the temporary
    # file created at the start.
    sys.stdout = sys.__stdout__
    temp_out.seek(0)
    results = temp_out.read()
    temp_out.close()
    code_file.close()
    os.remove(code_filename)
    # Parse the output from the tool into a dictionary of structured data.
    style_feedback = {}
    for result in results.split('\n'):
        matcher = STYLE_REGEX.match(result)
        if matcher:
            line_no, col, msg = matcher.groups()
            line_no = int(line_no) - 1
            code, description = msg.split(' ', 1)
            if code == 'E303':
                description += ' above this line'
            if line_no not in style_feedback:
                style_feedback[line_no] = []
            style_feedback[line_no].append({
                'line_no': line_no,
                'column': int(col) - 1,
                'message': description.capitalize(),
                'code': code,
            })
    return style_feedback


class MuFlakeCodeReporter:
    """
    The class instantiates a reporter that creates structured data about
    code quality for Mu. Used by the PyFlakes module.
    """

    def __init__(self):
        """
        Set up the reporter object to be used to report PyFlake's results.
        """
        self.log = []

    def unexpectedError(self, filename, message):
        """
        Called if an unexpected error occured while trying to process the file
        called filename. The message parameter contains a description of the
        problem.
        """
        self.log.append({
            'line_no': 0,
            'filename': filename,
            'message': str(message)
        })

    def syntaxError(self, filename, message, line_no, column, source):
        """
        Records a syntax error in the file called filename.

        The message argument contains an explanation of the syntax error,
        line_no indicates the line where the syntax error occurred, column
        indicates the column on which the error occurred and source is the
        source code containing the syntax error.
        """
        msg = ('Syntax error. Python cannot understand this line. Check for '
               'missing characters!')
        self.log.append({
            'message': msg,
            'line_no': int(line_no) - 1,  # Zero based counting in Mu.
            'column': column - 1,
            'source': source
        })

    def flake(self, message):
        """
        PyFlakes found something wrong with the code.
        """
        matcher = FLAKE_REGEX.match(str(message))
        if matcher:
            line_no, msg = matcher.groups()
            self.log.append({
                'line_no': int(line_no) - 1,  # Zero based counting in Mu.
                'column': 0,
                'message': msg,
            })
        else:
            self.log.append({
                'line_no': 0,
                'column': 0,
                'message': str(message),
            })


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
        self.fs = None
        self.theme = 'day'
        self.user_defined_microbit_path = None
        if not os.path.exists(get_python_dir()):
            logger.debug('Creating directory: {}'.format(get_python_dir()))
            os.makedirs(get_python_dir())
        if not os.path.exists(DATA_DIR):
            logger.debug('Creating directory: {}'.format(DATA_DIR))
            os.makedirs(DATA_DIR)

    def restore_session(self):
        """
        Attempts to recreate the tab state from the last time the editor was
        run.
        """
        settings_path = get_settings_path()
        with open(settings_path) as f:
            try:
                old_session = json.load(f)
            except ValueError:
                logger.error('Settings file {} could not be parsed.'.format(
                             settings_path))
            else:
                logger.info('Restoring session from: {}'.format(settings_path))
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
            py = 'from microbit import *{}{}# Write your code here :-)'.format(
                os.linesep, os.linesep)
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
        if len(python_script) >= 8192:
            message = 'Unable to flash "{}"'.format(tab.label)
            information = ("Your script is too long!")
            self._view.show_message(message, information, 'Warning')
            return
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

    def add_fs(self):
        """
        If the REPL is not active, add the file system navigator to the UI.
        """
        if self.repl is None:
            if self.fs is None:
                try:
                    microfs.get_serial()
                    self._view.add_filesystem(home=get_python_dir())
                    self.fs = True
                except IOError:
                    message = 'Could not find an attached BBC micro:bit.'
                    information = ("Please make sure the device is plugged "
                                   "into this computer.\n\nThe device must "
                                   "have MicroPython flashed onto it before "
                                   "the file system will work.\n\n"
                                   "Finally, press the device's reset button "
                                   "and wait a few seconds before trying "
                                   "again.")
                    self._view.show_message(message, information)

    def remove_fs(self):
        """
        If the REPL is not active, remove the file system navigator from
        the UI.
        """
        if self.fs is None:
            raise RuntimeError("File system not running")
        self._view.remove_filesystem()
        self.fs = None

    def toggle_fs(self):
        """
        If the file system navigator is active enable it. Otherwise hide it.
        If the REPL is active, display a message.
        """
        if self.repl is None:
            if self.fs is None:
                self.add_fs()
            else:
                self.remove_fs()
        else:
            message = "File system and REPL cannot work at the same time."
            information = ("The file system and REPL both use the same USB "
                           "serial connection. Only one can be active "
                           "at any time. Toggle the REPL off and try again.")
            self._view.show_message(message, information)

    def add_repl(self):
        """
        Detect a connected BBC micro:bit and if found, connect to the
        MicroPython REPL and display it to the user.
        """
        if self.fs:
            raise RuntimeError("File system already connected")
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
        if self.fs is None:
            if self.repl is None:
                self.add_repl()
            else:
                self.remove_repl()
        else:
            message = "REPL and file system cannot work at the same time."
            information = ("The REPL and file system both use the same USB "
                           "serial connection. Only one can be active "
                           "at any time. Toggle the file system off and "
                           "try again.")
            self._view.show_message(message, information)

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
        path = self._view.get_load_path(get_python_dir())
        logger.info('Loading script from: {}'.format(path))
        try:
            if path.endswith('.py'):
                # Open the file, read the textual content and set the name as
                # the path to the file.
                with open(path, newline='') as f:
                    text = f.read()
                name = path
            else:
                # Open the hex, extract the Python script therein and set the
                # name to None, thus forcing the user to work out what to name
                # the recovered script.
                with open(path, newline='') as f:
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
            tab.path = self._view.get_save_path(get_python_dir())
        if tab.path:
            # The user specified a path to a file.
            if not os.path.basename(tab.path).endswith('.py'):
                # No extension given, default to .py
                tab.path += '.py'
            with open(tab.path, 'w', newline='') as f:
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

    def check_code(self):
        """
        Uses PyFlakes and PyCodeStyle to gather information about potential
        problems with the code in the current tab.
        """
        self._view.reset_annotations()
        tab = self._view.current_tab
        if tab is None:
            # There is no active text editor so abort.
            return
        filename = tab.path if tab.path else 'untitled'
        flake = check_flake(filename, tab.text())
        if flake:
            logger.info(flake)
            self._view.annotate_code(flake, 'error')
        pep8 = check_pycodestyle(tab.text())
        if pep8:
            logger.info(pep8)
            self._view.annotate_code(pep8, 'style')

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
            'paths': paths,
            'python_dir': get_python_dir()
        }
        logger.debug(session)
        settings_path = get_settings_path()
        with open(settings_path, 'w') as out:
            logger.debug('Saving session to: {}'.format(settings_path))
            json.dump(session, out, indent=2)
        sys.exit(0)
