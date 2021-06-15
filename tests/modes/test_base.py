# -*- coding: utf-8 -*-
"""
Tests for the BaseMode class.
"""
import os
import mu
import pytest
import mu.config
from mu.logic import Device
from mu.modes.base import (
    BaseMode,
    MicroPythonMode,
    FileManager,
    REPLConnection,
)
import mu.settings
from PyQt5.QtCore import QIODevice
from unittest import mock


@pytest.fixture()
def microbit():
    return Device(
        0x0D28, 0x0204, "COM0", "123456", "ARM", "BBC micro:bit", "microbit"
    )


def test_base_mode():
    """
    Sanity check for the parent class of all modes.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    assert bm.name == "UNNAMED MODE"
    assert bm.short_name == "UNDEFINED_MODE"
    assert bm.description == "DESCRIPTION NOT AVAILABLE."
    assert bm.icon == "help"
    assert bm.is_debugger is False
    assert bm.editor == editor
    assert bm.view == view
    assert bm.stop() is None
    assert bm.actions() == NotImplemented
    assert bm.workspace_dir()
    assert bm.api() == NotImplemented
    assert bm.builtins is None


@pytest.mark.skip(
    "No longer needed now that settings are part of the settings module"
)
def test_base_mode_workspace_dir():
    """
    Return settings file workspace value.
    """
    # read from our demo settings.json
    with mock.patch(
        "mu.modes.base.get_settings_path", return_value="tests/settings.json"
    ), mock.patch("os.path.isdir", return_value=True):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == "/home/foo/mycode"


def test_base_mode_workspace_not_present():
    """
    No workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(
        mu.config.HOME_DIRECTORY, mu.config.WORKSPACE_NAME
    )
    mocked_settings = mu.settings.UserSettings()
    del mocked_settings["workspace"]
    assert "workspace" not in mocked_settings
    with mock.patch.object(mu.settings, "settings", mocked_settings):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace


def test_base_mode_workspace_invalid_value():
    """
    Invalid workspace key in settings file, return default folder.
    """
    default_workspace = os.path.join(
        mu.config.HOME_DIRECTORY, mu.config.WORKSPACE_NAME
    )
    mocked_settings = mu.settings.UserSettings()
    mocked_settings["workspace"] = "*invalid*"
    with mock.patch.object(
        mu.settings, "settings", mocked_settings
    ), mock.patch("mu.modes.base.logger", return_value=None) as logger:
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace
        assert logger.warning.call_count == 1


def test_base_mode_workspace_invalid_json(tmp_path):
    """
    Invalid workspace key in settings file, return default folder.

    NB most of the work here is done in the settings.py module so we're
    just testing that we get a suitable default back
    """
    default_workspace = os.path.join(
        mu.config.HOME_DIRECTORY, mu.config.WORKSPACE_NAME
    )
    mocked_settings = mu.settings.UserSettings()
    settings_filepath = os.path.join(str(tmp_path), "settings.json")
    with open(settings_filepath, "w") as f:
        f.write("*invalid JSON*")
    mocked_settings.load(settings_filepath)
    with mock.patch.object(mu.settings, "settings", mocked_settings):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace


def test_base_mode_workspace_no_settings_file():
    """
    Invalid settings file, return default folder.

    NB most of the work here is done in the settings.py module so we're
    just testing that we get a suitable default back
    """
    default_workspace = os.path.join(
        mu.config.HOME_DIRECTORY, mu.config.WORKSPACE_NAME
    )
    mocked_settings = mu.settings.UserSettings()
    with mock.patch.object(mu.settings, "settings", mocked_settings):
        editor = mock.MagicMock()
        view = mock.MagicMock()
        bm = BaseMode(editor, view)
        assert bm.workspace_dir() == default_workspace


def test_base_mode_set_buttons():
    """
    Ensure only buttons for existing actions have their "Enabled" states
    updates.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.button_bar.slots = {"foo": mock.MagicMock(), "bar": mock.MagicMock()}
    bm = BaseMode(editor, view)
    bm.set_buttons(foo=True, bar=False, baz=True)
    view.button_bar.slots["foo"].setEnabled.assert_called_once_with(True)
    view.button_bar.slots["bar"].setEnabled.assert_called_once_with(False)
    assert "baz" not in view.button_bar.slots


def test_base_mode_add_plotter():
    """
    Ensure the child classes need to implement this.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    assert bm.add_plotter() == NotImplemented


