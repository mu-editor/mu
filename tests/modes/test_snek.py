# -*- coding: utf-8 -*-
"""
Tests for the Snek mode.
"""
import pytest
from mu.logic import Device
from mu.modes.snek import SnekMode
from mu.modes.api import SNEK_APIS
from PyQt5.QtWidgets import QMessageBox
from unittest import mock


@pytest.fixture()
def snek_device():
    return Device(
        0x0403, 0x6001, "COM0", "123456", "Snek", "Snekboard", "snek"
    )


def test_snek_mode():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = SnekMode(editor, view)
    assert am.name == "Snek"
    assert am.description is not None
    assert am.icon == "snek"
    assert am.editor == editor
    assert am.view == view

    actions = am.actions()
    assert 3 <= len(actions) <= 4
    assert actions[0]["name"] == "serial"
    assert actions[0]["handler"] == am.toggle_repl
    assert actions[1]["name"] == "flash"
    assert actions[1]["handler"] == am.put
    assert actions[2]["name"] == "getflash"
    assert actions[2]["handler"] == am.get

    # Sometimes charts just aren't available for testing
    if len(actions) == 4:
        assert actions[3]["name"] == "plotter"
        assert actions[3]["handler"] == am.toggle_plotter
    assert "code" not in am.module_names


def test_snek_mode_no_charts():
    """
    If QCharts is not available, ensure the plotter feature is not available.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = SnekMode(editor, view)
    with mock.patch("mu.modes.snek.CHARTS", False):
        actions = am.actions()
        assert len(actions) == 3
        assert actions[0]["name"] == "serial"
        assert actions[0]["handler"] == am.toggle_repl
        assert actions[1]["name"] == "flash"
        assert actions[1]["handler"] == am.put
        assert actions[2]["name"] == "getflash"
        assert actions[2]["handler"] == am.get


def test_snek_put():
    """
    Put current editor contents to eeprom
    """

    class TestSnekMode(SnekMode):
        def toggle_repl(self, event):
            self.repl = True

    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.text.return_value = "# Write your code here :-)"
    view.current_tab = mock_tab
    view.repl_pane = mock.MagicMock()
    view.repl_pane.send_commands = mock.MagicMock()
    mm = TestSnekMode(editor, view)
    mm.repl = None
    mm.put()
    assert view.repl_pane.send_commands.call_count == 1
    assert (
        view.repl_pane.send_commands.call_args[0][0][0]
        == "eeprom.write()\n"
        + mock_tab.text.return_value
        + "\n"
        + "\x04reset()\n"
    )


def test_snek_put_empty():
    """
    Put empty editor contents to eeprom
    """

    class TestSnekMode(SnekMode):
        def toggle_repl(self, event):
            self.repl = True

    editor = mock.MagicMock()
    view = mock.MagicMock()
    mock_tab = mock.MagicMock()
    mock_tab.text.return_value = ""
    view.current_tab = mock_tab
    view.repl_pane = mock.MagicMock()
    view.repl_pane.send_commands = mock.MagicMock()
    print("send commands mock is %r" % view.repl_pane.send_commands)
    mm = TestSnekMode(editor, view)
    mm.repl = None
    mm.put()
    assert view.repl_pane.send_commands.call_count == 1
    assert (
        view.repl_pane.send_commands.call_args[0][0][0]
        == "eeprom.write()\n"
        + mock_tab.text.return_value
        + "\n"
        + "\x04reset()\n"
    )


def test_snek_put_none():
    """
    Put current editor contents to eeprom
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    view.repl_pane = mock.MagicMock()
    view.repl_pane.send_commands = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = SnekMode(editor, view)
    mm.put()
    assert view.repl_pane.send_commands.call_count == 0


mm = None


def set_snek_repl(*args, **kwargs):
    mm.repl = True


def test_snek_get_new():
    """
    Get current editor contents to eeprom
    """
    global mm
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.repl_pane = mock.MagicMock()
    view.repl_pane.send_commands = mock.MagicMock()
    view.widgets = ()
    view.add_tab = mock.MagicMock()
    mm = SnekMode(editor, view)
    mm.repl = False
    mm.toggle_repl = mock.MagicMock()
    mm.toggle_repl.side_effect = set_snek_repl
    mm.get()
    assert mm.toggle_repl.call_count == 1
    assert view.repl_pane.send_commands.call_count == 1
    mm.recv_text("hello")
    assert view.add_tab.call_count == 1


