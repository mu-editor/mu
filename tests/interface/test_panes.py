# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QListWidget
from PyQt5.QtCore import QIODevice, Qt
from PyQt5.QtGui import QTextCursor
from unittest import mock
import sys
import os
import mu
import platform
import mu.interface.panes
import pytest

# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


def test_MicroPythonREPLPane_init_default_args():
    """
    Ensure the MicroPython REPLPane object is instantiated as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
    assert mock_serial_class.call_count == 1
    mock_serial.setPortName.assert_called_once_with('COM0')
    mock_serial.setBaudRate.assert_called_once_with(115200)
    mock_serial.open.assert_called_once_with(QIODevice.ReadWrite)
    mock_serial.readyRead.connect.assert_called_once_with(rp.on_serial_read)
    mock_serial.write.assert_called_once_with(b'\x03')


def test_MicroPythonREPLPane_init_cannot_open():
    """
    If serial.open fails raise an IOError.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=False)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        with pytest.raises(IOError):
            mu.interface.panes.MicroPythonREPLPane('COM0')


def test_MicroPythonREPLPane_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'paste me!'
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        with mock.patch('mu.interface.panes.QApplication', mock_application):
            rp = mu.interface.panes.MicroPythonREPLPane('COM0')
            mock_serial.write.reset_mock()
            rp.paste()
    mock_serial.write.assert_called_once_with(bytes('paste me!', 'utf8'))


def test_MicroPythonREPLPane_paste_only_works_if_there_is_something_to_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = ''
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        with mock.patch('mu.interface.panes.QApplication', mock_application):
            rp = mu.interface.panes.MicroPythonREPLPane('COM0')
            mock_serial.write.reset_mock()
            rp.paste()
    assert mock_serial.write.call_count == 0


def test_MicroPythonREPLPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'WinNT'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class), \
            mock.patch('mu.interface.panes.platform', mock_platform), \
            mock.patch('mu.interface.panes.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.panes.QCursor'):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == 'Copy'
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == 'Ctrl+Shift+C'
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == 'Paste'
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == 'Ctrl+Shift+V'
    assert mock_qmenu.exec_.call_count == 1


def test_MicroPythonREPLPane_context_menu_darwin():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'Darwin'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class), \
            mock.patch('mu.interface.panes.platform', mock_platform), \
            mock.patch('mu.interface.panes.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.panes.QCursor'):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == 'Copy'
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == 'Ctrl+C'
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == 'Paste'
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == 'Ctrl+V'
    assert mock_qmenu.exec_.call_count == 1


def test_MicroPythonREPLPane_cursor_to_end():
    """
    Ensure the cursor is set to the very end of the available text using the
    appropriate Qt related magic.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_text_cursor = mock.MagicMock()
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.textCursor = mock.MagicMock(return_value=mock_text_cursor)
        rp.setTextCursor = mock.MagicMock()
        rp.cursor_to_end()
        mock_text_cursor.movePosition.assert_called_once_with(QTextCursor.End)
        rp.setTextCursor.assert_called_once_with(mock_text_cursor)


def test_MicroPythonREPLPane_set_theme():
    """
    Ensure the set_theme toggles as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.setStyleSheet = mock.MagicMock(return_value=None)
        rp.set_theme('day')
        rp.setStyleSheet.assert_called_once_with(mu.interface.themes.DAY_STYLE)
        rp.setStyleSheet.reset_mock()
        rp.set_theme('night')
        rp.setStyleSheet.assert_called_once_with(
            mu.interface.themes.NIGHT_STYLE)
        rp.setStyleSheet.reset_mock()
        rp.set_theme('contrast')
        rp.setStyleSheet.assert_called_once_with(
            mu.interface.themes.CONTRAST_STYLE)


def test_MicroPythonREPLPane_on_serial_read():
    """
    Ensure the method calls process_bytes.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readAll = mock.MagicMock(return_value='abc'.encode('utf-8'))
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.process_bytes = mock.MagicMock()
        rp.on_serial_read()
        rp.process_bytes.assert_called_once_with(bytes('abc'.encode('utf-8')))


def test_MicroPythonREPLPane_keyPressEvent():
    """
    Ensure key presses in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_A)
        data.text = mock.MagicMock(return_value='a')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(bytes('a', 'utf-8'))


def test_MicroPythonREPLPane_keyPressEvent_backspace():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
        data.text = mock.MagicMock(return_value='\b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\b')


