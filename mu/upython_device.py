import logging
import time
import ast
import os
from PyQt5 import QtSerialPort, QtWebSockets
from PyQt5.QtCore import QIODevice, QUrl, QTimer, QByteArray
from PyQt5.QtWidgets import QDialog, QLabel, QInputDialog, QLineEdit
from mu import config

logger = logging.getLogger(__name__)


class uPythonDevice():
    """Abstract base class/Interface for defining a micropython device."""
    def __init__(self, async=True, data_received_callback=None):
        self.data_received_callback = data_received_callback
        self.async = async
        if async:
            self.set_async()
        else:
            self.set_sync()
        self.saved_callback = None
        pass

    def __del__(self):
        self.close()

    def close(self):
        pass

    def set_sync(self):
        self.async = False

    def set_async(self):
        self.async = True

    def add_callback(self, data_received_callback):
        self.data_received_callback = data_received_callback

    def remove_callback(self):
        self.data_received_callback = None

    def suspend_callback(self):
        if self.data_received_callback is not None:
            self.saved_callback = self.data_received_callback
        self.remove_callback()

    def reinstate_callback(self):
        if self.saved_callback is not None:
            self.add_callback(self.saved_callback)
        self.saved_callback = None

    def send(self, bs):
        """send str to the device"""
        pass

    def data_received(self, data):
        """called when data is received from the device"""
        if self.data_received_callback is not None:
            self.data_received_callback(data)

    def execute_commands(self, commands):
        """
        executes the commands in the list `commands` on the device via the REPL

        For this to work correctly, a particular sequence of commands needs to
        be sent to put the device into a good state to process the incoming
        command.

        Returns the stdout and stderr output from the micro:bit.
        """
        result = b''
        self.raw_on()
        # Write the actual command and send CTRL-D to evaluate.
        for command in commands:
            command_bytes = command.encode('utf-8')
            for i in range(0, len(command_bytes), 32):
                self.send(command_bytes[i:min(i + 32, len(command_bytes))])
                time.sleep(0.01)
            self.send(b'\x04')
            response = bytearray()
            while not response.endswith(b'\x04>'):  # Read until prompt.
                response.extend(self.read_all())
            out, err = response[2:-2].split(b'\x04', 1)  # Split stdout, stderr
            result += out
            if err:
                return b'', err
        self.raw_off()
        return result, err

        pass

    def raw_on(self):
        """ Puts the device into raw mode. """
        print(self.read_all())  # TODO - some ugly hacks due to timing issues
        print(self.read_all())
        print(self.read_all())
        print(self.read_all())
        self.send(b'\x03')  # Send CTRL-C to break out of loop.
        print(self.read_until(b'\n>>> '))  # Flush buffer until prompt.
        print(self.read_all())
        self.send(b'\x01')  # CTRL-A to go into raw mode.
        self.send(b'\n')    # dummy command for prompt
        self.send(b'\x04')  # CTRL-D to get prompt (TODO -check on others)
        print(self.read_until(b'OK'))  # Flush buffer until raw mode prompt.
        print(self.read_all())

    def raw_off(self):
        """ Takes the device out of raw mode. """
        self.send(b'\x02')  # Send CTRL-B to get out of raw mode.

    def read(self, count=1):
        """Returns `count` bytes from buffer"""
        pass

    def read_all(self):
        """Returns all bytes in buffer"""
        pass

    def read_until(self, terminator=b'\n', size=None):
        """
        Read until a termination sequence is found ('\n' by default), the size
        is exceeded or until timeout occurs.
        """
        lenterm = len(terminator)
        line = bytearray()
        while True:
            c = self.read(1)
            if c:
                line += c
                if line[-lenterm:] == terminator:
                    break
                if size is not None and len(line) >= size:
                    break
            else:
                break
        return bytes(line)

    def list_files(self):
        """
        Returns a list of the files on the connected device or raises an IOError
        if there's a problem.
        """
        out, err = self.execute_commands([
            'import os',
            'print(os.listdir())',
        ])
        if err:
            raise IOError(err)
        return ast.literal_eval(out.decode('utf-8'))

    def put_file(self, local_path, remote_filename=None):
        """
        Puts a referenced file on the LOCAL file system onto the
        file system on the remote device.

        Returns True for success or raises an IOError if there's a problem.
        """
        if not os.path.isfile(local_path):
            raise IOError('No such file.')
        with open(local_path, 'rb') as local:
            content = local.read()
        if remote_filename is None:
            remote_filename = os.path.basename(local_path)
        commands = [
            "fd = open('{}', 'wb')".format(remote_filename),
            "f = fd.write",
        ]
        while content:
            line = content[:64]
            commands.append('f(' + repr(line) + ')')
            content = content[64:]
        commands.append('fd.close()')
        out, err = self.execute_commands(commands)
        if err:
            raise IOError(err)
        return True

    def get_file(self, remote_filename, local_path=None):
        """
        Gets a referenced file on the device's file system and copies it to the
        target (or current working directory if unspecified).

        Returns True for success or raises an IOError if there's a problem.
        """
        if local_path is None:
            local_path = remote_filename
        commands = [  # TODO - should ensure ESP OS debugging is off
            "f = open('{}', 'rb')".format(remote_filename),
            "r = f.read",
            "result = True",
            "while result:\n    result = r(32)\n    if result:\n" # cont below
            "        print(result, end='')\n",
            #"while f.read(32): print(_, end='')\n",
            "f.close()",
        ]
        out, err = self.execute_commands(commands)
        if err:
            raise IOError(err)
        # Recombine the bytes while removing "b'" from start and "'" from end.
        with open(local_path, 'wb') as f:
            f.write(out)
        return True

    def del_file(self, remote_filename):
        """
        Removes a referenced file on the micro:bit.

        Returns True for success or raises an IOError if there's a problem.
        """
        commands = [
            "import os",
            "os.remove('{}')".format(remote_filename),
        ]
        out, err = self.execute_commands(commands)
        if err:
            raise IOError(err)
        return True