def test_base_mode_remove_plotter():
    """
    Ensure the plotter is removed and data is saved as a CSV file in the
    expected directory.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.plotter_pane.raw_data = [1, 2, 3]
    bm = BaseMode(editor, view)
    bm.plotter = mock.MagicMock()
    mock_mkdir = mock.MagicMock()
    mock_open = mock.mock_open()
    mock_csv_writer = mock.MagicMock()
    mock_csv = mock.MagicMock()
    mock_csv.writer.return_value = mock_csv_writer
    with mock.patch(
        "mu.modes.base.os.path.exists", return_value=False
    ), mock.patch("mu.modes.base.os.makedirs", mock_mkdir), mock.patch(
        "builtins.open", mock_open
    ), mock.patch(
        "mu.modes.base.csv", mock_csv
    ):
        bm.remove_plotter()
    assert bm.plotter is False
    view.remove_plotter.assert_called_once_with()
    dd = os.path.join(bm.workspace_dir(), "data_capture")
    mock_mkdir.assert_called_once_with(dd)
    mock_csv_writer.writerows.assert_called_once_with(
        view.plotter_pane.raw_data
    )


def test_base_mode_write_csv(tmp_path):
    """When the plotter is removed the resulting csv should represent
    the data -- an should not not include interspersed blank lines
    """
    csv_filepath = str(tmp_path / "plotter.csv")
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.plotter_pane.raw_data = [[1, 2, 3], [4, 5, 6]]
    bm = BaseMode(editor, view)
    bm.write_plotter_data_to_csv(csv_filepath)

    expected_output = ["1,2,3", "4,5,6"]
    with open(csv_filepath, "r") as f:
        output = f.read().splitlines()
    assert output == expected_output


def test_base_on_data_flood():
    """
    Ensure the plotter is removed and a helpful message is displayed to the
    user.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    bm.on_data_flood()
    view.remove_plotter.assert_called_once_with()
    assert view.show_message.call_count == 1


def test_base_mode_open_file():
    """
    Ensure the the base class returns None to indicate it can't open the file.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    text, newline = bm.open_file("unused/path")
    assert text is None
    assert newline is None


def test_base_mode_activate_deactivate_change(microbit):
    """
    Dummy test of no-operation base methods only meant for overriding.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    bm = BaseMode(editor, view)
    bm.activate()
    bm.deactivate()
    bm.device_changed(microbit)


# TODO Avoid using BOARD_IDS from base.py (which is only ever used in
# this test)
def test_micropython_mode_find_device():
    """
    Ensure it's possible to detect a device and return the expected port.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_port = mock.MagicMock()
    for vid, pid, manufacturer, board_name in mm.valid_boards:
        mock_port.vid = vid
        mock_port.productIdentifier = mock.MagicMock(return_value=pid)
        mock_port.vendorIdentifier = mock.MagicMock(return_value=vid)
        mock_port.manufacturer = mock.MagicMock(return_value=manufacturer)
        mock_port.portName = mock.MagicMock(return_value="COM0")
        mock_port.serialNumber = mock.MagicMock(return_value="12345")
        mock_os = mock.MagicMock()
        mock_os.name = "nt"
        mock_sys = mock.MagicMock()
        mock_sys.platform = "win32"
        device = Device(
            mock_port.vendorIdentifier(),
            mock_port.productIdentifier(),
            mock_port.portName(),
            mock_port.serialNumber(),
            "micro:bit",
            board_name,
            None,
        )
        with mock.patch(
            "mu.modes.base.QSerialPortInfo.availablePorts",
            return_value=[mock_port],
        ), mock.patch("mu.modes.base.os", mock_os), mock.patch(
            "mu.modes.base.sys", mock_sys
        ):
            assert mm.find_devices() == [device]


def test_micropython_mode_find_device_no_ports():
    """
    There are no connected devices so return None.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch(
        "mu.modes.base.QSerialPortInfo.availablePorts", return_value=[]
    ):
        assert mm.find_devices() == []


