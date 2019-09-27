# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QTreeWidgetItem
from PyQt5.QtChart import QChart, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QTextCursor
from unittest import mock
import sys
import os
import signal
import mu
import platform
from collections import deque
import mu.interface.panes
import pytest


# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


@pytest.fixture
def drop_event():
    drop_event = mock.MagicMock()
    source = mu.interface.panes.LocalFileList('pc_home_path')
    mock_item = mock.MagicMock()
    mock_item.text = mock.MagicMock(return_value='pc_foo.py')
    source.currentItem = mock.MagicMock(return_value=mock_item)
    drop_event.source = mock.MagicMock(return_value=source)
    drop_event.pos.return_value = QPoint(0, 0)
    return drop_event


def test_PANE_ZOOM_SIZES():
    """
    Ensure the expected entries define font sizes in PANE_ZOOM_SIZES.
    """
    expected_sizes = ('xs', 's', 'm', 'l', 'xl', 'xxl', 'xxxl')
    for size in expected_sizes:
        assert size in mu.interface.panes.PANE_ZOOM_SIZES
    assert len(expected_sizes) == len(mu.interface.panes.PANE_ZOOM_SIZES)


def test_MicroPythonREPLPane_init_default_args():
    """
    Ensure the MicroPython REPLPane object is instantiated as expected.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    assert rp.serial == mock_serial


def test_MicroPythonREPLPane_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'paste me!'
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.panes.QApplication', mock_application):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
        rp.paste()
    mock_serial.write.assert_called_once_with(bytes('paste me!', 'utf8'))


def test_MicroPythonREPLPane_paste_handle_unix_newlines():
    """
    Pasting into the REPL should handle '\n' properly.

    '\n' -> '\r'
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'paste\nme!'
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.panes.QApplication', mock_application):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
        rp.paste()
    mock_serial.write.assert_called_once_with(bytes('paste\rme!', 'utf8'))


def test_MicroPythonREPLPane_paste_handle_windows_newlines():
    """
    Pasting into the REPL should handle '\r\n' properly.

    '\r\n' -> '\r'
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'paste\r\nme!'
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.panes.QApplication', mock_application):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
        rp.paste()
    mock_serial.write.assert_called_once_with(bytes('paste\rme!', 'utf8'))


def test_MicroPythonREPLPane_paste_only_works_if_there_is_something_to_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = ''
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.panes.QApplication', mock_application):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
        rp.paste()
    assert mock_serial.write.call_count == 0


def test_MicroPythonREPLPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'WinNT'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.panes.platform', mock_platform), \
            mock.patch('mu.interface.panes.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.panes.QCursor'):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'Darwin'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.panes.platform', mock_platform), \
            mock.patch('mu.interface.panes.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.panes.QCursor'):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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


def test_MicroPythonREPLPane_keyPressEvent():
    """
    Ensure key presses in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
    data.text = mock.MagicMock(return_value='\b')
    data.modifiers = mock.MagicMock(return_value=None)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(b'\b')


def test_MicroPythonREPLPane_keyPressEvent_delete():
    """
    Ensure delete in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Delete)
    data.text = mock.MagicMock(return_value='\b')
    data.modifiers = mock.MagicMock(return_value=None)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(b'\x1B[\x33\x7E')


def test_MicroPythonREPLPane_keyPressEvent_up():
    """
    Ensure up arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    rp.copy = mock.MagicMock()
    data = mock.MagicMock()
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    rp.paste = mock.MagicMock()
    data = mock.MagicMock()
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(side_effect=[True, False, True,
                                                       True])
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
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
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    rp.setText = mock.MagicMock(return_value=None)
    rp.clear()
    rp.setText.assert_called_once_with('')


def test_MicroPythonREPLPane_set_font_size():
    """
    Ensure the font is updated to the expected point size.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    mock_font = mock.MagicMock()
    rp.font = mock.MagicMock(return_value=mock_font)
    rp.setFont = mock.MagicMock()
    rp.set_font_size(123)
    mock_font.setPointSize.assert_called_once_with(123)
    rp.setFont.assert_called_once_with(mock_font)


def test_MicroPythonREPLPane_set_zoom():
    """
    Ensure the font size is correctly set from the t-shirt size.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    rp.set_font_size = mock.MagicMock()
    rp.set_zoom('xxl')
    expected = mu.interface.panes.PANE_ZOOM_SIZES['xxl']
    rp.set_font_size.assert_called_once_with(expected)


def test_MicroPythonREPLPane_send_commands():
    """
    Ensure the list of commands is correctly encoded and bound by control
    commands to put the board into and out of raw mode.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    rp.execute = mock.MagicMock()
    commands = [
        "import os",
        "print(os.listdir())",
    ]
    rp.send_commands(commands)
    expected = [
        b'\x02',  # Put the board into raw mode.
        b'\r\x03',
        b'\r\x03',
        b'\r\x03',
        b'\r\x01',
        b'print("\\n")\r',  # Ensure a newline at the start of output.
        b'import os\r',  # The commands to run.
        b'print(os.listdir())\r',
        b'\r',  # Ensure newline after commands.
        b'\x04',  # Evaluate the commands.
        b'\x02',  # Leave raw mode.
    ]
    rp.execute.assert_called_once_with(expected)


def test_MicroPythonREPLPane_execute():
    """
    Ensure the first command is sent via serial to the connected device, and
    further commands are scheduled for the future.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    commands = [b'A', b'B', ]
    with mock.patch('mu.interface.panes.QTimer') as mock_timer:
        rp.execute(commands)
        mock_serial.write.assert_called_once_with(b'A')
        assert mock_timer.singleShot.call_count == 1


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
    msg = _('File already exists; overwrite it?')
    mock_qmb.setText.assert_called_once_with(msg)
    mock_qmb.setWindowTitle.assert_called_once_with(_('File already exists'))
    mock_qmb.setIcon.assert_called_once_with(QMessageBox.Information)


def test_MicroPythonDeviceFileList_init():
    """
    Check the widget references the user's home and allows drag and drop.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileList('home/path')
    assert mfs.home == 'home/path'
    assert mfs.dragDropMode() == mfs.DragDrop


def test_MicroPythonDeviceFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.LocalFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mfs = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.put = mock.MagicMock()
    # Test
    mfs.dropEvent(mock_event)
    fn = os.path.join('homepath', 'foo.py')
    assert mfs.set_message.emit.call_count == 1
    mfs.put.emit.assert_called_once_with(fn)


def test_MicroPythonDeviceFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    mfs = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mfs.findItems = mock.MagicMock()
    mfs.dropEvent(mock_event)
    assert mfs.findItems.call_count == 0


def test_MicroPythonDeviceFileList_on_put():
    """
    A message and list_files signal should be emitted.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mfs.set_message = mock.MagicMock()
    mfs.list_files = mock.MagicMock()
    mfs.on_put('my_file.py')
    msg = _("'{}' successfully copied to micro:bit.").format('my_file.py')
    mfs.set_message.emit.assert_called_once_with(msg)
    mfs.list_files.emit.assert_called_once_with()


def test_MicroPythonDeviceFileList_contextMenuEvent():
    """
    Ensure that the menu displayed when a file on the micro:bit is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.delete = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    with mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    mfs.disable.emit.assert_called_once_with()
    assert mfs.set_message.emit.call_count == 1
    mfs.delete.emit.assert_called_once_with('foo.py')


def test_MicroPythonFileList_on_delete():
    """
    On delete should emit a message and list_files signal.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mfs.set_message = mock.MagicMock()
    mfs.list_files = mock.MagicMock()
    mfs.on_delete('my_file.py')
    msg = "'my_file.py' successfully deleted from micro:bit."
    mfs.set_message.emit.assert_called_once_with(msg)
    mfs.list_files.emit.assert_called_once_with()


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
    source = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    lfs = mu.interface.panes.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.set_message = mock.MagicMock()
    lfs.get = mock.MagicMock()
    # Test
    lfs.dropEvent(mock_event)
    fn = os.path.join('homepath', 'foo.py')
    lfs.disable.emit.assert_called_once_with()
    assert lfs.set_message.emit.call_count == 1
    lfs.get.emit.assert_called_once_with('foo.py', fn)


def test_LocalFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    lfs = mu.interface.panes.LocalFileList('homepath')
    lfs.findItems = mock.MagicMock()
    lfs.dropEvent(mock_event)
    assert lfs.findItems.call_count == 0


def test_LocalFileList_on_get():
    """
    On get should emit two signals: a message and list_files.
    """
    lfs = mu.interface.panes.LocalFileList('homepath')
    lfs.set_message = mock.MagicMock()
    lfs.list_files = mock.MagicMock()
    lfs.on_get('my_file.py')
    msg = _("Successfully copied '{}' from the micro:bit "
            "to your computer.").format('my_file.py')
    lfs.set_message.emit.assert_called_once_with(msg)
    lfs.list_files.emit.assert_called_once_with()


def test_LocalFileList_contextMenuEvent():
    """
    Ensure that the menu displayed when a local file is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action_first = mock.MagicMock()
    mock_action_second = mock.MagicMock()
    mock_menu.addAction.side_effect = [mock_action_first,
                                       mock_action_second]
    mock_menu.exec_.return_value = mock_action_first
    mfs = mu.interface.panes.LocalFileList('homepath')
    mock_open = mock.MagicMock()
    mfs.open_file = mock.MagicMock()
    mfs.open_file.emit = mock_open
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.set_message = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    with mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    assert mfs.set_message.emit.call_count == 0
    mock_open.assert_called_once_with(os.path.join('homepath', 'foo.py'))


def test_LocalFileList_contextMenuEvent_external():
    """
    Ensure that the menu displayed when a local file is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.side_effect = [mock_action, mock.MagicMock()]
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.LocalFileList('homepath')
    mock_open = mock.MagicMock()
    mfs.open_file = mock.MagicMock()
    mfs.open_file.emit = mock_open
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.qwerty'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.set_message = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    with mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    assert mfs.set_message.emit.call_count == 1
    assert mock_open.call_count == 0