def test_snek_get_existing():
    """
    Get current editor contents to eeprom
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    tab = mock.MagicMock()
    tab.path = None
    tab.setText = mock.MagicMock()
    tab.setModified(False)
    view.repl_pane = mock.MagicMock()
    view.repl_pane.send_commands = mock.MagicMock()
    view.widgets = (tab,)
    mm = SnekMode(editor, view)
    mm.repl = True
    mm.get()
    assert view.repl_pane.send_commands.call_count == 1
    mm.recv_text("hello")
    assert tab.setText.call_count == 1


def test_snek_get_existing_modified():
    """
    Get current editor contents into a modified buffer from eeprom
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    tab = mock.MagicMock()
    tab.path = None
    tab.setText = mock.MagicMock()
    tab.isModified.return_value = True

    mock_window = mock.MagicMock()
    mock_window.show_confirmation = mock.MagicMock(
        return_value=QMessageBox.Cancel
    )
    tab.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    view.repl_pane = mock.MagicMock()
    view.repl_pane.send_commands = mock.MagicMock()
    view.widgets = (tab,)
    mm = SnekMode(editor, view)
    mm.repl = True
    mm.get()
    assert mock_window.show_confirmation.call_count == 1
    assert view.repl_pane.send_commands.call_count == 0


def test_api():
    """
    Ensure the correct API definitions are returned.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    am = SnekMode(editor, view)
    assert am.api() == SNEK_APIS


def test_snek_mode_add_repl_no_port():
    """
    If it's not possible to find a connected snek device then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    editor.current_device = None
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = SnekMode(editor, view)
    mm.add_repl()
    assert view.show_message.call_count == 1
    message = "Could not find an attached device."
    assert view.show_message.call_args[0][0] == message


def test_snek_mode_add_repl_ioerror(snek_device):
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    editor.current_device = snek_device
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError("Cannot connect to device on port COM0")
    mm = SnekMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_repl_connection.open = mock.MagicMock(side_effect=ex)
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.snek.SnekREPLConnection", mock_connection_class):
        mm.add_repl()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_snek_mode_add_repl_exception(snek_device):
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    editor.current_device = snek_device
    view = mock.MagicMock()
    ex = Exception("BOOM")
    mm = SnekMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_repl_connection.open = mock.MagicMock(side_effect=ex)
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.snek.logger", return_value=None) as logger:
        with mock.patch(
            "mu.modes.snek.SnekREPLConnection", mock_connection_class
        ):
            mm.add_repl()
            logger.error.assert_called_once_with(ex)


def test_snek_mode_add_repl(snek_device):
    """
    Nothing goes wrong so check the _view.add_snek_repl gets the
    expected argument.
    """
    editor = mock.MagicMock()
    editor.current_device = snek_device
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_snek_repl = mock.MagicMock()
    mm = SnekMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.snek.SnekREPLConnection", mock_connection_class):
        mm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_snek_repl.call_args[0][1] == mock_repl_connection
    mock_repl_connection.send_interrupt.assert_called_once_with()


def test_snek_mode_add_repl_no_force_interrupt(snek_device):
    """
    Nothing goes wrong so check the _view.add_snek_repl gets the
    expected arguments (including the flag so no keyboard interrupt is called).
    """
    editor = mock.MagicMock()
    editor.current_device = snek_device
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_snek_repl = mock.MagicMock()
    mm = SnekMode(editor, view)
    mm.force_interrupt = False
    mock_repl_connection = mock.MagicMock()
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.snek.SnekREPLConnection", mock_connection_class):
        mm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_snek_repl.call_args[0][1] == mock_repl_connection
    assert mock_repl_connection.send_interrupt.call_count == 0


def test_snek_stop(snek_device):
    """
    Ensure that this method, called when Mu is quitting, shuts down
    the serial port.
    """
    editor = mock.MagicMock()
    editor.current_device = snek_device
    view = mock.MagicMock()
    mm = SnekMode(editor, view)
    view.remove_repl = mock.MagicMock()
    mm.stop()
    view.remove_repl.assert_called_once_with()


def test_device_changed(snek_device):
    """
    Ensure REPL pane is updated, when the user changes
    device.
    """
    view = mock.MagicMock()
    editor = mock.MagicMock()
    mm = SnekMode(editor, view)
    mm.repl = mock.MagicMock()
    mm.add_repl = mock.MagicMock()
    mm.remove_repl = mock.MagicMock()
    mm.plotter = mock.MagicMock()
    mm.add_plotter = mock.MagicMock()
    mm.remove_plotter = mock.MagicMock()
    mm.connection = mock.MagicMock()
    mm.device_changed(snek_device)
    mm.remove_repl.assert_called_once_with()
    mm.add_repl.assert_called_once_with()
    mm.remove_plotter.assert_called_once_with()
    mm.add_plotter.assert_called_once_with()
    mm.connection.send_interrupt.assert_called_once_with()