def test_MicroPythonREPLPane_keyPressEvent_up():
    """
    Ensure up arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Up)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[A')


def test_MicroPythonREPLPane_keyPressEvent_down():
    """
    Ensure down arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Down)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[B')


def test_MicroPythonREPLPane_keyPressEvent_right():
    """
    Ensure right arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Right)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[C')


def test_MicroPythonREPLPane_keyPressEvent_left():
    """
    Ensure left arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Left)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[D')


def test_MicroPythonREPLPane_keyPressEvent_home():
    """
    Ensure home key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Home)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[H')


def test_MicroPythonREPLPane_keyPressEvent_end():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_End)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[F')


def test_MicroPythonREPLPane_keyPressEvent_CTRL_C_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.copy = mock.MagicMock()
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_C)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
        rp.keyPressEvent(data)
        rp.copy.assert_called_once_with()


def test_MicroPythonREPLPane_keyPressEvent_CTRL_V_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.paste = mock.MagicMock()
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_V)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
        rp.keyPressEvent(data)
        rp.paste.assert_called_once_with()


def test_MicroPythonREPLPane_keyPressEvent_meta():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_M)
        data.text = mock.MagicMock(return_value='a')
        if platform.system() == 'Darwin':
            data.modifiers = mock.MagicMock(return_value=Qt.MetaModifier)
        else:
            data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier)
        rp.keyPressEvent(data)
        expected = 1 + Qt.Key_M - Qt.Key_A
        mock_serial.write.assert_called_once_with(bytes([expected]))


def test_MicroPythonREPLPane_process_bytes():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. Backspace is enacted, carriage-return is ignored, newline moves
    the cursor position to the end of the line before enacted and all others
    are simply inserted.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(side_effect=[True, False, True,
                                                       True])
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.textCursor = mock.MagicMock(return_value=mock_tc)
        rp.setTextCursor = mock.MagicMock(return_value=None)
        rp.insertPlainText = mock.MagicMock(return_value=None)
        rp.ensureCursorVisible = mock.MagicMock(return_value=None)
        bs = bytes([8, 13, 10, 65, ])  # \b, \r, \n, 'A'
        rp.process_bytes(bs)
        rp.textCursor.assert_called_once_with()
        assert mock_tc.movePosition.call_count == 4
        assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
        assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Down
        assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Left
        assert mock_tc.movePosition.call_args_list[3][0][0] == QTextCursor.End
        assert rp.setTextCursor.call_count == 3
        assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[1][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[2][0][0] == mock_tc
        assert rp.insertPlainText.call_count == 2
        assert rp.insertPlainText.call_args_list[0][0][0] == chr(10)
        assert rp.insertPlainText.call_args_list[1][0][0] == chr(65)
        rp.ensureCursorVisible.assert_called_once_with()


def test_MicroPythonREPLPane_process_bytes_VT100():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure VT100 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.textCursor = mock.MagicMock(return_value=mock_tc)
        rp.setTextCursor = mock.MagicMock(return_value=None)
        rp.insertPlainText = mock.MagicMock(return_value=None)
        rp.ensureCursorVisible = mock.MagicMock(return_value=None)
        bs = bytes([
            27, 91, ord('1'), ord('A'),  # <Esc>[1A
            27, 91, ord('1'), ord('B'),  # <Esc>[1B
            27, 91, ord('1'), ord('C'),  # <Esc>[1C
            27, 91, ord('1'), ord('D'),  # <Esc>[1D
            27, 91, ord('K'),  # <Esc>[K
        ])
        rp.process_bytes(bs)
        rp.textCursor.assert_called_once_with()
        assert mock_tc.movePosition.call_count == 6
        assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
        assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Up
        assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Down
        assert mock_tc.movePosition.call_args_list[3][0][0] == \
            QTextCursor.Right
        assert mock_tc.movePosition.call_args_list[4][0][0] == QTextCursor.Left
        assert mock_tc.movePosition.call_args_list[5][0][0] == \
            QTextCursor.EndOfLine
        assert mock_tc.movePosition.call_args_list[5][1]['mode'] == \
            QTextCursor.KeepAnchor
        assert rp.setTextCursor.call_count == 5
        assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[1][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[2][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[3][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[4][0][0] == mock_tc
        mock_tc.removeSelectedText.assert_called_once_with()
        rp.ensureCursorVisible.assert_called_once_with()


def test_MicroPythonREPLPane_clear():
    """
    Ensure setText is called with an empty string.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.panes.QSerialPort', mock_serial_class):
        rp = mu.interface.panes.MicroPythonREPLPane('COM0')
        rp.setText = mock.MagicMock(return_value=None)
        rp.clear()
        rp.setText.assert_called_once_with('')


def test_MuFileList_disable():
    """
    Disable and block drops on the current and sibling MuFileList.
    """
    mock_sibling = mock.MagicMock()
    mfl = mu.interface.panes.MuFileList()
    mfl.setDisabled = mock.MagicMock(return_value=True)
    mfl.setAcceptDrops = mock.MagicMock(return_value=True)
    mfl.disable(mock_sibling)
    mfl.setDisabled.assert_called_once_with(True)
    mock_sibling.setDisabled.assert_called_once_with(True)
    mfl.setAcceptDrops.assert_called_once_with(False)
    mock_sibling.setAcceptDrops.assert_called_once_with(False)


def test_MuFileList_enable():
    """
    Allow drops and interactions with current and sibling MuFileList.
    """
    mock_sibling = mock.MagicMock()
    mfl = mu.interface.panes.MuFileList()
    mfl.setDisabled = mock.MagicMock(return_value=True)
    mfl.setAcceptDrops = mock.MagicMock(return_value=True)
    mfl.enable(mock_sibling)
    mfl.setDisabled.assert_called_once_with(False)
    mock_sibling.setDisabled.assert_called_once_with(False)
    mfl.setAcceptDrops.assert_called_once_with(True)
    mock_sibling.setAcceptDrops.assert_called_once_with(True)


def test_MuFileList_show_confirm_overwrite_dialog():
    """
    Ensure the user is notified of an existing file.
    """
    mfl = mu.interface.panes.MuFileList()
    mock_qmb = mock.MagicMock()
    mock_qmb.setIcon = mock.MagicMock(return_value=None)
    mock_qmb.setText = mock.MagicMock(return_value=None)
    mock_qmb.setWindowTitle = mock.MagicMock(return_value=None)
    mock_qmb.exec_ = mock.MagicMock(return_value=QMessageBox.Ok)
    mock_qmb_class = mock.MagicMock(return_value=mock_qmb)
    mock_qmb_class.Ok = QMessageBox.Ok
    mock_qmb_class.Information = QMessageBox.Information
    with mock.patch('mu.interface.panes.QMessageBox', mock_qmb_class):
        assert mfl.show_confirm_overwrite_dialog()
    msg = 'File already exists; overwrite it?'
    mock_qmb.setText.assert_called_once_with(msg)
    mock_qmb.setWindowTitle.assert_called_once_with('File already exists')
    mock_qmb.setIcon.assert_called_once_with(QMessageBox.Information)


def test_MicrobitFileList_init():
    """
    Check the widget references the user's home and allows drag and drop.
    """
    mfs = mu.interface.panes.MicrobitFileList('home/path')
    assert mfs.home == 'home/path'
    assert mfs.dragDropMode() == mfs.DragDrop


def test_MicrobitFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.LocalFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mfs = mu.interface.panes.MicrobitFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.enable = mock.MagicMock()
    mfs.parent = mock.MagicMock()
    with mock.patch('mu.interface.panes.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.panes.MuFileList.dropEvent',
                       return_value=None) as mock_dropEvent, \
            mock.patch('mu.interface.panes.microfs.put',
                       return_value=True) as mock_put:
        mfs.dropEvent(mock_event)
        mfs.disable.assert_called_once_with(source)
        home = os.path.join('homepath', 'foo.py')
        mock_put.assert_called_once_with(home, mock_serial)
        mock_dropEvent.assert_called_once_with(mock_event)
        mfs.enable.assert_called_once_with(source)
        mfs.parent().ls.assert_called_once_with()


def test_MicrobitFileList_dropEvent_error():
    """
    Ensure that if an error occurs there is no change in the file list state.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.LocalFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mfs = mu.interface.panes.MicrobitFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.enable = mock.MagicMock()
    ex = IOError('BANG')
    with mock.patch('mu.interface.panes.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.panes.microfs.put', side_effect=ex), \
            mock.patch('mu.interface.panes.logger.error',
                       return_value=None) as log:
        mfs.dropEvent(mock_event)
        log.assert_called_once_with(ex)
        mfs.disable.assert_called_once_with(source)
        mfs.enable.assert_called_once_with(source)


def test_MicrobitFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    mfs = mu.interface.panes.MicrobitFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.enable = mock.MagicMock()
    with mock.patch('mu.interface.panes.microfs.put', return_value=None) as mp:
        mfs.dropEvent(mock_event)
        assert mp.call_count == 0
    mfs.disable.assert_called_once_with(source)
    mfs.enable.assert_called_once_with(source)


def test_MicrobitFileList_contextMenuEvent():
    """
    Ensure that the menu displayed when a file on the micro:bit is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicrobitFileList('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.mapToGlobal = mock.MagicMock(return_value=None)
    mfs.setDisabled = mock.MagicMock(return_value=None)
    mfs.setAcceptDrops = mock.MagicMock(return_value=None)
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mock_event = mock.MagicMock()
    with mock.patch('mu.interface.panes.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.panes.microfs.rm',
                       return_value=None) as mock_rm, \
            mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
        mock_rm.assert_called_once_with('foo.py', mock_serial)
        assert mfs.setDisabled.call_count == 2
        assert mfs.setAcceptDrops.call_count == 2


def test_MicrobitFileList_contextMenuEvent_error():
    """
    Ensure that if there's an error while preparing for the rm operation that
    it aborts without enacting.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicrobitFileList('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.mapToGlobal = mock.MagicMock(return_value=None)
    mfs.setDisabled = mock.MagicMock(return_value=None)
    mfs.setAcceptDrops = mock.MagicMock(return_value=None)
    mfs.takeItem = mock.MagicMock(return_value=None)
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mock_event = mock.MagicMock()
    ex = IOError('BANG')
    with mock.patch('mu.interface.panes.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.panes.microfs.rm', side_effect=ex), \
            mock.patch('mu.interface.panes.QMenu', return_value=mock_menu), \
            mock.patch('mu.interface.panes.logger.error',
                       return_value=None) as log:
        mfs.contextMenuEvent(mock_event)
        log.assert_called_once_with(ex)
        assert mfs.takeItem.call_count == 0
        assert mfs.setDisabled.call_count == 2
        assert mfs.setAcceptDrops.call_count == 2


def test_LocalFileList_init():
    """
    Ensure the class instantiates with the expected state.
    """
    lfl = mu.interface.panes.LocalFileList('home/path')
    assert lfl.home == 'home/path'
    assert lfl.dragDropMode() == lfl.DragDrop


def test_LocalFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.MicrobitFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    lfs = mu.interface.panes.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.enable = mock.MagicMock()
    lfs.parent = mock.MagicMock()
    with mock.patch('mu.interface.panes.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.panes.MuFileList.dropEvent',
                       return_value=None) as mock_dropEvent, \
            mock.patch('mu.interface.panes.microfs.get',
                       return_value=True) as mock_get:
        lfs.dropEvent(mock_event)
        lfs.disable.assert_called_once_with(source)
        home = os.path.join('homepath', 'foo.py')
        mock_get.assert_called_once_with('foo.py', home, mock_serial)
        mock_dropEvent.assert_called_once_with(mock_event)
        lfs.enable.assert_called_once_with(source)
        lfs.parent().ls.assert_called_once_with()


def test_LocalFileList_dropEvent_error():
    """
    Ensure that if an error occurs there is no change in the file list state.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.MicrobitFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    lfs = mu.interface.panes.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.enable = mock.MagicMock()
    ex = IOError('BANG')
    with mock.patch('mu.interface.panes.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.panes.microfs.get', side_effect=ex), \
            mock.patch('mu.interface.panes.logger.error',
                       return_value=None) as log:
        lfs.dropEvent(mock_event)
        log.assert_called_once_with(ex)
        lfs.disable.assert_called_once_with(source)
        lfs.enable.assert_called_once_with(source)


def test_LocalFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    lfs = mu.interface.panes.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.enable = mock.MagicMock()
    with mock.patch('mu.interface.panes.microfs.put', return_value=None) as mp:
        lfs.dropEvent(mock_event)
        assert mp.call_count == 0
    lfs.disable.assert_called_once_with(source)
    lfs.enable.assert_called_once_with(source)


def test_FileSystemPane_init():
    """
    Check things are set up as expected.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls',
                    return_value=None) as mock_ls:
        fsp = mu.interface.panes.FileSystemPane('homepath')
    mock_ls.assert_called_once_with()
    assert isinstance(fsp.microbit_label, QLabel)
    assert isinstance(fsp.local_label, QLabel)
    assert isinstance(fsp.microbit_fs, QListWidget)
    assert isinstance(fsp.local_fs, QListWidget)


def test_FileSystemPane_ls():
    """
    Ensure the ls method works as expected.
    """
    microbit_files = ['foo.py', 'bar.py', 'baz.py']
    local_files = ['spam.py', 'eggs.py']
    # MOCK ALL TEH THIGNS!
    with mock.patch('mu.interface.panes.MicrobitFileList.clear',
                    return_value=None) as mfs_clear, \
            mock.patch('mu.interface.panes.LocalFileList.clear',
                       return_value=None) as lfs_clear, \
            mock.patch('mu.interface.panes.microfs.ls',
                       return_value=microbit_files), \
            mock.patch('mu.interface.panes.microfs.get_serial',
                       return_value=None), \
            mock.patch('mu.interface.panes.os.listdir',
                       return_value=local_files), \
            mock.patch('mu.interface.panes.os.path.isfile',
                       return_value=True), \
            mock.patch('mu.interface.panes.os.path.join',
                       return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
        mfs_clear.assert_called_once_with()
        lfs_clear.assert_called_once_with()
        assert fsp.microbit_fs.count() == 3
        assert fsp.local_fs.count() == 2


def test_FileSystemPane_set_theme_day():
    """
    Ensures the day theme is set.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.setStyleSheet = mock.MagicMock()
    fsp.set_theme('day')
    fsp.setStyleSheet.assert_called_once_with(mu.interface.themes.DAY_STYLE)


def test_FileSystemPane_set_theme_night():
    """
    Ensures the night theme is set.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.setStyleSheet = mock.MagicMock()
    fsp.set_theme('night')
    fsp.setStyleSheet.assert_called_once_with(mu.interface.themes.NIGHT_STYLE)


def test_FileSystemPane_set_theme_contrast():
    """
    Ensures the contrast theme is set.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.setStyleSheet = mock.MagicMock()
    fsp.set_theme('contrast')
    fsp.setStyleSheet.assert_called_once_with(
        mu.interface.themes.CONTRAST_STYLE)


def test_FileSystemPane_set_font_size():
    """
    Ensure the right size is set as the point size and the text based UI child
    widgets are updated.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.font = mock.MagicMock()
    fsp.microbit_label = mock.MagicMock()
    fsp.local_label = mock.MagicMock()
    fsp.microbit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.set_font_size(22)
    fsp.font.setPointSize.assert_called_once_with(22)
    fsp.microbit_label.setFont.assert_called_once_with(fsp.font)
    fsp.local_label.setFont.assert_called_once_with(fsp.font)
    fsp.microbit_fs.setFont.assert_called_once_with(fsp.font)
    fsp.local_fs.setFont.assert_called_once_with(fsp.font)


def test_FileSystemPane_zoom_in():
    """
    Ensure the font is re-set bigger when zooming in.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.set_font_size = mock.MagicMock()
    fsp.zoomIn()
    expected = mu.interface.themes.DEFAULT_FONT_SIZE + 2
    fsp.set_font_size.assert_called_once_with(expected)


def test_FileSystemPane_zoom_out():
    """
    Ensure the font is re-set smaller when zooming out.
    """
    with mock.patch('mu.interface.panes.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.set_font_size = mock.MagicMock()
    fsp.zoomOut()
    expected = mu.interface.themes.DEFAULT_FONT_SIZE - 2
    fsp.set_font_size.assert_called_once_with(expected)


def test_JupyterREPLPane_init():
    """
    Ensure the widget is setup with the correct defaults.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    assert jw.console_height == 10


def test_JupyterREPLPane_set_font_size():
    """
    Check the correct stylesheet values are being set.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_font_size(16)
    style = jw.setStyleSheet.call_args[0][0]
    assert 'font-size: 16pt;' in style
    assert 'font-family: Monospace;' in style


def test_JupyterREPLPane_zoomIn():
    """
    Ensure zooming in increases the font size.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_font_size = mock.MagicMock()
    old_size = jw.font.pointSize()
    jw.zoomIn(delta=4)
    jw.set_font_size.assert_called_once_with(old_size + 4)


def test_JupyterREPLPane_zoomOut():
    """
    Ensure zooming out decreases the font size.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_font_size = mock.MagicMock()
    old_size = jw.font.pointSize()
    jw.zoomOut(delta=4)
    jw.set_font_size.assert_called_once_with(old_size - 4)


def test_JupyterREPLPane_set_theme_day():
    """
    Make sure the theme is correctly set for day.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_theme('day')
    jw.set_default_style.assert_called_once_with()
    jw.setStyleSheet.assert_called_once_with(mu.interface.themes.DAY_STYLE)


def test_JupyterREPLPane_set_theme_night():
    """
    Make sure the theme is correctly set for night.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_theme('night')
    jw.set_default_style.assert_called_once_with(colors='nocolor')
    jw.setStyleSheet.assert_called_once_with(mu.interface.themes.NIGHT_STYLE)


def test_JupyterREPLPane_set_theme_contrast():
    """
    Make sure the theme is correctly set for high contrast.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_theme('contrast')
    jw.set_default_style.assert_called_once_with(colors='nocolor')
    jw.setStyleSheet.assert_called_once_with(
        mu.interface.themes.CONTRAST_STYLE)


def test_PythonProcessPane_init():
    """
    Check the font and input_buffer is set.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    assert ppp.font()
    assert ppp.input_buffer == []


def test_PythonProcessPane_start_process():
    """
    Ensure the widget is created as expected.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.start_process('workspace', 'script.py')
    assert mock_process_class.call_count == 1
    assert ppp.process == mock_process
    ppp.process.setProcessChannelMode.assert_called_once_with(mock_merge_chans)
    ppp.process.setWorkingDirectory.assert_called_once_with('workspace')
    ppp.process.readyRead.connect.assert_called_once_with(ppp.read)
    ppp.process.finished.connect.assert_called_once_with(ppp.finished)
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    mu_dir = os.path.dirname(os.path.abspath(mu.__file__))
    runner = os.path.join(mu_dir, 'mu-debug.py')
    expected_args = ['-i', runner, expected_script, ]
    expected_python = sys.executable
    ppp.process.start.assert_called_once_with(expected_python, expected_args)


def test_PythonProcessPane_finished():
    """
    Check the functionality to handle the process finishing is correct.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.insertText = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setReadOnly = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.finished(0, 1)
    assert mock_cursor.insertText.call_count == 2
    assert 'exit code: 0' in mock_cursor.insertText.call_args[0][0]
    assert 'status: 1' in mock_cursor.insertText.call_args[0][0]
    ppp.setReadOnly.assert_called_once_with(True)
    ppp.setTextCursor.assert_called_once_with(ppp.textCursor())


def test_PythonProcessPane_append():
    """
    Ensure the referenced byte_stream is added to the textual content of the
    QTextEdit.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.insertText = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.append(b'hello')
    mock_cursor.insertText.assert_called_once_with('hello')


def test_PythonProcessPane_delete():
    """
    Make sure that removing a character from the QTextEdit works as expected.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.input_buffer = ['a', 'b', ]
    mock_cursor = mock.MagicMock()
    mock_cursor.deletePreviousChar = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.delete()
    assert ppp.input_buffer == ['a', ]
    mock_cursor.deletePreviousChar.assert_called_once_with()


def test_PythonProcessPane_read():
    """
    Ensure incoming bytes from sub-process's stout are processed correctly.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.append = mock.MagicMock()
    ppp.process = mock.MagicMock()
    ppp.read()
    assert ppp.append.call_count == 1
    assert ppp.process.readAll().data.call_count == 1


def test_PythonProcessPane_keyPressEvent_a():
    """
    A "regular" character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_A)
    data.text = mock.MagicMock(return_value='a')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    assert ppp.input_buffer == [b'a', ]


def test_PythonProcessPane_keyPressEvent_backspace():
    """
    A backspace is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.input_buffer = [b'a', 'b', ]
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
    data.text = mock.MagicMock(return_value='\b')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    assert ppp.input_buffer == [b'a', ]


def test_PythonProcessPane_keyPressEvent_paste():
    """
    Control-V (paste)  character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_V)
    data.text = mock.MagicMock(return_value='')
    data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier |
                                    Qt.ShiftModifier)
    ppp.paste = mock.MagicMock()
    ppp.keyPressEvent(data)
    ppp.paste.assert_called_once_with()


