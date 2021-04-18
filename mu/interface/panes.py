"""
Contains the UI classes used to populate the various panes used by Mu.

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
import re
import platform
import logging
import signal
import string
import bisect
import os.path
import codecs

from PyQt5.QtCore import (
    Qt,
    QProcess,
    QProcessEnvironment,
    pyqtSignal,
    QTimer,
    QUrl,
)
from collections import deque
from PyQt5.QtWidgets import (
    QMessageBox,
    QTextEdit,
    QFrame,
    QListWidget,
    QGridLayout,
    QLabel,
    QMenu,
    QApplication,
    QTreeView,
)
from PyQt5.QtGui import (
    QKeySequence,
    QTextCursor,
    QCursor,
    QPainter,
    QDesktopServices,
    QStandardItem,
)
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from ..i18n import language_code
from mu.interface.themes import Font, DEFAULT_FONT_SIZE
from mu.interface.themes import DAY_STYLE, NIGHT_STYLE, CONTRAST_STYLE


logger = logging.getLogger(__name__)


CHARTS = True
try:  # pragma: no cover
    from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis
except ImportError:  # pragma: no cover
    logger.info("Unable to find QChart. Plotter button will not display.")
    QChartView = object
    CHARTS = False


PANE_ZOOM_SIZES = {
    "xs": 8,
    "s": 10,
    "m": 14,
    "l": 16,
    "xl": 18,
    "xxl": 24,
    "xxxl": 28,
}


class JupyterREPLPane(RichJupyterWidget):
    """
    REPL = Read, Evaluate, Print, Loop.

    Displays a Jupyter iPython session.
    """

    on_append_text = pyqtSignal(bytes)

    def __init__(self, theme="day", parent=None):
        super().__init__(parent)
        self.set_theme(theme)
        self.console_height = 10

    def _append_plain_text(self, text, *args, **kwargs):
        """
        Ensures appended text is emitted as a signal with associated bytes.
        """
        super()._append_plain_text(text, *args, **kwargs)
        self.on_append_text.emit(text.encode("utf-8"))

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        font = self.font
        font.setPointSize(new_size)
        self._set_font(font)

    def set_zoom(self, size):
        """
        Set the current zoom level given the "t-shirt" size.
        """
        self.set_font_size(PANE_ZOOM_SIZES[size])

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == "contrast":
            self.style_sheet = CONTRAST_STYLE
            self.syntax_style = "bw"
        elif theme == "night":
            self.style_sheet = NIGHT_STYLE
            self.syntax_style = "monokai"
        else:
            self.style_sheet = DAY_STYLE
            self.syntax_style = "default"

    def setFocus(self):
        """
        Override base setFocus so the focus happens to the embedded _control
        within this widget.
        """
        self._control.setFocus()


VT100_RETURN = b"\r"
VT100_BACKSPACE = b"\b"
VT100_DELETE = b"\x1B[\x33\x7E"
VT100_UP = b"\x1B[A"
VT100_DOWN = b"\x1B[B"
VT100_RIGHT = b"\x1B[C"
VT100_LEFT = b"\x1B[D"
VT100_HOME = b"\x1B[H"
VT100_END = b"\x1B[F"


class MicroPythonREPLPane(QTextEdit):
    """
    REPL = Read, Evaluate, Print, Loop.

    This widget represents a REPL client connected to a device running
    MicroPython.

    The device MUST be flashed with MicroPython for this to work.
    """

    def __init__(self, connection, theme="day", parent=None):
        super().__init__(parent)
        self.connection = connection
        self.setFont(Font().load())
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setUndoRedoEnabled(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        # The following variable maintains the position where we know
        # the device cursor is placed. It is initialized to the beginning
        # of the QTextEdit (i.e. equal to the Qt cursor position)
        self.device_cursor_position = self.textCursor().position()
        self.setObjectName("replpane")
        self.set_theme(theme)
        self.unprocessed_input = b""  # used by process_bytes
        self.decoder = codecs.getincrementaldecoder("utf8")("replace")
        self.vt100_regex = re.compile(
            r"\x1B\[(?P<count>[\d]*)(;?[\d]*)*(?P<action>[A-Za-z])"
        )

    def paste(self):
        """
        Grabs clipboard contents then sends to the REPL.
        """
        clipboard = QApplication.clipboard()
        if clipboard and clipboard.text():
            to_paste = (
                clipboard.text().replace("\n", "\r").replace("\r\r", "\r")
            )
            self.connection.write(bytes(to_paste, "utf8"))

    def context_menu(self):
        """
        Creates custom context menu with just copy and paste.
        """
        menu = QMenu(self)
        if platform.system() == "Darwin":
            copy_keys = QKeySequence(Qt.CTRL + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.Key_V)
        else:
            copy_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_V)

        menu.addAction("Copy", self.copy, copy_keys)
        menu.addAction("Paste", self.paste, paste_keys)
        menu.exec_(QCursor.pos())

    def set_theme(self, theme):
        pass

    def send(self, msg):
        self.connection.write(msg)

    def keyPressEvent(self, data):
        """
        Called when the user types something in the REPL.

        Correctly encodes it and sends it to the connected device.
        """
        tc = self.textCursor()
        key = data.key()
        ctrl_only = data.modifiers() == Qt.ControlModifier
        meta_only = data.modifiers() == Qt.MetaModifier
        ctrl_shift_only = (
            data.modifiers() == Qt.ControlModifier | Qt.ShiftModifier
        )
        shift_down = data.modifiers() & Qt.ShiftModifier
        on_osx = platform.system() == "Darwin"

        if key == Qt.Key_Return:
            # Move cursor to the end of document before sending carriage return
            tc.movePosition(QTextCursor.End, mode=QTextCursor.MoveAnchor)
            self.device_cursor_position = tc.position()
            self.send(VT100_RETURN)
        elif key == Qt.Key_Backspace:
            if not self.delete_selection():
                self.send(VT100_BACKSPACE)
        elif key == Qt.Key_Delete:
            if not self.delete_selection():
                self.send(VT100_DELETE)
        elif key == Qt.Key_Up:
            self.send(VT100_UP)
        elif key == Qt.Key_Down:
            self.send(VT100_DOWN)
        elif key == Qt.Key_Right:
            if shift_down:
                # Text selection - pass down
                super().keyPressEvent(data)
            elif tc.hasSelection():
                self.move_cursor_to(tc.selectionEnd())
            else:
                self.send(VT100_RIGHT)
        elif key == Qt.Key_Left:
            if shift_down:
                # Text selection - pass down
                super().keyPressEvent(data)
            elif tc.hasSelection():
                self.move_cursor_to(tc.selectionStart())
            else:
                self.send(VT100_LEFT)
        elif key == Qt.Key_Home:
            self.send(VT100_HOME)
        elif key == Qt.Key_End:
            self.send(VT100_END)
        elif (on_osx and meta_only) or (not on_osx and ctrl_only):
            # Handle the Control key. On OSX/macOS/Darwin (python calls this
            # platform Darwin), this is handled by Qt.MetaModifier. Other
            # platforms (Linux, Windows) call this Qt.ControlModifier. Go
            # figure. See http://doc.qt.io/qt-5/qt.html#KeyboardModifier-enum
            if Qt.Key_A <= key <= Qt.Key_Z:
                # The microbit treats an input of \x01 as Ctrl+A, etc.
                self.send(bytes([1 + key - Qt.Key_A]))
        elif ctrl_shift_only or (on_osx and ctrl_only):
            # Command-key on Mac, Ctrl-Shift on Win/Lin
            if key == Qt.Key_C:
                self.copy()
            elif key == Qt.Key_V:
                self.delete_selection()
                self.paste()
        else:
            self.delete_selection()
            self.send(bytes(data.text(), "utf8"))

    def set_qtcursor_to_devicecursor(self):
        """
        Resets the Qt TextCursor to where we know the device has the cursor
        placed.
        """
        tc = self.textCursor()
        tc.setPosition(self.device_cursor_position)
        self.setTextCursor(tc)

    def set_devicecursor_to_qtcursor(self):
        """
        Call this whenever the cursor has been moved by the user, to send
        the cursor movement to the device.
        """
        self.move_cursor_to(self.textCursor().position())

    def move_cursor_to(self, new_position):
        """Move the cursor, by sending vt100 left/right signals through
        serial. The Qt cursor is first returned to the known location
        of the device cursor.  Then the appropriate number of move
        left or right signals are send.  The Qt cursor is not moved to
        the new_position here, but will be moved once receiving a
        response (in process_tty_data).
        """
        # Reset Qt cursor position
        self.set_qtcursor_to_devicecursor()
        # Calculate number of steps
        steps = new_position - self.device_cursor_position
        # Send the appropriate right/left moves
        if steps > 0:
            # Move cursor right if positive
            self.send(VT100_RIGHT * steps)
        elif steps < 0:
            # Move cursor left if negative
            self.send(VT100_LEFT * abs(steps))

    def delete_selection(self):
        """
        Returns true if deletion happened, returns false if there was no
        selection to delete.
        """
        tc = self.textCursor()
        if tc.hasSelection():
            # Calculate how much should be deleted (N)
            selectionSize = tc.selectionEnd() - tc.selectionStart()
            # Move cursor to end of selection
            self.move_cursor_to(tc.selectionEnd())
            # Send N backspaces
            self.send(VT100_BACKSPACE * selectionSize)
            return True
        return False

    def mouseReleaseEvent(self, mouseEvent):
        """Called whenever a user have had a mouse button pressed, and
        releases it. We pass it through to the normal way Qt handles
        button pressed, but also sends as cursor movement signal to
        the device (except if a selection is made, for selections we first
        move the cursor on deselection)
        """
        super().mouseReleaseEvent(mouseEvent)

        # If when a user have clicked and not made a selection
        # move the device cursor to where the user clicked
        if not self.textCursor().hasSelection():
            self.set_devicecursor_to_qtcursor()

    def process_tty_data(self, data):
        """
        Given some incoming bytes of data, work out how to handle / display
        them in the REPL widget.
        If received input is incomplete, stores remainder in
        self.unprocessed_input.

        Updates the self.device_cursor_position to match that of the device
        for every input received.
        """
        i = 0
        data = self.decoder.decode(data)
        if len(self.unprocessed_input) > 0:
            # Prepend bytes from last time, that wasn't processed
            data = self.unprocessed_input + data
            self.unprocessed_input = ""

        # Reset cursor. E.g. if doing a selection, the qt cursor and
        # device cursor will not match, we reset it here to make sure
        # they do match (this removes any selections when new input is
        # received)
        self.set_qtcursor_to_devicecursor()
        tc = self.textCursor()

        while i < len(data):
            if data[i] == "\b":
                tc.movePosition(QTextCursor.Left)
                self.device_cursor_position = tc.position()
            elif data[i] == "\r":
                # Carriage return. Do nothing, we handle newlines when
                # reading \n
                pass
            elif data[i] == "\x1b":
                # Escape
                if len(data) > i + 1 and data[i + 1] == "[":
                    # VT100 cursor detected: <Esc>[
                    match = self.vt100_regex.search(data[i:])
                    if match:
                        # move to (almost) after control seq
                        # (will ++ at end of loop)
                        i += match.end() - 1
                        count_string = match.group("count")
                        count = 1 if count_string == "" else int(count_string)
                        action = match.group("action")
                        if action == "A":  # up
                            tc.movePosition(QTextCursor.Up, n=count)
                            self.device_cursor_position = tc.position()
                        elif action == "B":  # down
                            tc.movePosition(QTextCursor.Down, n=count)
                            self.device_cursor_position = tc.position()
                        elif action == "C":  # right
                            tc.movePosition(QTextCursor.Right, n=count)
                            self.device_cursor_position = tc.position()
                        elif action == "D":  # left
                            tc.movePosition(QTextCursor.Left, n=count)
                            self.device_cursor_position = tc.position()
                        elif action == "K":  # delete things
                            if count_string == "":  # delete to end of line
                                tc.movePosition(
                                    QTextCursor.EndOfLine,
                                    mode=QTextCursor.KeepAnchor,
                                )
                                tc.removeSelectedText()
                                self.device_cursor_position = tc.position()
                        else:
                            # Unknown action, log warning and ignore
                            command = match.group(0).replace("\x1B", "<Esc>")
                            msg = "Received unsupported VT100 command: {}"
                            logger.warning(msg.format(command))
                    else:
                        # Cursor detected, but no match, must be
                        # incomplete input
                        self.unprocessed_input = data[i:]
                        break
                elif len(data) == i + 1:
                    # Escape received as end of transmission. Perhaps
                    # the transmission is incomplete, wait until next
                    # bytes are received to determine what to do
                    self.unprocessed_input = data[i:]
                    break
            elif data[i] == "\n":
                tc.movePosition(QTextCursor.End)
                self.device_cursor_position = tc.position() + 1
                self.setTextCursor(tc)
                self.insertPlainText(data[i])
            else:
                # Char received, with VT100 that should be interpreted
                # as overwrite the char in front of the cursor
                tc.deleteChar()
                self.device_cursor_position = tc.position() + 1
                self.insertPlainText(data[i])
            self.setTextCursor(tc)
            i += 1
        # Scroll textarea if necessary to see cursor
        self.ensureCursorVisible()

    def clear(self):
        """
        Clears the text of the REPL.
        """
        self.setText("")

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        font = self.font()
        font.setPointSize(new_size)
        self.setFont(font)

    def set_zoom(self, size):
        """
        Set the current zoom level given the "t-shirt" size.
        """
        self.set_font_size(PANE_ZOOM_SIZES[size])


class MuFileList(QListWidget):
    """
    Contains shared methods for the two types of file listing used in Mu.
    """

    disable = pyqtSignal()
    list_files = pyqtSignal()
    set_message = pyqtSignal(str)

    def show_confirm_overwrite_dialog(self):
        """
        Display a dialog to check if an existing file should be overwritten.

        Returns a boolean indication of the user's decision.
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(_("File already exists; overwrite it?"))
        msg.setWindowTitle(_("File already exists"))
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec_() == QMessageBox.Ok