def test_FileSystemPane_init():
    """
    Check things are set up as expected.
    """
    home = 'homepath'
    test_microbit_fs = mu.interface.panes.MicroPythonDeviceFileList(home)
    test_microbit_fs.disable = mock.MagicMock()
    test_microbit_fs.set_message = mock.MagicMock()
    test_local_fs = mu.interface.panes.LocalFileList(home)
    test_local_fs.disable = mock.MagicMock()
    test_local_fs.set_message = mock.MagicMock()
    mock_mfl = mock.MagicMock(return_value=test_microbit_fs)
    mock_lfl = mock.MagicMock(return_value=test_local_fs)
    with mock.patch('mu.interface.panes.MicroPythonDeviceFileList',
                    mock_mfl), \
            mock.patch('mu.interface.panes.LocalFileList', mock_lfl):
        fsp = mu.interface.panes.FileSystemPane('homepath')
        assert isinstance(fsp.microbit_label, QLabel)
        assert isinstance(fsp.local_label, QLabel)
        assert fsp.microbit_fs == test_microbit_fs
        assert fsp.local_fs == test_local_fs
        test_microbit_fs.disable.connect.assert_called_once_with(fsp.disable)
        test_microbit_fs.set_message.connect.\
            assert_called_once_with(fsp.show_message)
        test_local_fs.disable.connect.assert_called_once_with(fsp.disable)
        test_local_fs.set_message.connect.\
            assert_called_once_with(fsp.show_message)


def test_FileSystemPane_disable():
    """
    The child list widgets are disabled correctly.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.microbit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.disable()
    fsp.microbit_fs.setDisabled.assert_called_once_with(True)
    fsp.local_fs.setDisabled.assert_called_once_with(True)
    fsp.microbit_fs.setAcceptDrops.assert_called_once_with(False)
    fsp.local_fs.setAcceptDrops.assert_called_once_with(False)


def test_FileSystemPane_enable():
    """
    The child list widgets are enabled correctly.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.microbit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.enable()
    fsp.microbit_fs.setDisabled.assert_called_once_with(False)
    fsp.local_fs.setDisabled.assert_called_once_with(False)
    fsp.microbit_fs.setAcceptDrops.assert_called_once_with(True)
    fsp.local_fs.setAcceptDrops.assert_called_once_with(True)


def test_FileSystemPane_set_theme():
    """
    Setting theme doesn't error
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.set_theme('test')


def test_FileSystemPane_show_message():
    """
    Ensure the expected message signal is emitted.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.set_message = mock.MagicMock()
    fsp.show_message('Hello')
    fsp.set_message.emit.assert_called_once_with('Hello')


def test_FileSystemPane_show_warning():
    """
    Ensure the expected warning signal is emitted.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.set_warning = mock.MagicMock()
    fsp.show_warning('Hello')
    fsp.set_warning.emit.assert_called_once_with('Hello')


def test_FileSystemPane_on_ls():
    """
    When lists of files have been obtained from the micro:bit and local
    filesystem, make sure they're properly processed by the on_ls event
    handler.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    microbit_files = ['foo.py', 'bar.py', ]
    fsp.microbit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.enable = mock.MagicMock()
    local_files = ['qux.py', 'baz.py', ]
    mock_listdir = mock.MagicMock(return_value=local_files)
    mock_isfile = mock.MagicMock(return_value=True)
    with mock.patch('mu.interface.panes.os.listdir', mock_listdir),\
            mock.patch('mu.interface.panes.os.path.isfile', mock_isfile):
        fsp.on_ls(microbit_files)
    fsp.microbit_fs.clear.assert_called_once_with()
    fsp.local_fs.clear.assert_called_once_with()
    assert fsp.microbit_fs.addItem.call_count == 2
    assert fsp.local_fs.addItem.call_count == 2
    fsp.enable.assert_called_once_with()


def test_FileSystemPane_on_ls_fail():
    """
    A warning is emitted and the widget disabled if listing files fails.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.disable = mock.MagicMock()
    fsp.on_ls_fail()
    assert fsp.show_warning.call_count == 1
    fsp.disable.assert_called_once_with()


def test_FileSystem_Pane_on_put_fail():
    """
    A warning is emitted if putting files on the micro:bit fails.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.on_put_fail('foo.py')
    assert fsp.show_warning.call_count == 1


def test_FileSystem_Pane_on_delete_fail():
    """
    A warning is emitted if deleting files on the micro:bit fails.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.on_delete_fail('foo.py')
    assert fsp.show_warning.call_count == 1


def test_FileSystem_Pane_on_get_fail():
    """
    A warning is emitted if getting files from the micro:bit fails.
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.on_get_fail('foo.py')
    assert fsp.show_warning.call_count == 1


def test_FileSystemPane_set_font_size():
    """
    Ensure the right size is set as the point size and the text based UI child
    widgets are updated.
    """
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


def test_FileSystemPane_open_file():
    """
    FileSystemPane should propogate the open_file signal
    """
    fsp = mu.interface.panes.FileSystemPane('homepath')
    fsp.open_file = mock.MagicMock()
    mock_open_emit = mock.MagicMock()
    fsp.open_file.emit = mock_open_emit
    fsp.local_fs.open_file.emit('test')
    mock_open_emit.assert_called_once_with('test')


def test_JupyterREPLPane_init():
    """
    Ensure the widget is setup with the correct defaults.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    assert jw.console_height == 10


def test_JupyterREPLPane_append_plain_text():
    """
    Ensure signal and expected bytes are emitted when _append_plain_text is
    called.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.on_append_text = mock.MagicMock()
    jw._append_plain_text('hello')
    jw.on_append_text.emit.assert_called_once_with('hello'.encode('utf-8'))


def test_JupyterREPLPane_set_font_size():
    """
    Check the new point size is succesfully applied.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_font_size(16)
    assert jw.font.pointSize() == 16


def test_JupyterREPLPane_set_zoom():
    """
    Ensure the expected font point size is set from the zoom size.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_font_size = mock.MagicMock()
    jw.set_zoom('xxl')
    jw.set_font_size.\
        assert_called_once_with(mu.interface.panes.PANE_ZOOM_SIZES['xxl'])


def test_JupyterREPLPane_set_theme_day():
    """
    Make sure the theme is correctly set for day.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.set_theme('day')
    jw.set_default_style.assert_called_once_with()


def test_JupyterREPLPane_set_theme_night():
    """
    Make sure the theme is correctly set for night.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.set_theme('night')
    jw.set_default_style.assert_called_once_with(colors='nocolor')


def test_JupyterREPLPane_set_theme_contrast():
    """
    Make sure the theme is correctly set for high contrast.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.set_theme('contrast')
    jw.set_default_style.assert_called_once_with(colors='nocolor')


def test_JupyterREPLPane_setFocus():
    """
    Ensures setFocus actually occurs to the _control containing the REPL.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw._control = mock.MagicMock()
    jw.setFocus()
    jw._control.setFocus.assert_called_once_with()


def test_PythonProcessPane_init():
    """
    Check the font, input_buffer and other initial state is set as expected.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    assert ppp.font()
    assert ppp.process is None
    assert ppp.input_history == []
    assert ppp.start_of_current_line == 0
    assert ppp.history_position == 0
    assert ppp.running is False
    assert ppp.stdout_buffer == b''
    assert ppp.reading_stdout is False


def test_PythonProcessPane_start_process():
    """
    Ensure the default arguments for starting a new process work as expected.
    Interactive mode is True, no debugger flag nor additional arguments.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.start_process('script.py', 'workspace')
    assert mock_process_class.call_count == 1
    assert ppp.process == mock_process
    ppp.process.setProcessChannelMode.assert_called_once_with(mock_merge_chans)
    ppp.process.setWorkingDirectory.assert_called_once_with('workspace')
    ppp.process.readyRead.connect.\
        assert_called_once_with(ppp.try_read_from_stdout)
    ppp.process.finished.connect.assert_called_once_with(ppp.finished)
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    assert ppp.script == expected_script
    runner = sys.executable
    expected_args = ['-i', expected_script, ]  # called with interactive flag.
    ppp.process.start.assert_called_once_with(runner, expected_args)
    assert ppp.running is True


def test_PythonProcessPane_start_process_command_args():
    """
    Ensure that the new process is passed the expected comand line args.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ['foo', 'bar', ]
        ppp.start_process('script.py', 'workspace', command_args=args)
    runner = sys.executable
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    expected_args = ['-i', expected_script, 'foo', 'bar', ]
    ppp.process.start.assert_called_once_with(runner, expected_args)


def test_PythonProcessPane_start_process_debugger():
    """
    Ensure starting a new process with the debugger flag set to True uses the
    debug runner to execute the script.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ['foo', 'bar', ]
        ppp.start_process('script.py', 'workspace', debugger=True,
                          command_args=args)
    mu_dir = os.path.dirname(os.path.abspath(mu.__file__))
    runner = os.path.join(mu_dir, 'mu-debug.py')
    python_exec = sys.executable
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    expected_args = [runner, expected_script, 'foo', 'bar', ]
    ppp.process.start.assert_called_once_with(python_exec, expected_args)