def test_micropython_mode_find_device_but_no_device():
    """
    None of the connected devices is a valid board so return None.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_port = mock.MagicMock()
    mock_port.productIdentifier = mock.MagicMock(return_value=666)
    mock_port.vendorIdentifier = mock.MagicMock(return_value=999)
    mock_port.serialNumber = mock.MagicMock(return_value="123456")
    with mock.patch(
        "mu.modes.base.QSerialPortInfo.availablePorts",
        return_value=[mock_port],
    ):
        assert mm.find_devices() == []


def test_micropython_mode_find_device_darwin_remove_extraneous_devices():
    """
    Check that if on OS X, only one version of the same device is shown,
    as OS X shows every device on two different ports.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.valid_boards = [(0x0D28, 0x0204, None, "micro:bit")]
    mock_port = mock.MagicMock()
    mock_port.portName = mock.MagicMock(return_value="tty.usbserial-XXX")
    mock_port.productIdentifier = mock.MagicMock(return_value=0x0204)
    mock_port.vendorIdentifier = mock.MagicMock(return_value=0x0D28)
    mock_port.serialNumber = mock.MagicMock(return_value="123456")
    mock_port2 = mock.MagicMock()
    mock_port2.portName = mock.MagicMock(return_value="cu.usbserial-XXX")
    mock_port2.productIdentifier = mock.MagicMock(return_value=0x0204)
    mock_port2.vendorIdentifier = mock.MagicMock(return_value=0x0D28)
    mock_port2.serialNumber = mock.MagicMock(return_value="123456")
    device = Device(
        mock_port2.vendorIdentifier(),
        mock_port2.productIdentifier(),
        "/dev/" + mock_port2.portName(),
        mock_port2.serialNumber(),
        "ARM",
        "BBC micro:bit",
        "microbit",
        None,
    )
    with mock.patch("sys.platform", "darwin"), mock.patch(
        "os.name", "posix"
    ), mock.patch(
        "mu.modes.base.QSerialPortInfo.availablePorts",
        return_value=[mock_port, mock_port2],
    ):
        assert mm.find_devices() == [device]


def test_micropython_mode_port_path_posix():
    """
    Ensure the correct path for a port_name is returned if the platform is
    posix.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch("os.name", "posix"):
        assert mm.port_path("tty1") == "/dev/tty1"


def test_micropython_mode_port_path_nt():
    """
    Ensure the correct path for a port_name is returned if the platform is
    nt.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch("os.name", "nt"):
        assert mm.port_path("COM0") == "COM0"


def test_micropython_mode_port_path_unknown():
    """
    If the platform is unknown, raise NotImplementedError.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    with mock.patch("os.name", "foo"):
        with pytest.raises(NotImplementedError):
            mm.port_path("bar")


def test_micropython_mode_add_repl_no_port():
    """
    If it's not possible to find a connected micro:bit then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    editor.current_device = None
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_repl()
    assert view.show_message.call_count == 1
    message = "Could not find an attached device."
    assert view.show_message.call_args[0][0] == message


def test_micropython_mode_add_repl_ioerror(microbit):
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError("BOOM")
    mm = MicroPythonMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_repl_connection.open = mock.MagicMock(side_effect=ex)
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
        mm.add_repl()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_micropython_mode_add_repl_exception(microbit):
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    ex = Exception("BOOM")
    mm = MicroPythonMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_repl_connection.open = mock.MagicMock(side_effect=ex)
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.logger", return_value=None) as logger:
        with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
            mm.add_repl()
            logger.error.assert_called_once_with(ex)


