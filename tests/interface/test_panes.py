# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QMessageBox, QLabel, QMenu
from PyQt5.QtCore import Qt, QEvent, QPointF, QUrl
from PyQt5.QtGui import QTextCursor, QMouseEvent
from collections import deque
from unittest import mock

import sys
import os
import signal
import pytest

import mu
import mu.interface.panes
from mu import i18n
from mu.interface.panes import CHARTS
from mu.interface.themes import DAY_STYLE, NIGHT_STYLE, CONTRAST_STYLE


def test_PANE_ZOOM_SIZES():
    """
    Ensure the expected entries define font sizes in PANE_ZOOM_SIZES.
    """
    expected_sizes = ("xs", "s", "m", "l", "xl", "xxl", "xxxl")
    for size in expected_sizes:
        assert size in mu.interface.panes.PANE_ZOOM_SIZES
    assert len(expected_sizes) == len(mu.interface.panes.PANE_ZOOM_SIZES)


def test_MicroPythonREPLPane_paste_fragment():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_repl_connection = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste me!"
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertFromMimeData(mock_clipboard)
    mock_repl_connection.write.assert_called_once_with(b"paste me!")


def test_MicroPythonREPLPane_paste_multiline():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_repl_connection = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste\nme!"
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertFromMimeData(mock_clipboard)
    assert mock_repl_connection.write.call_count == 3
    assert mock_repl_connection.write.call_args_list[0][0][0] == b"\x05"
    assert mock_repl_connection.write.call_args_list[1][0][0] == bytes(
        "paste\rme!", "utf8"
    )
    assert mock_repl_connection.write.call_args_list[2][0][0] == b"\x04"


def test_MicroPythonREPLPane_paste_handle_unix_newlines():
    """
    Pasting into the REPL should handle '\n' properly.

    '\n' -> '\r'
    """
    mock_repl_connection = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste\nme!"
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertFromMimeData(mock_clipboard)
    assert mock_repl_connection.write.call_count == 3
    assert mock_repl_connection.write.call_args_list[0][0][0] == b"\x05"
    assert mock_repl_connection.write.call_args_list[1][0][0] == bytes(
        "paste\rme!", "utf8"
    )
    assert mock_repl_connection.write.call_args_list[2][0][0] == b"\x04"


def test_MicroPythonREPLPane_paste_handle_windows_newlines():
    """
    Pasting into the REPL should handle '\r\n' properly.

    '\r\n' -> '\r'
    """
    mock_repl_connection = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste\r\nme!"
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertFromMimeData(mock_clipboard)
    assert mock_repl_connection.write.call_count == 3
    assert mock_repl_connection.write.call_args_list[0][0][0] == b"\x05"
    assert mock_repl_connection.write.call_args_list[1][0][0] == bytes(
        "paste\rme!", "utf8"
    )
    assert mock_repl_connection.write.call_args_list[2][0][0] == b"\x04"


def test_MicroPythonREPLPane_paste_only_works_if_something_to_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_repl_connection = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = ""
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertFromMimeData(mock_clipboard)
    assert mock_repl_connection.write.call_count == 0


def test_MicroPythonREPLPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_repl_connection = mock.MagicMock()
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = "WinNT"
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch("mu.interface.panes.platform", mock_platform), mock.patch(
        "mu.interface.panes.QMenu", mock_qmenu_class
    ), mock.patch("mu.interface.panes.QCursor"):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == "Copy"
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == "Ctrl+Shift+C"
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == "Paste"
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == "Ctrl+Shift+V"
    assert mock_qmenu.exec_.call_count == 1


def test_MicroPythonREPLPane_context_menu_darwin():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_repl_connection = mock.MagicMock()
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = "Darwin"
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch("mu.interface.panes.platform", mock_platform), mock.patch(
        "mu.interface.panes.QMenu", mock_qmenu_class
    ), mock.patch("mu.interface.panes.QCursor"):
        rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == "Copy"
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == "Ctrl+C"
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == "Paste"
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == "Ctrl+V"
    assert mock_qmenu.exec_.call_count == 1


def test_MicroPythonREPLPane_keyPressEvent():
    """
    Ensure key presses in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_A)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(bytes("a", "utf-8"))


def test_MicroPythonREPLPane_keyPressEvent_backspace():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_BACKSPACE
    )


def test_MicroPythonREPLPane_keyPressEvent_return():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Return)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(mu.interface.panes.VT100_RETURN)


def test_MicroPythonREPLPane_keyPressEvent_delete():
    """
    Ensure delete in the REPL is handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Delete)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_DELETE
    )


def test_MicroPythonREPLPane_keyPressEvent_up():
    """
    Ensure up arrows in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Up)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_UP
    )


def test_MicroPythonREPLPane_keyPressEvent_down():
    """
    Ensure down arrows in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Down)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_DOWN
    )


def test_MicroPythonREPLPane_keyPressEvent_right():
    """
    Ensure right arrows in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Right)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_RIGHT
    )


def test_MicroPythonREPLPane_keyPressEvent_left():
    """
    Ensure left arrows in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Left)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_LEFT
    )


@mock.patch("PyQt5.QtWidgets.QTextEdit.keyPressEvent")
def test_MicroPythonREPLPane_keyPressEvent_shift_right(
    mock_super_keyPressEvent,
):
    """
    Ensure right arrows with shift in the REPL are passed through to
    the super class, to perform a selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Right)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.ShiftModifier)
    rp.keyPressEvent(data)
    mock_super_keyPressEvent.assert_called_once_with(data)


@mock.patch("PyQt5.QtWidgets.QTextEdit.keyPressEvent")
def test_MicroPythonREPLPane_keyPressEvent_shift_left(
    mock_super_keyPressEvent,
):
    """
    Ensure left arrows with shift in the REPL are passed through to
    the super class, to perform a selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Left)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.ShiftModifier)
    rp.keyPressEvent(data)
    mock_super_keyPressEvent.assert_called_once_with(data)


@mock.patch("PyQt5.QtGui.QTextCursor.hasSelection", return_value=True)
@mock.patch("PyQt5.QtGui.QTextCursor.selectionEnd", return_value=30)
def test_MicroPythonREPLPane_keyPressEvent_right_with_selection(a, b):
    """
    Ensure right arrows in the REPL when a selection is made, moves the cursor
    to the end of the selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Right)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.move_cursor_to = mock.MagicMock()
    rp.keyPressEvent(data)
    rp.move_cursor_to.assert_called_once_with(30)


@mock.patch("PyQt5.QtGui.QTextCursor.hasSelection", return_value=True)
@mock.patch("PyQt5.QtGui.QTextCursor.selectionStart", return_value=20)
def test_MicroPythonREPLPane_keyPressEvent_left_with_selection(a, b):
    """
    Ensure left arrows in the REPL when a selection is made, moves the cursor
    to the start of the selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Left)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.move_cursor_to = mock.MagicMock()
    rp.keyPressEvent(data)
    rp.move_cursor_to.assert_called_once_with(20)


def test_MicroPythonREPLPane_keyPressEvent_home():
    """
    Ensure home key in the REPL is handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Home)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_HOME
    )


def test_MicroPythonREPLPane_keyPressEvent_end():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_End)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_repl_connection.write.assert_called_once_with(
        mu.interface.panes.VT100_END
    )


def test_MicroPythonREPLPane_keyPressEvent_CTRL_C_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.copy = mock.MagicMock()
    data = mock.MagicMock()
    data.key = mock.MagicMock(return_value=Qt.Key_C)
    data.text = mock.MagicMock(return_value="")
    data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
    rp.keyPressEvent(data)
    rp.copy.assert_called_once_with()


def test_MicroPythonREPLPane_keyPressEvent_CTRL_V_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.paste = mock.MagicMock()
    data = mock.MagicMock()
    data.key = mock.MagicMock(return_value=Qt.Key_V)
    data.text = mock.MagicMock(return_value="")
    data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
    rp.keyPressEvent(data)
    rp.paste.assert_called_once_with()


@mock.patch("platform.system", mock.MagicMock(return_value="Darwin"))
def test_MicroPythonREPLPane_keyPressEvent_ctrl_passthrough_darwin():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_M)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=Qt.MetaModifier)
    rp.keyPressEvent(data)
    expected = 1 + Qt.Key_M - Qt.Key_A
    mock_repl_connection.write.assert_called_once_with(bytes([expected]))


@mock.patch("platform.system", mock.MagicMock(return_value="Windows"))
def test_MicroPythonREPLPane_keyPressEvent_ctrl_passthrough_windows():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_M)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier)
    rp.keyPressEvent(data)
    expected = 1 + Qt.Key_M - Qt.Key_A
    mock_repl_connection.write.assert_called_once_with(bytes([expected]))


def test_MicroPythonREPLPane_set_qtcursor_to_devicecursor():
    """
    Test that set_qtcursor_to_devicecursor updates the
    Qt cursor, if the self.device_cursor_position has changed
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    rp.device_cursor_position = 10
    rp.set_qtcursor_to_devicecursor()
    assert rp.textCursor().position() == 10