def test_PythonProcessPane_start_process_not_interactive():
    """
    Ensure that if the interactive flag is unset, the "-i" flag passed into
    the Python process is missing.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ['foo', 'bar', ]
        ppp.start_process('script.py', 'workspace', interactive=False,
                          command_args=args)
    runner = sys.executable
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    expected_args = [expected_script, 'foo', 'bar', ]
    ppp.process.start.assert_called_once_with(runner, expected_args)


def test_PythonProcessPane_start_process_windows_path():
    """
    If running on Windows via the installer ensure that the expected paths
    find their way into a temporary mu.pth file.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    mock_sys = mock.MagicMock()
    mock_sys.platform = 'win32'
    mock_sys.executable = 'C:\\Program Files\\Mu\\Python\\pythonw.exe'
    mock_os_p_e = mock.MagicMock(return_value=True)
    mock_os_makedirs = mock.MagicMock()
    mock_site = mock.MagicMock()
    mock_site.ENABLE_USER_SITE = True
    mock_site.USER_SITE = ('C:\\Users\\foo\\AppData\\Roaming\\Python\\'
                           'Python36\\site-packages')
    mock_site.getusersitepackages.return_value = mock_site.USER_SITE
    mock_open = mock.mock_open()
    with mock.patch('mu.interface.panes.QProcess', mock_process_class),\
            mock.patch('mu.interface.panes.sys', mock_sys),\
            mock.patch('mu.interface.panes.os.path.exists', mock_os_p_e),\
            mock.patch('mu.interface.panes.os.makedirs', mock_os_makedirs),\
            mock.patch('mu.interface.panes.site', mock_site),\
            mock.patch('builtins.open', mock_open):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.start_process('script.py', 'workspace', interactive=False)
    expected_pth = os.path.join(mock_site.USER_SITE, 'mu.pth')
    mock_os_makedirs.assert_called_once_with(mock_site.USER_SITE,
                                             exist_ok=True)
    mock_open.assert_called_once_with(expected_pth, 'w')
    expected = [
        'workspace',
        os.path.normcase(os.path.dirname(os.path.abspath('script.py'))),
    ]
    mock_file = mock_open()
    added_paths = [call[0][0] for call in mock_file.write.call_args_list]
    for e in expected:
        assert e + '\n' in added_paths


def test_PythonProcessPane_start_process_windows_path_no_user_site():
    """
    If running on Windows via the installer ensure that the Mu logs the
    fact it's unable to use the temporary mu.pth file because there is no
    USER_SITE enabled.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    mock_sys = mock.MagicMock()
    mock_sys.platform = 'win32'
    mock_sys.executable = 'C:\\Program Files\\Mu\\Python\\pythonw.exe'
    mock_os_p_e = mock.MagicMock(return_value=True)
    mock_site = mock.MagicMock()
    mock_site.ENABLE_USER_SITE = False
    mock_log = mock.MagicMock()
    with mock.patch('mu.interface.panes.QProcess', mock_process_class),\
            mock.patch('mu.interface.panes.sys', mock_sys),\
            mock.patch('mu.interface.panes.os.path.exists', mock_os_p_e),\
            mock.patch('mu.interface.panes.site', mock_site),\
            mock.patch('mu.interface.panes.logger', mock_log):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.start_process('script.py', 'workspace', interactive=False)
    logs = [call[0][0] for call in mock_log.info.call_args_list]
    expected = ("Unable to set Python paths. Python's USER_SITE not enabled."
                " Check configuration with administrator.")
    assert expected in logs


def test_PythonProcessPane_start_process_windows_path_with_exception():
    """
    If running on Windows via the installer ensure that the expected paths
    find their way into a temporary mu.pth file.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    mock_sys = mock.MagicMock()
    mock_sys.platform = 'win32'
    mock_sys.executable = 'C:\\Program Files\\Mu\\Python\\pythonw.exe'
    mock_os_p_e = mock.MagicMock(return_value=True)
    mock_site = mock.MagicMock()
    mock_site.ENABLE_USER_SITE = True
    mock_site.USER_SITE = ('C:\\Users\\foo\\AppData\\Roaming\\Python\\'
                           'Python36\\site-packages')
    mock_open = mock.MagicMock(side_effect=Exception("Boom"))
    mock_log = mock.MagicMock()
    with mock.patch('mu.interface.panes.QProcess', mock_process_class),\
            mock.patch('mu.interface.panes.sys', mock_sys),\
            mock.patch('mu.interface.panes.os.path.exists', mock_os_p_e),\
            mock.patch('mu.interface.panes.site', mock_site),\
            mock.patch('builtins.open', mock_open),\
            mock.patch('mu.interface.panes.logger', mock_log):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.start_process('script.py', 'workspace', interactive=False)
    logs = [call[0][0] for call in mock_log.error.call_args_list]
    expected = ("Could not set Python paths with mu.pth file.")
    assert expected in logs


def test_PythonProcessPane_start_process_user_enviroment_variables():
    """
    Ensure that if environment variables are set, they are set in the context
    of the new child Python process.

    If running on Darwin, ensure that the correct encoding for the Python
    environment is used (Flask stop and complain about a misconfigured
    Python 3 using an ASCII encoding).
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    mock_environment = mock.MagicMock()
    mock_environment_class = mock.MagicMock()
    mock_environment_class.systemEnvironment.return_value = mock_environment
    pypath = sys.path
    with mock.patch('mu.interface.panes.QProcess', mock_process_class), \
            mock.patch('mu.interface.panes.sys') as mock_sys, \
            mock.patch('mu.interface.panes.QProcessEnvironment',
                       mock_environment_class):
        mock_sys.platform = "darwin"
        mock_sys.path = pypath
        ppp = mu.interface.panes.PythonProcessPane()
        envars = [['name', 'value'], ]
        ppp.start_process('script.py', 'workspace', interactive=False,
                          envars=envars, runner='foo')
    expected_encoding = "{}.utf-8".format(mu.language_code)
    assert mock_environment.insert.call_count == 6
    assert mock_environment.insert.call_args_list[0][0] == ('PYTHONUNBUFFERED',
                                                            '1')
    assert mock_environment.insert.call_args_list[1][0] == ('PYTHONIOENCODING',
                                                            'utf-8')
    assert mock_environment.insert.call_args_list[2][0] == ('LC_ALL',
                                                            expected_encoding)
    assert mock_environment.insert.call_args_list[3][0] == ('LANG',
                                                            expected_encoding)
    assert mock_environment.insert.call_args_list[4][0] == ('name', 'value')
    expected_path = os.pathsep.join(pypath)
    assert mock_environment.insert.call_args_list[5][0] == ('PYTHONPATH',
                                                            expected_path)


def test_PythonProcessPane_start_process_custom_runner():
    """
    Ensure that if the runner is set, it is used as the command to start the
    new child Python process.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ['foo', 'bar', ]
        ppp.start_process('script.py', 'workspace', interactive=False,
                          command_args=args, runner='foo')
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    expected_args = [expected_script, 'foo', 'bar', ]
    ppp.process.start.assert_called_once_with('foo', expected_args)


def test_PythonProcessPane_start_process_custom_python_args():
    """
    Ensure that if there are arguments to be passed into the Python runtime
    starting the child process, these are passed on correctly.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.panes.QProcess', mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        py_args = ['-m', 'pgzero', ]
        ppp.start_process('script.py', 'workspace', interactive=False,
                          python_args=py_args)
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    expected_args = ['-m', 'pgzero', expected_script]
    runner = sys.executable
    ppp.process.start.assert_called_once_with(runner, expected_args)


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


def test_PythonProcessPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'WinNT'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.panes.platform', mock_platform), \
            mock.patch('mu.interface.panes.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.panes.QCursor'):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == 'Copy'
    assert copy_action[1] == ppp.copy
    assert copy_action[2].toString() == 'Ctrl+Shift+C'
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == 'Paste'
    assert paste_action[1] == ppp.paste
    assert paste_action[2].toString() == 'Ctrl+Shift+V'
    assert mock_qmenu.exec_.call_count == 1


def test_PythonProcessPane_context_menu_darwin():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'Darwin'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.panes.platform', mock_platform), \
            mock.patch('mu.interface.panes.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.panes.QCursor'):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == 'Copy'
    assert copy_action[1] == ppp.copy
    assert copy_action[2].toString() == 'Ctrl+C'
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == 'Paste'
    assert paste_action[1] == ppp.paste
    assert paste_action[2].toString() == 'Ctrl+V'
    assert mock_qmenu.exec_.call_count == 1


def test_PythonProcessPane_paste():
    """
    Ensure pasted text is handed off to the parse_paste method.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_paste = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'Hello'
    with mock.patch('mu.interface.panes.QApplication.clipboard',
                    return_value=mock_clipboard):
        ppp.paste()
    ppp.parse_paste.assert_called_once_with('Hello')


def test_PythonProcessPane_paste_normalize_windows_newlines():
    """
    Ensure that pasted text containing Windows style line-ends is normalised
    to '\n'.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_paste = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'h\r\ni'
    with mock.patch('mu.interface.panes.QApplication.clipboard',
                    return_value=mock_clipboard):
        ppp.paste()
    ppp.parse_paste.assert_called_once_with('h\ni')


def test_PythonProcessPane_parse_paste():
    """
    Given some text ensure that the first character is correctly handled and
    the remaining text to be processed is scheduled to be parsed in the future.

    Essentially parse_paste pretends to be someone typing in the characters of
    the pasted text *really fast*, rather than as a single shot dump of data.
    This is so the event loop can cycle to handle any output from the child
    process.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.parse_paste('hello')
    ppp.parse_input.assert_called_once_with(None, 'h', None)
    assert mock_timer.singleShot.call_count == 1


