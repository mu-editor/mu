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
import os.path
import mu
from PyQt5.QtCore import (Qt, QIODevice, QProcess, QProcessEnvironment,
                          pyqtSignal)
from collections import deque
from itertools import islice
from PyQt5.QtWidgets import (QMessageBox, QTextEdit, QFrame, QListWidget,
                             QGridLayout, QLabel, QMenu, QApplication,
                             QTreeView)
from PyQt5.QtGui import QKeySequence, QTextCursor, QCursor, QPainter
from PyQt5.QtSerialPort import QSerialPort
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from mu.interface.themes import Font
from mu.interface.themes import (DEFAULT_FONT_SIZE, NIGHT_STYLE, DAY_STYLE,
                                 CONTRAST_STYLE)
import serial


logger = logging.getLogger(__name__)


class JupyterREPLPane(RichJupyterWidget):
    """
    REPL = Read, Evaluate, Print, Loop.

    Displays a Jupyter iPython session.
    """

    def __init__(self, theme='day', parent=None):
        super().__init__(parent)
        self.set_theme(theme)
        self.console_height = 10

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        stylesheet = ("QWidget{font-size: " + str(new_size) +
                      "pt; font-family: Monospace;}")
        self.setStyleSheet(stylesheet)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font.pointSize()
        new_size = min(old_size + delta, 34)
        self.set_font_size(new_size)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font.pointSize()
        new_size = max(old_size - delta, 4)
        self.set_font_size(new_size)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'contrast':
            self.set_default_style(colors='nocolor')
            self.setStyleSheet(CONTRAST_STYLE)
        elif theme == 'night':
            self.set_default_style(colors='nocolor')
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.set_default_style()
            self.setStyleSheet(DAY_STYLE)

    def setFocus(self):
        """
        Override base setFocus so the focus happens to the embedded _control
        within this widget.
        """
        self._control.setFocus()