def test_MicroPythonREPLPane_set_devicecursor_to_qtcursor():
    """
    Test that set_devicecursor_to_qtcursor calls
    move_cursor_to with the appropriate number of steps
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.move_cursor_to = mock.MagicMock()
    rp.setPlainText("Hello world!")
    # Move Qt cursor 10 steps forward
    tc = rp.textCursor()
    tc.setPosition(tc.position() + 10)
    rp.setTextCursor(tc)
    rp.set_devicecursor_to_qtcursor()
    rp.move_cursor_to.assert_called_once_with(10)


def test_MicroPythonREPLPane_set_move_cursor_to_right():
    """
    Test that move_cursor_to sends the appropriate
    number of steps, when moving to the right.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.send = mock.MagicMock()
    rp.setPlainText("Hello world!")
    rp.move_cursor_to(10)
    rp.send.assert_called_once_with(mu.interface.panes.VT100_RIGHT * 10)


def test_MicroPythonREPLPane_set_move_cursor_to_left():
    """
    Test that move_cursor_to sends the appropriate
    number of steps, when moving to the left.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    rp.device_cursor_position = 10
    rp.send = mock.MagicMock()
    rp.move_cursor_to(0)
    rp.send.assert_called_once_with(mu.interface.panes.VT100_LEFT * 10)


def test_MicroPythonREPLPane_delete_selection():
    """
    Test that delete_selection sends the appropriate number of backspaces
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.send = mock.MagicMock()
    rp.move_cursor_to = mock.MagicMock()
    rp.setPlainText("Hello world!")
    tc = rp.textCursor()
    # Make a selection, with the cursor placed
    # at selectionStart and anchor at selectionEnd
    tc.setPosition(rp.textCursor().position() + 10)
    tc.setPosition(0, mode=QTextCursor.KeepAnchor)
    rp.setTextCursor(tc)
    # Try to delete the selection
    assert rp.delete_selection()
    # Check that cursor is moved to end and then
    # backspace called 10 times
    rp.move_cursor_to.assert_called_once_with(tc.selectionEnd())
    rp.send.assert_called_once_with(mu.interface.panes.VT100_BACKSPACE * 10)


def test_MicroPythonREPLPane_delete_selection_w_no_selection():
    """
    Test that delete_election returns false on no selection
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    assert not rp.delete_selection()


def test_MicroPythonREPLPane_mouseReleasedEvent_no_selection():
    """
    Test that when no selection is made, a mouse click updates
    the device cursor to the new location of the cursor in Qt
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.set_devicecursor_to_qtcursor = mock.MagicMock()
    rp.setPlainText("Hello world!")
    # Simulate mouse click
    mouseEvent = QMouseEvent(
        QEvent.MouseButtonRelease,
        QPointF(0.0, 0.0),
        Qt.LeftButton,
        Qt.LeftButton,
        Qt.NoModifier,
    )
    rp.mouseReleaseEvent(mouseEvent)
    # Check set_devicecursor_to_qtcursor was called
    rp.set_devicecursor_to_qtcursor.assert_called_once_with()


def test_MicroPythonREPLPane_mouseReleasedEvent_with_selection():
    """
    Test that when a selection is made in Qt, the cursor movement is
    not send to the device.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.set_devicecursor_to_qtcursor = mock.MagicMock()
    rp.setPlainText("Hello world!")
    tc = rp.textCursor()
    # Make a selection, with the cursor placed
    # at selectionStart and anchor at selectionEnd
    tc.setPosition(rp.textCursor().position() + 10)
    tc.setPosition(0, mode=QTextCursor.KeepAnchor)
    rp.setTextCursor(tc)
    # Simulate mouse click
    mouseEvent = QMouseEvent(
        QEvent.MouseButtonRelease,
        QPointF(0.0, 0.0),
        Qt.LeftButton,
        Qt.LeftButton,
        Qt.NoModifier,
    )
    rp.mouseReleaseEvent(mouseEvent)
    # Check set_devicecursor_to_qtcursor was not called
    rp.set_devicecursor_to_qtcursor.assert_not_called()


def test_MicroPythonREPLPane_process_tty_data():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. Backspace is enacted, carriage-return is ignored, newline moves
    the cursor position to the end of the line before enacted and all others
    are simply inserted.
    """
    mock_repl_connection = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(
        side_effect=[True, False, True, True]
    )
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([8, 13, 10, 65])  # \b, \r, \n, 'A'
    rp.process_tty_data(bs)
    assert mock_tc.movePosition.call_count == 2
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Left
    assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.End
    assert rp.insertPlainText.call_count == 2
    assert rp.insertPlainText.call_args_list[0][0][0] == chr(10)
    assert rp.insertPlainText.call_args_list[1][0][0] == chr(65)
    rp.ensureCursorVisible.assert_called_once_with()


def test_MicroPythonREPLPane_process_tty_data_multibyte_sequence():
    """
    Ensure multibyte unicode characters are correctly parsed, even
    over multiple invocations of process_tty_data
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertPlainText = mock.MagicMock(return_value=None)

    # Copyright symbol: © (0xC2A9)
    rp.process_tty_data(b"\xc2")
    rp.process_tty_data(b"\xa9")

    assert rp.insertPlainText.call_args_list[0][0][0] == "©"


def test_MicroPythonREPLPane_process_tty_data_handle_malformed_unicode():
    """
    Ensure no exception is raised due to malformed unicode sequences
    from the device
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.insertPlainText = mock.MagicMock(return_value=None)

    rp.process_tty_data(b"foo \xd8 bar")

    # Test that malformed input are correctly replaced with the standard
    # unicode replacement character (�, U+FFFD)
    assert rp.insertPlainText.call_args_list[4][0][0] == u"\uFFFD"


def test_MicroPythonREPLPane_process_tty_data_VT100():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure VT100 related codes are handled
    properly.
    """
    mock_repl_connection = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes(
        [
            27,
            91,
            ord("1"),
            ord("A"),  # <Esc>[1A    (VT100 UP)
            27,
            91,
            ord("1"),
            ord("B"),  # <Esc>[1B    (VT100 DOWN)
            27,
            91,
            ord("1"),
            ord("C"),  # <Esc>[1C    (VT100 RIGHT)
            27,
            91,
            ord("1"),
            ord("D"),  # <Esc>[1D    (VT100 LEFT)
            27,
            91,
            ord("K"),  # <Esc>[K     (VT100 DELETE to end of line)
        ]
    )
    rp.process_tty_data(bs)
    assert mock_tc.movePosition.call_count == 5
    assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Up
    assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Down
    assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Right
    assert mock_tc.movePosition.call_args_list[3][0][0] == QTextCursor.Left
    assert (
        mock_tc.movePosition.call_args_list[4][0][0] == QTextCursor.EndOfLine
    )
    assert (
        mock_tc.movePosition.call_args_list[4][1]["mode"]
        == QTextCursor.KeepAnchor
    )
    mock_tc.removeSelectedText.assert_called_once_with()
    rp.ensureCursorVisible.assert_called_once_with()


def test_MicroPythonREPLPane_process_tty_data_backspace():
    """
    Ensure backspace's are interpreted correctly
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to between 'l' and 'd'
    rp.device_cursor_position = 10
    rp.set_qtcursor_to_devicecursor()
    # Receive backspace \b
    # (VT100: \b      - one char back,
    #         \x1b[Kd - delete to end of line
    #         d!      - send the two chars 'd!' again
    #         \b\b    - move cursor back where it were)
    bs = b"\b\x1b[Kd!\b\b"
    rp.process_tty_data(bs)
    assert rp.toPlainText() == "Hello word!"
    assert rp.textCursor().position() == 9
    assert rp.device_cursor_position == 9


def test_MicroPythonREPLPane_process_tty_data_carriage_return():
    """
    Ensure carriage return's are not handled (will be handled on \n)
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to between 'l' and 'd'
    rp.device_cursor_position = 10
    rp.set_qtcursor_to_devicecursor()
    # Receive carriage return \r
    bs = b"\r"
    rp.process_tty_data(bs)
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 10
    assert rp.device_cursor_position == 10


def test_MicroPythonREPLPane_process_tty_data_newline():
    """
    Ensure newline are interpreted correctly (move to end of line,
    then insert new line)
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to between 'l' and 'd'
    rp.device_cursor_position = 10
    rp.set_qtcursor_to_devicecursor()
    # Receive new line \n
    bs = b"\n"
    rp.process_tty_data(bs)
    assert rp.toPlainText() == "Hello world!\n"
    assert rp.textCursor().position() == 13
    assert rp.device_cursor_position == 13


def test_MicroPythonREPLPane_process_tty_data_printed_chars():
    """
    Ensure printed characters are handled correctly, in this case
    overwriting what comes after (as if Insert was pushed)
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to after first 'o'
    rp.device_cursor_position = 5
    rp.set_qtcursor_to_devicecursor()
    # Receive ' foobar!'
    bs = b" foobar!"
    rp.process_tty_data(bs)
    assert rp.toPlainText() == "Hello foobar!"
    assert rp.textCursor().position() == 13
    assert rp.device_cursor_position == 13


def test_MicroPythonREPLPane_process_tty_data_vt100_cursor_left():
    """
    Ensure left cursor movement of several steps works correctly
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to after first 'o'
    rp.device_cursor_position = 5
    rp.set_qtcursor_to_devicecursor()
    # Receive: move 4 times left
    bs = b"\x1B[4D"
    rp.process_tty_data(bs)
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 1
    assert rp.device_cursor_position == 1