def test_PythonProcessPane_parse_paste_non_ascii():
    """
    Given some non-ascii yet printable text, ensure that the first character is
    correctly handled and the remaining text to be processed is scheduled to be
    parsed in the future.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.parse_paste('ÅÄÖ')
    ppp.parse_input.assert_called_once_with(None, 'Å', None)
    assert mock_timer.singleShot.call_count == 1


def test_PythonProcessPane_parse_paste_newline():
    """
    As above, but ensure the correct handling of a newline character.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.parse_paste('\nhello')
    ppp.parse_input.assert_called_once_with(Qt.Key_Enter, '\n', None)
    assert mock_timer.singleShot.call_count == 1


def test_PythonProcessPane_parse_paste_final_character():
    """
    As above, but ensure that if there a no more remaining characters to parse
    in the pasted text, then don't schedule any more recursive calls.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.parse_paste('\n')
    ppp.parse_input.assert_called_once_with(Qt.Key_Enter, '\n', None)
    assert mock_timer.singleShot.call_count == 0


def test_PythonProcessPane_keyPressEvent_a():
    """
    A character is typed and passed into parse_input in the expected manner.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_A)
    data.text = mock.MagicMock(return_value='a')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    ppp.parse_input.assert_called_once_with(Qt.Key_A, 'a', None)


def test_PythonProcessPane_on_process_halt():
    """
    Ensure the output from the halted process is dumped to the UI.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.readAll().data.return_value = b'halted'
    ppp.append = mock.MagicMock()
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    ppp.on_process_halt()
    ppp.process.readAll().data.assert_called_once_with()
    ppp.append.assert_called_once_with(b'halted')
    ppp.on_append_text.emit.assert_called_once_with(b'halted')
    ppp.set_start_of_current_line.assert_called_once_with()


def test_PythonProcessPane_on_process_halt_badly_formed_bytes():
    """
    If the bytes read from the child process's stdout starts with a badly
    formed unicode character (e.g. a fragment of a multi-byte character such as
    "𠜎"), then ensure the problem bytes at the start of the data are discarded
    until a valid result can be turned into a string.
    """
    data = "𠜎Hello, World!".encode('utf-8')  # Contains a multi-byte char.
    data = data[1:]  # Split the muti-byte character (cause UnicodeDecodeError)
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.readAll().data.return_value = data
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    ppp.on_process_halt()
    ppp.process.readAll().data.assert_called_once_with()
    ppp.on_append_text.emit.assert_called_once_with(b'Hello, World!')
    ppp.set_start_of_current_line.assert_called_once_with()


def test_PythonProcessPane_parse_input_a():
    """
    Ensure a regular printable character is inserted into the text area.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.insert = mock.MagicMock()
    key = Qt.Key_A
    text = 'a'
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.insert.assert_called_once_with(b'a')


def test_PythonProcessPane_parse_input_non_ascii():
    """
    Ensure a non-ascii printable character is inserted into the text area.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.insert = mock.MagicMock()
    key = Qt.Key_A
    text = 'Å'
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.insert.assert_called_once_with('Å'.encode('utf-8'))


def test_PythonProcessPane_parse_input_ctrl_c():
    """
    Control-C (SIGINT / KeyboardInterrupt) character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.processId.return_value = 123
    ppp.running = True
    key = Qt.Key_C
    text = ''
    modifiers = Qt.ControlModifier
    mock_kill = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.os.kill', mock_kill), \
            mock.patch('mu.interface.panes.QTimer', mock_timer), \
            mock.patch('mu.interface.panes.platform.system',
                       return_value='win32'):
        ppp.parse_input(key, text, modifiers)
    mock_kill.assert_called_once_with(123, signal.SIGINT)
    ppp.process.readAll.assert_called_once_with()
    mock_timer.singleShot.assert_called_once_with(1, ppp.on_process_halt)


def test_PythonProcessPane_parse_input_ctrl_d():
    """
    Control-D (Kill process) character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.running = True
    key = Qt.Key_D
    text = ''
    modifiers = Qt.ControlModifier
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.platform.system',
                    return_value='win32'), \
            mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.parse_input(key, text, modifiers)
        ppp.process.kill.assert_called_once_with()
    ppp.process.readAll.assert_called_once_with()
    mock_timer.singleShot.assert_called_once_with(1, ppp.on_process_halt)


def test_PythonProcessPane_parse_input_ctrl_c_after_process_finished():
    """
    Control-C (SIGINT / KeyboardInterrupt) character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.processId.return_value = 123
    ppp.running = False
    key = Qt.Key_C
    text = ''
    modifiers = Qt.ControlModifier
    mock_kill = mock.MagicMock()
    with mock.patch('mu.interface.panes.os.kill', mock_kill), \
            mock.patch('mu.interface.panes.platform.system',
                       return_value='win32'):
        ppp.parse_input(key, text, modifiers)
    assert mock_kill.call_count == 0


def test_PythonProcessPane_parse_input_ctrl_d_after_process_finished():
    """
    Control-D (Kill process) character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.running = False
    key = Qt.Key_D
    text = ''
    modifiers = Qt.ControlModifier
    with mock.patch('mu.interface.panes.platform.system',
                    return_value='win32'):
        ppp.parse_input(key, text, modifiers)
        assert ppp.process.kill.call_count == 0


def test_PythonProcessPane_parse_input_up_arrow():
    """
    Up Arrow causes the input line to be replaced with movement back in
    command history.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.history_back = mock.MagicMock()
    key = Qt.Key_Up
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    assert ppp.history_back.call_count == 1


def test_PythonProcessPane_parse_input_down_arrow():
    """
    Down Arrow causes the input line to be replaced with movement forward
    through command line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.history_forward = mock.MagicMock()
    key = Qt.Key_Down
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    assert ppp.history_forward.call_count == 1


def test_PythonProcessPane_parse_input_right_arrow():
    """
    Right Arrow causes the cursor to move to the right one place.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setTextCursor = mock.MagicMock()
    key = Qt.Key_Right
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    mock_cursor.movePosition.assert_called_once_with(QTextCursor.Right)
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_parse_input_left_arrow():
    """
    Left Arrow causes the cursor to move to the left one place if not at the
    start of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 1
    ppp.start_of_current_line = 0
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setTextCursor = mock.MagicMock()
    key = Qt.Key_Left
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    mock_cursor.movePosition.assert_called_once_with(QTextCursor.Left)
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_parse_input_left_arrow_at_start_of_line():
    """
    Left Arrow doesn't do anything if the current cursor position is at the
    start of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 1
    ppp.start_of_current_line = 1
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setTextCursor = mock.MagicMock()
    key = Qt.Key_Left
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    assert mock_cursor.movePosition.call_count == 0
    assert ppp.setTextCursor.call_count == 0


def test_PythonProcessPane_parse_input_home():
    """
    Home moves cursor to the start of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value='hello')
    mock_cursor = mock.MagicMock()
    ppp.start_of_current_line = 0
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setTextCursor = mock.MagicMock()
    key = Qt.Key_Home
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    # Move to the end of the line, then move left len of 'hello'.
    assert mock_cursor.movePosition.call_count == 6
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_parse_input_end():
    """
    End moves cursor to the end of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setTextCursor = mock.MagicMock()
    key = Qt.Key_End
    text = ''
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    mock_cursor.movePosition.assert_called_once_with(QTextCursor.End)
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_parse_input_paste():
    """
    Control-Shift-V (paste) character causes a paste to happen.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    key = Qt.Key_V
    text = ''
    modifiers = Qt.ControlModifier | Qt.ShiftModifier
    ppp.paste = mock.MagicMock()
    ppp.parse_input(key, text, modifiers)
    ppp.paste.assert_called_once_with()


def test_PythonProcessPane_parse_input_copy():
    """
    Control-Shift-C (copy) character causes copy to happen.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    key = Qt.Key_C
    text = ''
    modifiers = Qt.ControlModifier | Qt.ShiftModifier
    ppp.copy = mock.MagicMock()
    ppp.parse_input(key, text, modifiers)
    ppp.copy.assert_called_once_with()


def test_PythonProcessPane_parse_input_backspace():
    """
    Backspace call causes a backspace from the character at the cursor
    position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.backspace = mock.MagicMock()
    key = Qt.Key_Backspace
    text = '\b'
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.backspace.assert_called_once_with()


def test_PythonProcessPane_parse_input_delete():
    """
    Delete deletes the character to the right of the cursor position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.delete = mock.MagicMock()
    key = Qt.Key_Delete
    text = '\b'
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.delete.assert_called_once_with()


def test_PythonProcessPane_parse_input_newline():
    """
    Newline causes the input line to be written to the child process's stdin.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value='abc\n')
    ppp.start_of_current_line = 0
    ppp.textCursor = mock.MagicMock()
    ppp.textCursor().position.return_value = 666
    ppp.setTextCursor = mock.MagicMock()
    ppp.insert = mock.MagicMock()
    ppp.write_to_stdin = mock.MagicMock()
    key = Qt.Key_Enter
    text = '\r'
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.write_to_stdin.assert_called_once_with(b'abc\n')
    assert b'abc' in ppp.input_history
    assert ppp.history_position == 0
    # On newline, the start of the current line should be set correctly.
    assert ppp.start_of_current_line == 4   # len('abc\n')


def test_PythonProcessPane_parse_input_newline_ignore_empty_input_in_history():
    """
    Newline causes the input line to be written to the child process's stdin,
    but if the resulting line is either empty or only contains whitespace, do
    not add it to the input_history.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value='   \n')
    ppp.start_of_current_line = 0
    ppp.write_to_stdin = mock.MagicMock()
    key = Qt.Key_Enter
    text = '\r'
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.write_to_stdin.assert_called_once_with(b'   \n')
    assert len(ppp.input_history) == 0
    assert ppp.history_position == 0


