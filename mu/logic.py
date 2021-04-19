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
import logging
import tempfile
import webbrowser
import random
import locale
import shutil

import appdirs
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore
from pyflakes.api import check
from pycodestyle import StyleGuide, Checker

from . import __version__
from . import i18n
from .resources import path
from .debugger.utils import is_breakpoint_line
from .config import DATA_DIR, VENV_DIR, MAX_LINE_LENGTH
from . import settings
from .virtual_environment import venv

# The default directory for application logs.
LOG_DIR = appdirs.user_log_dir(appname="mu", appauthor="python")
# The path to the log file for the application.
LOG_FILE = os.path.join(LOG_DIR, "mu.log")
# Regex to match pycodestyle (PEP8) output.
STYLE_REGEX = re.compile(r".*:(\d+):(\d+):\s+(.*)")
# Regex to match flake8 output.
FLAKE_REGEX = re.compile(r".*:(\d+):(\d+)\s+(.*)")
# Regex to match undefined name errors for given builtins
BUILTINS_REGEX = r"^undefined name '({})'"
# Regex to match false positive flake errors if microbit.* is expanded.
EXPAND_FALSE_POSITIVE = re.compile(
    r"^.*'microbit\.(\w+)' imported but unused$"
)
# The text to which "from microbit import \*" should be expanded.
EXPANDED_IMPORT = (
    "from microbit import pin15, pin2, pin0, pin1, "
    " pin3, pin6, pin4, i2c, pin5, pin7, pin8, Image, "
    "pin9, pin14, pin16, reset, pin19, temperature, "
    "sleep, pin20, button_a, button_b, running_time, "
    "accelerometer, display, uart, spi, panic, pin13, "
    "pin12, pin11, pin10, compass"
)
# Default images to copy over for use in PyGameZero demo apps.
DEFAULT_IMAGES = [
    "alien.png",
    "alien_hurt.png",
    "cat1.png",
    "cat2.png",
    "cat3.png",
    "cat4.png",
    "splat.png",
]
# Default sound effects to copy over for use in PyGameZero demo apps.
DEFAULT_SOUNDS = [
    "eep.wav",
    "meow1.wav",
    "meow2.wav",
    "meow3.wav",
    "meow4.wav",
    "splat.wav",
]
MOTD = [  # Candidate phrases for the message of the day (MOTD).
    _("Hello, World!"),
    _(
        "This editor is free software written in Python. You can modify it, "
        "add features or fix bugs if you like."
    ),
    _("This editor is called Mu (you say it 'mew' or 'moo')."),
    _("Google, Facebook, NASA, Pixar, Disney and many more use Python."),
    _(
        "Programming is a form of magic. Learn to cast the right spells with "
        "code and you'll be a wizard."
    ),
    _(
        "REPL stands for read, evaluate, print, loop. It's a fun way to talk "
        "to your computer! :-)"
    ),
    _("Be brave, break things, learn and have fun!"),
    _("Make your software both useful AND fun. Empower your users."),
    _("For the Zen of Python: import this"),
    _("Diversity promotes creativity."),
    _("An open mind, spirit of adventure and respect for diversity are key."),
    _(
        "Don't worry if it doesn't work. Learn the lesson, fix it and try "
        "again! :-)"
    ),
    _("Coding is collaboration."),
    _("Compliment and amplify the good things with code."),
    _(
        "In theory, theory and practice are the same. In practice, they're "
        "not. ;-)"
    ),
    _("Debugging is twice as hard as writing the code in the first place."),
    _("It's fun to program."),
    _("Programming has more to do with problem solving than writing code."),
    _("Start with your users' needs."),
    _("Try to see things from your users' point of view."),
    _("Put yourself in your users' shoes."),
    _(
        "Explaining a programming problem to a friend often reveals the "
        "solution. :-)"
    ),
    _("If you don't know, ask. Nobody to ask? Just look it up."),
    _("Complexity is the enemy. KISS - keep it simple, stupid!"),
    _("Beautiful is better than ugly."),
    _("Explicit is better than implicit."),
    _("Simple is better than complex. Complex is better than complicated."),
    _("Flat is better than nested."),
    _("Sparse is better than dense."),
    _("Readability counts."),
    _(
        "Special cases aren't special enough to break the rules. "
        "Although practicality beats purity."
    ),
    _("Errors should never pass silently. Unless explicitly silenced."),
    _("In the face of ambiguity, refuse the temptation to guess."),
    _("There should be one-- and preferably only one --obvious way to do it."),
    _(
        "Now is better than never. Although never is often better than "
        "*right* now."
    ),
    _("If the implementation is hard to explain, it's a bad idea."),
    _("If the implementation is easy to explain, it may be a good idea."),
    _("Namespaces are one honking great idea -- let's do more of those!"),
    _("Mu was created by Nicholas H.Tollervey."),
    _("To understand what recursion is, you must first understand recursion."),
    _(
        "Algorithm: a word used by programmers when they don't want to "
        "explain what they did."
    ),
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
    "^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)"
)

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

    with open(filepath, "w", encoding=encoding, newline="") as f:
        text_to_write = (
            newline.join(line.rstrip(" ") for line in text.splitlines())
            + newline
        )
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
        ("\n", "^\n|[^\r]\n"),
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


def extract_envars(raw):
    """
    Returns a list of environment variables given a string containing
    NAME=VALUE definitions on separate lines.
    """
    result = []
    for line in raw.split("\n"):
        definition = line.split("=", 1)
        if len(definition) == 2:
            result.append([definition[0].strip(), definition[1].strip()])
    return result