def test_MicroPythonREPLPane_process_tty_data_vt100_cursor_right():
    """
    Ensure right cursor movement of several steps works correctly
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to after first 'o'
    rp.device_cursor_position = 5
    rp.set_qtcursor_to_devicecursor()
    # Receive: move 4 times right
    bs = b"\x1B[4C"
    rp.process_tty_data(bs)
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 9
    assert rp.device_cursor_position == 9


def test_MicroPythonREPLPane_process_tty_data_partial_reception():
    """
    Ensure that when partially received multibyte commands are
    received they are handled properly
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to after first 'o'
    rp.device_cursor_position = 5
    rp.set_qtcursor_to_devicecursor()
    # Receive: \x1B
    bs = b"\x1B"
    rp.process_tty_data(bs)
    assert rp.unprocessed_input == "\x1B"
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 5
    assert rp.device_cursor_position == 5
    # Receive [4C - 4 times right
    bs = b"[4C"
    rp.process_tty_data(bs)
    assert rp.unprocessed_input == ""
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 9
    assert rp.device_cursor_position == 9


def test_MicroPythonREPLPane_process_tty_data_partial_reception2():
    """
    Ensure that when partially received multibyte commands are
    received they are handled properly
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to after first 'o'
    rp.device_cursor_position = 5
    rp.set_qtcursor_to_devicecursor()
    # Receive: \x1B
    bs = b"\x1B["
    rp.process_tty_data(bs)
    assert rp.unprocessed_input == "\x1B["
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 5
    assert rp.device_cursor_position == 5
    # Receive 4C - 4 times right
    bs = b"4C"
    rp.process_tty_data(bs)
    assert rp.unprocessed_input == ""
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 9
    assert rp.device_cursor_position == 9


def test_MicroPythonREPLPane_process_tty_data_unsupported_vt100_command():
    """
    Ensure nothing is done, when receiving an unsupported VT100 command
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setPlainText("Hello world!")
    # Move cursor to after first 'o'
    rp.device_cursor_position = 5
    rp.set_qtcursor_to_devicecursor()
    # Receive: \x1B[4X - unknown command X
    bs = b"\x1B[4X"
    rp.process_tty_data(bs)
    # Do nothing
    assert rp.unprocessed_input == b""
    assert rp.toPlainText() == "Hello world!"
    assert rp.textCursor().position() == 5
    assert rp.device_cursor_position == 5


def test_MicroPythonREPLPane_clear():
    """
    Ensure setText is called with an empty string.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.setText = mock.MagicMock(return_value=None)
    rp.clear()
    rp.setText.assert_called_once_with("")


def test_MicroPythonREPLPane_set_font_size():
    """
    Ensure the font is updated to the expected point size.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
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
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.MicroPythonREPLPane(mock_repl_connection)
    rp.set_font_size = mock.MagicMock()
    rp.set_zoom("xxl")
    expected = mu.interface.panes.PANE_ZOOM_SIZES["xxl"]
    rp.set_font_size.assert_called_once_with(expected)


def test_SnekREPLPane_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste me!"
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.insertFromMimeData(mock_clipboard)
    mock_serial.write.assert_called_once_with(bytes("paste me!", "utf8"))


def test_SnekREPLPane_paste_handle_mac_newlines():
    """
    Pasting into the REPL should handle '\r' properly.

    '\r' -> '\n'
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste\rme!"
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.insertFromMimeData(mock_clipboard)
    mock_serial.write.assert_called_once_with(bytes("paste\nme!", "utf8"))


def test_SnekREPLPane_paste_handle_windows_newlines():
    """
    Pasting into the REPL should handle '\r\n' properly.

    '\r\n' -> '\n'
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "paste\r\nme!"
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.insertFromMimeData(mock_clipboard)
    mock_serial.write.assert_called_once_with(bytes("paste\nme!", "utf8"))


def test_SnekREPLPane_paste_only_works_if_there_is_something_to_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = ""
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.insertFromMimeData(mock_clipboard)
    assert mock_serial.write.call_count == 0


def test_SnekREPLPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = "WinNT"
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch("mu.interface.panes.platform", mock_platform), mock.patch(
        "mu.interface.panes.QMenu", mock_qmenu_class
    ), mock.patch("mu.interface.panes.QCursor"):
        rp = mu.interface.panes.SnekREPLPane(mock_serial)
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == "Copy"
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == "Ctrl+Shift+C"
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == "Paste"
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == "Ctrl+Shift+V"
    assert mock_qmenu.exec_.call_count == 1


def test_SnekREPLPane_context_menu_darwin():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = "Darwin"
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch("mu.interface.panes.platform", mock_platform), mock.patch(
        "mu.interface.panes.QMenu", mock_qmenu_class
    ), mock.patch("mu.interface.panes.QCursor"):
        rp = mu.interface.panes.SnekREPLPane(mock_serial)
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == "Copy"
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == "Ctrl+C"
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == "Paste"
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == "Ctrl+V"
    assert mock_qmenu.exec_.call_count == 1


def test_SnekREPLPane_keyPressEvent():
    """
    Ensure key presses in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_A)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=None)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(bytes("a", "utf-8"))


def test_SnekREPLPane_keyPressEvent_backspace():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
    data.text = mock.MagicMock(return_value="\b")
    data.modifiers = mock.MagicMock(return_value=None)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(b"\b")


def test_SnekREPLPane_keyPressEvent_return():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Return)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(mu.interface.panes.VT100_RETURN)


def test_SnekREPLPane_keyPressEvent_delete():
    """
    Ensure delete in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Delete)
    data.text = mock.MagicMock(return_value="\b")
    data.modifiers = mock.MagicMock(return_value=None)
    rp.keyPressEvent(data)
    mock_serial.write.assert_called_once_with(b"\x1B[\x33\x7E")


@mock.patch("PyQt5.QtWidgets.QTextEdit.keyPressEvent")
def test_SnekREPLPane_keyPressEvent_shift_right(
    mock_super_keyPressEvent,
):
    """
    Ensure right arrows with shift in the REPL are passed through to
    the super class, to perform a selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Right)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.ShiftModifier)
    rp.keyPressEvent(data)
    mock_super_keyPressEvent.assert_called_once_with(data)


@mock.patch("PyQt5.QtWidgets.QTextEdit.keyPressEvent")
def test_SnekREPLPane_keyPressEvent_shift_left(
    mock_super_keyPressEvent,
):
    """
    Ensure left arrows with shift in the REPL are passed through to
    the super class, to perform a selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Left)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.ShiftModifier)
    rp.keyPressEvent(data)
    mock_super_keyPressEvent.assert_called_once_with(data)


@mock.patch("PyQt5.QtGui.QTextCursor.hasSelection", return_value=True)
@mock.patch("PyQt5.QtGui.QTextCursor.selectionEnd", return_value=30)
def test_SnekREPLPane_keyPressEvent_right_with_selection(a, b):
    """
    Ensure right arrows in the REPL when a selection is made, moves the cursor
    to the end of the selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Right)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.move_cursor_to = mock.MagicMock()
    rp.keyPressEvent(data)
    rp.move_cursor_to.assert_called_once_with(30)


@mock.patch("PyQt5.QtGui.QTextCursor.hasSelection", return_value=True)
@mock.patch("PyQt5.QtGui.QTextCursor.selectionStart", return_value=20)
def test_SnekREPLPane_keyPressEvent_left_with_selection(a, b):
    """
    Ensure left arrows in the REPL when a selection is made, moves the cursor
    to the start of the selection.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Left)
    data.text = mock.MagicMock(return_value="")
    data.modifiers = mock.MagicMock(return_value=Qt.NoModifier)
    rp.move_cursor_to = mock.MagicMock()
    rp.keyPressEvent(data)
    rp.move_cursor_to.assert_called_once_with(20)


def test_SnekREPLPane_keyPressEvent_CTRL_C_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.copy = mock.MagicMock()
    data = mock.MagicMock()
    data.key = mock.MagicMock(return_value=Qt.Key_C)
    data.text = mock.MagicMock(return_value="1b")
    data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
    rp.keyPressEvent(data)
    rp.copy.assert_called_once_with()


def test_SnekREPLPane_keyPressEvent_CTRL_V_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.paste = mock.MagicMock()
    data = mock.MagicMock()
    data.key = mock.MagicMock(return_value=Qt.Key_V)
    data.text = mock.MagicMock(return_value="1b")
    data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
    rp.keyPressEvent(data)
    rp.paste.assert_called_once_with()


@mock.patch("platform.system", mock.MagicMock(return_value="Darwin"))
def test_SnekREPLPane_keyPressEvent_ctrl_passthrough_darwin():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_M)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=Qt.MetaModifier)
    rp.keyPressEvent(data)
    expected = 1 + Qt.Key_M - Qt.Key_A
    mock_repl_connection.write.assert_called_once_with(bytes([expected]))