def test_PythonProcessPane_parse_input_newline_with_cursor_midline():
    """
    Ensure that when the cursor is placed in the middle of a line and enter is
    pressed the whole line is sent to std_in.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.write_to_stdin = mock.MagicMock()
    ppp.parse_input(None, "abc", None)
    ppp.parse_input(Qt.Key_Left, None, None)
    ppp.parse_input(Qt.Key_Enter, '\r', None)
    ppp.write_to_stdin.assert_called_with(b'abc\n')


def test_PythonProcessPane_set_start_of_current_line():
    """
    Ensure the start of the current line is set to the current length of the
    text in the editor pane.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value="Hello𠜎")
    ppp.set_start_of_current_line()
    assert ppp.start_of_current_line == len("Hello𠜎")


def test_PythonProcessPane_history_back():
    """
    Ensure the current input line is replaced by the next item back in time
    from the current history position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ['a', 'b', 'c', ]
    ppp.history_position = 0
    ppp.replace_input_line = mock.MagicMock()
    ppp.history_back()
    ppp.replace_input_line.assert_called_once_with('c')
    assert ppp.history_position == -1


def test_PythonProcessPane_history_back_at_first_item():
    """
    Ensure the current input line is replaced by the next item back in time
    from the current history position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ['a', 'b', 'c', ]
    ppp.history_position = -3
    ppp.replace_input_line = mock.MagicMock()
    ppp.history_back()
    ppp.replace_input_line.assert_called_once_with('a')
    assert ppp.history_position == -3


def test_PythonProcessPane_history_forward():
    """
    Ensure the current input line is replaced by the next item forward in time
    from the current history position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ['a', 'b', 'c', ]
    ppp.history_position = -3
    ppp.replace_input_line = mock.MagicMock()
    ppp.history_forward()
    ppp.replace_input_line.assert_called_once_with('b')
    assert ppp.history_position == -2


def test_PythonProcessPane_history_forward_at_last_item():
    """
    Ensure the current input line is cleared if the history position was at
    the most recent item.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ['a', 'b', 'c', ]
    ppp.history_position = -1
    ppp.replace_input_line = mock.MagicMock()
    ppp.clear_input_line = mock.MagicMock()
    ppp.history_forward()
    ppp.clear_input_line.assert_called_once_with()
    assert ppp.replace_input_line.call_count == 0
    assert ppp.history_position == 0


def test_PythonProcessPane_try_read_from_stdout_not_started():
    """
    If the process pane is NOT already reading from STDOUT then ensure it
    starts to.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.read_from_stdout = mock.MagicMock()
    ppp.try_read_from_stdout()
    assert ppp.reading_stdout is True
    ppp.read_from_stdout.assert_called_once_with()


def test_PythonProcessPane_try_read_from_stdout_has_started():
    """
    If the process pane is already reading from STDOUT then ensure it
    doesn't keep trying.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.read_from_stdout = mock.MagicMock()
    ppp.reading_stdout = True
    ppp.try_read_from_stdout()
    assert ppp.reading_stdout is True
    assert ppp.read_from_stdout.call_count == 0


def test_PythonProcessPane_read_from_stdout():
    """
    Ensure incoming bytes from sub-process's stout are processed correctly.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.append = mock.MagicMock()
    ppp.process = mock.MagicMock()
    ppp.process.read.return_value = b'hello world'
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.read_from_stdout()
    assert ppp.append.call_count == 1
    ppp.process.read.assert_called_once_with(256)
    ppp.on_append_text.emit.assert_called_once_with(b'hello world')
    ppp.set_start_of_current_line.assert_called_once_with()
    mock_timer.singleShot.assert_called_once_with(2, ppp.read_from_stdout)


def test_PythonProcessPane_read_from_stdout_with_stdout_buffer():
    """
    Ensure incoming bytes from sub-process's stdout are processed correctly if
    there was a split between reads in a multi-byte character (such as "𠜎").

    The buffer is pre-pended to the current read, thus resulting in bytes that
    can be successfully represented in a UTF based string.
    """
    msg = "Hello 𠜎 world".encode('utf-8')
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.stdout_buffer = msg[:7]  # Start of msg but split in multi-byte char.
    ppp.process = mock.MagicMock()
    ppp.process.read.return_value = msg[7:]  # Remainder of msg.
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.read_from_stdout()
    ppp.process.read.assert_called_once_with(256)
    ppp.on_append_text.emit.assert_called_once_with(msg)
    ppp.set_start_of_current_line.assert_called_once_with()
    mock_timer.singleShot.assert_called_once_with(2, ppp.read_from_stdout)
    assert ppp.stdout_buffer == b''


def test_PythonProcessPane_read_from_stdout_with_unicode_error():
    """
    Ensure incoming bytes from sub-process's stdout are processed correctly if
    there was a split between reads in a multi-byte character (such as "𠜎").

    If the read bytes end with a split of a multi-byte character, ensure they
    are put into the self.stdout_buffer so they can be pre-pended to the next
    bytes read from the child process.
    """
    msg = "Hello 𠜎 world".encode('utf-8')
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.read.return_value = msg[:7]  # Split the multi-byte character.
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch('mu.interface.panes.QTimer', mock_timer):
        ppp.read_from_stdout()
    ppp.process.read.assert_called_once_with(256)
    assert ppp.on_append_text.emit.call_count == 0
    assert ppp.set_start_of_current_line.call_count == 0
    mock_timer.singleShot.assert_called_once_with(2, ppp.read_from_stdout)
    assert ppp.stdout_buffer == msg[:7]


def test_PythonProcessPane_read_from_stdout_no_data():
    """
    If no data is returned, ensure the reading_stdout flag is reset to False.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.reading_stdout = True
    ppp.process = mock.MagicMock()
    ppp.process.read.return_value = b''
    ppp.read_from_stdout()
    assert ppp.reading_stdout is False


def test_PythonProcessPane_write_to_stdin():
    """
    Ensure input from the user is written to the child process.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.write_to_stdin(b'hello')
    ppp.process.write.assert_called_once_with(b'hello')


def test_PythonProcessPane_append():
    """
    Ensure the referenced byte_stream is added to the textual content of the
    QTextEdit.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.append(b'hello')
    mock_cursor.insertText.assert_called_once_with('hello')
    assert mock_cursor.movePosition.call_count == 2


def test_PythonProcessPane_insert_within_input_line():
    """
    Ensure text is inserted at the end of the document if the current cursor
    position is not within the bounds of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 1
    ppp.start_of_current_line = 100
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.insert(b'hello')
    mock_cursor.movePosition.assert_called_once_with(QTextCursor.End)
    mock_cursor.insertText.assert_called_once_with('hello')


def test_PythonProcessPane_insert():
    """
    Ensure text is inserted at the current cursor position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 100
    ppp.start_of_current_line = 1
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.insert(b'hello')
    assert mock_cursor.movePosition.call_count == 0
    mock_cursor.insertText.assert_called_once_with('hello')


def test_PythonProcessPane_backspace():
    """
    Make sure that removing a character to the left of the current cursor
    position works as expected.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.start_of_current_line = 123
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 124
    mock_cursor.deletePreviousChar = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.backspace()
    mock_cursor.deletePreviousChar.assert_called_once_with()
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_backspace_at_start_of_input_line():
    """
    Make sure that removing a character will not work if the cursor is at the
    left-hand boundary of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.start_of_current_line = 123
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 123
    mock_cursor.deletePreviousChar = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.backspace()
    assert mock_cursor.deletePreviousChar.call_count == 0


def test_PythonProcessPane_delete():
    """
    Make sure that removing a character to the right of the current cursor
    position works as expected.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.start_of_current_line = 123
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 124
    mock_cursor.deletePreviousChar = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.delete()
    mock_cursor.deleteChar.assert_called_once_with()
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_delete_at_start_of_input_line():
    """
    Make sure that removing a character will not work if the cursor is at the
    left-hand boundary of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.start_of_current_line = 123
    mock_cursor = mock.MagicMock()
    mock_cursor.position.return_value = 122
    mock_cursor.deletePreviousChar = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.delete()
    assert mock_cursor.deleteChar.call_count == 0


def test_PythonProcessPane_clear_input_line():
    """
    Ensure the input line is cleared back to the start of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.start_of_current_line = 0
    ppp.toPlainText = mock.MagicMock(return_value='hello')
    mock_cursor = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.clear_input_line()
    assert mock_cursor.deletePreviousChar.call_count == 5
    mock_cursor.movePosition.assert_called_once_with(QTextCursor.End)
    ppp.setTextCursor.assert_called_once_with(mock_cursor)


def test_PythonProcessPane_replace_input_line():
    """
    Ensure that the input line is cleared and then the replacement text is
    appended to the text area.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.clear_input_line = mock.MagicMock()
    ppp.append = mock.MagicMock()
    ppp.replace_input_line('hello')
    ppp.clear_input_line.assert_called_once_with()
    ppp.append.assert_called_once_with('hello')


