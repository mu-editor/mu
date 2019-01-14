"""
Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

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
import sys
import codecs
import io
import re
import json
import logging
import tempfile
import platform
import webbrowser
import random
import locale
import shutil
import appdirs
import site
from PyQt5.QtWidgets import QMessageBox
from pyflakes.api import check
from pycodestyle import StyleGuide, Checker
from . import localedetect
from mu.resources import path
from mu.debugger.utils import is_breakpoint_line
from mu import __version__


# The user's home directory.
HOME_DIRECTORY = os.path.expanduser('~')
# Name of the directory within the home folder to use by default
WORKSPACE_NAME = 'mu_code'
# The default directory for application data (i.e., configuration).
DATA_DIR = appdirs.user_data_dir(appname='mu', appauthor='python')
# The default directory for application logs.
LOG_DIR = appdirs.user_log_dir(appname='mu', appauthor='python')
# The path to the log file for the application.
LOG_FILE = os.path.join(LOG_DIR, 'mu.log')
# Regex to match pycodestyle (PEP8) output.
STYLE_REGEX = re.compile(r'.*:(\d+):(\d+):\s+(.*)')
# Regex to match flake8 output.
FLAKE_REGEX = re.compile(r'.*:(\d+):\s+(.*)')
# Regex to match false positive flake errors if microbit.* is expanded.
EXPAND_FALSE_POSITIVE = re.compile(r"^'microbit\.(\w+)' imported but unused$")
# The text to which "from microbit import \*" should be expanded.
EXPANDED_IMPORT = ("from microbit import pin15, pin2, pin0, pin1, "
                   " pin3, pin6, pin4, i2c, pin5, pin7, pin8, Image, "
                   "pin9, pin14, pin16, reset, pin19, temperature, "
                   "sleep, pin20, button_a, button_b, running_time, "
                   "accelerometer, display, uart, spi, panic, pin13, "
                   "pin12, pin11, pin10, compass")
# Port number for debugger.
DEBUGGER_PORT = 31415
MOTD = [  # Candidate phrases for the message of the day (MOTD).
    _('Hello, World!'),
    _("This editor is free software written in Python. You can modify it, "
      "add features or fix bugs if you like."),
    _("This editor is called Mu (you say it 'mew' or 'moo')."),
    _("Google, Facebook, NASA, Pixar, Disney and many more use Python."),
    _("Programming is a form of magic. Learn to cast the right spells with "
      "code and you'll be a wizard."),
    _("REPL stands for read, evaluate, print, loop. It's a fun way to talk to "
      "your computer! :-)"),
    _('Be brave, break things, learn and have fun!'),
    _("Make your software both useful AND fun. Empower your users."),
    _('For the Zen of Python: import this'),
    _('Diversity promotes creativity.'),
    _("An open mind, spirit of adventure and respect for diversity are key."),
    _("Don't worry if it doesn't work. Learn the lesson, fix it and try "
      "again! :-)"),
    _("Coding is collaboration."),
    _("Compliment and amplify the good things with code."),
    _("In theory, theory and practice are the same. In practice, they're "
      "not. ;-)"),
    _("Debugging is twice as hard as writing the code in the first place."),
    _("It's fun to program."),
    _("Programming has more to do with problem solving than writing code."),
    _("Start with your users' needs."),
    _("Try to see things from your users' point of view."),
    _("Put yourself in your users' shoes."),
    _("Explaining a programming problem to a friend often reveals the "
      "solution. :-)"),
    _("If you don't know, ask. Nobody to ask? Just look it up."),
    _("Complexity is the enemy. KISS - keep it simple, stupid!"),
    _("Beautiful is better than ugly."),
    _("Explicit is better than implicit."),
    _("Simple is better than complex. Complex is better than complicated."),
    _("Flat is better than nested."),
    _("Sparse is better than dense."),
    _("Readability counts."),
    _("Special cases aren't special enough to break the rules. "
      "Although practicality beats purity."),
    _("Errors should never pass silently. Unless explicitly silenced."),
    _("In the face of ambiguity, refuse the temptation to guess."),
    _("There should be one-- and preferably only one --obvious way to do it."),
    _("Now is better than never. Although never is often better than "
      "*right* now."),
    _("If the implementation is hard to explain, it's a bad idea."),
    _("If the implementation is easy to explain, it may be a good idea."),
    _("Namespaces are one honking great idea -- let's do more of those!"),
    _("Mu was created by Nicholas H.Tollervey."),
    _("To understand what recursion is, you must first understand recursion."),
    _("Algorithm: a word used by programmers when they don't want to explain "
      "what they did."),
    _("Programmers count from zero."),
    _("Simplicity is the ultimate sophistication."),
    _("A good programmer is humble."),
    _("A good programmer is playful."),
    _("A good programmer learns to learn."),
    _("A good programmer thinks beyond the obvious."),
    _("A good programmer promotes simplicity."),
    _("A good programmer avoids complexity."),
    _("A good programmer is patient."),
    _("A good programmer asks questions."),
    _("A good programmer is willing to say, 'I don't know'."),
    _("Wisest are they that know they know nothing."),
]

NEWLINE = "\n"

#
# We write all files as UTF-8 unless they arrived with a PEP 263 encoding
# cookie, in which case we honour that encoding.
#
ENCODING = "utf-8"
ENCODING_COOKIE_RE = re.compile(
    "^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")

logger = logging.getLogger(__name__)


def write_and_flush(fileobj, content):
    """
    Write content to the fileobj then flush and fsync to ensure the data is,
    in fact, written.

    This is especially necessary for USB-attached devices
    """
    fileobj.write(content)
    fileobj.flush()
    #
    # Theoretically this shouldn't work; fsync takes a file descriptor,
    # not a file object. However, there's obviously some under-the-cover
    # mechanism which converts one to the other (at least on Windows)
    #
    os.fsync(fileobj)


def save_and_encode(text, filepath, newline=os.linesep):
    """
    Detect the presence of an encoding cookie and use that encoding; if
    none is present, do not add one and use the Mu default encoding.
    If the codec is invalid, log a warning and fall back to the default.
    """
    match = ENCODING_COOKIE_RE.match(text)
    if match:
        encoding = match.group(1)
        try:
            codecs.lookup(encoding)
        except LookupError:
            logger.warning("Invalid codec in encoding cookie: %s", encoding)
            encoding = ENCODING
    else:
        encoding = ENCODING

    with open(filepath, "w", encoding=encoding, newline='') as f:
        text_to_write = newline.join(l.rstrip(" ") for l in text.splitlines())
        write_and_flush(f, text_to_write)


def sniff_encoding(filepath):
    """Determine the encoding of a file:

    * If there is a BOM, return the appropriate encoding
    * If there is a PEP 263 encoding cookie, return the appropriate encoding
    * Otherwise return None for read_and_decode to attempt several defaults
    """
    boms = [
        (codecs.BOM_UTF8, "utf-8-sig"),
        (codecs.BOM_UTF16_BE, "utf-16"),
        (codecs.BOM_UTF16_LE, "utf-16"),
    ]
    #
    # Try for a BOM
    #
    with open(filepath, "rb") as f:
        line = f.readline()
    for bom, encoding in boms:
        if line.startswith(bom):
            return encoding

    #
    # Look for a PEP 263 encoding cookie
    #
    default_encoding = locale.getpreferredencoding()
    try:
        uline = line.decode(default_encoding)
    except UnicodeDecodeError:
        #
        # Can't even decode the line in order to match the cookie
        #
        pass
    else:
        match = ENCODING_COOKIE_RE.match(uline)
        if match:
            return match.group(1)

    #
    # Fall back to the locale default
    #
    return None


def sniff_newline_convention(text):
    """Determine which line-ending convention predominates in the text.

    Windows usually has U+000D U+000A
    Posix usually has U+000A
    But editors can produce either convention from either platform. And
    a file which has been copied and edited around might even have both!
    """
    candidates = [
        ("\r\n", "\r\n"),
        # Match \n at the start of the string
        # or \n preceded by any character other than \r
        ("\n", "^\n|[^\r]\n")
    ]
    #
    # If no lines are present, default to the platform newline
    # If there's a tie, use the platform default
    #
    conventions_found = [(0, 1, os.linesep)]
    for candidate, pattern in candidates:
        instances = re.findall(pattern, text)
        convention = (len(instances), candidate == os.linesep, candidate)
        conventions_found.append(convention)
    majority_convention = max(conventions_found)
    return majority_convention[-1]


def read_and_decode(filepath):
    """
    Read the contents of a file,
    """
    sniffed_encoding = sniff_encoding(filepath)
    #
    # If sniff_encoding has found enough clues to indicate an encoding,
    # use that. Otherwise try a series of defaults before giving up.
    #
    if sniffed_encoding:
        logger.debug("Detected encoding %s", sniffed_encoding)
        candidate_encodings = [sniffed_encoding]
    else:
        candidate_encodings = [ENCODING, locale.getpreferredencoding()]

    with open(filepath, "rb") as f:
        btext = f.read()
    for encoding in candidate_encodings:
        logger.debug("Trying to decode with %s", encoding)
        try:
            text = btext.decode(encoding)
            logger.info("Decoded with %s", encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise UnicodeDecodeError(encoding, btext, 0, 0, "Unable to decode")

    #
    # Sniff and convert newlines here so that, by the time
    # the text reaches the editor it is ready to use. Then
    # convert everything to the Mu internal newline character
    #
    newline = sniff_newline_convention(text)
    logger.debug("Detected newline %r", newline)
    text = re.sub("\r\n", NEWLINE, text)
    return text, newline


def get_admin_file_path(filename):
    """
    Given an admin related filename, this function will attempt to get the
    most relevant version of this file (the default location is the application
    data directory, although a file of the same name in the same directory as
    the application itself takes preference). If this file isn't found, an
    empty one is created in the default location.
    """
    # App location depends on being interpreted by normal Python or bundled
    app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
    app_dir = os.path.dirname(os.path.abspath(app_path))
    # The os x bundled application is placed 3 levels deep in the .app folder
    if platform.system() == 'Darwin' and getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(app_dir)))
    file_path = os.path.join(app_dir, filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as f:
                    logger.debug('Creating admin file: {}'.format(
                                 file_path))
                    json.dump({}, f)
            except FileNotFoundError:
                logger.error('Unable to create admin file: {}'.format(
                             file_path))
    return file_path


def get_session_path():
    """
    The session file stores details about the state of Mu from the user's
    perspective (tabs open, current mode etc...).

    The session file default location is the application data directory.
    However, a session file in the same directory as the application itself
    takes preference.

    If no session file is detected a blank one in the default location is
    automatically created.
    """
    return get_admin_file_path('session.json')


def get_settings_path():
    """
    The settings file stores details about the configuration of Mu from an
    administrators' perspective (default workspace etc...).

    The settings file default location is the application data directory.
    However, a settings file in the same directory as the application itself
    takes preference.

    If no settings file is detected a blank one in the default location is
    automatically created.
    """
    return get_admin_file_path('settings.json')


def extract_envars(raw):
    """
    Returns a list of environment variables given a string containing
    NAME=VALUE definitions on separate lines.
    """
    result = []
    for line in raw.split('\n'):
        definition = line.split('=', 1)
        if len(definition) == 2:
            result.append([definition[0].strip(), definition[1].strip()])
    return result


def check_flake(filename, code, builtins=None):
    """
    Given a filename and some code to be checked, uses the PyFlakesmodule to
    return a dictionary describing issues of code quality per line. See:

    https://github.com/PyCQA/pyflakes

    If a list symbols is passed in as "builtins" these are assumed to be
    additional builtins available when run by Mu.
    """
    import_all = "from microbit import *" in code
    if import_all:
        # Massage code so "from microbit import *" is expanded so the symbols
        # are known to flake.
        code = code.replace("from microbit import *", EXPANDED_IMPORT)
    reporter = MuFlakeCodeReporter()
    check(code, filename, reporter)
    if builtins:
        builtins_regex = re.compile(r"^undefined name '(" +
                                    '|'.join(builtins) + r")'")
    feedback = {}
    for log in reporter.log:
        if import_all:
            # Guard to stop unwanted "microbit.* imported but unused" messages.
            message = log['message']
            if EXPAND_FALSE_POSITIVE.match(message):
                continue
        if builtins:
            if builtins_regex.match(log['message']):
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
    save_and_encode(code, code_filename)
    # Configure which PEP8 rules to ignore.
    ignore = ('E121', 'E123', 'E126', 'E226', 'E302', 'E305', 'E24', 'E704',
              'W291', 'W292', 'W293', 'W391', 'W503', )
    style = StyleGuide(parse_argv=False, config_file=False)
    style.options.ignore = ignore
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
                description += _(' above this line')
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
        msg = _('Syntax error. Python cannot understand this line. Check for '
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

    def __init__(self, view, status_bar=None):
        logger.info('Setting up editor.')
        self._view = view
        self._status_bar = status_bar
        self.fs = None
        self.theme = 'day'
        self.mode = 'python'
        self.modes = {}  # See set_modes.
        self.envars = []  # See restore session and show_admin
        self.minify = False
        self.microbit_runtime = ''
        self.connected_devices = set()
        self.find = ''
        self.replace = ''
        self.current_path = ''  # Directory of last loaded file.
        self.global_replace = False
        self.selecting_mode = False  # Flag to stop auto-detection of modes.
        if not os.path.exists(DATA_DIR):
            logger.debug('Creating directory: {}'.format(DATA_DIR))
            os.makedirs(DATA_DIR)
        logger.info('Settings path: {}'.format(get_settings_path()))
        logger.info('Session path: {}'.format(get_session_path()))
        logger.info('Log directory: {}'.format(LOG_DIR))
        logger.info('Data directory: {}'.format(DATA_DIR))

        @view.open_file.connect
        def on_open_file(file):
            # Open the file
            self.direct_load(file)

    def setup(self, modes):
        """
        Define the available modes and ensure there's a default working
        directory.
        """
        self.modes = modes
        logger.info('Available modes: {}'.format(', '.join(self.modes.keys())))
        # Ensure there is a workspace directory.
        wd = self.modes['python'].workspace_dir()
        if not os.path.exists(wd):
            logger.debug('Creating directory: {}'.format(wd))
            os.makedirs(wd)
        # Ensure PyGameZero assets are copied over.
        images_path = os.path.join(wd, 'images')
        fonts_path = os.path.join(wd, 'fonts')
        sounds_path = os.path.join(wd, 'sounds')
        music_path = os.path.join(wd, 'music')
        if not os.path.exists(images_path):
            logger.debug('Creating directory: {}'.format(images_path))
            os.makedirs(images_path)
            shutil.copy(path('alien.png', 'pygamezero/'),
                        os.path.join(images_path, 'alien.png'))
            shutil.copy(path('alien_hurt.png', 'pygamezero/'),
                        os.path.join(images_path, 'alien_hurt.png'))
        if not os.path.exists(fonts_path):
            logger.debug('Creating directory: {}'.format(fonts_path))
            os.makedirs(fonts_path)
        if not os.path.exists(sounds_path):
            logger.debug('Creating directory: {}'.format(sounds_path))
            os.makedirs(sounds_path)
            shutil.copy(path('eep.wav', 'pygamezero/'),
                        os.path.join(sounds_path, 'eep.wav'))
        if not os.path.exists(music_path):
            logger.debug('Creating directory: {}'.format(music_path))
            os.makedirs(music_path)
        # Start the timer to poll every second for an attached or removed
        # USB device.
        self._view.set_usb_checker(1, self.check_usb)

    def restore_session(self, paths=None):
        """
        Attempts to recreate the tab state from the last time the editor was
        run. If paths contains a collection of additional paths specified by
        the user, they are also "restored" at the same time (duplicates will be
        ignored).
        """
        settings_path = get_session_path()
        self.change_mode(self.mode)
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
                if 'mode' in old_session:
                    old_mode = old_session['mode']
                    if old_mode in self.modes:
                        self.mode = old_session['mode']
                    else:
                        # Unknown mode (perhaps an old version?)
                        self.select_mode(None)
                else:
                    # So ask for the desired mode.
                    self.select_mode(None)
                if 'paths' in old_session:
                    old_paths = self._abspath(old_session['paths'])
                    launch_paths = self._abspath(paths) if paths else set()
                    for old_path in old_paths:
                        # if the os passed in a file, defer loading it now
                        if old_path in launch_paths:
                            continue
                        self.direct_load(old_path)
                    logger.info('Loaded files.')
                if 'envars' in old_session:
                    self.envars = old_session['envars']
                    logger.info('User defined environment variables: '
                                '{}'.format(self.envars))
                if 'minify' in old_session:
                    self.minify = old_session['minify']
                    logger.info('Minify scripts on micro:bit? '
                                '{}'.format(self.minify))
                if 'microbit_runtime' in old_session:
                    self.microbit_runtime = old_session['microbit_runtime']
                    if self.microbit_runtime:
                        logger.info('Custom micro:bit runtime path: '
                                    '{}'.format(self.microbit_runtime))
                        if not os.path.isfile(self.microbit_runtime):
                            self.microbit_runtime = ''
                            logger.warning('The specified micro:bit runtime '
                                           'does not exist. Using default '
                                           'runtime instead.')
                if 'zoom_level' in old_session:
                    self._view.zoom_position = old_session['zoom_level']
                    self._view.set_zoom()
        # handle os passed file last,
        # so it will not be focused over by another tab
        if paths and len(paths) > 0:
            self.load_cli(paths)
        if not self._view.tab_count:
            py = _('# Write your code here :-)') + NEWLINE
            tab = self._view.add_tab(None, py, self.modes[self.mode].api(),
                                     NEWLINE)
            tab.setCursorPosition(len(py.split(NEWLINE)), 0)
            logger.info('Starting with blank file.')
        self.change_mode(self.mode)
        self._view.set_theme(self.theme)
        self.show_status_message(random.choice(MOTD), 10)

    def toggle_theme(self):
        """
        Switches between themes (night, day or high-contrast).
        """
        if self.theme == 'day':
            self.theme = 'night'
        elif self.theme == 'night':
            self.theme = 'contrast'
        else:
            self.theme = 'day'
        logger.info('Toggle theme to: {}'.format(self.theme))
        self._view.set_theme(self.theme)

    def new(self):
        """
        Adds a new tab to the editor.
        """
        logger.info('Added a new tab.')
        self._view.add_tab(None, '', self.modes[self.mode].api(), NEWLINE)

    def _load(self, path):
        """
        Attempt to load a Python script from the passed in path. This path may
        be a .py file containing Python source code, or a .hex file, created
        for a micro:bit like device, with the source code embedded therein.

        This method will work its way around duplicate paths and also attempt
        to cleanly handle / report / log errors when encountered in a helpful
        manner.
        """
        logger.info('Loading script from: {}'.format(path))
        error = _("The file contains characters Mu expects to be encoded as "
                  "{0} or as the computer's default encoding {1}, but which "
                  "are encoded in some other way.\n\nIf this file was saved "
                  "in another application, re-save the file via the "
                  "'Save as' option and set the encoding to {0}")
        error = error.format(ENCODING, locale.getpreferredencoding())
        # Does the file even exist?
        if not os.path.isfile(path):
            logger.info('The file {} does not exist.'.format(path))
            return
        # see if file is open first
        for widget in self._view.widgets:
            if widget.path is None:  # this widget is an unsaved buffer
                continue
            if os.path.samefile(path, widget.path):
                logger.info('Script already open.')
                msg = _('The file "{}" is already open.')
                self._view.show_message(msg.format(os.path.basename(path)))
                self._view.focus_tab(widget)
                return
        name, text, newline, file_mode = None, None, None, None
        try:
            if path.lower().endswith('.py'):
                # Open the file, read the textual content and set the name as
                # the path to the file.
                try:
                    text, newline = read_and_decode(path)
                except UnicodeDecodeError:
                    message = _("Mu cannot read the characters in {}")
                    filename = os.path.basename(path)
                    self._view.show_message(message.format(filename), error)
                    return
                name = path
            else:
                # Delegate the open operation to the Mu modes. Leave the name
                # as None, thus forcing the user to work out what to name the
                # recovered script.
                for mode_name, mode in self.modes.items():
                    try:
                        text = mode.open_file(path)
                    except Exception as exc:
                        # No worries, log it and try the next mode
                        logger.warning('Error when mode {} try to open the '
                                       '{} file.'.format(mode_name, path),
                                       exc_info=exc)
                    else:
                        if text:
                            newline = sniff_newline_convention(text)
                            file_mode = mode_name
                            break
                else:
                    message = _('Mu was not able to open this file')
                    info = _('Currently Mu only works with Python source '
                             'files or hex files created with embedded '
                             'MicroPython code.')
                    self._view.show_message(message, info)
                    return
        except OSError:
            message = _("Could not load {}").format(path)
            logger.exception('Could not load {}'.format(path))
            info = _("Does this file exist?\nIf it does, do you have "
                     "permission to read it?\n\nPlease check and try again.")
            self._view.show_message(message, info)
        else:
            if file_mode and self.mode != file_mode:
                device_name = self.modes[file_mode].name
                message = _('Is this a {} file?').format(device_name)
                info = _('It looks like this could be a {} file.\n\n'
                         'Would you like to change Mu to the {}'
                         'mode?').format(device_name, device_name)
                if self._view.show_confirmation(
                        message, info, icon='Question') == QMessageBox.Ok:
                    self.change_mode(file_mode)
            logger.debug(text)
            self._view.add_tab(
                name, text, self.modes[self.mode].api(), newline)

    def get_dialog_directory(self):
        """
        Return the directory folder in which a load/save dialog box should
        open into. In order of precedence this function will return:

        1) The last location used by a load/save dialog.
        2) The directory containing the current file.
        3) The mode's reported workspace directory.
        """
        if self.current_path and os.path.isdir(self.current_path):
            folder = self.current_path
        else:
            current_file_path = ''
            workspace_path = self.modes[self.mode].workspace_dir()
            tab = self._view.current_tab
            if tab and tab.path:
                current_file_path = os.path.dirname(os.path.abspath(tab.path))
            folder = current_file_path if current_file_path else workspace_path
        logger.info('Using path for file dialog: {}'.format(folder))
        return folder

    def load(self):
        """
        Loads a Python file from the file system or extracts a Python script
        from a hex file.
        """
        # Get all supported extensions from the different modes
        extensions = ['py']
        for mode_name, mode in self.modes.items():
            if mode.file_extensions:
                extensions += mode.file_extensions
        extensions = set([e.lower() for e in extensions])
        extensions = '*.{} *.{}'.format(' *.'.join(extensions),
                                        ' *.'.join(extensions).upper())
        folder = self.get_dialog_directory()
        path = self._view.get_load_path(folder, extensions)
        if path:
            self.current_path = os.path.dirname(os.path.abspath(path))
            self._load(path)

    def direct_load(self, path):
        """ for loading files passed from command line or the OS launch"""
        self._load(path)

    def load_cli(self, paths):
        """
        Given a set of paths, passed in by the user when Mu starts, this
        method will attempt to load them and log / report a problem if Mu is
        unable to open a passed in path.
        """
        for p in paths:
            try:
                logger.info('Passed-in filename: {}'.format(p))
                # abspath will fail for non-paths
                self.direct_load(os.path.abspath(p))
            except Exception as e:
                logging.warning('Can\'t open file from command line {}'.
                                format(p), exc_info=e)

    def _abspath(self, paths):
        """
        Safely convert an arrary of paths to their absolute forms and remove
        duplicate items.
        """
        result = set()
        for p in paths:
            try:
                result.add(os.path.abspath(p))
            except Exception as ex:
                logger.error('Could not get path for {}: {}'.format(p, ex))
        return result

    def save_tab_to_file(self, tab):
        """
        Given a tab, will attempt to save the script in the tab to the path
        associated with the tab. If there's a problem this will be logged and
        reported and the tab status will continue to show as Modified.
        """
        logger.info('Saving script to: {}'.format(tab.path))
        logger.debug(tab.text())
        try:
            save_and_encode(tab.text(), tab.path, tab.newline)
        except OSError as e:
            logger.error(e)
            error_message = _('Could not save file (disk problem)')
            information = _("Error saving file to disk. Ensure you have "
                            "permission to write the file and "
                            "sufficient disk space.")
        except UnicodeEncodeError:
            error_message = _("Could not save file (encoding problem)")
            logger.exception(error_message)
            information = _("Unable to convert all the characters. If you "
                            "have an encoding line at the top of the file, "
                            "remove it and try again.")
        else:
            error_message = information = None
        if error_message:
            self._view.show_message(error_message, information)
        else:
            tab.setModified(False)
            self.show_status_message(_("Saved file: {}").format(tab.path))

    def check_for_shadow_module(self, path):
        """
        Check if the filename in the path is a shadow of a module already in
        the Python path. For example, many learners will save their first
        turtle based script as turtle.py, thus causing Python to never find
        the built in turtle module because of the name conflict.

        If the filename shadows an existing module, return True, otherwise,
        return False.
        """
        logger.info('Checking path "{}" for shadow module.'.format(path))
        filename = os.path.basename(path).replace('.py', '')
        return filename in self.modes[self.mode].module_names

    def save(self):
        """
        Save the content of the currently active editor tab.
        """
        tab = self._view.current_tab
        if tab is None:
            # There is no active text editor so abort.
            return
        if not tab.path:
            # Unsaved file.
            folder = self.get_dialog_directory()
            path = self._view.get_save_path(folder)
            if path and self.check_for_shadow_module(path):
                message = _('You cannot use the filename '
                            '"{}"').format(os.path.basename(path))
                info = _('This name is already used by another part of '
                         'Python. If you use this name, things are '
                         'likely to break. Please try again with a '
                         'different filename.')
                self._view.show_message(message, info)
                return
            tab.path = path
        if tab.path:
            # The user specified a path to a file.
            if os.path.splitext(tab.path)[1] == '':
                # the user didn't specify an extension, default to .py
                tab.path += '.py'
            self.save_tab_to_file(tab)
        else:
            # The user cancelled the filename selection.
            tab.path = None

    def get_tab(self, path):
        """
        Given a path, returns either an existing tab for the path or creates /
        loads a new tab for the path.
        """
        normalised_path = os.path.normcase(os.path.abspath(path))
        for tab in self._view.widgets:
            if tab.path:
                tab_path = os.path.normcase(os.path.abspath(tab.path))
                if tab_path == normalised_path:
                    self._view.focus_tab(tab)
                    return tab
        self.direct_load(path)
        return self._view.current_tab

    def zoom_in(self):
        """
        Make the editor's text bigger
        """
        logger.info('Zoom in')
        self._view.zoom_in()

    def zoom_out(self):
        """
        Make the editor's text smaller.
        """
        logger.info('Zoom out')
        self._view.zoom_out()

    def check_code(self):
        """
        Uses PyFlakes and PyCodeStyle to gather information about potential
        problems with the code in the current tab.
        """
        tab = self._view.current_tab
        if tab is None:
            # There is no active text editor so abort.
            return
        tab.has_annotations = not tab.has_annotations
        if tab.has_annotations:
            logger.info('Checking code.')
            self._view.reset_annotations()
            filename = tab.path if tab.path else _('untitled')
            builtins = self.modes[self.mode].builtins
            flake = check_flake(filename, tab.text(), builtins)
            if flake:
                logger.info(flake)
                self._view.annotate_code(flake, 'error')
            pep8 = check_pycodestyle(tab.text())
            if pep8:
                logger.info(pep8)
                self._view.annotate_code(pep8, 'style')
            self._view.show_annotations()
            tab.has_annotations = bool(flake or pep8)
            if not tab.has_annotations:
                # No problems detected, so confirm this with a friendly
                # message.
                ok_messages = [
                    _('Good job! No problems found.'),
                    _('Hurrah! Checker turned up no problems.'),
                    _('Nice one! Zero problems detected.'),
                    _('Well done! No problems here.'),
                    _('Awesome! Zero problems found.'),
                ]
                self.show_status_message(random.choice(ok_messages))
        else:
            self._view.reset_annotations()

    def show_help(self):
        """
        Display browser based help about Mu.
        """
        language_code = localedetect.language_code()[:2]
        major_version = '.'.join(__version__.split('.')[:2])
        url = 'https://codewith.mu/{}/help/{}'.format(language_code,
                                                      major_version)
        logger.info('Showing help at %r.', url)
        webbrowser.open_new(url)

    def quit(self, *args, **kwargs):
        """
        Exit the application.
        """
        if self._view.modified:
            # Alert the user to handle unsaved work.
            msg = _('There is un-saved work, exiting the application will'
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
                paths.append(os.path.abspath(widget.path))
        if self.modes[self.mode].is_debugger:
            # If quitting while debugging, make sure everything is cleaned
            # up.
            self.modes[self.mode].stop()
        session = {
            'theme': self.theme,
            'mode': self.mode,
            'paths': paths,
            'envars': self.envars,
            'minify': self.minify,
            'microbit_runtime': self.microbit_runtime,
            'zoom_level': self._view.zoom_position,
        }
        session_path = get_session_path()
        with open(session_path, 'w') as out:
            logger.debug('Session: {}'.format(session))
            logger.debug('Saving session to: {}'.format(session_path))
            json.dump(session, out, indent=2)
        # Clean up temporary mu.pth file if needed (Windows only).
        if sys.platform == 'win32' and 'pythonw.exe' in sys.executable:
            if site.ENABLE_USER_SITE:
                site_path = site.USER_SITE
                path_file = os.path.join(site_path, 'mu.pth')
                if os.path.exists(path_file):
                    try:
                        os.remove(path_file)
                        logger.info('{} removed.'.format(path_file))
                    except Exception as ex:
                        logger.error('Unable to delete {}'.format(path_file))
                        logger.error(ex)
        logger.info('Quitting.\n\n')
        sys.exit(0)

    def show_admin(self, event=None):
        """
        Cause the editor's admin dialog to be displayed to the user.

        Ensure any changes to the envars is updated.
        """
        logger.info('Showing logs from {}'.format(LOG_FILE))
        envars = '\n'.join(['{}={}'.format(name, value) for name, value in
                            self.envars])
        settings = {
            'envars': envars,
            'minify': self.minify,
            'microbit_runtime': self.microbit_runtime,
        }
        with open(LOG_FILE, 'r', encoding='utf8') as logfile:
            new_settings = self._view.show_admin(logfile.read(), settings)
            self.envars = extract_envars(new_settings['envars'])
            self.minify = new_settings['minify']
            runtime = new_settings['microbit_runtime'].strip()
            if runtime and not os.path.isfile(runtime):
                self.microbit_runtime = ''
                message = _('Could not find MicroPython runtime.')
                information = _("The micro:bit runtime you specified ('{}') "
                                "does not exist. "
                                "Please try again.").format(runtime)
                self._view.show_message(message, information)
            else:
                self.microbit_runtime = runtime

    def select_mode(self, event=None):
        """
        Select the mode that editor is supposed to be in.
        """
        if self.modes[self.mode].is_debugger:
            return
        logger.info('Showing available modes: {}'.format(
            list(self.modes.keys())))
        self.selecting_mode = True  # Flag to stop auto-detection of modes.
        new_mode = self._view.select_mode(self.modes, self.mode)
        self.selecting_mode = False
        if new_mode and new_mode != self.mode:
            logger.info('New mode selected: {}'.format(new_mode))
            self.change_mode(new_mode)

    def change_mode(self, mode):
        """
        Given the name of a mode, will make the necessary changes to put the
        editor into the new mode.
        """
        # Remove the old mode's REPL / filesystem / plotter if required.
        old_mode = self.modes[self.mode]
        if hasattr(old_mode, 'remove_repl'):
            old_mode.remove_repl()
        if hasattr(old_mode, 'remove_fs'):
            old_mode.remove_fs()
        if hasattr(old_mode, 'remove_plotter'):
            if old_mode.plotter:
                old_mode.remove_plotter()
        # Re-assign to new mode.
        self.mode = mode
        # Update buttons.
        self._view.change_mode(self.modes[mode])
        button_bar = self._view.button_bar
        button_bar.connect('modes', self.select_mode, 'Ctrl+Shift+M')
        button_bar.connect("new", self.new, "Ctrl+N")
        button_bar.connect("load", self.load, "Ctrl+O")
        button_bar.connect("save", self.save, "Ctrl+S")
        for action in self.modes[mode].actions():
            button_bar.connect(action['name'], action['handler'],
                               action['shortcut'])
        button_bar.connect("zoom-in", self.zoom_in, "Ctrl++")
        button_bar.connect("zoom-out", self.zoom_out, "Ctrl+-")
        button_bar.connect("theme", self.toggle_theme, "F1")
        button_bar.connect("check", self.check_code, "F2")
        button_bar.connect("help", self.show_help, "Ctrl+H")
        button_bar.connect("quit", self.quit, "Ctrl+Q")
        self._view.status_bar.set_mode(mode)
        # Update references to default file locations.
        logger.info('Workspace directory: {}'.format(
            self.modes[mode].workspace_dir()))
        # Reset remembered current path for load/save dialogs.
        self.current_path = ''
        # Ensure auto-save timeouts are set.
        if self.modes[mode].save_timeout > 0:
            # Start the timer
            self._view.set_timer(self.modes[mode].save_timeout, self.autosave)
        else:
            # Stop the timer
            self._view.stop_timer()
        # Update breakpoint states.
        if not (self.modes[mode].is_debugger or self.modes[mode].has_debugger):
            for tab in self._view.widgets:
                tab.breakpoint_handles = set()
                tab.reset_annotations()
        self.show_status_message(_('Changed to {} mode.').format(
            mode.capitalize()))

    def autosave(self):
        """
        Cycles through each tab and, if changed, saves it to the filesystem.
        """
        if self._view.modified:
            # Something has changed, so save it!
            for tab in self._view.widgets:
                if tab.path and tab.isModified():
                    self.save_tab_to_file(tab)
                    logger.info('Autosave detected and saved '
                                'changes in {}.'.format(tab.path))

    def check_usb(self):
        """
        Ensure connected USB devices are polled. If there's a change and a new
        recognised device is attached, inform the user via a status message.
        If a single device is found and Mu is in a different mode ask the user
        if they'd like to change mode.
        """
        devices = []
        device_types = set()
        # Detect connected devices.
        for name, mode in self.modes.items():
            if hasattr(mode, 'find_device'):
                # The mode can detect an attached device.
                port, serial = mode.find_device(with_logging=False)
                if port:
                    devices.append((name, port))
                    device_types.add(name)
        # Remove no-longer connected devices.
        to_remove = []
        for connected in self.connected_devices:
            if connected not in devices:
                to_remove.append(connected)
        for device in to_remove:
            self.connected_devices.remove(device)
        # Add newly connected devices.
        for device in devices:
            if device not in self.connected_devices:
                self.connected_devices.add(device)
                mode_name = device[0]
                device_name = self.modes[mode_name].name
                msg = _('Detected new {} device.').format(device_name)
                self.show_status_message(msg)
                # Only ask to switch mode if a single device type is connected
                # and we're not already trying to select a new mode via the
                # dialog. Cannot change mode if a script is already being run
                # by the current mode.
                m = self.modes[self.mode]
                running = hasattr(m, "runner") and m.runner
                if (len(device_types) == 1 and self.mode != mode_name and not
                        self.selecting_mode) and not running:
                    msg_body = _('Would you like to change Mu to the {} '
                                 'mode?').format(device_name)
                    change_confirmation = self._view.show_confirmation(
                        msg, msg_body, icon='Question')
                    if change_confirmation == QMessageBox.Ok:
                        self.change_mode(mode_name)

    def show_status_message(self, message, duration=5):
        """
        Displays the referenced message for duration seconds.
        """
        self._view.status_bar.set_message(message, duration * 1000)

    def debug_toggle_breakpoint(self, margin, line, modifiers):
        """
        How to handle the toggling of a breakpoint.
        """
        if (self.modes[self.mode].has_debugger or
                self.modes[self.mode].is_debugger):
            tab = self._view.current_tab
            code = tab.text(line)
            if self.mode == 'debugger':
                # The debugger is running.
                if is_breakpoint_line(code):
                    self.modes['debugger'].toggle_breakpoint(line, tab)
                    return
            else:
                # The debugger isn't running.
                if tab.markersAtLine(line):
                    tab.markerDelete(line, -1)
                    return
                elif is_breakpoint_line(code):
                    handle = tab.markerAdd(line, tab.BREAKPOINT_MARKER)
                    tab.breakpoint_handles.add(handle)
                    return
            msg = _('Cannot Set Breakpoint.')
            info = _("Lines that are comments or some multi-line "
                     "statements cannot have breakpoints.")
            self._view.show_message(msg, info)

    def rename_tab(self, tab_id=None):
        """
        How to handle double-clicking a tab in order to rename the file. If
        activated by the shortcut, activate against the current tab.
        """
        tab = None
        if tab_id:
            tab = self._view.tabs.widget(tab_id)
        else:
            tab = self._view.current_tab
        if tab:
            new_path = self._view.get_save_path(tab.path)
            if new_path and new_path != tab.path:
                if self.check_for_shadow_module(new_path):
                    message = _('You cannot use the filename '
                                '"{}"').format(os.path.basename(new_path))
                    info = _('This name is already used by another part of '
                             'Python. If you use that name, things are '
                             'likely to break. Please try again with a '
                             'different filename.')
                    self._view.show_message(message, info)
                    return
                logger.info('Attempting to rename {} to {}'.format(tab.path,
                                                                   new_path))
                # The user specified a path to a file.
                if not os.path.basename(new_path).endswith('.py'):
                    # No extension given, default to .py
                    new_path += '.py'
                # Check for duplicate path with currently open tab.
                for other_tab in self._view.widgets:
                    if other_tab.path == new_path:
                        logger.info('Cannot rename, a file of that name is '
                                    'already open in Mu')
                        message = _('Could not rename file.')
                        information = _("A file of that name is already open "
                                        "in Mu.")
                        self._view.show_message(message, information)
                        return
                # Finally rename
                tab.path = new_path
                logger.info('Renamed file to: {}'.format(tab.path))
                self.save()

    def find_replace(self):
        """
        Handle find / replace functionality.

        If find/replace dialog is dismissed, do nothing.

        Otherwise, check there's something to find, warn if there isn't.

        If there is, find (and, optionally, replace) then confirm outcome with
        a status message.
        """
        result = self._view.show_find_replace(self.find, self.replace,
                                              self.global_replace)
        if result:
            self.find, self.replace, self.global_replace = result
            if self.find:
                if self.replace:
                    replaced = self._view.replace_text(self.find, self.replace,
                                                       self.global_replace)
                    if replaced == 1:
                        msg = _('Replaced "{}" with "{}".')
                        self.show_status_message(msg.format(self.find,
                                                            self.replace))
                    elif replaced > 1:
                        msg = _('Replaced {} matches of "{}" with "{}".')
                        self.show_status_message(msg.format(replaced,
                                                            self.find,
                                                            self.replace))
                    else:
                        msg = _('Could not find "{}".')
                        self.show_status_message(msg.format(self.find))
                else:
                    matched = self._view.highlight_text(self.find)
                    if matched:
                        msg = _('Highlighting matches for "{}".')
                    else:
                        msg = _('Could not find "{}".')
                    self.show_status_message(msg.format(self.find))
            else:
                message = _('You must provide something to find.')
                information = _("Please try again, this time with something "
                                "in the find box.")
                self._view.show_message(message, information)

    def toggle_comments(self):
        """
        Ensure all highlighted lines are toggled between comments/uncommented.
        """
        self._view.toggle_comments()