def test_micropython_mode_add_repl(microbit):
    """
    Nothing goes wrong so check the _view.add_micropython_repl gets the
    expected argument.
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_micropython_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
        mm.add_repl()
    assert view.show_message.call_count == 0
    assert view.add_micropython_repl.call_args[0][1] == mock_repl_connection
    mock_repl_connection.send_interrupt.assert_called_once_with()


def test_micropython_mode_add_repl_no_force_interrupt(microbit):
    """
    Nothing goes wrong so check the _view.add_micropython_repl gets the
    expected arguments (including the flag so no keyboard interrupt
    is called).
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.force_interrupt = False
    mock_repl_connection = mock.MagicMock()
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
        mm.add_repl()
    view.show_message.assert_not_called()
    mock_repl_connection.send_interrupt.assert_not_called()


def test_micropython_mode_remove_repl():
    """
    If there is a repl, make sure it's removed as expected and the state is
    updated.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.remove_repl = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = True
    mm.remove_repl()
    assert view.remove_repl.call_count == 1
    assert mm.repl is False


def test_micropython_mode_remove_repl_and_disconnect():
    """
    If there is a repl, make sure it's removed as expected and the state is
    updated. Disconnect any open serial connection.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = True
    mm.plotter = False
    mock_repl_connection = mock.MagicMock()
    mm.connection = mock_repl_connection
    mm.remove_repl()
    mock_repl_connection.close.assert_called_once_with()
    assert mm.connection is None


def test_micropython_mode_remove_plotter_disconnects():
    """
    Ensure that connections are closed when plotter is closed.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.repl = False
    mm.plotter = True
    mock_repl_connection = mock.MagicMock()
    mm.connection = mock_repl_connection
    mm.remove_plotter()
    mock_repl_connection.close.assert_called_once_with()
    assert mm.connection is None


def test_micropython_mode_remove_repl_active_plotter():
    """
    When removing the repl, if the plotter is active, retain the
    connection.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.connection = mock.MagicMock()
    mm.plotter = True
    mm.remove_repl()
    assert mm.repl is False
    assert mm.connection is not None


def test_micropython_mode_remove_plotter_active_repl():
    """
    When removing the plotter, if the repl is active, retain the
    connection.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.connection = mock.MagicMock()
    mm.repl = True
    mm.remove_plotter()
    assert mm.plotter is False
    assert mm.connection is not None


def test_micropython_mode_toggle_repl_on():
    """
    There is no repl, so toggle on.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_repl = mock.MagicMock()
    mm.repl = None
    mm.toggle_repl(None)
    assert mm.add_repl.call_count == 1


def test_micropython_mode_toggle_repl_off():
    """
    There is a repl, so toggle off.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    mm.repl = True
    mm.toggle_repl(None)
    assert mm.remove_repl.call_count == 1


def test_micropython_mode_toggle_plotter_on():
    """
    There is no plotter, so toggle on.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_plotter = mock.MagicMock()
    mm.plotter = None
    mm.toggle_plotter(None)
    assert mm.add_plotter.call_count == 1


def test_micropython_mode_toggle_plotter_off():
    """
    There is a plotter, so toggle off.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_plotter = mock.MagicMock()
    mm.plotter = True
    mm.toggle_plotter(None)
    assert mm.remove_plotter.call_count == 1


def test_micropython_mode_add_plotter_no_port():
    """
    If it's not possible to find a connected micro:bit then ensure a helpful
    message is enacted.
    """
    editor = mock.MagicMock()
    editor.current_device = None
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_plotter()
    assert view.show_message.call_count == 1
    message = "Could not find an attached device."
    assert view.show_message.call_args[0][0] == message


def test_micropython_mode_add_plotter_ioerror(microbit):
    """
    Sometimes when attempting to connect to the device there is an IOError
    because it's still booting up or connecting to the host computer. In this
    case, ensure a useful message is displayed.
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    ex = IOError("BOOM")
    mm = MicroPythonMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_repl_connection.open = mock.MagicMock(side_effect=ex)
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
        mm.add_plotter()
    assert view.show_message.call_count == 1
    assert view.show_message.call_args[0][0] == str(ex)