def test_PythonProcessPane_set_font_size():
    """
    Ensure the font size is set to the expected point size.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_font = mock.MagicMock()
    ppp.font = mock.MagicMock(return_value=mock_font)
    ppp.setFont = mock.MagicMock()
    ppp.set_font_size(123)
    mock_font.setPointSize.assert_called_once_with(123)
    ppp.setFont.assert_called_once_with(mock_font)


def test_PythonProcessPane_set_zoom():
    """
    Ensure the expected point size is set from the given "t-shirt" size.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.set_font_size = mock.MagicMock()
    ppp.set_zoom('xl')
    expected = mu.interface.panes.PANE_ZOOM_SIZES['xl']
    ppp.set_font_size.assert_called_once_with(expected)


def test_PythonProcessPane_set_theme():
    """
    Setting the theme shouldn't do anything
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.set_theme('test')


def test_DebugInspectorItem():
    item = mu.interface.panes.DebugInspectorItem('test')
    assert item.text() == 'test'
    assert not item.isEditable()


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


def test_DebugInspector_set_zoom():
    """
    Ensure the expected point size is set from the given "t-shirt" size.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_font_size = mock.MagicMock()
    di.set_zoom('xl')
    expected = mu.interface.panes.PANE_ZOOM_SIZES['xl']
    di.set_font_size.assert_called_once_with(expected)


def test_DebugInspector_set_theme():
    """
    Setting the theme shouldn't do anything
    """
    di = mu.interface.panes.DebugInspector()
    di.set_theme('test')


def test_PlotterPane_init():
    """
    Ensure the plotter pane is created in the expected manner.
    """
    pp = mu.interface.panes.PlotterPane()
    assert pp.input_buffer == []
    assert pp.raw_data == []
    assert pp.max_x == 100
    assert pp.max_y == 1000
    assert len(pp.data) == 1
    assert isinstance(pp.data[0], deque)
    assert len(pp.series) == 1
    assert isinstance(pp.series[0], QLineSeries)
    assert isinstance(pp.chart, QChart)
    assert isinstance(pp.axis_x, QValueAxis)
    assert isinstance(pp.axis_y, QValueAxis)


def test_PlotterPane_process_bytes():
    """
    If a byte representation of a Python tuple containing numeric values,
    starting at the beginning of a new line and terminating with a new line is
    received, then the add_data method is called with the resulting Python
    tuple.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.add_data = mock.MagicMock()
    pp.process_bytes(b'(1, 2.3, 4)\r\n')
    pp.add_data.assert_called_once_with((1, 2.3, 4))


def test_PlotterPane_process_bytes_guards_against_data_flood():
    """
    If the process_bytes method gets data of more than 1024 bytes then trigger
    a data_flood signal and ensure the plotter no longer processes incoming
    bytes.

    (The assumption is that Mu will clean up once the data_flood signal is
    emitted.)
    """
    pp = mu.interface.panes.PlotterPane()
    pp.data_flood = mock.MagicMock()
    pp.add_data = mock.MagicMock()
    data_flood = b'X' * 1025
    pp.process_bytes(data_flood)
    assert pp.flooded is True
    pp.data_flood.emit.assert_called_once_with()
    assert pp.add_data.call_count == 0
    pp.process_bytes(data_flood)
    assert pp.add_data.call_count == 0


def test_PlotterPane_process_bytes_tuple_not_numeric():
    """
    If a byte representation of a tuple is received but it doesn't contain
    numeric values, then the add_data method MUST NOT be called.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.add_data = mock.MagicMock()
    pp.process_bytes(b'("a", "b", "c")\r\n')
    assert pp.add_data.call_count == 0


def test_PlotterPane_process_bytes_overrun_input_buffer():
    """
    If the incoming bytes are not complete, ensure the input_buffer caches them
    until the newline is detected.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.add_data = mock.MagicMock()
    pp.process_bytes(b'(1, 2.3, 4)\r\n')
    pp.add_data.assert_called_once_with((1, 2.3, 4))
    pp.add_data.reset_mock()
    pp.process_bytes(b'(1, 2.')
    assert pp.add_data.call_count == 0
    pp.process_bytes(b'3, 4)\r\n')
    pp.add_data.assert_called_once_with((1, 2.3, 4))
    pp.add_data.reset_mock()
    pp.process_bytes(b'(1, 2.3, 4)\r\n')
    pp.add_data.assert_called_once_with((1, 2.3, 4))


def test_PlotterPane_add_data():
    """
    Given a tuple with a single value, ensure it is logged and correctly added
    to the chart.
    """
    pp = mu.interface.panes.PlotterPane()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series, ]
    pp.add_data((1, ))
    assert (1, ) in pp.raw_data
    mock_line_series.clear.assert_called_once_with()
    for i in range(99):
        mock_line_series.append.call_args_list[i][0] == (i, 0)
    mock_line_series.append.call_args_list[99][0] == (99, 1)


def test_PlotterPane_add_data_adjust_values_up():
    """
    If more values than have been encountered before are added to the incoming
    data then increase the number of QLineSeries instances.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.series = [mock.MagicMock(), ]
    pp.chart = mock.MagicMock()
    with mock.patch('mu.interface.panes.QLineSeries'):
        pp.add_data((1, 2, 3, 4))
    assert len(pp.series) == 4
    assert pp.chart.addSeries.call_count == 3
    assert pp.chart.setAxisX.call_count == 3
    assert pp.chart.setAxisY.call_count == 3
    assert len(pp.data) == 4


def test_PlotterPane_add_data_adjust_values_down():
    """
    If less values are encountered, before they are added to the incoming
    data then decrease the number of QLineSeries instances.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.series = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]
    pp.data.append(mock.MagicMock())
    pp.data.append(mock.MagicMock())
    pp.chart = mock.MagicMock()
    with mock.patch('mu.interface.panes.QLineSeries'):
        pp.add_data((1, ))
    assert len(pp.series) == 1
    assert len(pp.data) == 1
    assert pp.chart.removeSeries.call_count == 2


def test_PlotterPane_add_data_re_scale_up():
    """
    If the y axis contains data greater than the current range, then ensure
    the range is doubled.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series, ]
    pp.add_data((1001, ))
    assert pp.max_y == 2000
    pp.axis_y.setRange.assert_called_once_with(-2000, 2000)


def test_PlotterPane_add_data_re_scale_down():
    """
    If the y axis contains data less than half of the current range, then
    ensure the range is halved.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.max_y = 4000
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series, ]
    pp.add_data((1999, ))
    assert pp.max_y == 2000
    pp.axis_y.setRange.assert_called_once_with(-2000, 2000)


def test_PlotterPane_set_label_format_to_float_when_range_small():
    """
    If the max_y is 5 or less, make sure the label format is set to being a
    float with two decimal places.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.max_y = 10
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series, ]
    pp.add_data((1, ))
    assert pp.max_y == 1
    pp.axis_y.setRange.assert_called_once_with(-1, 1)
    pp.axis_y.setLabelFormat.assert_called_once_with("%2.2f")


def test_PlotterPane_set_label_format_to_int_when_range_large():
    """
    If the max_y is 5 or less, make sure the label format is set to being a
    float with two decimal places.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.max_y = 5
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series, ]
    pp.add_data((10, ))
    assert pp.max_y == 10
    pp.axis_y.setRange.assert_called_once_with(-10, 10)
    pp.axis_y.setLabelFormat.assert_called_once_with("%d")


def test_PlotterPane_set_theme():
    """
    Ensure the themes for the chart relate correctly to the theme names used
    by Mu.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.chart = mock.MagicMock()
    pp.set_theme('day')
    pp.chart.setTheme.assert_called_once_with(QChart.ChartThemeLight)
    pp.chart.setTheme.reset_mock()
    pp.set_theme('night')
    pp.chart.setTheme.assert_called_once_with(QChart.ChartThemeDark)
    pp.chart.setTheme.reset_mock()
    pp.set_theme('contrast')
    pp.chart.setTheme.assert_called_once_with(QChart.ChartThemeHighContrast)


def test_MuFileTree_show_confirm_overwrite_dialog():
    """
    Ensure the user is notified of an existing file.
    """
    mfl = mu.interface.panes.MuFileTree()
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
    msg = _('File already exists; overwrite it?')
    mock_qmb.setText.assert_called_once_with(msg)
    mock_qmb.setWindowTitle.assert_called_once_with(_('File already exists'))
    mock_qmb.setIcon.assert_called_once_with(QMessageBox.Information)


