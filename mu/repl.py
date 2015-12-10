from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import Qt
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

# TODO:
#   - shutdown serial port cleanly on exit
#   - use monospace font
#   - get backspace and arrow keys working

MICROBIT_PID = 516
MICROBIT_VID = 3368


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
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setObjectName('replpane')

        # open the serial port
        self.serial = QSerialPort(self)
        self.serial.setPortName(port)
        self.serial.setBaudRate(115200)
        print(self.serial.open(QIODevice.ReadWrite))
        self.serial.readyRead.connect(self.on_serial_read)

        # clear the text
        self.clear()

    def on_serial_read(self):
        self.process_bytes(bytes(self.serial.readAll()))

    def keyPressEvent(self, data):
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
        tc = self.textCursor()

        for b in bs:
            if b == 8: # \b
                tc.movePosition(QTextCursor.Left)
                self.setTextCursor(tc)
            elif b == 13: # \r
                pass
            else:
                tc.deleteChar()
                self.setTextCursor(tc)
                self.insertPlainText(chr(b))

        self.ensureCursorVisible()

    def clear(self):
        self.setText('')