def test_PythonProcessPane_keyPressEvent_copy():
    """
    A "regular" character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_C)
    data.text = mock.MagicMock(return_value='')
    data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier |
                                    Qt.ShiftModifier)
    ppp.copy = mock.MagicMock()
    ppp.keyPressEvent(data)
    ppp.copy.assert_called_once_with()


def test_PythonProcessPane_keyPressEvent_newline():
    """
    A "regular" character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.input_buffer = [b'a', ]
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Enter)
    data.text = mock.MagicMock(return_value='\r')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    assert ppp.input_buffer == []
    ppp.process.write.assert_called_once_with(b'a\n')


def test_PythonProcessPane_zoomIn():
    """
    Check ZoomIn increases point size.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 12
    with mock.patch('mu.interface.panes.QTextEdit.zoomIn') as mock_zoom:
        ppp.zoomIn(8)
        mock_zoom.assert_called_once_with(8)


def test_PythonProcessPane_zoomIn_max():
    """
    Check ZoomIn only works up to point size of 34
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 34
    with mock.patch('mu.interface.panes.QTextEdit.zoomIn') as mock_zoom:
        ppp.zoomIn(8)
        assert mock_zoom.call_count == 0


def test_PythonProcessPane_zoomOut():
    """
    Check ZoomOut decreases point size.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 12
    with mock.patch('mu.interface.panes.QTextEdit.zoomOut') as mock_zoom:
        ppp.zoomOut(6)
        mock_zoom.assert_called_once_with(6)


def test_PythonProcessPane_zoomOut_min():
    """
    Check ZoomOut decreases point size down to 4
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 4
    with mock.patch('mu.interface.panes.QTextEdit.zoomOut') as mock_zoom:
        ppp.zoomOut(8)
        assert mock_zoom.call_count == 0


