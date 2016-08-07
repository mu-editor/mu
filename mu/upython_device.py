import logging
from PyQt5 import QtSerialPort, QtWebSockets
from PyQt5.QtCore import QIODevice, QUrl, QTimer
from mu import config

logger = logging.getLogger(__name__)


class uPythonDevice():
    """Abstract base class/Interface for defining a micropython device."""
    def __init__(self, data_received_callback=None):
        self.data_received_callback = data_received_callback
        pass

    def __del__(self):
        self.close()

    def close(self):
        pass

    def add_callback(self, data_received_callback):
        self.data_received_callback = data_received_callback

    def remove_callback(self):
        self.data_received_callback = None

    def send(self, bs):
        """send str to the device"""
        pass

    def data_received(self, data):
        """called when data is received from the device"""
        if self.data_received_callback is not None:
            self.data_received_callback(data)

    def execute_commands(self, commands):
        """executes the commands in the list `commands` on the device via the REPL"""
        pass

    def list_files(self):
        pass

    def put_file(self, local_path, remote_filename):
        pass

    def get_file(self, remote_filename, local_path=None):
        pass

    def del_file(self, remote_filename):
        pass


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

    def send(self, bs):
        self.ws.sendTextMessage(bs.decode('utf-8'))  # sendTextMessage takes a string


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
        self.data_received(self.serial.readAll())


class MicrobitDevice(SerialuPythonDevice):
    MICROBIT_PID = 516  # USB product ID.
    MICROBIT_VID = 3368  # USB vendor ID.
    MICROBIT_SERIAL_SPEED = 115200

    def __init__(self, data_received_callback=None):
        port = self.find_microbit()
        if port is None:
            raise IOError("Cannot find Microbit")
        super().__init__(data_received_callback, port=port, speed=self.MICROBIT_SERIAL_SPEED)

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
                logger.info('Found micro:bit with portName: {}'.format(port_name))
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