def test_micropython_mode_add_plotter_exception(microbit):
    """
    Ensure that any non-IOError based exceptions are logged.
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    ex = Exception("BOOM")
    mm = MicroPythonMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_repl_connection.open = mock.MagicMock(side_effect=ex)
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.logger", return_value=None) as logger:
        with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
            mm.add_plotter()
            logger.error.assert_called_once_with(ex)


def test_micropython_mode_add_plotter(microbit):
    """
    Nothing goes wrong so check the _view.add_micropython_plotter gets the
    expected argument.
    """
    editor = mock.MagicMock()
    editor.current_device = microbit
    view = mock.MagicMock()
    view.show_message = mock.MagicMock()
    view.add_micropython_plotter = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mock_repl_connection = mock.MagicMock()
    mock_connection_class = mock.MagicMock(return_value=mock_repl_connection)
    with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
        mm.add_plotter()
    view.show_message.assert_not_called()
    assert view.add_micropython_plotter.call_args[0][1] == mock_repl_connection
    mock_repl_connection.open.assert_called_once_with()


def test_micropython_on_data_flood():
    """
    Ensure that the REPL is removed before calling the base on_data_flood
    method.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    with mock.patch("builtins.super") as mock_super:
        mm.on_data_flood()
        mm.remove_repl.assert_called_once_with()
        mock_super().on_data_flood.assert_called_once_with()


def test_micropython_activate():
    """
    Ensure the device selector is shown when MicroPython-mode is activated.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_device_selector = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.activate()
    view.show_device_selector.assert_called_once_with()


def test_micropython_deactivate():
    """
    Ensure REPL/Plotter and device_selector is hidden, when
    MicroPython-mode is deactivated.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_device_selector = mock.MagicMock()
    view.hide_device_selector = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.remove_repl = mock.MagicMock()
    mm.remove_plotter = mock.MagicMock()
    mm.activate()
    mm.repl = True
    mm.plotter = True
    mm.deactivate()
    view.hide_device_selector.assert_called_once_with()
    mm.remove_repl.assert_called_once_with()
    mm.remove_plotter.assert_called_once_with()


def test_micropython_device_changed(microbit):
    """
    Ensure REPL/Plotter and connection are reconnected, when the
    user changes device.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.show_device_selector = mock.MagicMock()
    view.hide_device_selector = mock.MagicMock()
    mm = MicroPythonMode(editor, view)
    mm.add_repl = mock.MagicMock()
    mm.add_plotter = mock.MagicMock()
    mm.remove_repl = mock.MagicMock()
    mm.remove_plotter = mock.MagicMock()
    mm.repl = True
    mm.plotter = True
    mm.connection = mock.MagicMock()
    mm.activate()
    mm.device_changed(microbit)
    mm.add_repl.assert_called_once_with()
    mm.add_plotter.assert_called_once_with()
    mm.remove_repl.assert_called_once_with()
    mm.remove_plotter.assert_called_once_with()
    mm.connection.send_interrupt.assert_called_once_with()


def test_FileManager_on_start():

    """
    When a thread signals it has started, create a serial connection and then
    list the files.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.ls = mock.MagicMock()
    with mock.patch("mu.modes.base.Serial") as mock_serial:
        fm.on_start()
        mock_serial.assert_called_once_with(
            "/dev/ttyUSB0", 115200, timeout=2, parity="N"
        )
    fm.ls.assert_called_once_with()


def test_FileManager_on_start_fails():
    """
    When a thread signals it has started, but the serial connection cannot be
    established, ensure that the on_list_fail is emitted to signal Mu can't get
    the list of files from the board (because a connection cannot be
    established).
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.on_list_fail = mock.MagicMock()
    mock_serial = mock.MagicMock(side_effect=Exception("BOOM!"))
    with mock.patch("mu.modes.base.Serial", mock_serial):
        fm.on_start()
        mock_serial.assert_called_once_with(
            "/dev/ttyUSB0", 115200, timeout=2, parity="N"
        )
    fm.on_list_fail.emit.assert_called_once_with()


def test_FileManager_ls():
    """
    The on_list_files signal is emitted with a tuple of files when microfs.ls
    completes successfully.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.serial = mock.MagicMock()
    fm.on_list_files = mock.MagicMock()
    mock_ls = mock.MagicMock(return_value=["foo.py", "bar.py"])
    with mock.patch("mu.modes.base.microfs.ls", mock_ls):
        fm.ls()
    fm.on_list_files.emit.assert_called_once_with(("foo.py", "bar.py"))