def test_PythonProcessPane_set_theme_day():
    """
    Set the theme to day.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.setStyleSheet = mock.MagicMock()
    ppp.set_theme('day')
    ppp.setStyleSheet.assert_called_once_with(mu.interface.themes.DAY_STYLE)


def test_PythonProcessPane_set_theme_night():
    """
    Set the theme to night.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.setStyleSheet = mock.MagicMock()
    ppp.set_theme('night')
    ppp.setStyleSheet.assert_called_once_with(mu.interface.themes.NIGHT_STYLE)


def test_PythonProcessPane_set_theme_contrast():
    """
    Set the theme to high contrast.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.setStyleSheet = mock.MagicMock()
    ppp.set_theme('contrast')
    ppp.setStyleSheet.assert_called_once_with(
        mu.interface.themes.CONTRAST_STYLE)


def test_DebugInspector_set_font_size():
    """
    Check the correct stylesheet values are being set.
    """
    di = mu.interface.panes.DebugInspector()
    di.setStyleSheet = mock.MagicMock()
    di.set_font_size(16)
    style = di.setStyleSheet.call_args[0][0]
    assert 'font-size: 16pt;' in style
    assert 'font-family: Monospace;' in style


def test_DebugInspector_zoomIn():
    """
    Ensure zooming in increases the font size.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_font_size = mock.MagicMock()
    old_size = di.font().pointSize()
    di.zoomIn(delta=4)
    di.set_font_size.assert_called_once_with(old_size + 4)


def test_DebugInspector_zoomOut():
    """
    Ensure zooming out decreases the font size.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_font_size = mock.MagicMock()
    old_size = di.font().pointSize()
    di.zoomOut(delta=4)
    di.set_font_size.assert_called_once_with(old_size - 4)


def test_DebugInspector_set_theme_day():
    """
    Make sure the theme is correctly set for day.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_default_style = mock.MagicMock()
    di.setStyleSheet = mock.MagicMock()
    di.set_theme('day')
    di.setStyleSheet.assert_called_once_with(mu.interface.themes.DAY_STYLE)


def test_DebugInspector_set_theme_night():
    """
    Make sure the theme is correctly set for night.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_default_style = mock.MagicMock()
    di.setStyleSheet = mock.MagicMock()
    di.set_theme('night')
    di.setStyleSheet.assert_called_once_with(mu.interface.themes.NIGHT_STYLE)


def test_DebugInspector_set_theme_contrast():
    """
    Make sure the theme is correctly set for high contrast.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_default_style = mock.MagicMock()
    di.setStyleSheet = mock.MagicMock()
    di.set_theme('contrast')
    di.setStyleSheet.assert_called_once_with(
        mu.interface.themes.CONTRAST_STYLE)