class MicroPythonREPLPane(QTextEdit):
    """
    REPL = Read, Evaluate, Print, Loop.

    This widget represents a REPL client connected to a BBC micro:bit running
    MicroPython.

    The device MUST be flashed with MicroPython for this to work.
    """

    def __init__(self, serial, theme='day', parent=None):
        super().__init__(parent)
        self.serial = serial
        self.setFont(Font().load())
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setUndoRedoEnabled(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.setObjectName('replpane')
        self.set_theme(theme)

    def paste(self):
        """
        Grabs clipboard contents then sends down the serial port.
        """
        clipboard = QApplication.clipboard()
        if clipboard and clipboard.text():
            self.serial.write(bytes(clipboard.text(), 'utf8'))

    def context_menu(self):
        """
        Creates custom context menu with just copy and paste.
        """
        menu = QMenu(self)
        if platform.system() == 'Darwin':
            copy_keys = QKeySequence(Qt.CTRL + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.Key_V)
        else:
            copy_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_V)

        menu.addAction("Copy", self.copy, copy_keys)
        menu.addAction("Paste", self.paste, paste_keys)
        menu.exec_(QCursor.pos())

    def cursor_to_end(self):
        """
        Moves the cursor to the very end of the available text.
        """
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)

    def keyPressEvent(self, data):
        """
        Called when the user types something in the REPL.

        Correctly encodes it and sends it to the connected device.
        """
        key = data.key()
        msg = bytes(data.text(), 'utf8')
        if key == Qt.Key_Backspace:
            msg = b'\b'
        elif key == Qt.Key_Up:
            msg = b'\x1B[A'
        elif key == Qt.Key_Down:
            msg = b'\x1B[B'
        elif key == Qt.Key_Right:
            msg = b'\x1B[C'
        elif key == Qt.Key_Left:
            msg = b'\x1B[D'
        elif key == Qt.Key_Home:
            msg = b'\x1B[H'
        elif key == Qt.Key_End:
            msg = b'\x1B[F'
        elif (platform.system() == 'Darwin' and
                data.modifiers() == Qt.MetaModifier) or \
             (platform.system() != 'Darwin' and
                data.modifiers() == Qt.ControlModifier):
            # Handle the Control key. On OSX/macOS/Darwin (python calls this
            # platform Darwin), this is handled by Qt.MetaModifier. Other
            # platforms (Linux, Windows) call this Qt.ControlModifier. Go
            # figure. See http://doc.qt.io/qt-5/qt.html#KeyboardModifier-enum
            if Qt.Key_A <= key <= Qt.Key_Z:
                # The microbit treats an input of \x01 as Ctrl+A, etc.
                msg = bytes([1 + key - Qt.Key_A])
        elif (data.modifiers() == Qt.ControlModifier | Qt.ShiftModifier) or \
                (platform.system() == 'Darwin' and
                    data.modifiers() == Qt.ControlModifier):
            # Command-key on Mac, Ctrl-Shift on Win/Lin
            if key == Qt.Key_C:
                self.copy()
                msg = b''
            elif key == Qt.Key_V:
                self.paste()
                msg = b''
        self.serial.write(msg)

    def process_bytes(self, data):
        """
        Given some incoming bytes of data, work out how to handle / display
        them in the REPL widget.
        """
        tc = self.textCursor()
        # The text cursor must be on the last line of the document. If it isn't
        # then move it there.
        while tc.movePosition(QTextCursor.Down):
            pass
        i = 0
        while i < len(data):
            if data[i] == 8:  # \b
                tc.movePosition(QTextCursor.Left)
                self.setTextCursor(tc)
            elif data[i] == 13:  # \r
                pass
            elif data[i] == 27 and data[i + 1] == 91:  # VT100 cursor: <Esc>[
                i += 2  # move index to after the [
                m = re.search(r'(?P<count>[\d]*)(?P<action>[ABCDK])',
                              data[i:].decode('utf-8'))

                # move to (almost) after control seq (will ++ at end of loop)
                i += m.end() - 1

                if m.group("count") == '':
                    count = 1
                else:
                    count = int(m.group("count"))

                if m.group("action") == "A":  # up
                    tc.movePosition(QTextCursor.Up, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "B":  # down
                    tc.movePosition(QTextCursor.Down, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "C":  # right
                    tc.movePosition(QTextCursor.Right, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "D":  # left
                    tc.movePosition(QTextCursor.Left, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "K":  # delete things
                    if m.group("count") == "":  # delete to end of line
                        tc.movePosition(QTextCursor.EndOfLine,
                                        mode=QTextCursor.KeepAnchor)
                        tc.removeSelectedText()
                        self.setTextCursor(tc)
            elif data[i] == 10:  # \n
                tc.movePosition(QTextCursor.End)
                self.setTextCursor(tc)
                self.insertPlainText(chr(data[i]))
            else:
                tc.deleteChar()
                self.setTextCursor(tc)
                self.insertPlainText(chr(data[i]))
            i += 1
        self.ensureCursorVisible()

    def clear(self):
        """
        Clears the text of the REPL.
        """
        self.setText('')


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


class MicrobitFileList(MuFileList):
    """
    Represents a list of files on the micro:bit.
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
            file_exists = self.findItems(source.currentItem().text(),
                                         Qt.MatchExactly)
            if not file_exists or \
                    file_exists and self.show_confirm_overwrite_dialog():
                self.disable.emit()
                local_filename = os.path.join(self.home,
                                              source.currentItem().text())
                msg = _("Copying '{}' to micro:bit.").format(local_filename)
                logger.info(msg)
                self.set_message.emit(msg)
                self.put.emit(local_filename)

    def on_put(self, microbit_file):
        """
        Fired when the put event is completed for the given filename.
        """
        msg = _("'{}' successfully copied to micro:bit.").format(microbit_file)
        self.set_message.emit(msg)
        self.list_files.emit()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        delete_action = menu.addAction(_("Delete (cannot be undone)"))
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == delete_action:
            self.disable.emit()
            microbit_filename = self.currentItem().text()
            logger.info("Deleting {}".format(microbit_filename))
            msg = _("Deleting '{}' from micro:bit.").format(microbit_filename)
            logger.info(msg)
            self.set_message.emit(msg)
            self.delete.emit(microbit_filename)

    def on_delete(self, microbit_file):
        """
        Fired when the delete event is completed for the given filename.
        """
        msg = _("'{}' successfully deleted from micro:bit.").\
            format(microbit_file)
        self.set_message.emit(msg)
        self.list_files.emit()


class LocalFileList(MuFileList):
    """
    Represents a list of files in the Mu directory on the local machine.
    """

    get = pyqtSignal(str, str)

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.setDragDropMode(QListWidget.DragDrop)

    def dropEvent(self, event):
        source = event.source()
        if isinstance(source, MicrobitFileList):
            file_exists = self.findItems(source.currentItem().text(),
                                         Qt.MatchExactly)
            if not file_exists or \
                    file_exists and self.show_confirm_overwrite_dialog():
                self.disable.emit()
                microbit_filename = source.currentItem().text()
                local_filename = os.path.join(self.home,
                                              microbit_filename)
                msg = _("Getting '{}' from micro:bit. "
                        "Copying to '{}'.").format(microbit_filename,
                                                   local_filename)
                logger.info(msg)
                self.set_message.emit(msg)
                self.get.emit(microbit_filename, local_filename)

    def on_get(self, microbit_file):
        """
        Fired when the get event is completed for the given filename.
        """
        msg = _("Successfully copied '{}' "
                "from the micro:bit to your computer.").format(microbit_file)
        self.set_message.emit(msg)
        self.list_files.emit()


class FileSystemPane(QFrame):
    """
    Contains two QListWidgets representing the micro:bit and the user's code
    directory. Users transfer files by dragging and dropping. Highlighted files
    can be selected for deletion.
    """

    set_message = pyqtSignal(str)
    set_warning = pyqtSignal(str)
    list_files = pyqtSignal()

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.font = Font().load()
        microbit_fs = MicrobitFileList(home)
        local_fs = LocalFileList(home)
        layout = QGridLayout()
        self.setLayout(layout)
        microbit_label = QLabel()
        microbit_label.setText(_('Files on your micro:bit:'))
        local_label = QLabel()
        local_label.setText(_('Files on your computer:'))
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
        local_files = [f for f in os.listdir(self.home)
                       if os.path.isfile(os.path.join(self.home, f))]
        local_files.sort()
        for f in local_files:
            self.local_fs.addItem(f)
        self.enable()

    def on_ls_fail(self):
        """
        Fired when listing files fails.
        """
        self.show_warning(_("There was a problem getting the list of files on "
                            "the micro:bit. Please check Mu's logs for "
                            "technical information. Alternatively, try "
                            "unplugging/plugging-in your micro:bit and/or "
                            "restarting Mu."))
        self.disable()

    def on_put_fail(self, microbit_filename):
        """
        Fired when the referenced file cannot be copied onto the micro:bit.
        """
        self.show_warning(_("There was a problem copying the file '{}' onto "
                            "the micro:bit. Please check Mu's logs for "
                            "technical information."))

    def on_delete_fail(self, microbit_filename):
        """
        Fired when a deletion on the micro:bit for the given file failed.
        """
        self.show_warning(_("There was a problem deleting '{}' from the "
                            "micro:bit. Please check Mu's logs for "
                            "technical information."))

    def on_get_fail(self, microbit_filename):
        """
        Fired when getting the referenced file on the micro:bit failed.
        """
        self.show_warning(_("There was a problem getting '{}' from the "
                            "micro:bit. Please check Mu's logs for "
                            "technical information."))

    def set_theme(self, theme):
        """
        Sets the theme / look for the FileSystemPane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        self.font.setPointSize(new_size)
        self.microbit_label.setFont(self.font)
        self.local_label.setFont(self.font)
        self.microbit_fs.setFont(self.font)
        self.local_fs.setFont(self.font)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font.pointSize()
        new_size = min(old_size + delta, 34)
        self.set_font_size(new_size)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font.pointSize()
        new_size = max(old_size - delta, 4)
        self.set_font_size(new_size)


class PythonProcessPane(QTextEdit):
    """
    Captures, displays and works with the stdin, stdout and stderr of a Python
    process.

    Used for running / debugging standard Python3 scripts.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(Font().load())
        self.input_buffer = []

    def start_process(self, workspace, script):
        """
        Start the child process from the workspace with the script.
        """
        self.script = os.path.abspath(os.path.normcase(script))
        logger.info('Running script: {}'.format(script))
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        # Force buffers to flush immediately.
        env = QProcessEnvironment.systemEnvironment()
        env.insert('PYTHONUNBUFFERED', '1')
        self.process.setProcessEnvironment(env)
        logger.info('Working directory: {}'.format(workspace))
        self.process.setWorkingDirectory(workspace)
        self.process.readyRead.connect(self.read)
        self.process.finished.connect(self.finished)
        python_exec = sys.executable
        mu_dir = os.path.dirname(os.path.abspath(mu.__file__))
        runner = os.path.join(mu_dir, 'mu-debug.py')
        # Start the mu-debug runner within an interactive Python shell.
        self.process.start(python_exec, [runner, self.script])

    def finished(self, code, status):
        """
        Called when the process is finished.
        """
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(_('\n\n---------- FINISHED ----------\n'))
        msg = _('exit code: {} status: {}').format(code, status)
        cursor.insertText(msg)
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.setReadOnly(True)

    def append(self, byte_stream):
        """
        Append text to the text area.
        """
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(byte_stream.decode('utf-8'))
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def delete(self):
        """
        Removes a character from the end of the text (to facilitate when a
        user presses the delete button).
        """
        if self.input_buffer:
            self.input_buffer.pop()
            cursor = self.textCursor()
            cursor.movePosition(cursor.End)
            cursor.deletePreviousChar()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)

    def read(self):
        """
        From the process's stdout.
        """
        self.input_buffer = []
        data = self.process.readAll().data()
        if data:
            self.append(data)

    def keyPressEvent(self, data):
        """
        Called when the user types something in the REPL.

        Correctly encodes it and sends it to the connected process.
        """
        key = data.key()
        msg = bytes(data.text(), 'utf8')
        if key == Qt.Key_Backspace:
            msg = b'\b'
        elif (data.modifiers() == Qt.ControlModifier | Qt.ShiftModifier) or \
                (platform.system() == 'Darwin' and
                    data.modifiers() == Qt.ControlModifier):
            # Command-key on Mac, Ctrl-Shift on Win/Lin
            if key == Qt.Key_C:
                self.copy()
                msg = b''
            elif key == Qt.Key_V:
                self.paste()
                msg = b''
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            msg = b'\n'
        if key == Qt.Key_Backspace:
            self.delete()
        else:
            self.input_buffer.append(msg)
            if not self.isReadOnly():
                self.append(msg)
        if self.input_buffer and self.input_buffer[-1] == b'\n':
            if hasattr(self, 'process') and self.process:
                self.process.write(b''.join(self.input_buffer))
            self.input_buffer = []

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font().pointSize()
        new_size = old_size + delta
        if new_size <= 34:
            super().zoomIn(delta)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font().pointSize()
        new_size = old_size - delta
        if new_size >= 4:
            super().zoomOut(delta)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)


class DebugInspector(QTreeView):
    """
    Presents a tree like representation of the current state of the call stack
    to the user.
    """

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        stylesheet = ("QWidget{font-size: " + str(new_size) +
                      "pt; font-family: Monospace;}")
        self.setStyleSheet(stylesheet)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font().pointSize()
        new_size = min(old_size + delta, 34)
        self.set_font_size(new_size)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font().pointSize()
        new_size = max(old_size - delta, 4)
        self.set_font_size(new_size)

    def set_theme(self, theme):
        """
        Sets the theme / look for the debug inspector pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)


class PlotterPane(QChartView):
    """
    This plotter widget makes viewing sensor data easy!

    This widget represents a chart that will look for CSV data on
    the REPL and will auto-generate a graph

    The device MUST be flashed with MicroPython for this to work.
    """

    def __init__(self, theme='day', parent=None):
        super().__init__(parent)
        self.input_buffer = []
        self.setObjectName('plotterpane')
        self.x_range = [0, 100]   # start out with a dummy range, resize later
        self.y_range = [-1000, 1000]  # ditto

        self.t = range(self.x_range[0], self.x_range[1])
        self.q = deque([0] * len(self.t))

        self.series = QLineSeries()
        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.series)

        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.axis_x.setRange(self.x_range[0], self.x_range[1])
        self.axis_y.setRange(self.y_range[0], self.y_range[1])
        self.axis_x.setLabelFormat("")
        self.axis_y.setLabelFormat("%d")
        self.chart.setAxisX(self.axis_x, self.series)
        self.chart.setAxisY(self.axis_y, self.series)

        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

        self.resizeEvent = lambda e: self.on_resize(e)

    def process_bytes(self, data):
        """
        Takes raw baytes and, if a valid tuple is detected, adds the data to
        the plotter.
        """
        self.input_buffer.append(data)
        # Check if the data contains a Python tuple, containing numbers, on a
        # single line (i.e. ends with \n).
        input_bytes = b''.join(self.input_buffer)
        lines = input_bytes.split(b'\r\n')
        for line in lines:
            if line.startswith(b'(') and line.endswith(b')'):
                # Candidate tuple. Extract the raw bytes into a numeric tuple.
                raw_values = [val.strip() for val in line[1:-1].split(b',')]
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
                    # There were numeric values in the tuple, so emit them!
                    self.add_data(tuple(numeric_values))
        # Reset the input buffer.
        self.input_buffer = []
        if lines[-1]:
            # Append any bytes that are not yet at the end of a line, for
            # processing next time we read data from self.serial.
            self.input_buffer.append(lines[-1])

    def add_data(self, values):
        value = values[0]
        self.q.appendleft(value)
        if len(self.q) > len(self.t):
            self.q.pop()

        p_list = []
        for i in range(0, len(self.t)):
            if i > (len(self.q) - 1):
                temp = 0
            else:
                temp = self.q[len(self.t) - 1 - i]
            p_list.append((self.t[i], temp))
        self.series.clear()
        for i in p_list:
            self.series.append(*i)

    def on_resize(self, event):
        return
        x = event.size().width()
        y = event.size().height()
        self.chart.axisY().setMax(y)
        self.chart.axisX().setMax(x)
        self.t = range(0, x)
        q_len = len(self.q)
        if x > q_len:  # extend it!
            self.q.extendleft([0] * (x - q_len))
        if x < q_len:  # contract it
            self.q = deque(islice(self.q, q_len - x, q_len))
        self.chartView.update()

    def set_theme(self, theme):
        """
        Sets the theme / look for the plotter pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) does nothing yet
        """
        pass

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) does nothing yet
        """
        pass
