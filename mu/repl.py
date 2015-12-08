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
        self.serial_input_buffer = b''

        # clear the text
        self.clear()

    def on_serial_read(self):
        self.process_bytes(bytes(self.serial.readAll()))

    def keyPressEvent(self, data):
        text = data.text()
        msg = bytes(text, 'utf8')
        key = data.key()
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
        self.serial.write(msg)

    def process_bytes(self, bs):
        bs = self.serial_input_buffer + bs
        while len(bs):
            num_use = 0
            if bs[0] == 8: # backspace
                self.delete()
                num_use = 1
            elif bs[0] == 13: # \r
                # ignore
                num_use = 1
            elif bs[0] == 27: # escape
                if bs.startswith(b'\x1b[K'):
                    # kill to end of line
                    num_use = 3
                elif bs.startswith(b'\x1b[') and len(bs) >= 3 and chr(bs[2]).isdigit():
                    n = bs[2] - ord('0')
                    cmd_idx = 3
                    if len(bs) >= 4 and chr(bs[3]).isdigit():
                        n = 10 * n + bs[3] - ord('0')
                        cmd_idx = 4
                    if cmd_idx < len(bs):
                        if bs[cmd_idx] == ord('D'):
                            # backspace n chars
                            for i in range(n):
                                self.delete()
                            num_use = cmd_idx + 1
                if num_use == 0:
                    # unknown or incomplete escape sequence
                    print(bs)
            else:
                self.append(chr(bs[0]))
                num_use = 1
            if num_use == 0:
                break
            bs = bs[num_use:]
        self.serial_input_buffer = bs

    def append(self, txt):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)
        self.insertPlainText(txt)
        self.ensureCursorVisible()

    def delete(self):
        tc = self.textCursor()
        tc.deletePreviousChar()

    def clear(self):
        self.setText('')

    def kill(self):
        if self.serial.isOpen():
            self.serial.close()