class MicroPythonDeviceFileList(MuFileList):
    """
    Represents a list of files on a MicroPython device.
    """

    put = pyqtSignal(str)
    delete = pyqtSignal(str)

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.setDragDropMode(QListWidget.DragDrop)

    def dropEvent(self, event):
        source = event.source()
        if isinstance(source, LocalFileList):
            file_exists = self.findItems(
                source.currentItem().text(), Qt.MatchExactly
            )
            if (
                not file_exists
                or file_exists
                and self.show_confirm_overwrite_dialog()
            ):
                self.disable.emit()
                local_filename = os.path.join(
                    self.home, source.currentItem().text()
                )
                msg = _("Copying '{}' to device.").format(local_filename)
                logger.info(msg)
                self.set_message.emit(msg)
                self.put.emit(local_filename)

    def on_put(self, microbit_file):
        """
        Fired when the put event is completed for the given filename.
        """
        msg = _("'{}' successfully copied to device.").format(microbit_file)
        self.set_message.emit(msg)
        self.list_files.emit()

    def contextMenuEvent(self, event):
        menu_current_item = self.currentItem()
        if menu_current_item is None:
            return
        menu = QMenu(self)
        delete_action = menu.addAction(_("Delete (cannot be undone)"))
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == delete_action:
            self.disable.emit()
            microbit_filename = menu_current_item.text()
            logger.info("Deleting {}".format(microbit_filename))
            msg = _("Deleting '{}' from device.").format(microbit_filename)
            logger.info(msg)
            self.set_message.emit(msg)
            self.delete.emit(microbit_filename)

    def on_delete(self, microbit_file):
        """
        Fired when the delete event is completed for the given filename.
        """
        msg = _("'{}' successfully deleted from device.").format(microbit_file)
        self.set_message.emit(msg)
        self.list_files.emit()


