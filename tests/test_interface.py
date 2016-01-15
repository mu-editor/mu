# -*- coding: utf-8 -*-
"""
Tests for the ui elements of Mu.
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QIODevice, Qt
from unittest import mock
import mu.interface
import pytest


# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


def test_REPLPane_init_default_args():
    """
    Ensure the REPLPane object is instantiated as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.REPLPane('COM0')
    assert mock_serial_class.call_count == 1
    mock_serial.setPortName.assert_called_once_with('COM0')
    mock_serial.setBaudRate.assert_called_once_with(115200)
    mock_serial.open.assert_called_once_with(QIODevice.ReadWrite)
    mock_serial.readyRead.connect.assert_called_once_with(rp.on_serial_read)
    mock_serial.write.assert_called_once_with(b'\x03')


def test_REPLPane_init_cannot_open():
    """
    If serial.open fails raise an IOError.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=False)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        with pytest.raises(IOError):
            mu.interface.REPLPane('COM0')


def test_REPLPane_set_theme():
    """
    Ensure the set_theme toggles as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.REPLPane('COM0')
        rp.setStyleSheet = mock.MagicMock(return_value=None)
        rp.set_theme('day')
        rp.setStyleSheet.assert_called_once_with(mu.interface.DAY_STYLE)
        rp.setStyleSheet.reset_mock()
        rp.set_theme('night')
        rp.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_REPLPane_on_serial_read():
    """
    Ensure the method calls process_bytes.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readAll = mock.MagicMock(return_value='abc'.encode('utf-8'))
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.REPLPane('COM0')
        rp.process_bytes = mock.MagicMock()
        rp.on_serial_read()
        rp.process_bytes.assert_called_once_with(bytes('abc'.encode('utf-8')))


def test_REPLPane_keyPressEvent():
    """
    Ensure key presses in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.REPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_A)
        data.text = mock.MagicMock(return_value='a')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(bytes('a', 'utf-8'))