def test_MicroPythonDeviceFileTree_init():
    """
    Check the widget references the user's home and allows drag and drop.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('home/path')
    assert mfs.home == 'home/path'
    assert mfs.dragDropMode() == mfs.DragDrop


def test_MicroPythonDeviceFileTree_dropEvent_no_target(drop_event):
    # create object in MicroPythonDeviceFileTree
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('pc_home_path')
    mfs.itemAt = mock.MagicMock(return_value=None)
    mfs.show_confirm_overwrite_dialog = mock.MagicMock(return_value=False)
    mfs.findItems = mock.MagicMock(return_value=False)
    # create result check
    msg_emit = mock.MagicMock()
    mfs.set_message = mock.MagicMock(return_value=msg_emit)
    put_emit = mock.MagicMock()
    mfs.put = mock.MagicMock(return_value=put_emit)
    # go
    mfs.dropEvent(drop_event)
    # check result
    msg = _("Copying 'pc_home_path\\pc_foo.py' to device.")
    assert mfs.findItems.call_count == 1
    assert mfs.show_confirm_overwrite_dialog.call_count == 0
    mfs.set_message.emit.assert_called_once_with(msg)
    mfs.put.emit.assert_called_once_with('pc_home_path\\pc_foo.py', '')


def test_MicroPythonDeviceFileTree_dropEvent_target_has_child(drop_event):
    # create object in MicroPythonDeviceFileTree
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('pc_home_path')
    target_item = mock.MagicMock()
    target_item.childCount.return_value = 1
    target_item.text = mock.MagicMock(return_value='bar')
    child_item = mock.MagicMock()
    child_item.text.return_value = 'dev_foo.py'
    target_item.child = mock.MagicMock(return_value=child_item)
    target_item.parent = mock.MagicMock(return_value=None)
    mfs.itemAt = mock.MagicMock(return_value=target_item)
    mfs.show_confirm_overwrite_dialog = mock.MagicMock(return_value=False)
    mfs.findItems = mock.MagicMock(return_value=False)
    # create result check
    msg_emit = mock.MagicMock()
    mfs.set_message = mock.MagicMock(return_value=msg_emit)
    put_emit = mock.MagicMock()
    mfs.put = mock.MagicMock(return_value=put_emit)
    # go
    mfs.dropEvent(drop_event)
    # check result
    msg = _("Copying 'pc_home_path\\pc_foo.py' to device.")
    assert mfs.findItems.call_count == 0
    assert mfs.show_confirm_overwrite_dialog.call_count == 0
    mfs.set_message.emit.assert_called_once_with(msg)
    mfs.put.emit.assert_called_once_with('pc_home_path\\pc_foo.py', 'bar')


def test_MicroPythonDeviceFileTree_dropEvent_target_has_paraent(drop_event):
    # create object in MicroPythonDeviceFileTree
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('pc_home_path')
    target_item = mock.MagicMock()
    target_item.childCount.return_value = 0
    target_item.text.return_value = 'dev_foo.py'
    p_item = mock.MagicMock()
    p_item.text = mock.MagicMock(return_value='bar')
    p_item.parent.return_value = None
    target_item.parent = mock.MagicMock(return_value=p_item)
    mfs.itemAt = mock.MagicMock(return_value=target_item)
    mfs.show_confirm_overwrite_dialog = mock.MagicMock(return_value=False)
    mfs.findItems = mock.MagicMock(return_value=False)
    # create result check
    msg_emit = mock.MagicMock()
    mfs.set_message = mock.MagicMock(return_value=msg_emit)
    put_emit = mock.MagicMock()
    mfs.put = mock.MagicMock(return_value=put_emit)
    # go
    mfs.dropEvent(drop_event)
    # check result
    msg = _("Copying 'pc_home_path\\pc_foo.py' to device.")
    assert mfs.findItems.call_count == 0
    assert mfs.show_confirm_overwrite_dialog.call_count == 0
    mfs.set_message.emit.assert_called_once_with(msg)
    mfs.put.emit.assert_called_once_with('pc_home_path\\pc_foo.py', 'bar')


def test_MicroPythonDeviceFileTree_dropEvent_rewrite(drop_event):
    # create object in MicroPythonDeviceFileTree
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('pc_home_path')
    target_item = mock.MagicMock()
    target_item.childCount.return_value = 1
    target_item.text = mock.MagicMock(return_value='bar')
    child_item = mock.MagicMock()
    child_item.text.return_value = 'pc_foo.py'
    target_item.child = mock.MagicMock(return_value=child_item)
    target_item.parent = mock.MagicMock(return_value=None)
    mfs.itemAt = mock.MagicMock(return_value=target_item)
    mfs.show_confirm_overwrite_dialog = mock.MagicMock(return_value=True)
    mfs.findItems = mock.MagicMock(return_value=False)
    # create result check
    msg_emit = mock.MagicMock()
    mfs.set_message = mock.MagicMock(return_value=msg_emit)
    put_emit = mock.MagicMock()
    mfs.put = mock.MagicMock(return_value=put_emit)
    # go
    mfs.dropEvent(drop_event)
    # check result
    assert mfs.findItems.call_count == 0
    assert mfs.show_confirm_overwrite_dialog.call_count == 1
    msg = _("Copying 'pc_home_path\\pc_foo.py' to device.")
    mfs.set_message.emit.assert_called_once_with(msg)
    mfs.put.emit.assert_called_once_with('pc_home_path\\pc_foo.py', 'bar')


def test_MicroPythonDeviceFileTree_dropEvent_cancel(drop_event):
    # create object in MicroPythonDeviceFileTree
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('pc_home_path')
    mfs.itemAt = mock.MagicMock(return_value=None)
    mfs.show_confirm_overwrite_dialog = mock.MagicMock(return_value=False)
    mfs.findItems = mock.MagicMock(return_value=True)
    # create result check
    msg_emit = mock.MagicMock()
    mfs.set_message = mock.MagicMock(return_value=msg_emit)
    put_emit = mock.MagicMock()
    mfs.put = mock.MagicMock(return_value=put_emit)
    # go
    mfs.dropEvent(drop_event)
    # check result
    assert mfs.findItems.call_count == 1
    assert mfs.show_confirm_overwrite_dialog.call_count == 1
    mfs.set_message.emit.call_count = 0
    mfs.put.emit.call_count = 0


def test_MicroPythonDeviceFileTree_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    mfs.findItems = mock.MagicMock()
    mfs.dropEvent(mock_event)
    assert mfs.findItems.call_count == 0


def test_MicroPythonDeviceFileTree_on_put():
    """
    A message and list_files signal should be emitted.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    mfs.set_message = mock.MagicMock()
    mfs.list_files = mock.MagicMock()
    mfs.on_put('my_file.py')
    mfs.list_files.emit.assert_called_once_with()


def test_MicroPythonDeviceFileTree_contextMenuEvent():
    """
    Ensure that the menu displayed when a file on the micro:bit is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mock_current.childCount.return_value = 0
    mock_current.parent.return_value = None
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.delete = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    with mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    mfs.disable.emit.assert_called_once_with()
    assert mfs.set_message.emit.call_count == 1
    mfs.delete.emit.assert_called_once_with('/foo.py')


def test_MicroPythonDeviceFileTree_contextMenuEvent_has_child():
    """
    Ensure that the menu displayed when a file on the micro:bit is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo'
    mock_current.childCount.return_value = 1
    mock_current.parent.return_value = None
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    # create result check
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.delete = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    # go
    with mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    # result check
    assert mfs.disable.emit.call_count == 0
    assert mfs.delete.emit.call_count == 0
    mfs.set_message.emit.assert_called_once_with(_("Can't delete folder."))


def test_MicroPythonDeviceFileTree_contextMenuEvent_has_parent():
    """
    Ensure that the menu displayed when a file on the micro:bit is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    mock_current = mock.MagicMock()
    mock_current.text = mock.MagicMock(return_value='foo.py')
    mock_current.childCount.return_value = 0
    p_item = mock.MagicMock()
    p_item.text = mock.MagicMock(return_value='bar')
    p_item.parent.return_value = None
    mock_current.parent = mock.MagicMock(return_value=p_item)
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    # create result check
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.delete = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    # go
    with mock.patch('mu.interface.panes.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    # result check
    mfs.disable.emit.assert_called_once_with()
    assert mfs.set_message.emit.call_count == 1
    mfs.delete.emit.assert_called_once_with('bar/foo.py')


def test_MicroPythonDeviceFileTree_on_delete():
    """
    On delete should emit a message and list_files signal.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    mfs.set_message = mock.MagicMock()
    mfs.list_files = mock.MagicMock()
    mfs.on_delete('my_file.py')
    mfs.list_files.emit.assert_called_once_with()


def test_StuduinoBitFileSystemPane_init():
    """
    Check things are set up as expected.
    """
    home = 'homepath'
    test_studuinobit_fs = mu.interface.panes.MicroPythonDeviceFileTree(home)
    test_studuinobit_fs.disable = mock.MagicMock()
    test_studuinobit_fs.set_message = mock.MagicMock()
    test_local_fs = mu.interface.panes.StuduinoBitLocalFileList(home)
    test_local_fs.disable = mock.MagicMock()
    test_local_fs.set_message = mock.MagicMock()
    mock_mfl = mock.MagicMock(return_value=test_studuinobit_fs)
    mock_lfl = mock.MagicMock(return_value=test_local_fs)
    with mock.patch('mu.interface.panes.MicroPythonDeviceFileTree',
                    mock_mfl), \
            mock.patch('mu.interface.panes.StuduinoBitLocalFileList',
                       mock_lfl):
        fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
        assert isinstance(fsp.studuinobit_label, QLabel)
        assert isinstance(fsp.local_label, QLabel)
        assert fsp.studuinobit_fs == test_studuinobit_fs
        assert fsp.local_fs == test_local_fs
        test_studuinobit_fs.disable.connect.\
            assert_called_once_with(fsp.disable)
        test_studuinobit_fs.set_message.connect.\
            assert_called_once_with(fsp.show_message)
        test_local_fs.disable.connect.assert_called_once_with(fsp.disable)
        test_local_fs.set_message.connect.\
            assert_called_once_with(fsp.show_message)


def test_StuduinoBitFileSystemPane_disable():
    """
    The child list widgets are disabled correctly.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.studuinobit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.disable()
    fsp.studuinobit_fs.setDisabled.assert_called_once_with(True)
    fsp.local_fs.setDisabled.assert_called_once_with(True)
    fsp.studuinobit_fs.setAcceptDrops.assert_called_once_with(False)
    fsp.local_fs.setAcceptDrops.assert_called_once_with(False)


def test_StuduinoBitFileSystemPane_enable():
    """
    The child list widgets are enabled correctly.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.studuinobit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.enable()
    fsp.studuinobit_fs.setDisabled.assert_called_once_with(False)
    fsp.local_fs.setDisabled.assert_called_once_with(False)
    fsp.studuinobit_fs.setAcceptDrops.assert_called_once_with(True)
    fsp.local_fs.setAcceptDrops.assert_called_once_with(True)