def test_FileManager_ls_fail():
    """
    The on_list_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.on_list_fail = mock.MagicMock()
    with mock.patch("mu.modes.base.microfs.ls", side_effect=Exception("boom")):
        fm.ls()
    fm.on_list_fail.emit.assert_called_once_with()


def test_fileManager_get():
    """
    The on_get_file signal is emitted with the name of the effected file when
    microfs.get completes successfully.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.serial = mock.MagicMock()
    fm.on_get_file = mock.MagicMock()
    mock_get = mock.MagicMock()
    with mock.patch("mu.modes.base.microfs.get", mock_get):
        fm.get("foo.py", "bar.py")
    mock_get.assert_called_once_with("foo.py", "bar.py", serial=fm.serial)
    fm.on_get_file.emit.assert_called_once_with("foo.py")


def test_FileManager_get_fail():
    """
    The on_get_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.on_get_fail = mock.MagicMock()
    with mock.patch(
        "mu.modes.base.microfs.get", side_effect=Exception("boom")
    ):
        fm.get("foo.py", "bar.py")
    fm.on_get_fail.emit.assert_called_once_with("foo.py")


def test_FileManager_put():
    """
    The on_put_file signal is emitted with the name of the effected file when
    microfs.put completes successfully.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.serial = mock.MagicMock()
    fm.on_put_file = mock.MagicMock()
    mock_put = mock.MagicMock()
    path = os.path.join("directory", "foo.py")
    with mock.patch("mu.modes.base.microfs.put", mock_put):
        fm.put(path)
    mock_put.assert_called_once_with(path, target=None, serial=fm.serial)
    fm.on_put_file.emit.assert_called_once_with("foo.py")


def test_FileManager_put_fail():
    """
    The on_put_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.on_put_fail = mock.MagicMock()
    with mock.patch(
        "mu.modes.base.microfs.put", side_effect=Exception("boom")
    ):
        fm.put("foo.py")
    fm.on_put_fail.emit.assert_called_once_with("foo.py")


def test_FileManager_delete():
    """
    The on_delete_file signal is emitted with the name of the effected file
    when microfs.rm completes successfully.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.serial = mock.MagicMock()
    fm.on_delete_file = mock.MagicMock()
    mock_rm = mock.MagicMock()
    with mock.patch("mu.modes.base.microfs.rm", mock_rm):
        fm.delete("foo.py")
    mock_rm.assert_called_once_with("foo.py", serial=fm.serial)
    fm.on_delete_file.emit.assert_called_once_with("foo.py")


def test_FileManager_delete_fail():
    """
    The on_delete_fail signal is emitted when a problem is encountered.
    """
    fm = FileManager("/dev/ttyUSB0")
    fm.on_delete_fail = mock.MagicMock()
    with mock.patch("mu.modes.base.microfs.rm", side_effect=Exception("boom")):
        fm.delete("foo.py")
    fm.on_delete_fail.emit.assert_called_once_with("foo.py")


def test_REPLConnection_init_default_args():
    """
    Ensure the MicroPython REPLConnection object is instantiated as expected.
    """
    mock_serial_class = mock.MagicMock()
    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0", baudrate=9600)

    assert conn.port == "COM0"
    assert conn.baudrate == 9600


def test_REPLConnection_open():
    """
    Ensure the serial port is opened in the expected manner.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0", baudrate=9600)
        conn.open()
    mock_serial.setPortName.assert_called_once_with("COM0")
    mock_serial.setBaudRate.assert_called_once_with(9600)
    mock_serial.open.assert_called_once_with(QIODevice.ReadWrite)
    mock_serial.readyRead.connect.assert_called_once_with(conn._on_serial_read)


def test_REPLConnection_open_unable_to_connect():
    """
    If serial.open fails raise an IOError.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=False)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        with pytest.raises(IOError):
            conn = REPLConnection("COM0")
            conn.open()