def save_session(session):
    settings.session.update(session)
    settings.session.save()


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
        builtins_regex = re.compile(BUILTINS_REGEX.format("|".join(builtins)))
    feedback = {}
    for log in reporter.log:
        if import_all:
            # Guard to stop unwanted "microbit.* imported but unused" messages.
            message = log["message"]
            if EXPAND_FALSE_POSITIVE.match(message):
                continue
        if builtins:
            if builtins_regex.match(log["message"]):
                continue
        if log["line_no"] not in feedback:
            feedback[log["line_no"]] = []
        feedback[log["line_no"]].append(log)
    return feedback


def check_pycodestyle(code, config_file=False):
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
    ignore = (
        "E121",
        "E123",
        "E126",
        "E226",
        "E203",
        "E302",
        "E305",
        "E24",
        "E704",
        "W291",
        "W292",
        "W293",
        "W391",
        "W503",
    )
    style = StyleGuide(
        parse_argv=False,
        config_file=config_file,
        max_line_length=MAX_LINE_LENGTH,
    )

    # StyleGuide() returns pycodestyle module's own ignore list. That list may
    # be a default list or a custom list provided by the user
    # merge the above ignore list with StyleGuide() returned list, then
    # remove duplicates with set(), convert back to tuple()
    ignore = style.options.ignore + ignore
    style.options.ignore = tuple(set(ignore))

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
    for result in results.split("\n"):
        matcher = STYLE_REGEX.match(result)
        if matcher:
            line_no, col, msg = matcher.groups()
            line_no = int(line_no) - 1
            code, description = msg.split(" ", 1)
            if code == "E303":
                description += _(" above this line")
            if line_no not in style_feedback:
                style_feedback[line_no] = []
            style_feedback[line_no].append(
                {
                    "line_no": line_no,
                    "column": int(col) - 1,
                    "message": description.capitalize(),
                    "code": code,
                }
            )
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
        self.log.append(
            {"line_no": 0, "filename": filename, "message": str(message)}
        )

    def syntaxError(self, filename, message, line_no, column, source):
        """
        Records a syntax error in the file called filename.

        The message argument contains an explanation of the syntax error,
        line_no indicates the line where the syntax error occurred, column
        indicates the column on which the error occurred and source is the
        source code containing the syntax error.
        """
        msg = _(
            "Syntax error. Python cannot understand this line. Check for "
            "missing characters!"
        )
        self.log.append(
            {
                "message": msg,
                "line_no": int(line_no) - 1,  # Zero based counting in Mu.
                "column": column - 1,
                "source": source,
            }
        )

    def flake(self, message):
        """
        PyFlakes found something wrong with the code.
        """
        matcher = FLAKE_REGEX.match(str(message))
        if matcher:
            line_no, col, msg = matcher.groups()
            self.log.append(
                {
                    "line_no": int(line_no) - 1,  # Zero based counting in Mu.
                    "column": int(col),
                    "message": msg,
                }
            )
        else:
            self.log.append(
                {"line_no": 0, "column": 0, "message": str(message)}
            )


class Device:
    """
    Device object, containing both information about the connected device,
    the port it's connected through and the mode it works with.
    """

    def __init__(
        self,
        vid,
        pid,
        port,
        serial_number,
        manufacturer,
        long_mode_name,
        short_mode_name,
        board_name=None,
    ):
        self.vid = vid
        self.pid = pid
        self.port = port
        self.serial_number = serial_number
        self.manufacturer = manufacturer
        self.long_mode_name = long_mode_name
        self.short_mode_name = short_mode_name
        self.board_name = board_name

    @property
    def name(self):
        """
        Returns the device name.
        """
        if self.board_name:
            return self.board_name
        else:
            return self.long_mode_name + " device"

    def __eq__(self, other):
        """
        Equality on devices. Comparison on vid, pid, and serial_number,
        and most importantly also matches on which port the device is
        connected to. That is, if two identical devices are connected
        to separate ports they are considered different.
        """
        return (
            isinstance(other, self.__class__)
            and self.pid == other.pid
            and self.vid == other.vid
            and self.port == other.port
            and self.serial_number == other.serial_number
        )

    def __ne__(self, other):
        """
        Inequality of devices is the negation of equality
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        Alphabetical ordering according to device name
        """
        return self.name < other.name

    def __gt__(self, other):
        """
        Alphabetical ordering according to device name
        """
        return self.name > other.name

    def __le__(self, other):
        """
        Alphabetical ordering according to device name
        """
        return self.name <= other.name

    def __ge__(self, other):
        """
        Alphabetical ordering according to device name
        """
        return self.name >= other.name

    def __str__(self):
        """
        String representation of devices includes name, port, and VID/PID
        """
        s = "{} on {} (VID: 0x{:04X}, PID: 0x{:04X})"
        return s.format(self.name, self.port, self.vid, self.pid)

    def __hash__(self):
        """
        Hash is the hash of the string representation, includes the same
        elements in the hash as in equality testing.
        """
        return hash(str(self))