class WEBREPLuPythonDevice(uPythonDevice):
    """A WebREPL/network connected device"""
    def __init__(self, async=True, data_received_callback=None, uri=None):
        self.password_dialog = QInputDialog()
        self.password_dialog.setLabelText('Enter the WebREPL password')
        self.password_dialog.setTextEchoMode(QLineEdit.Password)
        if not self.password_dialog.exec_():  # user hit cancel
            return
        self.password = self.password_dialog.textValue()

        self.buffer = QByteArray()
        self.ws = QtWebSockets.QWebSocket()
        if uri == None:
            uri = config.webrepl_options['uri']
        self.ws.open(QUrl(uri))
        self.set_sync()  # synchronous for sending password
        self.ws.textMessageReceived.connect(self.data_available)

        super().__init__(async=False)

        self.post_password_async = async
        self.post_password_callback = data_received_callback
        QTimer.singleShot(1000, self.send_password)

    def send_password(self):
        self.read_until('Password:')
        self.buffer.clear()
        self.send(bytes(self.password + '\n', 'utf-8'))
        if self.post_password_async:
            self.set_async()
        #self.data_received_callback = self.post_password_callback

    def close(self):
        self.ws.close()

    def data_available(self, data):
        self.buffer += bytes(data, 'utf-8')
        QTimer.singleShot(10, self.data_received)

    def data_received(self):
        if self.async:
            super().data_received(self.buffer)
            self.buffer.clear()

    def read(self, count):
        self.suspend_callback()
        data = self.buffer[:count]
        self.buffer.remove(0, count)
        self.reinstate_callback()
        return data

    def read_all(self):
        self.suspend_callback()
        data = QByteArray(self.buffer)
        self.buffer.clear()
        self.reinstate_callback()
        return data

    def send(self, bs):
        # sendTextMessage requires string
        self.ws.sendTextMessage(bs.decode('utf-8'))


class SerialuPythonDevice(uPythonDevice):
    """A generic serial-only micropython device"""
    def __init__(self, async=True, data_received_callback=None, port=None, speed=None):
        self.serial = QtSerialPort.QSerialPort()
        if port is None:
            port = config.serial_options['port']
        self.serial.setPortName(port)
        if self.serial.open(QIODevice.ReadWrite):
            if speed is None:
                speed = config.serial_options['speed']
            self.serial.setBaudRate(speed)
            #self.serial.readyRead.connect(self.data_available)
            self.serial.write(b'\x02')  # Send Ctrl-B to ensure not raw mode
            self.serial.write(b'\x03')  # Send a Control-C
        else:
            raise IOError("Cannot connect to device on port {}".format(port))
        super().__init__(async, data_received_callback)

    def set_sync(self):
        try:
            self.serial.readyRead.disconnect()
        except TypeError:  # ignore if nothing connected
            pass

    def set_async(self):
        self.serial.readyRead.connect(self.data_available)

    def close(self):
        try:
            self.serial.close()
        except AttributeError:  # is self.serial doesn't exist
            pass

    def send(self, bs):
        return self.serial.write(bs)  # serial.write takes a byte array

    def data_available(self):
        self.data_received(self.read_all())

    def read(self, count):
        self.suspend_callback()
        self.serial.waitForReadyRead(10)
        data = self.serial.read(count)
        self.reinstate_callback()
        return data

    def read_all(self):
        self.suspend_callback()
        self.serial.waitForReadyRead(10)
        data = self.serial.readAll()  # something wierd going on here
        self.reinstate_callback()
        return data


class MicrobitDevice(SerialuPythonDevice):
    MICROBIT_PID = 516  # USB product ID.
    MICROBIT_VID = 3368  # USB vendor ID.
    MICROBIT_SERIAL_SPEED = 115200

    def __init__(self, async=True, data_received_callback=None):
        port = self.find_microbit()
        if port is None:
            raise IOError("Cannot find Microbit")
        super().__init__(async=async, data_received_callback=data_received_callback, port=port,
                         speed=self.MICROBIT_SERIAL_SPEED)

    def find_microbit(self):
        """
        Returns the port for the first microbit it finds connected to the host
        computer. If no microbit is found, returns None.
        """
        available_ports = QtSerialPort.QSerialPortInfo.availablePorts()
        for port in available_ports:
            pid = port.productIdentifier()
            vid = port.vendorIdentifier()
            if pid == self.MICROBIT_PID and vid == self.MICROBIT_VID:
                port_name = port.portName()
                logger.info(
                    'Found micro:bit with portName: {}'.format(port_name))
                return port_name
        logger.warning('Could not find micro:bit.')
        logger.debug('Available ports:')
        logger.debug(['PID:{} VID:{} PORT:{}'.format(p.productIdentifier(),
                                                     p.vendorIdentifier(),
                                                     p.portName())
                      for p in available_ports])
        return None


def get_upython_device(async=True, data_received_callback=None):
    if config.board_type == 'microbit':
        return MicrobitDevice(async=async, data_received_callback=data_received_callback)
    elif config.board_type == 'serial':
        return SerialuPythonDevice(async=async, data_received_callback=data_received_callback)
    elif config.board_type == 'webrepl':
        return WEBREPLuPythonDevice(async=async, data_received_callback=data_received_callback)