def test_REPLConnection_open_DTR_unset():
    """
    If data terminal ready (DTR) is unset (as can be the case on some
    Windows / Qt combinations) then fall back to PySerial to correct. See
    issues #281 and #302 for details.
    """
    # Mock QtSerialPort object
    mock_qt_serial = mock.MagicMock()
    mock_qt_serial.isDataTerminalReady.return_value = False
    mock_qtserial_class = mock.MagicMock(return_value=mock_qt_serial)
    # Mock PySerial object
    mock_Serial = mock.MagicMock()
    mock_pyserial_class = mock.MagicMock(return_value=mock_Serial)
    with mock.patch("mu.modes.base.QSerialPort", mock_qtserial_class):
        with mock.patch("mu.modes.base.Serial", mock_pyserial_class):
            conn = REPLConnection("COM0")
            conn.open()

    # Check that Qt serial is opened twice
    mock_qt_serial.close.assert_called_once_with()
    assert mock_qt_serial.open.call_count == 2

    # Check that DTR is set true with PySerial
    assert mock_Serial.dtr is True
    mock_Serial.close.assert_called_once_with()


def test_REPLConnection_close():
    """
    Ensure the serial link is closed / cleaned up as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial_class = mock.MagicMock(return_value=mock_serial)

    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0")
        conn.open()
        conn.close()

    mock_serial.close.assert_called_once_with()
    assert conn.serial is None
    assert conn.port is None
    assert conn.baudrate is None


def test_REPLConnection_on_serial_read():
    """
    When data is received the data_received signal should emit it.
    """
    mock_serial = mock.MagicMock()
    mock_serial.readAll.return_value = b"Hello"
    mock_serial_class = mock.MagicMock(return_value=mock_serial)

    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0")

    conn.data_received = mock.MagicMock()
    conn._on_serial_read()
    conn.data_received.emit.assert_called_once_with(b"Hello")


def test_REPLConnection_write():
    mock_serial = mock.MagicMock()
    mock_serial_class = mock.MagicMock(return_value=mock_serial)

    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0")
        conn.open()
        conn.write(b"Hello")

    mock_serial.write.assert_called_once_with(b"Hello")


def test_REPLConnection_send_interrupt():
    mock_serial = mock.MagicMock()
    mock_serial_class = mock.MagicMock(return_value=mock_serial)

    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0")
        conn.open()
        conn.send_interrupt()

    mock_serial.write.assert_any_call(b"\x02")  # CTRL-B
    mock_serial.write.assert_any_call(b"\x03")  # CTRL-C


def test_REPLConnection_execute():
    """
    Ensure the first command is sent via serial to the connected device, and
    further commands are scheduled for the future.
    """
    mock_serial_class = mock.MagicMock()
    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0")
        conn.write = mock.MagicMock()

    # Mocks QTimer, so only first command will be sent
    commands = [b"A", b"B"]
    with mock.patch("mu.modes.base.QTimer") as mock_timer:
        conn.execute(commands)
        conn.write.assert_called_once_with(b"A")
        assert mock_timer.singleShot.call_count == 1


def test_REPLConnection_send_commands():
    """
    Ensure the list of commands is correctly encoded and bound by control
    commands to put the board into and out of raw mode.
    """
    mock_serial_class = mock.MagicMock()
    with mock.patch("mu.modes.base.QSerialPort", mock_serial_class):
        conn = REPLConnection("COM0")
        conn.execute = mock.MagicMock()
        commands = ["import os", "print(os.listdir())"]
        conn.send_commands(commands)

    expected = [
        b"\x03",  # Keyboard interrupt
        b"\x03",  # Keyboard interrupt
        b"\x01",  # Put the board into raw mode.
        b"\x04",  # Soft-reboot
        b"\x03",  # Keyboard interrupt
        b"\x03",  # Keyboard interrupt
        b'print("\\n");',  # Ensure a newline at the start of output.
        b"import os\r",  # The commands to run.
        b"print(os.listdir())\r",
        b"\r",  # Ensure newline after commands.
        b"\x04",  # Evaluate the commands.
        b"\x02",  # Leave raw mode.
    ]
    conn.execute.assert_called_once_with(expected)