class LocalFileList(MuFileList):
    """
    Represents a list of files in the Mu directory on the local machine.
    """

    get = pyqtSignal(str, str)
    put = pyqtSignal(str, str)
    open_file = pyqtSignal(str)

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.setDragDropMode(QListWidget.DragDrop)

    def dropEvent(self, event):
        source = event.source()
        if isinstance(source, MicroPythonDeviceFileList):
            file_exists = self.findItems(
                source.currentItem().text(), Qt.MatchExactly
            )
            if (
                not file_exists
                or file_exists
                and self.show_confirm_overwrite_dialog()
            ):
                self.disable.emit()
                microbit_filename = source.currentItem().text()
                local_filename = os.path.join(self.home, microbit_filename)
                msg = _(
                    "Getting '{}' from device. " "Copying to '{}'."
                ).format(microbit_filename, local_filename)
                logger.info(msg)
                self.set_message.emit(msg)
                self.get.emit(microbit_filename, local_filename)

    def on_get(self, microbit_file):
        """
        Fired when the get event is completed for the given filename.
        """
        msg = _(
            "Successfully copied '{}' " "from the device to your computer."
        ).format(microbit_file)
        self.set_message.emit(msg)
        self.list_files.emit()

    def contextMenuEvent(self, event):
        menu_current_item = self.currentItem()
        if menu_current_item is None:
            return
        local_filename = menu_current_item.text()
        # Get the file extension
        ext = os.path.splitext(local_filename)[1].lower()
        menu = QMenu(self)
        open_internal_action = None
        # Mu micro:bit mode only handles .py & .hex
        if ext == ".py" or ext == ".hex":
            open_internal_action = menu.addAction(_("Open in Mu"))
        if ext == ".py":
            write_to_main_action = menu.addAction(
                _("Write to main.py on device")
            )
        # Open outside Mu (things get meta if Mu is the default application)
        open_action = menu.addAction(_("Open"))
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == open_action:
            # Get the file's path
            path = os.path.abspath(os.path.join(self.home, local_filename))
            logger.info("Opening {}".format(path))
            msg = _("Opening '{}'").format(local_filename)
            logger.info(msg)
            self.set_message.emit(msg)
            # Let Qt work out how to open it
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        elif action == open_internal_action:
            logger.info("Open {} internally".format(local_filename))
            # Get the file's path
            path = os.path.join(self.home, local_filename)
            # Send the signal bubbling up the tree
            self.open_file.emit(path)
        elif action == write_to_main_action:
            path = os.path.join(self.home, local_filename)
            self.put.emit(path, "main.py")


