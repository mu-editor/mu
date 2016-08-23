import logging
import time
import ast
import os
from PyQt5 import QtSerialPort, QtWebSockets
from PyQt5.QtCore import QIODevice, QUrl, QTimer
from mu import config

logger = logging.getLogger(__name__)


class uPythonDevice():
    """Abstract base class/Interface for defining a micropython device."""
    def __init__(self, data_received_callback=None):
        self.data_received_callback = data_received_callback
        self.saved_callback = None
        pass

    def __del__(self):
        self.close()

    def close(self):
        pass

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
        self.send(b'\x03')  # Send CTRL-C to break out of loop.
        self.read_until(b'\n>')  # Flush buffer until prompt.
        self.send(b'\x01')  # Go into raw mode.
        self.read_until(b'\r\n>OK')  # Flush buffer until raw mode prompt.

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
        out, err = self.execute(commands)
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
        out, err = self.execute(commands)
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
        out, err = self.execute(commands)
        if err:
            raise IOError(err)
        return True


class WEBREPLuPythonDevice(uPythonDevice):
    """A WebREPL/network connected device"""
    def __init__(self, data_received_callback=None, uri=None):
        super().__init__(data_received_callback)
        self.buffer = ''
        self.ws = QtWebSockets.QWebSocket()
        if uri == None:
            uri = config.webrepl_options['uri']
        self.ws.open(QUrl(uri))
        self.ws.textMessageReceived.connect(self.data_available)

    def close(self):
        self.ws.close()

    def data_available(self, data):
        self.buffer += data
        QTimer.singleShot(10, self.data_received)

    def data_received(self):
        super().data_received(self.buffer)
        self.buffer = ''

    def read(self, count):
        self.suspend_callback()
        data = "" #TODO
        self.reinstate_callback()
        return data

    def read_all(self):
        self.suspend_callback()
        data = "" #TODO
        self.reinstate_callback()
        return data

    def send(self, bs):
        # sendTextMessage requires string
        self.ws.sendTextMessage(bs.decode('utf-8'))


class SerialuPythonDevice(uPythonDevice):
    """A generic serial-only micropython device"""
    def __init__(self, data_received_callback=None, port=None, speed=None):
        super().__init__(data_received_callback)
        self.serial = QtSerialPort.QSerialPort()
        if port is None:
            port = config.serial_options['port']
        self.serial.setPortName(port)
        if self.serial.open(QIODevice.ReadWrite):
            if speed is None:
                speed = config.serial_options['speed']
            self.serial.setBaudRate(speed)
            self.serial.readyRead.connect(self.data_available)
            # Send a Control-C
            self.serial.write(b'\x03')
        else:
            raise IOError("Cannot connect to device on port {}".format(port))

    def close(self):
        self.serial.close()

    def send(self, bs):
        return self.serial.write(bs)  # serial.write takes a byte array

    def data_available(self):
        self.data_received(self.read_all())

    def read(self, count):
        self.suspend_callback()
        data = self.serial.read(count)
        self.reinstate_callback()
        return data

    def read_all(self):
        self.suspend_callback()
        data = self.serial.readAll()
        self.reinstate_callback()
        return data


class MicrobitDevice(SerialuPythonDevice):
    MICROBIT_PID = 516  # USB product ID.
    MICROBIT_VID = 3368  # USB vendor ID.
    MICROBIT_SERIAL_SPEED = 115200

    def __init__(self, data_received_callback=None):
        port = self.find_microbit()
        if port is None:
            raise IOError("Cannot find Microbit")
        super().__init__(data_received_callback, port=port,
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


def get_upython_device(data_received_callback=None):
    if config.board_type == 'microbit':
        return MicrobitDevice(data_received_callback=None)
    elif config.board_type == 'serial':
        return SerialuPythonDevice(data_received_callback=None)
    elif config.board_type == 'webrepl':
        return WEBREPLuPythonDevice(data_received_callback=None)