class DeviceList(QtCore.QAbstractListModel):
    device_connected = pyqtSignal("PyQt_PyObject")
    device_disconnected = pyqtSignal("PyQt_PyObject")

    def __init__(self, modes, parent=None):
        super().__init__(parent)
        self.modes = modes
        self._devices = list()

    def __iter__(self):
        """
        Enables iteration over the list of devices
        """
        return iter(self._devices)

    def __getitem__(self, i):
        """
        Enable [] operator
        """
        return self._devices[i]

    def __len__(self):
        """
        Number of devices
        """
        return len(self._devices)

    def rowCount(self, parent):
        """
        Number of devices
        """
        return len(self._devices)

    def data(self, index, role):
        """
        Reimplements QAbstractListModel.data(): returns data for the
        specified index and role. In this case only implmented for
        ToolTipRole and DisplayRole
        """
        device = self._devices[index.row()]
        if role == QtCore.Qt.ToolTipRole:
            return str(device)
        elif role == QtCore.Qt.DisplayRole:
            return device.name

    def add_device(self, new_device):
        """
        Add a new device to the device list, maintains alphabetical ordering
        """
        parent = QtCore.QModelIndex()
        # Find position to insert sorted
        position = 0
        for i, device in enumerate(self._devices):
            if new_device > device:
                position = i + 1
        # Insert
        self.beginInsertRows(parent, position, position)
        self._devices.insert(position, new_device)
        self.endInsertRows()

    def remove_device(self, device):
        """
        Remove the given device from the device list
        """
        parent = QtCore.QModelIndex()
        position = self._devices.index(device)
        self.beginRemoveRows(parent, position, position)
        self._devices.remove(device)
        self.endRemoveRows()

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
        for mode_name, mode in self.modes.items():
            if hasattr(mode, "find_devices"):
                # The mode can detect attached devices.
                detected = mode.find_devices(with_logging=False)
                if detected:
                    device_types.add(mode_name)
                    devices.extend(detected)
        # Remove no-longer connected devices.
        for device in self:
            if device not in devices:
                self.remove_device(device)
                self.device_disconnected.emit(device)
                logger.info(
                    (
                        "{} device disconnected on port: {}"
                        "(VID: 0x{:04X}, PID: 0x{:04X}, manufacturer {})"
                    ).format(
                        device.short_mode_name,
                        device.port,
                        device.vid,
                        device.pid,
                        device.manufacturer,
                    )
                )
        # Add newly connected devices.
        for device in devices:
            if device not in self:
                self.add_device(device)
                self.device_connected.emit(device)
                logger.info(
                    (
                        "{} device connected on port: {}"
                        "(VID: 0x{:04X}, PID: 0x{:04X}, manufacturer: '{}')"
                    ).format(
                        device.short_mode_name,
                        device.port,
                        device.vid,
                        device.pid,
                        device.manufacturer,
                    )
                )