@mock.patch("platform.system", mock.MagicMock(return_value="Windows"))
def test_SnekREPLPane_keyPressEvent_ctrl_passthrough_windows():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_repl_connection)
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_M)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier)
    rp.keyPressEvent(data)
    expected = 1 + Qt.Key_M - Qt.Key_A
    mock_repl_connection.write.assert_called_once_with(bytes([expected]))


def test_SnekREPLPane_set_devicecursor_to_qtcursor():
    """
    Test that set_devicecursor_to_qtcursor resets
    cursor position correctly
    """
    mock_repl_connection = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_repl_connection)
    rp.move_cursor_to = mock.MagicMock()
    rp.setPlainText("Hello world!")
    # Move Qt cursor 10 steps forward
    tc = rp.textCursor()
    tc.setPosition(tc.position() + 10)
    rp.setTextCursor(tc)
    rp.set_devicecursor_to_qtcursor()
    assert tc.position() == 10


def test_SnekREPLPane_process_bytes():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. Backspace is enacted, carriage-return is ignored, newline moves
    the cursor position to the end of the line before enacted and all others
    are simply inserted.
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(
        side_effect=[True, False, True, True]
    )
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    bs = bytes([8, 13, 10, 65])  # \b, \r, \n, 'A'
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


def test_SnekREPLPane_process_bytes_gettext():
    """
    Ensure bytes coming from the device to the application in 'gettext' mode
    are processed as expected. Carriage-return is
    ignored, all others are simply passed to recv_text callback
    """
    mock_serial = mock.MagicMock()
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(
        side_effect=[True, False, True, True]
    )
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.textCursor = mock.MagicMock(return_value=mock_tc)
    rp.setTextCursor = mock.MagicMock(return_value=None)
    rp.insertPlainText = mock.MagicMock(return_value=None)
    rp.ensureCursorVisible = mock.MagicMock(return_value=None)
    rp.text_recv = mock.MagicMock()
    rp.text_recv.recv_text = mock.MagicMock()
    bs = bytes([2, 65, 66, 67, 13, 3])  # \2, 'A', 'B', 'C' \r \3
    rp.process_bytes(bs)
    rp.text_recv.recv_text.assert_called_once_with("ABC")


def test_SnekREPLPane_clear():
    """
    Ensure setText is called with an empty string.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.setText = mock.MagicMock(return_value=None)
    rp.clear()
    rp.setText.assert_called_once_with("")


def test_SnekREPLPane_set_font_size():
    """
    Ensure the font is updated to the expected point size.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    mock_font = mock.MagicMock()
    rp.font = mock.MagicMock(return_value=mock_font)
    rp.setFont = mock.MagicMock()
    rp.set_font_size(123)
    mock_font.setPointSize.assert_called_once_with(123)
    rp.setFont.assert_called_once_with(mock_font)


def test_SnekREPLPane_set_zoom():
    """
    Ensure the font size is correctly set from the t-shirt size.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.set_font_size = mock.MagicMock()
    rp.set_zoom("xxl")
    expected = mu.interface.panes.PANE_ZOOM_SIZES["xxl"]
    rp.set_font_size.assert_called_once_with(expected)


def test_SnekREPLPane_send_commands():
    """
    Ensure the list of commands is correctly encoded and bound by control
    commands to put the board into and out of raw mode.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    rp.execute = mock.MagicMock()
    commands = [
        "import os\n",
        "print(os.listdir())\n",
    ]
    rp.send_commands(commands)
    expected = [
        b"\x0e\x03",  # Put the board into raw mode.
        b"import os\n",  # The commands to run.
        b"print(os.listdir())\n",
        b"\x0f",  # Evaluate the commands.
    ]
    rp.execute.assert_called_once_with(expected)


def test_SnekREPLPane_execute():
    """
    Ensure the first command is sent via serial to the connected device, and
    further commands are scheduled for the future.
    """
    mock_serial = mock.MagicMock()
    rp = mu.interface.panes.SnekREPLPane(mock_serial)
    commands = [
        b"A",
        b"B",
    ]
    with mock.patch("mu.interface.panes.QTimer") as mock_timer:
        rp.execute(commands)
        mock_serial.write.assert_called_once_with(b"A")
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
    with mock.patch("mu.interface.panes.QMessageBox", mock_qmb_class):
        assert mfl.show_confirm_overwrite_dialog()
    msg = "File already exists; overwrite it?"
    mock_qmb.setText.assert_called_once_with(msg)
    mock_qmb.setWindowTitle.assert_called_once_with("File already exists")
    mock_qmb.setIcon.assert_called_once_with(QMessageBox.Information)


def test_MicroPythonDeviceFileList_init():
    """
    Check the widget references the user's home and allows drag and drop.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileList("home/path")
    assert mfs.home == "home/path"
    assert mfs.dragDropMode() == mfs.DragDrop


def test_MicroPythonDeviceFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.LocalFileList("homepath")
    mock_item = mock.MagicMock()
    mock_item.text.return_value = "foo.py"
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mfs = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.put = mock.MagicMock()
    # Test
    mfs.dropEvent(mock_event)
    fn = os.path.join("homepath", "foo.py")
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
    mfs = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mfs.findItems = mock.MagicMock()
    mfs.dropEvent(mock_event)
    assert mfs.findItems.call_count == 0


def test_MicroPythonDeviceFileList_on_put():
    """
    A message and list_files signal should be emitted.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mfs.set_message = mock.MagicMock()
    mfs.list_files = mock.MagicMock()

    mfs.on_put("my_file.py")

    mfs.set_message.emit.assert_called_once_with(
        "'my_file.py' successfully copied to device."
    )
    mfs.list_files.emit.assert_called_once_with()