class FileSystemPane(QFrame):
    """
    Contains two QListWidgets representing the micro:bit and the user's code
    directory. Users transfer files by dragging and dropping. Highlighted files
    can be selected for deletion.
    """

    set_message = pyqtSignal(str)
    set_warning = pyqtSignal(str)
    list_files = pyqtSignal()
    open_file = pyqtSignal(str)

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.font = Font().load()
        microbit_fs = MicroPythonDeviceFileList(home)
        local_fs = LocalFileList(home)

        @local_fs.open_file.connect
        def on_open_file(file):
            # Bubble the signal up
            self.open_file.emit(file)

        layout = QGridLayout()
        self.setLayout(layout)
        microbit_label = QLabel()
        microbit_label.setText(_("Files on your device:"))
        local_label = QLabel()
        local_label.setText(_("Files on your computer:"))
        self.microbit_label = microbit_label
        self.local_label = local_label
        self.microbit_fs = microbit_fs
        self.local_fs = local_fs
        self.set_font_size()
        layout.addWidget(microbit_label, 0, 0)
        layout.addWidget(local_label, 0, 1)
        layout.addWidget(microbit_fs, 1, 0)
        layout.addWidget(local_fs, 1, 1)
        self.microbit_fs.disable.connect(self.disable)
        self.microbit_fs.set_message.connect(self.show_message)
        self.local_fs.disable.connect(self.disable)
        self.local_fs.set_message.connect(self.show_message)

    def disable(self):
        """
        Stops interaction with the list widgets.
        """
        self.microbit_fs.setDisabled(True)
        self.local_fs.setDisabled(True)
        self.microbit_fs.setAcceptDrops(False)
        self.local_fs.setAcceptDrops(False)

    def enable(self):
        """
        Allows interaction with the list widgets.
        """
        self.microbit_fs.setDisabled(False)
        self.local_fs.setDisabled(False)
        self.microbit_fs.setAcceptDrops(True)
        self.local_fs.setAcceptDrops(True)

    def show_message(self, message):
        """
        Emits the set_message signal.
        """
        self.set_message.emit(message)

    def show_warning(self, message):
        """
        Emits the set_warning signal.
        """
        self.set_warning.emit(message)

    def on_ls(self, microbit_files):
        """
        Displays a list of the files on the micro:bit.

        Since listing files is always the final event in any interaction
        between Mu and the micro:bit, this enables the controls again for
        further interactions to take place.
        """
        self.microbit_fs.clear()
        self.local_fs.clear()
        for f in microbit_files:
            self.microbit_fs.addItem(f)
        local_files = [
            f
            for f in os.listdir(self.home)
            if os.path.isfile(os.path.join(self.home, f))
        ]
        local_files.sort()
        for f in local_files:
            self.local_fs.addItem(f)
        self.enable()

    def on_ls_fail(self):
        """
        Fired when listing files fails.
        """
        self.show_warning(
            _(
                "There was a problem getting the list of files on "
                "the device. Please check Mu's logs for "
                "technical information. Alternatively, try "
                "unplugging/plugging-in your device and/or "
                "restarting Mu."
            )
        )
        self.disable()

    def on_put_fail(self, filename):
        """
        Fired when the referenced file cannot be copied onto the device.
        """
        self.show_warning(
            _(
                "There was a problem copying the file '{}' onto "
                "the device. Please check Mu's logs for "
                "more information."
            ).format(filename)
        )

    def on_delete_fail(self, filename):
        """
        Fired when a deletion on the device for the given file failed.
        """
        self.show_warning(
            _(
                "There was a problem deleting '{}' from the "
                "device. Please check Mu's logs for "
                "more information."
            ).format(filename)
        )

    def on_get_fail(self, filename):
        """
        Fired when getting the referenced file on the device failed.
        """
        self.show_warning(
            _(
                "There was a problem getting '{}' from the "
                "device. Please check Mu's logs for "
                "more information."
            ).format(filename)
        )

    def set_theme(self, theme):
        pass

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        self.font.setPointSize(new_size)
        self.microbit_label.setFont(self.font)
        self.local_label.setFont(self.font)
        self.microbit_fs.setFont(self.font)
        self.local_fs.setFont(self.font)

    def set_zoom(self, size):
        """
        Set the current zoom level given the "t-shirt" size.
        """
        self.set_font_size(PANE_ZOOM_SIZES[size])