def test_StuduinoBitFileSystemPane_set_theme():
    """
    Setting theme doesn't error
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.set_theme('test')


def test_StuduinoBitFileSystemPane_show_message():
    """
    Ensure the expected message signal is emitted.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.set_message = mock.MagicMock()
    fsp.show_message('Hello')
    fsp.set_message.emit.assert_called_once_with('Hello')


def test_StuduinoBitFileSystemPane_show_warning():
    """
    Ensure the expected warning signal is emitted.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.set_warning = mock.MagicMock()
    fsp.show_warning('Hello')
    fsp.set_warning.emit.assert_called_once_with('Hello')


def test_StuduinoBitFileSystemPane_on_tree():
    """
    When lists of files have been obtained from the micro:bit and local
    filesystem, make sure they're properly processed by the on_tree event
    handler.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    studuinobit_files = ['./boot.py', './lib/pyatcrobo2/body.py',
                         './lib/pyatcrobo2/const.py']
    fsp.studuinobit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.enable = mock.MagicMock()
    local_files = ['qux.py', 'baz.py', ]
    mock_listdir = mock.MagicMock(return_value=local_files)
    mock_isfile = mock.MagicMock(return_value=True)
    with mock.patch('mu.interface.panes.os.listdir', mock_listdir),\
            mock.patch('mu.interface.panes.os.path.isfile', mock_isfile):
        fsp.on_tree(studuinobit_files)
    fsp.studuinobit_fs.clear.assert_called_once_with()
    fsp.local_fs.clear.assert_called_once_with()
    assert fsp.studuinobit_fs.addTopLevelItems.call_count == 1
    assert fsp.local_fs.addItem.call_count == 2
    fsp.enable.assert_called_once_with()


def test_StuduinoBitFileSystemPane_on_tree_fail():
    """
    A warning is emitted and the widget disabled if listing files fails.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.disable = mock.MagicMock()
    fsp.on_tree_fail()
    assert fsp.show_warning.call_count == 1
    fsp.disable.assert_called_once_with()


def test_StuduinoBitFileSystemPane_on_put_fail():
    """
    A warning is emitted if putting files on the micro:bit fails.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.on_put_fail('foo.py')
    assert fsp.show_warning.call_count == 1


def test_StuduinoBitFileSystemPane_on_delete_fail():
    """
    A warning is emitted if deleting files on the micro:bit fails.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.on_delete_fail('foo.py')
    assert fsp.show_warning.call_count == 1


def test_StuduinoBitFileSystemPane_on_get_fail():
    """
    A warning is emitted if getting files from the micro:bit fails.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.show_warning = mock.MagicMock()
    fsp.on_get_fail('foo.py')
    assert fsp.show_warning.call_count == 1


def test_StuduinoBitFileSystemPane_set_font_size():
    """
    Ensure the right size is set as the point size and the text based UI child
    widgets are updated.
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.font = mock.MagicMock()
    fsp.studuinobit_label = mock.MagicMock()
    fsp.local_label = mock.MagicMock()
    fsp.studuinobit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.set_font_size(22)
    fsp.font.setPointSize.assert_called_once_with(22)
    fsp.studuinobit_label.setFont.assert_called_once_with(fsp.font)
    fsp.local_label.setFont.assert_called_once_with(fsp.font)
    fsp.studuinobit_fs.setFont.assert_called_once_with(fsp.font)
    fsp.local_fs.setFont.assert_called_once_with(fsp.font)


def test_StuduinoBitFileSystemPane_open_file():
    """
    FileSystemPane should propogate the open_file signal
    """
    fsp = mu.interface.panes.StuduinoBitFileSystemPane('homepath')
    fsp.open_file = mock.MagicMock()
    mock_open_emit = mock.MagicMock()
    fsp.open_file.emit = mock_open_emit
    fsp.local_fs.open_file.emit('test')
    mock_open_emit.assert_called_once_with('test')


def test_StuduinoBitLocalFileList_dropEvent_Folder():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    source.currentItem = mock.MagicMock()
    parent = QTreeWidgetItem(None, ['foo'])
    entry = QTreeWidgetItem(None, ['bar'])
    child = QTreeWidgetItem(None, ['baz.py'])
    entry.addChild(child)
    parent.addChild(entry)
    source.currentItem.return_value = entry
    mock_event.source.return_value = source

    lfs = mu.interface.panes.StuduinoBitLocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.set_message = mock.MagicMock()
    lfs.get = mock.MagicMock()
    # Test
    lfs.dropEvent(mock_event)
    assert lfs.set_message.emit.call_count == 1


def test_StuduinoBitLocalFileList_dropEvent_File_Have_Parent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.MicroPythonDeviceFileTree('homepath')
    source.currentItem = mock.MagicMock()
    parent = QTreeWidgetItem(None, ['foo'])
    entry = QTreeWidgetItem(None, ['bar.py'])
    parent.addChild(entry)
    source.currentItem.return_value = entry
    mock_event.source.return_value = source

    lfs = mu.interface.panes.StuduinoBitLocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.set_message = mock.MagicMock()
    lfs.get = mock.MagicMock()
    # Test
    lfs.dropEvent(mock_event)
    fn = os.path.join('homepath', 'bar.py')
    lfs.disable.emit.assert_called_once_with()
    assert lfs.set_message.emit.call_count == 1
    lfs.get.emit.assert_called_once_with('foo/bar.py', fn)


def test_StuduinoBitLocalFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    mfs = mu.interface.panes.MicroPythonDeviceFileList('homepath')
    mfs.findItems = mock.MagicMock()
    mfs.dropEvent(mock_event)
    assert mfs.findItems.call_count == 0


def test_StuduinoBitREPLPane_process_bytes():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. Backspace is enacted, carriage-return is ignored, newline moves
    the cursor position to the end of the line before enacted and all others
    are simply inserted.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(side_effect=[True, False, True,
                                                       True])
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
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


def test_StuduinoBitREPLPane_process_bytes_VT100():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure VT100 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
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


def test_StuduinoBitREPLPane_process_bytes_UTF8():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure UTF8 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([
        0xe0, 0xa0, 0x80,  # min(U+0800)
        0xef, 0xbf, 0xbf,  # max(U+FFFF)
    ])
    rp.process_bytes(bs)
    rp.textCursor.assert_called_once_with()
    assert mock_tc.movePosition.call_count == 1
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
    assert rp.setTextCursor.call_count == 2
    assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
    assert rp.setTextCursor.call_args_list[1][0][0] == mock_tc
    rp.ensureCursorVisible.assert_called_once_with()


def test_StuduinoBitREPLPane_process_bytes_UTF8_Error():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure UTF8 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([
        0xef, 0xbf, 0xc0,  # over max(U+FFFF)
    ])
    rp.process_bytes(bs)
    rp.textCursor.assert_called_once_with()
    assert mock_tc.movePosition.call_count == 1
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
    assert rp.setTextCursor.call_count == 1
    assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
    rp.ensureCursorVisible.assert_called_once_with()


def test_StuduinoBitREPLPane_process_bytes_Div_ESC_CSI():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure UTF8 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([
        27,  # <Esc>[1A
    ])
    rp.process_bytes(bs)

    bs = bytes([
        91,  # <Esc>[1A
    ])
    rp.process_bytes(bs)

    bs = bytes([
        ord('1'),  # <Esc>[1A
    ])
    rp.process_bytes(bs)

    bs = bytes([
        ord('A'),  # <Esc>[1A
    ])
    rp.process_bytes(bs)

    # rp.textCursor.assert_called_once_with()
    assert mock_tc.movePosition.call_count == 5
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[3][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[4][0][0] == QTextCursor.Up
    assert rp.setTextCursor.call_count == 1
    assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
    rp.ensureCursorVisible.assert_called_once_with()


def test_StuduinoBitREPLPane_process_bytes_SGL():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure UTF8 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([
        27,  # ESC
    ])
    rp.process_bytes(bs)

    bs = bytes([
        91,  # CSI
    ])
    rp.process_bytes(bs)

    bs = bytes([
        ord('0'), ord(';'), 32, ord('m')    # SGR
    ])
    rp.process_bytes(bs)

    # rp.textCursor.assert_called_once_with()
    assert mock_tc.movePosition.call_count == 3
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Down
    assert rp.setTextCursor.call_count == 0
    # assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
    rp.ensureCursorVisible.assert_called_once_with()


def test_StuduinoBitREPLPane_process_bytes_Inv_ESC_CSI():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure UTF8 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.StuduinoBitREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([
        27,  # ESC
    ])
    rp.process_bytes(bs)

    bs = bytes([
        91,  # CSI
    ])
    rp.process_bytes(bs)

    bs = bytes([
        ord('1'),  # Ps
    ])
    rp.process_bytes(bs)

    bs = bytes([
        ord('E'),  # E
    ])
    rp.process_bytes(bs)

    # rp.textCursor.assert_called_once_with()
    assert mock_tc.movePosition.call_count == 4
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[3][0][0] == QTextCursor.Down
    assert rp.setTextCursor.call_count == 0
    # assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
    # rp.ensureCursorVisible.assert_called_once_with()