def test_MicroPythonDeviceFileList_contextMenuEvent():
    """
    Ensure that the menu displayed when a file on the MicroPython device is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mock_current = mock.MagicMock()
    mock_current.text.return_value = "foo.py"
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.disable = mock.MagicMock()
    mfs.set_message = mock.MagicMock()
    mfs.delete = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()
    with mock.patch("mu.interface.panes.QMenu", return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
    mfs.disable.emit.assert_called_once_with()
    assert mfs.set_message.emit.call_count == 1
    mfs.delete.emit.assert_called_once_with("foo.py")


def test_MicroPythonDeviceFileList_contextMenuEvent_empty_list():
    """
    Ensure that there is no menu displayed (and menu action processed) when
    there is not files in the MicroPython device and the list is right-clicked.
    """
    mock_menu = mock.MagicMock()
    mfs = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mfs.currentItem = mock.MagicMock(return_value=None)
    mock_event = mock.MagicMock()

    with mock.patch("mu.interface.panes.QMenu", return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)

    assert not mock_menu.called
    assert not mock_event.called


def test_MicroPythonFileList_on_delete():
    """
    On delete should emit a message and list_files signal.
    """
    mfs = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mfs.set_message = mock.MagicMock()
    mfs.list_files = mock.MagicMock()

    mfs.on_delete("my_file.py")

    mfs.set_message.emit.assert_called_once_with(
        "'my_file.py' successfully deleted from device."
    )
    mfs.list_files.emit.assert_called_once_with()


def test_LocalFileList_init():
    """
    Ensure the class instantiates with the expected state.
    """
    lfl = mu.interface.panes.LocalFileList("home/path")
    assert lfl.home == "home/path"
    assert lfl.dragDropMode() == lfl.DragDrop


def test_LocalFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.panes.MicroPythonDeviceFileList("homepath")
    mock_item = mock.MagicMock()
    mock_item.text.return_value = "foo.py"
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    lfs = mu.interface.panes.LocalFileList("homepath")
    lfs.disable = mock.MagicMock()
    lfs.set_message = mock.MagicMock()
    lfs.get = mock.MagicMock()
    # Test
    lfs.dropEvent(mock_event)
    fn = os.path.join("homepath", "foo.py")
    lfs.disable.emit.assert_called_once_with()
    assert lfs.set_message.emit.call_count == 1
    lfs.get.emit.assert_called_once_with("foo.py", fn)


def test_LocalFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    lfs = mu.interface.panes.LocalFileList("homepath")
    lfs.findItems = mock.MagicMock()
    lfs.dropEvent(mock_event)
    assert lfs.findItems.call_count == 0


def test_LocalFileList_on_get():
    """
    On get should emit two signals: a message and list_files.
    """
    lfs = mu.interface.panes.LocalFileList("homepath")
    lfs.set_message = mock.MagicMock()
    lfs.list_files = mock.MagicMock()

    lfs.on_get("my_file.py")

    lfs.set_message.emit.assert_called_once_with(
        "Successfully copied 'my_file.py' from the device to your computer."
    )
    lfs.list_files.emit.assert_called_once_with()


def test_LocalFileList_contextMenuEvent():
    """
    Ensure the menu displayed when a local .py file is right-clicked works as
    expected when activated and signals are sent for "Open in Mu" entry.
    """
    mock_menu = mock.create_autospec(QMenu, instance=True)
    mock_action_first = mock.MagicMock()
    mock_menu.addAction.side_effect = [
        mock_action_first,  # "Open in Mu"
        mock.MagicMock(),  # "Write to main.py on device"
        mock.MagicMock(),  # "Open"
    ]
    mock_menu.exec_.return_value = mock_action_first
    mfs = mu.interface.panes.LocalFileList("homepath")
    mock_open = mock.MagicMock()
    mfs.open_file = mock.MagicMock()
    mfs.open_file.emit = mock_open
    mock_current = mock.MagicMock()
    mock_current.text.return_value = "foo.py"
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.set_message = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()

    with mock.patch(
        "mu.interface.panes.QMenu", return_value=mock_menu, autospec=True
    ):
        mfs.contextMenuEvent(mock_event)

    assert mfs.set_message.emit.call_count == 0
    assert mock_menu.addAction.call_count == 3
    mock_open.assert_called_once_with(os.path.join("homepath", "foo.py"))


def test_LocalFileList_contextMenuEvent_hex():
    """
    Ensure the menu displayed when a local .hex file is right-clicked works as
    expected when activated and signals are sent for "Open" entry.
    """
    mock_menu = mock.create_autospec(QMenu, instance=True)
    mock_action_second = mock.MagicMock()
    mock_menu.addAction.side_effect = [
        mock.MagicMock(),  # "Open in Mu"
        mock_action_second,  # "Open"
    ]
    mock_menu.exec_.return_value = mock_action_second
    mfs = mu.interface.panes.LocalFileList("homepath")
    mock_current = mock.MagicMock()
    mock_current.text.return_value = "foo.hex"
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.set_message = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()

    with mock.patch(
        "mu.interface.panes.QMenu", return_value=mock_menu
    ), mock.patch(
        "mu.interface.panes.QDesktopServices", autospec=True
    ) as mock_QDesktopServices:
        mfs.contextMenuEvent(mock_event)

    assert mfs.set_message.emit.call_count == 1
    assert mock_menu.addAction.call_count == 2
    mock_QDesktopServices.openUrl.assert_called_once_with(
        QUrl.fromLocalFile(
            os.path.abspath(os.path.join("homepath", "foo.hex"))
        )
    )


def test_LocalFileList_contextMenuEvent_external():
    """
    Ensure the menu displayed when a local file with a non py/hex extension
    is right-clicked works as expected when the "Open" option is clicked.
    """
    mock_menu = mock.create_autospec(QMenu, instance=True)
    mock_action = mock.MagicMock()
    mock_menu.addAction.side_effect = [mock_action, mock.MagicMock()]  # "Open"
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.panes.LocalFileList("homepath")
    mock_open = mock.MagicMock()
    mfs.open_file = mock.MagicMock()
    mfs.open_file.emit = mock_open
    mock_current = mock.MagicMock()
    mock_current.text.return_value = "foo.qwerty"
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.set_message = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()

    with mock.patch(
        "mu.interface.panes.QMenu", return_value=mock_menu
    ), mock.patch(
        "mu.interface.panes.QDesktopServices", autospec=True
    ) as mock_QDesktopServices:
        mfs.contextMenuEvent(mock_event)

    assert mfs.set_message.emit.call_count == 1
    assert mock_menu.addAction.call_count == 1
    assert mock_open.call_count == 0
    mock_QDesktopServices.openUrl.assert_called_once_with(
        QUrl.fromLocalFile(
            os.path.abspath(os.path.join("homepath", "foo.qwerty"))
        )
    )


def test_LocalFileList_contextMenuEvent_write_to_mainpy():
    """
    Ensure that the filesystem put-signal is emitted when a local file
    is right-clicked and the appropriate menu item activated by a
    user.
    """
    mock_menu = mock.MagicMock()
    mock_action_first = mock.MagicMock()
    mock_action_second = mock.MagicMock()
    mock_action_third = mock.MagicMock()
    mock_menu.addAction.side_effect = [
        mock_action_first,
        mock_action_second,
        mock_action_third,
    ]
    mock_menu.exec_.return_value = mock_action_second
    mfs = mu.interface.panes.LocalFileList("homepath")
    mfs.put = mock.MagicMock()
    mock_current = mock.MagicMock()
    mock_current.text.return_value = "foo.py"
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.set_message = mock.MagicMock()
    mfs.mapToGlobal = mock.MagicMock()
    mock_event = mock.MagicMock()

    with mock.patch("mu.interface.panes.QMenu", return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)

    assert mfs.set_message.emit.call_count == 0
    mfs.put.emit.assert_called_once_with(
        os.path.join("homepath", "foo.py"), "main.py"
    )


def test_LocalFileList_contextMenuEvent_empty_list():
    """
    Ensure that there is no menu displayed with a right-clicked if the local
    file list is empty.
    """
    mock_menu = mock.MagicMock()
    mock_menu.exec_.return_value = mock.MagicMock()
    mfs = mu.interface.panes.LocalFileList("homepath")
    mfs.currentItem = mock.MagicMock(return_value=None)
    mock_event = mock.MagicMock()

    with mock.patch("mu.interface.panes.QMenu", return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)

    assert not mock_menu.called
    assert not mock_event.called
    assert mock_menu.addAction.call_count == 0


def test_FileSystemPane_init():
    """
    Check things are set up as expected.
    """
    home = "homepath"
    test_microbit_fs = mu.interface.panes.MicroPythonDeviceFileList(home)
    test_microbit_fs.disable = mock.MagicMock()
    test_microbit_fs.set_message = mock.MagicMock()
    test_local_fs = mu.interface.panes.LocalFileList(home)
    test_local_fs.disable = mock.MagicMock()
    test_local_fs.set_message = mock.MagicMock()
    mock_mfl = mock.MagicMock(return_value=test_microbit_fs)
    mock_lfl = mock.MagicMock(return_value=test_local_fs)
    with mock.patch(
        "mu.interface.panes.MicroPythonDeviceFileList", mock_mfl
    ), mock.patch("mu.interface.panes.LocalFileList", mock_lfl):
        fsp = mu.interface.panes.FileSystemPane("homepath")
        assert isinstance(fsp.microbit_label, QLabel)
        assert isinstance(fsp.local_label, QLabel)
        assert fsp.microbit_fs == test_microbit_fs
        assert fsp.local_fs == test_local_fs
        test_microbit_fs.disable.connect.assert_called_once_with(fsp.disable)
        test_microbit_fs.set_message.connect.assert_called_once_with(
            fsp.show_message
        )
        test_local_fs.disable.connect.assert_called_once_with(fsp.disable)
        test_local_fs.set_message.connect.assert_called_once_with(
            fsp.show_message
        )


def test_FileSystemPane_disable():
    """
    The child list widgets are disabled correctly.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
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
    fsp = mu.interface.panes.FileSystemPane("homepath")
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
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.set_theme("test")


def test_FileSystemPane_show_message():
    """
    Ensure the expected message signal is emitted.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.set_message = mock.MagicMock()
    fsp.show_message("Hello")
    fsp.set_message.emit.assert_called_once_with("Hello")


def test_FileSystemPane_show_warning():
    """
    Ensure the expected warning signal is emitted.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.set_warning = mock.MagicMock()
    fsp.show_warning("Hello")
    fsp.set_warning.emit.assert_called_once_with("Hello")


def test_FileSystemPane_on_ls():
    """
    When lists of files have been obtained from the micro:bit and local
    filesystem, make sure they're properly processed by the on_ls event
    handler.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
    microbit_files = ["foo.py", "bar.py"]
    fsp.microbit_fs = mock.MagicMock()
    fsp.local_fs = mock.MagicMock()
    fsp.enable = mock.MagicMock()
    local_files = ["qux.py", "baz.py"]
    mock_listdir = mock.MagicMock(return_value=local_files)
    mock_isfile = mock.MagicMock(return_value=True)
    with mock.patch("mu.interface.panes.os.listdir", mock_listdir), mock.patch(
        "mu.interface.panes.os.path.isfile", mock_isfile
    ):
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
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.show_warning = mock.MagicMock()
    fsp.disable = mock.MagicMock()
    fsp.on_ls_fail()
    assert fsp.show_warning.call_count == 1
    fsp.disable.assert_called_once_with()


def test_FileSystem_Pane_on_put_fail():
    """
    A warning is emitted if putting files on the micro:bit fails.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.show_warning = mock.MagicMock()
    fsp.on_put_fail("foo.py")
    assert fsp.show_warning.call_count == 1


def test_FileSystem_Pane_on_delete_fail():
    """
    A warning is emitted if deleting files on the micro:bit fails.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.show_warning = mock.MagicMock()
    fsp.on_delete_fail("foo.py")
    assert fsp.show_warning.call_count == 1


def test_FileSystem_Pane_on_get_fail():
    """
    A warning is emitted if getting files from the micro:bit fails.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.show_warning = mock.MagicMock()
    fsp.on_get_fail("foo.py")
    assert fsp.show_warning.call_count == 1


def test_FileSystemPane_set_font_size():
    """
    Ensure the right size is set as the point size and the text based UI child
    widgets are updated.
    """
    fsp = mu.interface.panes.FileSystemPane("homepath")
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
    fsp = mu.interface.panes.FileSystemPane("homepath")
    fsp.open_file = mock.MagicMock()
    mock_open_emit = mock.MagicMock()
    fsp.open_file.emit = mock_open_emit
    fsp.local_fs.open_file.emit("test")
    mock_open_emit.assert_called_once_with("test")


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
    jw._append_plain_text("hello")
    jw.on_append_text.emit.assert_called_once_with("hello".encode("utf-8"))


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
    jw.set_zoom("xxl")
    jw.set_font_size.assert_called_once_with(
        mu.interface.panes.PANE_ZOOM_SIZES["xxl"]
    )