class PythonProcessPane(QTextEdit):
    """
    Handles / displays a Python process's stdin/out with working command
    history and simple buffer editing.
    """

    on_append_text = pyqtSignal(bytes)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(Font().load())
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setUndoRedoEnabled(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.running = False  # Flag to show the child process is running.
        self.setObjectName("PythonRunner")
        self.process = None  # Will eventually reference the running process.
        self.input_history = []  # history of inputs entered in this session.
        self.start_of_current_line = 0  # start position of the input line.
        self.history_position = 0  # current position when navigation history.
        self.stdout_buffer = b""  # contains non-decoded bytes from stdout.
        self.reading_stdout = False  # flag showing if already reading stdout.

    def start_process(
        self,
        interpreter,
        script_name,
        working_directory,
        interactive=True,
        debugger=False,
        command_args=None,
        envars=None,
        python_args=None,
    ):
        """
        Start the child Python process.

        Will use the referenced interpreter to run the Python
        script_name within the context of the working directory.

        If interactive is True (the default) the Python process will run in
        interactive mode (dropping the user into the REPL when the script
        completes).

        If debugger is True (the default is False) then the script will run
        within a debug runner session.

        If there is a list of command_args (the default is None), then these
        will be passed as further arguments into the script to be run.

        If there is a list of environment variables, these will be part of the
        context of the new child process.

        If python_args is given, these are passed as arguments to the Python
        interpreter used to launch the child process.
        """
        if not envars:  # Envars must be a list if not passed a value.
            envars = []
        envars = [(name, v) for (name, v) in envars if name != "PYTHONPATH"]
        self.script = ""
        if script_name:
            self.script = os.path.abspath(os.path.normcase(script_name))
        logger.info("Running script: {}".format(self.script))
        logger.info("Using interpreter: {}".format(interpreter))
        if interactive:
            logger.info("Running with interactive mode.")
        if command_args is None:
            command_args = []
        logger.info("Command args: {}".format(command_args))
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        # Force buffers to flush immediately.
        env = QProcessEnvironment.systemEnvironment()
        env.insert("PYTHONUNBUFFERED", "1")
        env.insert("PYTHONIOENCODING", "utf-8")
        if sys.platform == "darwin":
            # Ensure the correct encoding is set for the environment. If the
            # following two lines are not set, then Flask will complain about
            # Python 3 being misconfigured to use ASCII encoding.
            # See: https://click.palletsprojects.com/en/7.x/python3/
            encoding = "{}.utf-8".format(language_code)
            env.insert("LC_ALL", encoding)
            env.insert("LANG", encoding)
        # Manage environment variables that may have been set by the user.
        if envars:
            logger.info(
                "Running with environment variables: " "{}".format(envars)
            )
            for name, value in envars:
                env.insert(name, value)
        logger.info("Working directory: {}".format(working_directory))
        self.process.setWorkingDirectory(working_directory)
        self.process.readyRead.connect(self.try_read_from_stdout)
        self.process.finished.connect(self.finished)
        logger.info("Python path: {}".format(sys.path))
        if debugger:
            # Start the mu_debug runner for the script.
            parent_dir = os.path.join(os.path.dirname(__file__), "..")
            mu_dir = os.path.abspath(parent_dir)
            logger.info("mu_dir: %s", mu_dir)
            runner = os.path.join(mu_dir, "mu_debug.py")
            args = [runner, self.script] + command_args
            #
            # The runtime virtualenvironment doesn't include Mu
            # itself (by design). But the debugger needs mu in
            # order to run, so we temporarily set the PYTHONPATH
            # to point to Mu's own directory
            #
            env.insert(
                "PYTHONPATH", os.path.abspath(os.path.join(mu_dir, ".."))
            )
            self.process.setProcessEnvironment(env)
            self.process.start(interpreter, args)
        else:
            args = []
            if self.script:
                if interactive:
                    # Start the script in interactive Python mode.
                    args = ["-i", self.script] + command_args
                else:
                    # Just run the command with no additional flags.
                    args = [self.script] + command_args
            if python_args:
                args = python_args + args
            logger.info("Args: {}".format(args))
            self.process.setProcessEnvironment(env)
            self.process.start(interpreter, args)
            self.running = True

    def finished(self, code, status):
        """
        Handle when the child process finishes.
        """
        self.running = False
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText("\n\n---------- FINISHED ----------\n")
        msg = "exit code: {} status: {}".format(code, status)
        cursor.insertText(msg)
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.setReadOnly(True)

    def context_menu(self):
        """
        Creates custom context menu with just copy and paste.
        """
        menu = QMenu(self)
        if platform.system() == "Darwin":
            copy_keys = QKeySequence(Qt.CTRL + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.Key_V)
        else:
            copy_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_V)
        menu.addAction("Copy", self.copy, copy_keys)
        menu.addAction("Paste", self.paste, paste_keys)
        menu.exec_(QCursor.pos())

    def paste(self):
        """
        Grabs clipboard contents then writes to the REPL.
        """
        clipboard = QApplication.clipboard()
        if clipboard and clipboard.text():
            # normalize for Windows line-ends.
            text = "\n".join(clipboard.text().splitlines())
            if text:
                self.parse_paste(text)

    def parse_paste(self, text):
        """
        Recursively takes characters from text to be parsed as input. We do
        this so the event loop has time to respond to output from the process
        to which the characters are sent (for example, when a newline is sent).

        Yes, this is a quick and dirty hack, but ensures the pasted input is
        also evaluated in an interactive manner rather than as a single-shot
        splurge of data. Essentially, it's simulating someone typing in the
        characters of the pasted text *really fast* but in such a way that the
        event loop cycles.
        """
        character = text[0]  # the current character to process.
        remainder = text[1:]  # remaining characters to process in the future.
        if character.isprintable() or character in string.printable:
            if character == "\n" or character == "\r":
                self.parse_input(Qt.Key_Enter, character, None)
            else:
                self.parse_input(None, character, None)
        if remainder:
            # Schedule a recursive call of parse_paste with the remaining text
            # to process. This allows the event loop to cycle and handle any
            # output from the child process as a result of the text pasted so
            # far (especially useful for handling responses from newlines).
            QTimer.singleShot(2, lambda text=remainder: self.parse_paste(text))

    def keyPressEvent(self, data):
        """
        Called when the user types something in the REPL.
        """
        key = data.key()
        text = data.text()
        modifiers = data.modifiers()
        self.parse_input(key, text, modifiers)

    def on_process_halt(self):
        """
        Called when the the user has manually halted a running process. Ensures
        that the remaining data from the halted process's stdout is handled
        properly.

        When the process is halted the user is dropped into the Python prompt
        and this method ensures the UI is updated in a clean, non-blocking
        way.
        """
        data = self.process.readAll().data()
        if data:
            while True:
                try:
                    self.append(data)
                    self.on_append_text.emit(data)
                    self.set_start_of_current_line()
                    break
                except UnicodeDecodeError:
                    # Discard problematic start byte and try again.
                    # (This may be caused by a split in multi-byte characters).
                    data = data[1:]

    def parse_input(self, key, text, modifiers):
        """
        Correctly encodes user input and sends it to the connected process.

        The key is a Qt.Key_Something value, text is the textual representation
        of the input, and modifiers are the control keys (shift, CTRL, META,
        etc) also used.
        """
        msg = b""  # Eventually to be inserted into the pane at the cursor.
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            msg = b"\n"
        elif (
            platform.system() == "Darwin" and modifiers == Qt.MetaModifier
        ) or (
            platform.system() != "Darwin" and modifiers == Qt.ControlModifier
        ):
            # Handle CTRL-C and CTRL-D
            if self.process and self.running:
                pid = self.process.processId()
                # NOTE: Windows related constraints don't allow us to send a
                # CTRL-C, rather, the process will just terminate.
                halt_flag = False
                if key == Qt.Key_C:
                    halt_flag = True
                    os.kill(pid, signal.SIGINT)
                if key == Qt.Key_D:
                    halt_flag = True
                    self.process.kill()
                if halt_flag:
                    # Clean up from kill signal.
                    self.process.readAll()  # Discard queued output.
                    self.stdout_buffer = b""
                    # Schedule update of the UI after the process halts (in
                    # next iteration of the event loop).
                    QTimer.singleShot(1, self.on_process_halt)
                    return
        elif key == Qt.Key_Up:
            self.history_back()
        elif key == Qt.Key_Down:
            self.history_forward()
        elif key == Qt.Key_Right:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Right)
            self.setTextCursor(cursor)
        elif key == Qt.Key_Left:
            cursor = self.textCursor()
            if cursor.position() > self.start_of_current_line:
                cursor.movePosition(QTextCursor.Left)
                self.setTextCursor(cursor)
        elif key == Qt.Key_Home:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            buffer_len = len(self.toPlainText()) - self.start_of_current_line
            for i in range(buffer_len):
                cursor.movePosition(QTextCursor.Left)
            self.setTextCursor(cursor)
        elif key == Qt.Key_End:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
        elif (modifiers == Qt.ControlModifier | Qt.ShiftModifier) or (
            platform.system() == "Darwin" and modifiers == Qt.ControlModifier
        ):
            # Command-key on Mac, Ctrl-Shift on Win/Lin
            if key == Qt.Key_C:
                self.copy()
            elif key == Qt.Key_V:
                self.paste()
        elif text.isprintable():
            # If the key is for a printable character then add it to the
            # active buffer and display it.
            msg = bytes(text, "utf8")
        if key == Qt.Key_Backspace:
            self.backspace()
        if key == Qt.Key_Delete:
            self.delete()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            # First move cursor to the end of the line and insert newline in
            # case return/enter is pressed while the cursor is in the
            # middle of the line
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            self.insert(msg)
            # Then write line to std_in and add to history
            content = self.toPlainText()
            line = content[self.start_of_current_line :].encode("utf-8")
            self.write_to_stdin(line)
            if line.strip():
                self.input_history.append(line.replace(b"\n", b""))
            self.history_position = 0
            self.set_start_of_current_line()
        elif not self.isReadOnly() and msg:
            self.insert(msg)

    def set_start_of_current_line(self):
        """
        Set the flag to indicate the start of the current line (used before
        waiting for input).

        This flag is used to discard the preceeding text in the text entry
        field when Mu parses new input from the user (i.e. any text beyond the
        self.start_of_current_line).
        """
        self.start_of_current_line = len(self.toPlainText())

    def history_back(self):
        """
        Replace the current input line with the next item BACK from the
        current history position.
        """
        if self.input_history:
            self.history_position -= 1
            history_pos = len(self.input_history) + self.history_position
            if history_pos < 0:
                self.history_position += 1
                history_pos = 0
            history_item = self.input_history[history_pos]
            self.replace_input_line(history_item)

    def history_forward(self):
        """
        Replace the current input line with the next item FORWARD from the
        current history position.
        """
        if self.input_history:
            self.history_position += 1
            history_pos = len(self.input_history) + self.history_position
            if history_pos >= len(self.input_history):
                # At the most recent command.
                self.history_position = 0
                self.clear_input_line()
                return
            history_item = self.input_history[history_pos]
            self.replace_input_line(history_item)

    def try_read_from_stdout(self):
        """
        Ensure reading from stdout only happens if there is NOT already current
        attempts to read from stdout.
        """
        if not self.reading_stdout:
            self.reading_stdout = True
            self.read_from_stdout()

    def read_from_stdout(self):
        """
        Process incoming data from the process's stdout.
        """
        data = self.process.read(256)
        if data:
            data = self.stdout_buffer + data
            try:
                self.append(data)
                self.on_append_text.emit(data)
                self.set_start_of_current_line()
                self.stdout_buffer = b""
            except UnicodeDecodeError:
                self.stdout_buffer = data
            QTimer.singleShot(2, self.read_from_stdout)
        else:
            self.reading_stdout = False

    def write_to_stdin(self, data):
        """
        Writes data from the Qt application to the child process's stdin.
        """
        if self.process:
            self.process.write(data)

    def append(self, msg):
        """
        Append text to the text area.
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(msg.decode("utf-8"))
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def insert(self, msg):
        """
        Insert text to the text area at the current cursor position.
        """
        cursor = self.textCursor()
        if cursor.position() < self.start_of_current_line:
            cursor.movePosition(QTextCursor.End)
        cursor.insertText(msg.decode("utf-8"))
        self.setTextCursor(cursor)

    def backspace(self):
        """
        Removes a character from the current buffer -- to the left of cursor.
        """
        cursor = self.textCursor()
        if cursor.position() > self.start_of_current_line:
            cursor = self.textCursor()
            cursor.deletePreviousChar()
            self.setTextCursor(cursor)

    def delete(self):
        """
        Removes a character from the current buffer -- to the right of cursor.
        """
        cursor = self.textCursor()
        if cursor.position() >= self.start_of_current_line:
            cursor.deleteChar()
            self.setTextCursor(cursor)

    def clear_input_line(self):
        """
        Remove all the characters currently in the input buffer line.
        """
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        buffer_len = len(self.toPlainText()) - self.start_of_current_line
        for i in range(buffer_len):
            cursor.deletePreviousChar()
        self.setTextCursor(cursor)

    def replace_input_line(self, text):
        """
        Replace the current input line with the passed in text.
        """
        self.clear_input_line()
        self.append(text)

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        f = self.font()
        f.setPointSize(new_size)
        self.setFont(f)

    def set_zoom(self, size):
        """
        Set the current zoom level given the "t-shirt" size.
        """
        self.set_font_size(PANE_ZOOM_SIZES[size])

    def set_theme(self, theme):
        pass


class DebugInspectorItem(QStandardItem):
    def __init__(self, *args):
        super().__init__(*args)
        self.setEditable(False)


class DebugInspector(QTreeView):
    """
    Presents a tree like representation of the current state of the call stack
    to the user.
    """

    def __init__(self):
        super().__init__()
        self.setUniformRowHeights(True)
        self.setSelectionBehavior(QTreeView.SelectRows)
        # Record row expansion/collapse to keep dicts expanded on update
        self.expanded.connect(self.record_expanded)
        self.collapsed.connect(self.record_collapsed)
        self.expanded_dicts = set()

    def record_expanded(self, index):
        """
        Keep track of expanded dicts for displaying in debugger.
        """
        expanded = self.model().itemFromIndex(index).text()
        self.expanded_dicts.add(expanded)

    def record_collapsed(self, index):
        """
        Remove collapsed dicts from set, so they render collapsed.
        """
        collapsed = self.model().itemFromIndex(index).text()
        if collapsed in self.expanded_dicts:
            self.expanded_dicts.remove(collapsed)

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        stylesheet = (
            "QWidget{font-size: "
            + str(new_size)
            + "pt; font-family: Monospace;}"
        )
        self.setStyleSheet(stylesheet)

    def set_zoom(self, size):
        """
        Set the current zoom level given the "t-shirt" size.
        """
        self.set_font_size(PANE_ZOOM_SIZES[size])

    def set_theme(self, theme):
        pass


class PlotterPane(QChartView):
    """
    This plotter widget makes viewing sensor data easy!

    This widget represents a chart that will look for tuple data from
    the MicroPython REPL, Python 3 REPL or Python 3 code runner and will
    auto-generate a graph.
    """

    data_flood = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Holds the raw input to be checked for actionable data to display.
        self.input_buffer = []
        # Holds the raw actionable data detected while plotting.
        self.raw_data = []
        self.setObjectName("plotterpane")
        # Number of datapoints to show (caps at self.max_x)
        self.num_datapoints = 0
        self.lookback = 500
        self.max_x = 100  # Maximum value along x axis
        self.max_y = 1000  # Maximum value +/- along y axis
        self.min_y = -1000
        self.flooded = False  # Flag to indicate if data flooding is happening.

        # Holds deques for each slot of incoming data (assumes 1 to start with)
        self.data = [deque([0] * self.lookback)]
        # Holds line series for each slot of incoming data (assumes 1 to start
        # with).
        self.series = [QLineSeries()]

        # Ranges used for the Y axis (up to 1000, after which we just double
        # the range).
        self.y_ranges = [0, 1, 5, 10, 25, 50, 100, 250, 500, 1000]

        # Set up the chart with sensible defaults.
        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series[0])
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.axis_x.setRange(0, self.max_x)
        self.axis_y.setRange(self.min_y, self.max_y)
        self.axis_x.setLabelFormat("time")
        self.axis_y.setLabelFormat("%d")
        self.chart.setAxisX(self.axis_x, self.series[0])
        self.chart.setAxisY(self.axis_y, self.series[0])
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

    def process_tty_data(self, data):
        """
        Takes raw bytes and, if a valid tuple is detected, adds the data to
        the plotter.

        The the length of the bytes data > 1024 then a data_flood signal is
        emitted to ensure Mu can take action to remain responsive.
        """
        # Data flooding guards.
        if self.flooded:
            return
        if len(data) > 1024:
            self.flooded = True
            self.data_flood.emit()
            return
        data = data.replace(b"\r\n", b"\n")
        self.input_buffer.append(data)
        # Check if the data contains a Python tuple, containing numbers, on a
        # single line (i.e. ends with \n).
        input_bytes = b"".join(self.input_buffer)
        lines = input_bytes.split(b"\n")
        for line in lines:
            if line.startswith(b"(") and line.endswith(b")"):
                # Candidate tuple. Extract the raw bytes into a numeric tuple.
                raw_values = [val.strip() for val in line[1:-1].split(b",")]
                numeric_values = []
                for raw in raw_values:
                    try:
                        numeric_values.append(int(raw))
                        # It worked, so move onto the next value.
                        continue
                    except ValueError:
                        # Try again as a float.
                        pass
                    try:
                        numeric_values.append(float(raw))
                    except ValueError:
                        # Not an int or float, so ignore this value.
                        continue
                if numeric_values:
                    # There were numeric values in the tuple, so use them!
                    self.add_data(tuple(numeric_values))
        # Reset the input buffer.
        self.input_buffer = []
        if lines[-1]:
            # Append any bytes that are not yet at the end of a line, for
            # processing next time we read data from self.connection.
            self.input_buffer.append(lines[-1])

    def add_data(self, values):
        """
        Given a tuple of values, ensures there are the required number of line
        series, add the data to the line series, update the range of the chart
        so the chart displays nicely.
        """
        # Store incoming data to dump as CSV at the end of the session.
        self.raw_data.append(values)
        # Check the number of incoming values.
        if len(values) != len(self.series):
            # Adjust the number of line series.
            value_len = len(values)
            series_len = len(self.series)
            if value_len > series_len:
                # Add new line series.
                for i in range(value_len - series_len):
                    new_series = QLineSeries()
                    self.chart.addSeries(new_series)
                    self.chart.setAxisX(self.axis_x, new_series)
                    self.chart.setAxisY(self.axis_y, new_series)
                    self.series.append(new_series)
                    self.data.append(deque([0] * self.lookback))
            else:
                # Remove old line series.
                for old_series in self.series[value_len:]:
                    self.chart.removeSeries(old_series)
                self.series = self.series[:value_len]
                self.data = self.data[:value_len]

        # Add the incoming values to the data to be displayed, and compute
        # max range.
        max_ranges = []
        min_ranges = []
        for i, value in enumerate(values):
            self.data[i].appendleft(value)
            max_ranges.append(max(self.data[i]))
            min_ranges.append(min(self.data[i]))
            if len(self.data[i]) > self.lookback:
                self.data[i].pop()
            self.num_datapoints = min(self.num_datapoints + 1, self.max_x)

        # Re-scale y-axis.
        max_y_range = max(max_ranges)
        y_range = bisect.bisect_left(self.y_ranges, max_y_range)
        if y_range < len(self.y_ranges):
            self.max_y = self.y_ranges[y_range]
        elif max_y_range > self.max_y:
            self.max_y += self.max_y
        elif max_y_range < self.max_y / 2:
            self.max_y = self.max_y / 2

        min_y_range = min(min_ranges)
        y_range = bisect.bisect_left(self.y_ranges, abs(min_y_range))
        if y_range < len(self.y_ranges):
            self.min_y = -self.y_ranges[y_range]
        elif min_y_range < self.min_y:
            self.min_y += self.min_y
        elif min_y_range > self.min_y / 2:
            self.min_y = self.min_y / 2

        self.axis_y.setRange(self.min_y, self.max_y)

        # Ensure floats are used to label y axis if the range is small.
        if self.max_y - self.min_y <= 10:
            self.axis_y.setLabelFormat("%2.2f")
        else:
            self.axis_y.setLabelFormat("%d")

        # Update the line series with the data.
        for i, line_series in enumerate(self.series):
            line_series.clear()
            xy_vals = []
            for j in range(self.num_datapoints):
                val = self.data[i][self.num_datapoints - 1 - j]
                xy_vals.append((j, val))
            for point in xy_vals:
                line_series.append(*point)

    def set_theme(self, theme):
        """
        Sets the theme / look for the plotter pane.
        """
        if theme == "day":
            self.chart.setTheme(QChart.ChartThemeLight)
        elif theme == "night":
            self.chart.setTheme(QChart.ChartThemeDark)
        else:
            self.chart.setTheme(QChart.ChartThemeHighContrast)
