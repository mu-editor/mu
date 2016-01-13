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
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor, QFont, QColor, QPalette
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


MICROBIT_PID = 516
MICROBIT_VID = 3368


LIGHT_THEME = "QTextEdit { background-color: white; color: black }"
DARK_THEME= "QTextEdit { background-color: black; color: white}"


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
            return port.portName()
    return None


class REPLPane(QTextEdit):
    """
    REPL = Read, Evaluate, Print, Loop.

    This widget represents a REPL client connected to a BBC micro:bit.
    """

    def __init__(self, port, theme='day', parent=None):
        super().__init__(parent)
        self.setFont(QFont('Courier', 14))
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setObjectName('replpane')
        # open the serial port
        self.serial = QSerialPort(self)
        self.serial.setPortName(port)
        self.serial.setBaudRate(115200)
        if self.serial.open(QIODevice.ReadWrite):
            self.serial.readyRead.connect(self.on_serial_read)
            # clear the text
            self.clear()
            # Send a Control-C
            self.serial.write(b'\x03')
        else:
            raise IOError("Cannot connect to device on port {}".format(port))
        self.set_theme(theme)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.setStyleSheet(LIGHT_THEME)
        else:
            self.setStyleSheet(DARK_THEME)

    def on_serial_read(self):
        """
        Called when the application gets data from the connected device.
        """
        self.process_bytes(bytes(self.serial.readAll()))

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
        elif data.modifiers() == Qt.MetaModifier:
            # Handle the Control key.  I would've expected us to have to test
            # for Qt.ControlModifier, but on (my!) OSX Qt.MetaModifier does
            # correspond to the Control key.  I've read something that suggests
            # that it's different on other platforms.
            if Qt.Key_A <= key <= Qt.Key_Z:
                # The microbit treats an input of \x01 as Ctrl+A, etc.
                msg = bytes([1 + key - Qt.Key_A])
        self.serial.write(msg)

    def process_bytes(self, bs):
        """
        Given some incoming bytes of data, works out how to handle / display
        them in the REPL widget.
        """
        tc = self.textCursor()
        # The text cursor must be on the last line of the document. If it isn't
        # then move it there.
        while tc.movePosition(QTextCursor.Down):
            pass
        for b in bs:
            if b == 8:  # \b
                tc.movePosition(QTextCursor.Left)
                self.setTextCursor(tc)
            elif b == 13:  # \r
                pass
            else:
                tc.deleteChar()
                self.setTextCursor(tc)
                self.insertPlainText(chr(b))
        self.ensureCursorVisible()

    def clear(self):
        """
        Clears the text of the REPL.
        """
        self.setText('')