def test_JupyterREPLPane_set_theme_day():
    """
    Make sure the theme is correctly set for day.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_theme("day")
    assert jw.style_sheet == DAY_STYLE
    assert jw.syntax_style == "default"


def test_JupyterREPLPane_set_theme_night():
    """
    Make sure the theme is correctly set for night.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_theme("night")
    assert jw.style_sheet == NIGHT_STYLE
    assert jw.syntax_style == "monokai"


def test_JupyterREPLPane_set_theme_contrast():
    """
    Make sure the theme is correctly set for high contrast.
    """
    jw = mu.interface.panes.JupyterREPLPane()
    jw.set_theme("contrast")
    assert jw.style_sheet == CONTRAST_STYLE
    assert jw.syntax_style == "bw"


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
    assert ppp.stdout_buffer == b""
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
    interpreter = sys.executable
    working_directory = "workspace"
    script_filename = "script.py"
    script_filepath = os.path.abspath(os.path.normcase(script_filename))
    with mock.patch("mu.interface.panes.QProcess", mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.start_process(interpreter, script_filename, working_directory)
    assert mock_process_class.call_count == 1
    assert ppp.process == mock_process
    ppp.process.setProcessChannelMode.assert_called_once_with(mock_merge_chans)
    ppp.process.setWorkingDirectory.assert_called_once_with(working_directory)
    ppp.process.readyRead.connect.assert_called_once_with(
        ppp.try_read_from_stdout
    )
    ppp.process.finished.connect.assert_called_once_with(ppp.finished)
    assert ppp.script == script_filepath
    expected_args = ["-i", script_filepath]  # called with interactive flag.
    ppp.process.start.assert_called_once_with(interpreter, expected_args)
    assert ppp.running is True


def test_PythonProcessPane_start_process_command_args():
    """
    Ensure that the new process is passed the expected comand line args.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    runner = sys.executable
    script_filename = "script.py"
    script_filepath = os.path.abspath(os.path.normcase(script_filename))
    with mock.patch("mu.interface.panes.QProcess", mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ["foo", "bar"]
        ppp.start_process(
            runner, script_filename, "workspace", command_args=args
        )
    expected_args = ["-i", script_filepath, "foo", "bar"]
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
    interpreter = sys.executable
    script_filename = "script.py"
    script_filepath = os.path.abspath(os.path.normcase(script_filename))
    working_directory = "workspace"
    with mock.patch("mu.interface.panes.QProcess", mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ["foo", "bar"]
        ppp.start_process(
            interpreter,
            script_filename,
            working_directory,
            debugger=True,
            command_args=args,
        )
    mu_dir = os.path.dirname(os.path.abspath(mu.__file__))
    runner = os.path.join(mu_dir, "mu_debug.py")
    expected_script = script_filepath
    expected_args = [runner, expected_script, "foo", "bar"]
    ppp.process.start.assert_called_once_with(interpreter, expected_args)


def test_PythonProcessPane_start_process_not_interactive():
    """
    Ensure that if the interactive flag is unset, the "-i" flag passed into
    the Python process is missing.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    interpreter = sys.executable
    script_filename = "script.py"
    script_filepath = os.path.abspath(os.path.normcase(script_filename))
    with mock.patch("mu.interface.panes.QProcess", mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ["foo", "bar"]
        ppp.start_process(
            interpreter,
            script_filename,
            "workspace",
            interactive=False,
            command_args=args,
        )
    expected_args = [script_filepath, "foo", "bar"]
    ppp.process.start.assert_called_once_with(interpreter, expected_args)


def test_PythonProcessPane_start_process_user_environment_variables():
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
    interpreter = sys.executable
    script_filename = "script.py"
    with mock.patch(
        "mu.interface.panes.QProcess", mock_process_class
    ), mock.patch("mu.interface.panes.sys") as mock_sys, mock.patch(
        "mu.interface.panes.QProcessEnvironment", mock_environment_class
    ):
        mock_sys.platform = "darwin"
        ppp = mu.interface.panes.PythonProcessPane()
        envars = {"name": "value"}
        ppp.start_process(
            interpreter,
            script_filename,
            "workspace",
            interactive=False,
            envars=envars,
        )
    expected_encoding = "{}.utf-8".format(i18n.language_code)
    assert mock_environment.insert.call_count == 5
    assert mock_environment.insert.call_args_list[0][0] == (
        "PYTHONUNBUFFERED",
        "1",
    )
    assert mock_environment.insert.call_args_list[1][0] == (
        "PYTHONIOENCODING",
        "utf-8",
    )
    assert mock_environment.insert.call_args_list[2][0] == (
        "LC_ALL",
        expected_encoding,
    )
    assert mock_environment.insert.call_args_list[3][0] == (
        "LANG",
        expected_encoding,
    )
    assert mock_environment.insert.call_args_list[4][0] == ("name", "value")


@pytest.mark.skip(reason="Only used by debugger; now refactored")
def test_PythonProcessPane_start_process_custom_runner():
    """
    Ensure that if the runner is set, it is used as the command to start the
    new child Python process.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch("mu.interface.panes.QProcess", mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        args = ["foo", "bar"]
        ppp.start_process(
            "script.py",
            "workspace",
            interactive=False,
            command_args=args,
            runner="foo",
        )
    expected_script = os.path.abspath(os.path.normcase("script.py"))
    expected_args = [expected_script, "foo", "bar"]
    ppp.process.start.assert_called_once_with("foo", expected_args)


def test_PythonProcessPane_start_process_custom_python_args():
    """
    Ensure that if there are arguments to be passed into the Python runtime
    starting the child process, these are passed on correctly.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch("mu.interface.panes.QProcess", mock_process_class):
        ppp = mu.interface.panes.PythonProcessPane()
        py_args = ["-m", "pgzero"]
        ppp.start_process(
            sys.executable,
            "script.py",
            "workspace",
            interactive=False,
            python_args=py_args,
        )
    expected_script = os.path.abspath(os.path.normcase("script.py"))
    expected_args = ["-m", "pgzero", expected_script]
    runner = sys.executable
    ppp.process.start.assert_called_once_with(runner, expected_args)


def test_PythonProcessPane_stop_process():
    """
    Ensure that a process is terminated on PythonProcessPane.stop_process
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.stop_process()
    ppp.process.terminate.assert_called_once_with()
    ppp.process.waitForFinished.assert_called_once_with(10)


def test_PythonProcessPane_stop_process_with_error():
    """
    If killing the child process encounters a problem (perhaps the
    process is already dead), then log this and tidy up.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.waitForFinished.return_value = False
    ppp.stop_process()
    ppp.process.terminate.assert_called_once_with()
    ppp.process.kill.assert_called_once_with()
    ppp.process.waitForFinished.call_count == 2


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
    assert "exit code: 0" in mock_cursor.insertText.call_args[0][0]
    assert "status: 1" in mock_cursor.insertText.call_args[0][0]
    ppp.setReadOnly.assert_called_once_with(True)
    ppp.setTextCursor.assert_called_once_with(ppp.textCursor())


def test_PythonProcessPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = "WinNT"
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch("mu.interface.panes.platform", mock_platform), mock.patch(
        "mu.interface.panes.QMenu", mock_qmenu_class
    ), mock.patch("mu.interface.panes.QCursor"):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == "Copy"
    assert copy_action[1] == ppp.copy
    assert copy_action[2].toString() == "Ctrl+Shift+C"
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == "Paste"
    assert paste_action[1] == ppp.paste
    assert paste_action[2].toString() == "Ctrl+Shift+V"
    assert mock_qmenu.exec_.call_count == 1


def test_PythonProcessPane_context_menu_darwin():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = "Darwin"
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch("mu.interface.panes.platform", mock_platform), mock.patch(
        "mu.interface.panes.QMenu", mock_qmenu_class
    ), mock.patch("mu.interface.panes.QCursor"):
        ppp = mu.interface.panes.PythonProcessPane()
        ppp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == "Copy"
    assert copy_action[1] == ppp.copy
    assert copy_action[2].toString() == "Ctrl+C"
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == "Paste"
    assert paste_action[1] == ppp.paste
    assert paste_action[2].toString() == "Ctrl+V"
    assert mock_qmenu.exec_.call_count == 1


def test_PythonProcessPane_paste():
    """
    Ensure pasted text is handed off to the parse_paste method.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_paste = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "Hello"
    ppp.insertFromMimeData(mock_clipboard)
    ppp.parse_paste.assert_called_once_with("Hello")


def test_PythonProcessPane_paste_normalize_windows_newlines():
    """
    Ensure that pasted text containing Windows style line-ends is normalised
    to '\n'.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_paste = mock.MagicMock()
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = "h\r\ni"
    ppp.insertFromMimeData(mock_clipboard)
    ppp.parse_paste.assert_called_once_with("h\ni")


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
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
        ppp.parse_paste("hello")
    ppp.parse_input.assert_called_once_with(None, "h", None)
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
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
        ppp.parse_paste("ÅÄÖ")
    ppp.parse_input.assert_called_once_with(None, "Å", None)
    assert mock_timer.singleShot.call_count == 1


def test_PythonProcessPane_parse_paste_newline():
    """
    As above, but ensure the correct handling of a newline character.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
        ppp.parse_paste("\nhello")
    ppp.parse_input.assert_called_once_with(Qt.Key_Enter, "\n", None)
    assert mock_timer.singleShot.call_count == 1


def test_PythonProcessPane_parse_paste_final_character():
    """
    As above, but ensure that if there a no more remaining characters to parse
    in the pasted text, then don't schedule any more recursive calls.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
        ppp.parse_paste("\n")
    ppp.parse_input.assert_called_once_with(Qt.Key_Enter, "\n", None)
    assert mock_timer.singleShot.call_count == 0


def test_PythonProcessPane_keyPressEvent_a():
    """
    A character is typed and passed into parse_input in the expected manner.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.parse_input = mock.MagicMock()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_A)
    data.text = mock.MagicMock(return_value="a")
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    ppp.parse_input.assert_called_once_with(Qt.Key_A, "a", None)


def test_PythonProcessPane_on_process_halt():
    """
    Ensure the output from the halted process is dumped to the UI.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.readAll().data.return_value = b"halted"
    ppp.append = mock.MagicMock()
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    ppp.on_process_halt()
    ppp.process.readAll().data.assert_called_once_with()
    ppp.append.assert_called_once_with(b"halted")
    ppp.on_append_text.emit.assert_called_once_with(b"halted")
    ppp.set_start_of_current_line.assert_called_once_with()


def test_PythonProcessPane_on_process_halt_badly_formed_bytes():
    """
    If the bytes read from the child process's stdout starts with a badly
    formed unicode character (e.g. a fragment of a multi-byte character such as
    "𠜎"), then ensure the problem bytes at the start of the data are discarded
    until a valid result can be turned into a string.
    """
    data = "𠜎Hello, World!".encode("utf-8")  # Contains a multi-byte char.
    data = data[1:]  # Split the muti-byte character (cause UnicodeDecodeError)
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.readAll().data.return_value = data
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    ppp.on_process_halt()
    ppp.process.readAll().data.assert_called_once_with()
    ppp.on_append_text.emit.assert_called_once_with(b"Hello, World!")
    ppp.set_start_of_current_line.assert_called_once_with()


def test_PythonProcessPane_parse_input_a():
    """
    Ensure a regular printable character is inserted into the text area.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.insert = mock.MagicMock()
    key = Qt.Key_A
    text = "a"
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.insert.assert_called_once_with(b"a")


def test_PythonProcessPane_parse_input_non_ascii():
    """
    Ensure a non-ascii printable character is inserted into the text area.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.insert = mock.MagicMock()
    key = Qt.Key_A
    text = "Å"
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.insert.assert_called_once_with("Å".encode("utf-8"))


def test_PythonProcessPane_parse_input_ctrl_c():
    """
    Control-C (SIGINT / KeyboardInterrupt) character is typed.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.processId.return_value = 123
    ppp.running = True
    key = Qt.Key_C
    text = ""
    modifiers = Qt.ControlModifier
    mock_kill = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.panes.os.kill", mock_kill), mock.patch(
        "mu.interface.panes.QTimer", mock_timer
    ), mock.patch("mu.interface.panes.platform.system", return_value="win32"):
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
    text = ""
    modifiers = Qt.ControlModifier
    mock_timer = mock.MagicMock()
    with mock.patch(
        "mu.interface.panes.platform.system", return_value="win32"
    ), mock.patch("mu.interface.panes.QTimer", mock_timer):
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
    text = ""
    modifiers = Qt.ControlModifier
    mock_kill = mock.MagicMock()
    with mock.patch("mu.interface.panes.os.kill", mock_kill), mock.patch(
        "mu.interface.panes.platform.system", return_value="win32"
    ):
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
    text = ""
    modifiers = Qt.ControlModifier
    with mock.patch(
        "mu.interface.panes.platform.system", return_value="win32"
    ):
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
    text = ""
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
    text = ""
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
    text = ""
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
    text = ""
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
    text = ""
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    assert mock_cursor.movePosition.call_count == 0
    assert ppp.setTextCursor.call_count == 0


def test_PythonProcessPane_parse_input_home():
    """
    Home moves cursor to the start of the input line.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value="hello")
    mock_cursor = mock.MagicMock()
    ppp.start_of_current_line = 0
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setTextCursor = mock.MagicMock()
    key = Qt.Key_Home
    text = ""
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
    text = ""
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
    text = ""
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
    text = ""
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
    text = "\b"
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
    text = "\b"
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.delete.assert_called_once_with()


def test_PythonProcessPane_parse_input_newline():
    """
    Newline causes the input line to be written to the child process's stdin.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value="abc\n")
    ppp.start_of_current_line = 0
    ppp.textCursor = mock.MagicMock()
    ppp.textCursor().position.return_value = 666
    ppp.setTextCursor = mock.MagicMock()
    ppp.insert = mock.MagicMock()
    ppp.write_to_stdin = mock.MagicMock()
    key = Qt.Key_Enter
    text = "\r"
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.write_to_stdin.assert_called_once_with(b"abc\n")
    assert b"abc" in ppp.input_history
    assert ppp.history_position == 0
    # On newline, the start of the current line should be set correctly.
    assert ppp.start_of_current_line == 4  # len('abc\n')


def test_PythonProcessPane_parse_input_newline_ignore_empty_input_in_history():
    """
    Newline causes the input line to be written to the child process's stdin,
    but if the resulting line is either empty or only contains whitespace, do
    not add it to the input_history.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.toPlainText = mock.MagicMock(return_value="   \n")
    ppp.start_of_current_line = 0
    ppp.write_to_stdin = mock.MagicMock()
    key = Qt.Key_Enter
    text = "\r"
    modifiers = None
    ppp.parse_input(key, text, modifiers)
    ppp.write_to_stdin.assert_called_once_with(b"   \n")
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
    ppp.parse_input(Qt.Key_Enter, "\r", None)
    ppp.write_to_stdin.assert_called_with(b"abc\n")


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
    ppp.input_history = ["a", "b", "c"]
    ppp.history_position = 0
    ppp.replace_input_line = mock.MagicMock()
    ppp.history_back()
    ppp.replace_input_line.assert_called_once_with("c")
    assert ppp.history_position == -1


def test_PythonProcessPane_history_back_at_first_item():
    """
    Ensure the current input line is replaced by the next item back in time
    from the current history position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ["a", "b", "c"]
    ppp.history_position = -3
    ppp.replace_input_line = mock.MagicMock()
    ppp.history_back()
    ppp.replace_input_line.assert_called_once_with("a")
    assert ppp.history_position == -3


def test_PythonProcessPane_history_forward():
    """
    Ensure the current input line is replaced by the next item forward in time
    from the current history position.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ["a", "b", "c"]
    ppp.history_position = -3
    ppp.replace_input_line = mock.MagicMock()
    ppp.history_forward()
    ppp.replace_input_line.assert_called_once_with("b")
    assert ppp.history_position == -2


def test_PythonProcessPane_history_forward_at_last_item():
    """
    Ensure the current input line is cleared if the history position was at
    the most recent item.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    # 'a' was typed first, 'c' is the most recent entry.
    ppp.input_history = ["a", "b", "c"]
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
    ppp.process.read.return_value = b"hello world"
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
        ppp.read_from_stdout()
    assert ppp.append.call_count == 1
    ppp.process.read.assert_called_once_with(256)
    ppp.on_append_text.emit.assert_called_once_with(b"hello world")
    ppp.set_start_of_current_line.assert_called_once_with()
    mock_timer.singleShot.assert_called_once_with(2, ppp.read_from_stdout)


def test_PythonProcessPane_read_from_stdout_with_stdout_buffer():
    """
    Ensure incoming bytes from sub-process's stdout are processed correctly if
    there was a split between reads in a multi-byte character (such as "𠜎").

    The buffer is pre-pended to the current read, thus resulting in bytes that
    can be successfully represented in a UTF based string.
    """
    msg = "Hello 𠜎 world".encode("utf-8")
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.stdout_buffer = msg[:7]  # Start of msg but split in multi-byte char.
    ppp.process = mock.MagicMock()
    ppp.process.read.return_value = msg[7:]  # Remainder of msg.
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
        ppp.read_from_stdout()
    ppp.process.read.assert_called_once_with(256)
    ppp.on_append_text.emit.assert_called_once_with(msg)
    ppp.set_start_of_current_line.assert_called_once_with()
    mock_timer.singleShot.assert_called_once_with(2, ppp.read_from_stdout)
    assert ppp.stdout_buffer == b""


def test_PythonProcessPane_read_from_stdout_with_unicode_error():
    """
    Ensure incoming bytes from sub-process's stdout are processed correctly if
    there was a split between reads in a multi-byte character (such as "𠜎").

    If the read bytes end with a split of a multi-byte character, ensure they
    are put into the self.stdout_buffer so they can be pre-pended to the next
    bytes read from the child process.
    """
    msg = "Hello 𠜎 world".encode("utf-8")
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.process.read.return_value = msg[:7]  # Split the multi-byte character.
    ppp.on_append_text = mock.MagicMock()
    ppp.set_start_of_current_line = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.panes.QTimer", mock_timer):
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
    ppp.process.read.return_value = b""
    ppp.read_from_stdout()
    assert ppp.reading_stdout is False


def test_PythonProcessPane_write_to_stdin():
    """
    Ensure input from the user is written to the child process.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.write_to_stdin(b"hello")
    ppp.process.write.assert_called_once_with(b"hello")


def test_PythonProcessPane_append():
    """
    Ensure the referenced byte_stream is added to the textual content of the
    QTextEdit.
    """
    ppp = mu.interface.panes.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.append(b"hello")
    mock_cursor.insertText.assert_called_once_with("hello")
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
    ppp.insert(b"hello")
    mock_cursor.movePosition.assert_called_once_with(QTextCursor.End)
    mock_cursor.insertText.assert_called_once_with("hello")


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
    ppp.insert(b"hello")
    assert mock_cursor.movePosition.call_count == 0
    mock_cursor.insertText.assert_called_once_with("hello")


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
    ppp.toPlainText = mock.MagicMock(return_value="hello")
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
    ppp.replace_input_line("hello")
    ppp.clear_input_line.assert_called_once_with()
    ppp.append.assert_called_once_with("hello")


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
    ppp.set_zoom("xl")
    expected = mu.interface.panes.PANE_ZOOM_SIZES["xl"]
    ppp.set_font_size.assert_called_once_with(expected)


def test_PythonProcessPane_set_theme():
    """
    Setting the theme shouldn't do anything
    """
    ppp = mu.interface.panes.PythonProcessPane()
    ppp.set_theme("test")


def test_DebugInspectorItem():
    item = mu.interface.panes.DebugInspectorItem("test")
    assert item.text() == "test"
    assert not item.isEditable()


def test_DebugInspector_set_font_size():
    """
    Check the correct stylesheet values are being set.
    """
    di = mu.interface.panes.DebugInspector()
    di.setStyleSheet = mock.MagicMock()
    di.set_font_size(16)
    style = di.setStyleSheet.call_args[0][0]
    assert "font-size: 16pt;" in style
    assert "font-family: Monospace;" in style


def test_DebugInspector_set_zoom():
    """
    Ensure the expected point size is set from the given "t-shirt" size.
    """
    di = mu.interface.panes.DebugInspector()
    di.set_font_size = mock.MagicMock()
    di.set_zoom("xl")
    expected = mu.interface.panes.PANE_ZOOM_SIZES["xl"]
    di.set_font_size.assert_called_once_with(expected)


def test_DebugInspector_set_theme():
    """
    Setting the theme shouldn't do anything
    """
    di = mu.interface.panes.DebugInspector()
    di.set_theme("test")


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
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
    assert isinstance(pp.series[0], mu.interface.panes.QLineSeries)
    assert isinstance(pp.chart, mu.interface.panes.QChart)
    assert isinstance(pp.axis_x, mu.interface.panes.QValueAxis)
    assert isinstance(pp.axis_y, mu.interface.panes.QValueAxis)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_process_tty_data():
    """
    If a byte representation of a Python tuple containing numeric values,
    starting at the beginning of a new line and terminating with a new line is
    received, then the add_data method is called with the resulting Python
    tuple.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.add_data = mock.MagicMock()
    pp.process_tty_data(b"(1, 2.3, 4)\r\n")
    pp.add_data.assert_called_once_with((1, 2.3, 4))


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_process_tty_data_guards_against_data_flood():
    """
    If the process_tty_data method gets data of more than 1024 bytes
    then trigger a data_flood signal and ensure the plotter no longer
    processes incoming bytes.

    (The assumption is that Mu will clean up once the data_flood signal is
    emitted.)

    """
    pp = mu.interface.panes.PlotterPane()
    pp.data_flood = mock.MagicMock()
    pp.add_data = mock.MagicMock()
    data_flood = b"X" * 1025
    pp.process_tty_data(data_flood)
    assert pp.flooded is True
    pp.data_flood.emit.assert_called_once_with()
    assert pp.add_data.call_count == 0
    pp.process_tty_data(data_flood)
    assert pp.add_data.call_count == 0


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_process_tty_data_tuple_not_numeric():
    """
    If a byte representation of a tuple is received but it doesn't contain
    numeric values, then the add_data method MUST NOT be called.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.add_data = mock.MagicMock()
    pp.process_tty_data(b'("a", "b", "c")\r\n')
    assert pp.add_data.call_count == 0


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_process_tty_data_overrun_input_buffer():
    """
    If the incoming bytes are not complete, ensure the input_buffer caches them
    until the newline is detected.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.add_data = mock.MagicMock()
    pp.process_tty_data(b"(1, 2.3, 4)\r\n")
    pp.add_data.assert_called_once_with((1, 2.3, 4))
    pp.add_data.reset_mock()
    pp.process_tty_data(b"(1, 2.")
    assert pp.add_data.call_count == 0
    pp.process_tty_data(b"3, 4)\r\n")
    pp.add_data.assert_called_once_with((1, 2.3, 4))
    pp.add_data.reset_mock()
    pp.process_tty_data(b"(1, 2.3, 4)\r\n")
    pp.add_data.assert_called_once_with((1, 2.3, 4))


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_add_data():
    """
    Given a tuple with a single value, ensure it is logged and correctly added
    to the chart.
    """
    pp = mu.interface.panes.PlotterPane()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((1,))
    assert (1,) in pp.raw_data
    mock_line_series.clear.assert_called_once_with()
    mock_line_series.append.call_args_list[0][0] == (0, 1)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_add_data_adjust_values_up():
    """
    If more values than have been encountered before are added to the incoming
    data then increase the number of QLineSeries instances.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.series = [mock.MagicMock()]
    pp.chart = mock.MagicMock()
    with mock.patch("mu.interface.panes.QLineSeries"):
        pp.add_data((1, 2, 3, 4))
    assert len(pp.series) == 4
    assert pp.chart.addSeries.call_count == 3
    assert pp.chart.setAxisX.call_count == 3
    assert pp.chart.setAxisY.call_count == 3
    assert len(pp.data) == 4


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
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
    with mock.patch("mu.interface.panes.QLineSeries"):
        pp.add_data((1,))
    assert len(pp.series) == 1
    assert len(pp.data) == 1
    assert pp.chart.removeSeries.call_count == 2


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_add_data_re_scale_up():
    """
    If the y axis contains data greater than the current range, then ensure
    the range is doubled.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((1001,))
    assert pp.max_y == 2000
    pp.axis_y.setRange.assert_called_once_with(0, 2000)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_add_data_re_scale_down():
    """
    If the y axis contains data less than half of the current range, then
    ensure the range is halved.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.max_y = 4000
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((1999,))
    assert pp.max_y == 2000
    pp.axis_y.setRange.assert_called_once_with(0, 2000)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_add_data_re_scale_min_up():
    """
    If the y axis contains (negative) data smaller than the current
    minimum, then ensure the negative range is doubled.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((-1001,))
    assert pp.min_y == -2000
    pp.axis_y.setRange.assert_called_once_with(-2000, 0)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_add_data_re_scale_min_down():
    """
    If the y axis contains (negative) data less than half of the
    current minimum, then ensure the negative range is halved.

    """
    pp = mu.interface.panes.PlotterPane()
    pp.min_y = -4000
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((-1999,))
    assert pp.min_y == -2000
    pp.axis_y.setRange.assert_called_once_with(-2000, 0)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_set_label_format_to_float_when_range_small():
    """
    If the max_y is 5 or less, make sure the label format is set to being a
    float with two decimal places.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.max_y = 10
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((1,))
    assert pp.max_y == 1
    pp.axis_y.setRange.assert_called_once_with(0, 1)
    pp.axis_y.setLabelFormat.assert_called_once_with("%2.2f")


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_set_label_format_to_int_when_range_large():
    """
    If the max_y is 5 or less, make sure the label format is set to being a
    float with two decimal places.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.max_y = 5
    pp.axis_y = mock.MagicMock()
    mock_line_series = mock.MagicMock()
    pp.series = [mock_line_series]
    pp.add_data((20,))
    assert pp.max_y == 25
    pp.axis_y.setRange.assert_called_once_with(0, 25)
    pp.axis_y.setLabelFormat.assert_called_once_with("%d")


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_PlotterPane_set_theme():
    """
    Ensure the themes for the chart relate correctly to the theme names used
    by Mu.
    """
    pp = mu.interface.panes.PlotterPane()
    pp.chart = mock.MagicMock()
    pp.set_theme("day")
    pp.chart.setTheme.assert_called_once_with(
        mu.interface.panes.QChart.ChartThemeLight
    )
    pp.chart.setTheme.reset_mock()
    pp.set_theme("night")
    pp.chart.setTheme.assert_called_once_with(
        mu.interface.panes.QChart.ChartThemeDark
    )
    pp.chart.setTheme.reset_mock()
    pp.set_theme("contrast")
    pp.chart.setTheme.assert_called_once_with(
        mu.interface.panes.QChart.ChartThemeHighContrast
    )