class Editor(QObject):
    """
    Application logic for the editor itself.
    """

    def __init__(self, view):
        super().__init__()
        logger.info("Setting up editor.")
        self._view = view
        self.fs = None
        self.theme = "day"
        self.mode = "python"
        self.python_extensions = [".py", ".pyw"]
        self.modes = {}
        self.envars = []  # See restore session and show_admin
        self.minify = False
        self.microbit_runtime = ""
        self.connected_devices = DeviceList(self.modes, parent=self)
        self.current_device = None
        self.find = ""
        self.replace = ""
        self.current_path = ""  # Directory of last loaded file.
        self.global_replace = False
        self.selecting_mode = False  # Flag to stop auto-detection of modes.
        if not os.path.exists(DATA_DIR):
            logger.debug("Creating directory: {}".format(DATA_DIR))
            os.makedirs(DATA_DIR)
        logger.info("Log directory: {}".format(LOG_DIR))
        logger.info("Data directory: {}".format(DATA_DIR))

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
        self.connected_devices.modes = modes
        logger.info("Available modes: {}".format(", ".join(self.modes.keys())))
        # Ensure there is a workspace directory.
        wd = self.modes["python"].workspace_dir()
        if not os.path.exists(wd):
            logger.debug("Creating directory: {}".format(wd))
            os.makedirs(wd)
        # Ensure PyGameZero assets are copied over.
        images_path = os.path.join(wd, "images")
        fonts_path = os.path.join(wd, "fonts")
        sounds_path = os.path.join(wd, "sounds")
        music_path = os.path.join(wd, "music")
        if not os.path.exists(images_path):
            logger.debug("Creating directory: {}".format(images_path))
            os.makedirs(images_path)
            for img in DEFAULT_IMAGES:
                shutil.copy(
                    path(img, "pygamezero/"), os.path.join(images_path, img)
                )
        if not os.path.exists(fonts_path):
            logger.debug("Creating directory: {}".format(fonts_path))
            os.makedirs(fonts_path)
        if not os.path.exists(sounds_path):
            logger.debug("Creating directory: {}".format(sounds_path))
            os.makedirs(sounds_path)
            for sfx in DEFAULT_SOUNDS:
                shutil.copy(
                    path(sfx, "pygamezero/"), os.path.join(sounds_path, sfx)
                )
        if not os.path.exists(music_path):
            logger.debug("Creating directory: {}".format(music_path))
            os.makedirs(music_path)
        # Ensure Web based assets are copied over.
        template_path = os.path.join(wd, "templates")
        static_path = os.path.join(wd, "static")
        if not os.path.exists(template_path):
            logger.debug("Creating directory: {}".format(template_path))
            shutil.copytree(path("templates", "web/"), template_path)
        if not os.path.exists(static_path):
            logger.debug("Creating directory: {}".format(static_path))
            shutil.copytree(path("static", "web/"), static_path)
            # Copy all the static directories.
        # Start the timer to poll every second for an attached or removed
        # USB device.
        self._view.set_usb_checker(1, self.connected_devices.check_usb)

    def connect_to_status_bar(self, status_bar):
        """
        Connect the editor with the Window-statusbar.
        Should be called after Editor.setup(), to ensure modes are initialized
        """
        # Connect to logs
        status_bar.connect_logs(self.show_admin, "Ctrl+Shift+D")
        # Show connection messages in status_bar
        self.connected_devices.device_connected.connect(
            status_bar.device_connected
        )
        # Connect to device list
        device_selector = status_bar.device_selector
        status_bar.device_selector.set_device_list(self.connected_devices)
        # Propagate device_changed events
        device_selector.device_changed.connect(self.device_changed)
        if self.modes:
            for mode in self.modes.values():
                device_selector.device_changed.connect(mode.device_changed)

    def restore_session(self, paths=None):
        """
        Attempts to recreate the tab state from the last time the editor was
        run. If paths contains a collection of additional paths specified by
        the user, they are also "restored" at the same time (duplicates will be
        ignored).
        """
        self.change_mode(self.mode)
        old_session = settings.session
        logger.debug(old_session)
        if "theme" in old_session:
            self.theme = old_session["theme"]
        self._view.set_theme(self.theme)
        if "mode" in old_session:
            old_mode = old_session["mode"]
            if old_mode in self.modes:
                self.mode = old_session["mode"]
            else:
                # Unknown mode (perhaps an old version?)
                self.select_mode(None)
        else:
            # So ask for the desired mode.
            self.select_mode(None)
        if "paths" in old_session:
            old_paths = self._abspath(old_session["paths"])
            launch_paths = self._abspath(paths) if paths else set()
            for old_path in old_paths:
                # if the os passed in a file, defer loading it now
                if old_path in launch_paths:
                    continue
                self.direct_load(old_path)
            logger.info("Loaded files.")
        if "envars" in old_session:
            self.envars = old_session["envars"]
            logger.info(
                "User defined environment variables: " "{}".format(self.envars)
            )
        if "minify" in old_session:
            self.minify = old_session["minify"]
            logger.info(
                "Minify scripts on micro:bit? " "{}".format(self.minify)
            )
        if "microbit_runtime" in old_session:
            self.microbit_runtime = old_session["microbit_runtime"]
            if self.microbit_runtime:
                logger.info(
                    "Custom micro:bit runtime path: "
                    "{}".format(self.microbit_runtime)
                )
                if not os.path.isfile(self.microbit_runtime):
                    self.microbit_runtime = ""
                    logger.warning(
                        "The specified micro:bit runtime "
                        "does not exist. Using default "
                        "runtime instead."
                    )
        if "zoom_level" in old_session:
            self._view.zoom_position = old_session["zoom_level"]
            self._view.set_zoom()

        if "venv_path" in old_session:
            venv.relocate(old_session["venv_path"])
            venv.ensure()

        old_window = old_session.get("window", {})
        self._view.size_window(**old_window)

        #
        # Doesn't seem to do anything useful
        #
        # ~ if old_session is None:
        # ~ self._view.set_theme(self.theme)

        # handle os passed file last,
        # so it will not be focused over by another tab
        if paths and len(paths) > 0:
            self.load_cli(paths)
        self.change_mode(self.mode)
        self.show_status_message(random.choice(MOTD), 10)
        if not self._view.tab_count:
            py = self.modes[self.mode].code_template + NEWLINE
            tab = self._view.add_tab(
                None, py, self.modes[self.mode].api(), NEWLINE
            )
            tab.setCursorPosition(len(py.split(NEWLINE)), 0)
            logger.info("Starting with blank file.")

    def toggle_theme(self):
        """
        Switches between themes (night, day or high-contrast).
        """
        if self.theme == "day":
            self.theme = "night"
        elif self.theme == "night":
            self.theme = "contrast"
        else:
            self.theme = "day"
        logger.info("Toggle theme to: {}".format(self.theme))
        self._view.set_theme(self.theme)

    def new(self):
        """
        Adds a new tab to the editor.
        """
        logger.info("Added a new tab.")
        default_text = self.modes[self.mode].code_template + NEWLINE
        self._view.add_tab(
            None, default_text, self.modes[self.mode].api(), NEWLINE
        )

    def _load(self, path):
        """
        Attempt to load a Python script from the passed in path. This path may
        be a .py file containing Python source code, or a .hex file, created
        for a micro:bit like device, with the source code embedded therein.

        This method will work its way around duplicate paths and also attempt
        to cleanly handle / report / log errors when encountered in a helpful
        manner.
        """
        logger.info("Loading script from: {}".format(path))
        error = _(
            "The file contains characters Mu expects to be encoded as "
            "{0} or as the computer's default encoding {1}, but which "
            "are encoded in some other way.\n\nIf this file was saved "
            "in another application, re-save the file via the "
            "'Save as' option and set the encoding to {0}"
        )
        error = error.format(ENCODING, locale.getpreferredencoding())
        # Does the file even exist?
        if not os.path.isfile(path):
            logger.info("The file {} does not exist.".format(path))
            return
        # see if file is open first
        for widget in self._view.widgets:
            if widget.path is None:  # this widget is an unsaved buffer
                continue
            # The widget could be for a file on a MicroPython device that
            # has since been unplugged. We should ignore it and assume that
            # folks understand this file is no longer available (there's
            # nothing else we can do).
            if not os.path.isfile(widget.path):
                logger.info(
                    "The file {} no longer exists.".format(widget.path)
                )
                continue
            # Check for duplication of open file.
            if os.path.samefile(path, widget.path):
                logger.info("Script already open.")
                msg = _('The file "{}" is already open.')
                self._view.show_message(msg.format(os.path.basename(path)))
                self._view.focus_tab(widget)
                return
        name, text, newline, file_mode = None, None, None, None
        try:
            if self.has_python_extension(path):
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
                # as None if handling a hex file, thus forcing the user to work
                # out what to name the recovered script.
                for mode_name, mode in self.modes.items():
                    try:
                        text, newline = mode.open_file(path)
                        if not path.endswith(".hex"):
                            name = path
                    except Exception as exc:
                        # No worries, log it and try the next mode
                        logger.warning(
                            "Error when mode {} try to open the "
                            "{} file.".format(mode_name, path),
                            exc_info=exc,
                        )
                    else:
                        if text:
                            file_mode = mode_name
                            break
                else:
                    message = _("Mu was not able to open this file")
                    info = _(
                        "Currently Mu only works with Python source "
                        "files or hex files created with embedded "
                        "MicroPython code."
                    )
                    self._view.show_message(message, info)
                    return
        except OSError:
            message = _("Could not load {}").format(path)
            logger.exception("Could not load {}".format(path))
            info = _(
                "Does this file exist?\nIf it does, do you have "
                "permission to read it?\n\nPlease check and try again."
            )
            self._view.show_message(message, info)
        else:
            if file_mode and self.mode != file_mode:
                mode_name = self.modes[file_mode].name
                message = _("Is this a {} file?").format(mode_name)
                info = _(
                    "It looks like this could be a {} file.\n\n"
                    "Would you like to change Mu to the {}"
                    "mode?"
                ).format(mode_name, mode_name)
                if (
                    self._view.show_confirmation(
                        message, info, icon="Question"
                    )
                    == QMessageBox.Ok
                ):
                    self.change_mode(file_mode)
            logger.debug(text)
            self._view.add_tab(
                name, text, self.modes[self.mode].api(), newline
            )

    def get_dialog_directory(self, default=None):
        """
        Return the directory folder which a load/save dialog box should
        open into. In order of precedence this function will return:

        0) If not None, the value of default.
        1) The last location used by a load/save dialog.
        2) The directory containing the current file.
        3) The mode's reported workspace directory.
        """
        if default is not None:
            folder = default
        elif self.current_path and os.path.isdir(self.current_path):
            folder = self.current_path
        else:
            current_file_path = ""
            try:
                workspace_path = self.modes[self.mode].workspace_dir()
            except Exception as e:
                # Avoid crashing if workspace_dir raises, use default path
                # instead
                workspace_path = self.modes["python"].workspace_dir()
                logger.error(
                    (
                        "Could not open {} mode workspace directory"
                        'due to exception "{}". Using:'
                        "\n\n{}\n\n...to store your code instead"
                    ).format(self.mode, e, workspace_path)
                )
            tab = self._view.current_tab
            if tab and tab.path:
                current_file_path = os.path.dirname(os.path.abspath(tab.path))
            folder = current_file_path if current_file_path else workspace_path
        logger.info("Using path for file dialog: {}".format(folder))
        return folder

    def load(self, *args, default_path=None):
        """
        Loads a Python (or other supported) file from the file system or
        extracts a Python script from a hex file.
        """
        # Get all supported extensions from the different modes
        extensions = [ext.strip("*.") for ext in self.python_extensions]
        for mode_name, mode in self.modes.items():
            if mode.file_extensions:
                extensions += mode.file_extensions
        extensions = [e.lower() for e in extensions]
        extensions = "*.{} *.{}".format(
            " *.".join(extensions), " *.".join(extensions).upper()
        )
        folder = self.get_dialog_directory(default_path)
        allow_previous = not bool(default_path)
        path = self._view.get_load_path(
            folder, extensions, allow_previous=allow_previous
        )
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
                logger.info("Passed-in filename: {}".format(p))
                # abspath will fail for non-paths
                self.direct_load(os.path.abspath(p))
            except Exception as e:
                logging.warning(
                    "Can't open file from command line {}".format(p),
                    exc_info=e,
                )

    def _abspath(self, paths):
        """
        Safely convert an arrary of paths to their absolute forms and remove
        duplicate items.
        """
        result = []
        for p in paths:
            try:
                abspath = os.path.abspath(p)
            except Exception as ex:
                logger.error("Could not get path for {}: {}".format(p, ex))
            else:
                if abspath not in result:
                    result.append(abspath)
        return result

    def save_tab_to_file(self, tab, show_error_messages=True):
        """
        Given a tab, will attempt to save the script in the tab to the path
        associated with the tab. If there's a problem this will be logged and
        reported and the tab status will continue to show as Modified.
        """
        logger.info("Saving script to: {}".format(tab.path))
        logger.debug(tab.text())
        try:
            save_and_encode(tab.text(), tab.path, tab.newline)
        except OSError as e:
            logger.error(e)
            error_message = _("Could not save file (disk problem)")
            information = _(
                "Error saving file to disk. Ensure you have "
                "permission to write the file and "
                "sufficient disk space."
            )
        except UnicodeEncodeError:
            error_message = _("Could not save file (encoding problem)")
            logger.exception(error_message)
            information = _(
                "Unable to convert all the characters. If you "
                "have an encoding line at the top of the file, "
                "remove it and try again."
            )
        else:
            error_message = information = None
        if error_message and show_error_messages:
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
        pyextensions = [".pyw", ".PYW", ".py", ".PY"]
        filename = os.path.basename(path)
        for ext in pyextensions:
            filename = filename.replace(ext, "")
        return filename in self.modes[self.mode].module_names

    def save(self, *args, default=None):
        """
        Save the content of the currently active editor tab.
        """
        tab = self._view.current_tab
        if tab is None:
            # There is no active text editor so abort.
            return
        if not tab.path:
            # Unsaved file.
            folder = self.get_dialog_directory(default)
            path = self._view.get_save_path(folder)
            if path and self.check_for_shadow_module(path):
                message = _("You cannot use the filename " '"{}"').format(
                    os.path.basename(path)
                )
                info = _(
                    "This name is already used by another part of "
                    "Python. If you use this name, things are "
                    "likely to break. Please try again with a "
                    "different filename."
                )
                self._view.show_message(message, info)
                return
            tab.path = path
        if tab.path:
            # The user specified a path to a file.
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
        logger.info("Zoom in")
        self._view.zoom_in()

    def zoom_out(self):
        """
        Make the editor's text smaller.
        """
        logger.info("Zoom out")
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
        if tab.path and not self.has_python_extension(tab.path):
            # Only works on Python files, so abort.
            return
        tab.has_annotations = not tab.has_annotations
        if tab.has_annotations:
            logger.info("Checking code.")
            self._view.reset_annotations()
            filename = tab.path if tab.path else _("untitled")
            builtins = self.modes[self.mode].builtins
            flake = check_flake(filename, tab.text(), builtins)
            if flake:
                logger.info(flake)
                self._view.annotate_code(flake, "error")
            pep8 = check_pycodestyle(tab.text())
            if pep8:
                logger.info(pep8)
                self._view.annotate_code(pep8, "style")
            self._view.show_annotations()
            tab.has_annotations = bool(flake or pep8)
            if not tab.has_annotations:
                # No problems detected, so confirm this with a friendly
                # message.
                ok_messages = [
                    _("Good job! No problems found."),
                    _("Hurrah! Checker turned up no problems."),
                    _("Nice one! Zero problems detected."),
                    _("Well done! No problems here."),
                    _("Awesome! Zero problems found."),
                ]
                self.show_status_message(random.choice(ok_messages))
                self._view.set_checker_icon("check-good.png")
            else:
                self._view.set_checker_icon("check-bad.png")
        else:
            self._view.reset_annotations()

    def show_help(self):
        """
        Display browser based help about Mu.
        """
        major_version = ".".join(__version__.split(".")[:2])
        url = "https://codewith.mu/{}/help/{}".format(
            i18n.language_code[:2], major_version
        )
        logger.info("Showing help at %r.", url)
        webbrowser.open_new(url)

    def quit(self, *args, **kwargs):
        """
        Exit the application.
        """
        if self._view.modified:
            # Alert the user to handle unsaved work.
            msg = _(
                "There is un-saved work, exiting the application will"
                " cause you to lose it."
            )
            result = self._view.show_confirmation(msg)
            if result == QMessageBox.Cancel:
                if args and hasattr(args[0], "ignore"):
                    # The function is handling an event, so ignore it.
                    args[0].ignore()
                return
        paths = []
        for widget in self._view.widgets:
            if widget.path:
                paths.append(os.path.abspath(widget.path))
        # Make sure the mode's stop method is called so
        # everything is cleaned up.
        self.modes[self.mode].stop()
        session = {
            "theme": self.theme,
            "mode": self.mode,
            "paths": paths,
            "envars": self.envars,
            "minify": self.minify,
            "microbit_runtime": self.microbit_runtime,
            "zoom_level": self._view.zoom_position,
            "window": {
                "x": self._view.x(),
                "y": self._view.y(),
                "w": self._view.width(),
                "h": self._view.height(),
            },
        }
        save_session(session)
        logger.info("Quitting.\n\n")
        sys.exit(0)

    def show_admin(self, event=None):
        """
        Cause the editor's admin dialog to be displayed to the user.

        Ensure any changes to the envars is updated.
        """
        logger.info("Showing admin with logs from {}".format(LOG_FILE))
        envars = "\n".join(
            ["{}={}".format(name, value) for name, value in self.envars]
        )
        settings = {
            "envars": envars,
            "minify": self.minify,
            "microbit_runtime": self.microbit_runtime,
        }
        baseline_packages, user_packages = venv.installed_packages()
        packages = user_packages
        with open(LOG_FILE, "r", encoding="utf8") as logfile:
            new_settings = self._view.show_admin(
                logfile.read(),
                settings,
                "\n".join(packages),
                self.modes[self.mode],
                self.connected_devices,
            )
        if new_settings:
            if "envars" in new_settings:
                self.envars = extract_envars(new_settings["envars"])
            if "minify" in new_settings:
                self.minify = new_settings["minify"]
            if "microbit_runtime" in new_settings:
                runtime = new_settings["microbit_runtime"].strip()
                if runtime and not os.path.isfile(runtime):
                    self.microbit_runtime = ""
                    message = _("Could not find MicroPython runtime.")
                    information = _(
                        "The micro:bit runtime you specified "
                        "('{}') does not exist. "
                        "Please try again."
                    ).format(runtime)
                    self._view.show_message(message, information)
                else:
                    self.microbit_runtime = runtime
            if "packages" in new_settings:
                new_packages = [
                    p
                    for p in new_settings["packages"].lower().split("\n")
                    if p.strip()
                ]
                old_packages = [p.lower() for p in user_packages]
                self.sync_package_state(old_packages, new_packages)
        else:
            logger.info("No admin settings changed.")

    def sync_package_state(self, old_packages, new_packages):
        """
        Given the state of the old third party packages, compared to the new
        third party packages, ensure that pip uninstalls and installs the
        packages so the currently available third party packages reflects the
        new state.
        """
        old = set(old_packages)
        new = set(new_packages)
        logger.info("Synchronize package states...")
        logger.info("Old: {}".format(old))
        logger.info("New: {}".format(new))
        to_remove = old.difference(new)
        to_add = new.difference(old)
        if to_remove or to_add:
            logger.info("To add: {}".format(to_add))
            logger.info("To remove: {}".format(to_remove))
            logger.info("Virtualenv: {}".format(VENV_DIR))
            self._view.sync_packages(to_remove, to_add)

    def select_mode(self, event=None):
        """
        Select the mode that editor is supposed to be in.
        """
        if self.modes[self.mode].is_debugger:
            return
        logger.info(
            "Showing available modes: {}".format(list(self.modes.keys()))
        )
        self.selecting_mode = True  # Flag to stop auto-detection of modes.
        new_mode = self._view.select_mode(self.modes, self.mode)
        self.selecting_mode = False
        if new_mode and new_mode != self.mode:
            logger.info("New mode selected: {}".format(new_mode))
            self.change_mode(new_mode)

    def change_mode(self, mode):
        """
        Given the name of a mode, will make the necessary changes to put the
        editor into the new mode.
        """
        # Remove the old mode's REPL / filesystem / plotter if required.
        old_mode = self.modes[self.mode]
        if hasattr(old_mode, "remove_repl"):
            old_mode.remove_repl()
        if hasattr(old_mode, "remove_fs"):
            old_mode.remove_fs()
        if hasattr(old_mode, "remove_plotter"):
            if old_mode.plotter:
                old_mode.remove_plotter()
        # Deactivate old mode
        self.modes[self.mode].deactivate()
        # Re-assign to new mode.
        self.mode = mode
        # Activate new mode
        self.modes[mode].activate()
        # Update buttons.
        self._view.change_mode(self.modes[mode])
        button_bar = self._view.button_bar
        button_bar.connect("modes", self.select_mode, "Ctrl+Shift+M")
        button_bar.connect("new", self.new, "Ctrl+N")
        button_bar.connect("load", self.load, "Ctrl+O")
        button_bar.connect("save", self.save, "Ctrl+S")
        for action in self.modes[mode].actions():
            button_bar.connect(
                action["name"], action["handler"], action["shortcut"]
            )
        button_bar.connect("zoom-in", self.zoom_in, "Ctrl++")
        button_bar.connect("zoom-out", self.zoom_out, "Ctrl+-")
        button_bar.connect("theme", self.toggle_theme, "F1")
        button_bar.connect("check", self.check_code, "F2")
        if sys.version_info[:2] >= (3, 6):
            button_bar.connect("tidy", self.tidy_code, "F10")
        button_bar.connect("help", self.show_help, "Ctrl+H")
        button_bar.connect("quit", self.quit, "Ctrl+Q")
        self._view.status_bar.set_mode(self.modes[mode].name)
        # Update references to default file locations.
        try:
            workspace_dir = self.modes[mode].workspace_dir()
            logger.info("Workspace directory: {}".format(workspace_dir))
        except Exception as e:
            # Avoid crashing if workspace_dir raises, use default path instead
            workspace_dir = self.modes["python"].workspace_dir()
            logger.error(
                (
                    "Could not open {} mode workspace directory, "
                    'due to exception "{}".'
                    "Using:\n\n{}\n\n...to store your code instead"
                ).format(mode, repr(e), workspace_dir)
            )
        # Reset remembered current path for load/save dialogs.
        self.current_path = ""
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
        self.show_status_message(
            _("Changed to {} mode.").format(self.modes[mode].name)
        )

    def autosave(self):
        """
        Cycles through each tab and, if changed, saves it to the filesystem.
        """
        if self._view.modified:
            # Something has changed, so save it!
            for tab in self._view.widgets:
                if tab.path and tab.isModified():
                    # Suppress error message on autosave attempts
                    self.save_tab_to_file(tab, show_error_messages=False)
                    logger.info(
                        "Autosave detected and saved "
                        "changes in {}.".format(tab.path)
                    )

    def ask_to_change_mode(self, new_mode, mode_name, heading):
        """
        Open a dialog asking the user, whether to change mode from
        mode_name to new_mode. The dialog can be customized by the
        heading-parameter.
        """
        # Only ask to switch mode if we're not already trying to
        # select a new mode via the dialog. Cannot change mode if
        # a script is already being run by the current mode.
        m = self.modes[self.mode]
        running = hasattr(m, "runner") and m.runner
        if (self.mode != new_mode and not self.selecting_mode) and not running:
            msg_body = _(
                "Would you like to change Mu to the {} " "mode?"
            ).format(mode_name)
            change_confirmation = self._view.show_confirmation(
                heading, msg_body, icon="Question"
            )
            if change_confirmation == QMessageBox.Ok:
                self.change_mode(new_mode)

    def device_changed(self, device):
        """
        Slot for receiving signals that the current device has changed.
        If the device change requires mode change, the user will be
        asked through a dialog.
        """
        if device:
            if self.current_device is None:
                heading = _("Detected new {} device.").format(device.name)
            else:
                heading = _("Device changed to {}.").format(device.name)
            self.ask_to_change_mode(
                device.short_mode_name, device.long_mode_name, heading
            )
        self.current_device = device

    def show_status_message(self, message, duration=5):
        """
        Displays the referenced message for duration seconds.
        """
        self._view.status_bar.set_message(message, duration * 1000)

    def debug_toggle_breakpoint(self, margin, line, modifiers):
        """
        How to handle the toggling of a breakpoint.
        """
        if (
            self.modes[self.mode].has_debugger
            or self.modes[self.mode].is_debugger
        ):
            tab = self._view.current_tab
            code = tab.text(line)
            if self.mode == "debugger":
                # The debugger is running.
                if is_breakpoint_line(code):
                    self.modes["debugger"].toggle_breakpoint(line, tab)
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
            msg = _("Cannot Set Breakpoint.")
            info = _(
                "Lines that are comments or some multi-line "
                "statements cannot have breakpoints."
            )
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
                    message = _("You cannot use the filename " '"{}"').format(
                        os.path.basename(new_path)
                    )
                    info = _(
                        "This name is already used by another part of "
                        "Python. If you use that name, things are "
                        "likely to break. Please try again with a "
                        "different filename."
                    )
                    self._view.show_message(message, info)
                    return
                logger.info(
                    "Attempting to rename {} to {}".format(tab.path, new_path)
                )
                # The user specified a path to a file.
                if not self.has_python_extension(os.path.basename(new_path)):
                    # No extension given, default to .py
                    new_path += ".py"
                # Check for duplicate path with currently open tab.
                for other_tab in self._view.widgets:
                    if other_tab.path == new_path:
                        logger.info(
                            "Cannot rename, a file of that name is "
                            "already open in Mu"
                        )
                        message = _("Could not rename file.")
                        information = _(
                            "A file of that name is already open " "in Mu."
                        )
                        self._view.show_message(message, information)
                        return
                # Finally rename
                tab.path = new_path
                logger.info("Renamed file to: {}".format(tab.path))
                self.save()

    def find_replace(self):
        """
        Handle find / replace functionality.

        If find/replace dialog is dismissed, do nothing.

        Otherwise, check there's something to find, warn if there isn't.

        If there is, find (and, optionally, replace) then confirm outcome with
        a status message.
        """
        result = self._view.show_find_replace(
            self.find, self.replace, self.global_replace
        )
        if result:
            self.find, self.replace, self.global_replace = result
            if self.find:
                if self.replace:
                    replaced = self._view.replace_text(
                        self.find, self.replace, self.global_replace
                    )
                    if replaced == 1:
                        msg = _('Replaced "{}" with "{}".')
                        self.show_status_message(
                            msg.format(self.find, self.replace)
                        )
                    elif replaced > 1:
                        msg = _('Replaced {} matches of "{}" with "{}".')
                        self.show_status_message(
                            msg.format(replaced, self.find, self.replace)
                        )
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
                message = _("You must provide something to find.")
                information = _(
                    "Please try again, this time with something "
                    "in the find box."
                )
                self._view.show_message(message, information)

    def find_again(self, forward=True):
        """
        Handle find again (F3 and Shift+F3) functionality.
        """
        if self.find:
            matched = self._view.highlight_text(self.find, forward)
            if matched:
                msg = _('Highlighting matches for "{}".')
            else:
                msg = _('Could not find "{}".')
            self.show_status_message(msg.format(self.find))
        else:
            message = _("You must provide something to find.")
            information = _(
                "Please try again, this time with something "
                "in the find box."
            )
            self._view.show_message(message, information)

    def find_again_backward(self, forward=False):
        """
        Handle find again backward (Shift+F3) functionality.
        """
        self.find_again(forward=False)

    def toggle_comments(self):
        """
        Ensure all highlighted lines are toggled between comments/uncommented.
        """
        self._view.toggle_comments()

    def tidy_code(self):
        """
        Prettify code with Black.
        """
        tab = self._view.current_tab
        if not tab or sys.version_info[:2] < (3, 6):
            return
        # Only works on Python, so abort.
        if tab.path and not self.has_python_extension(tab.path):
            return
        from black import format_str, FileMode, PY36_VERSIONS

        try:
            source_code = tab.text()
            logger.info("Tidy code.")
            logger.info(source_code)
            filemode = FileMode(
                target_versions=PY36_VERSIONS, line_length=MAX_LINE_LENGTH
            )
            tidy_code = format_str(source_code, mode=filemode)
            # The following bypasses tab.setText which resets the undo history.
            # Doing it this way means the user can use CTRL-Z to undo the
            # reformatting from black.
            tab.SendScintilla(tab.SCI_SETTEXT, tidy_code.encode("utf-8"))
            self.show_status_message(
                _("Successfully cleaned the code. " "Use CTRL-Z to undo.")
            )
        except Exception as ex:
            # The user's code is problematic. Recover with a modal dialog
            # containing a helpful message.
            logger.error(ex)
            message = _("Your code contains problems.")
            information = _(
                "These must be fixed before tidying will work. "
                "Please use the 'Check' button to highlight "
                "these problems."
            )
            self._view.show_message(message, information)

    def has_python_extension(self, filename):
        """
        Check whether the given filename matches recognized Python extensions.
        """
        file_ends = filename.lower().endswith
        return any(file_ends(ext) for ext in self.python_extensions)
