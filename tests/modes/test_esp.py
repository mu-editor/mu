# -*- coding: utf-8 -*-
import os
import pytest
from unittest import mock
from mu.modes.esp import ESPMode
from mu.modes.api import ESP_APIS, SHARED_APIS
from mu.logic import Device


@pytest.fixture
def esp_mode():
    editor = mock.MagicMock()
    view = mock.MagicMock()
    esp_mode = ESPMode(editor, view)
    return esp_mode


def test_ESPMode_init():
    """
    Sanity check for setting up the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    esp_mode = ESPMode(editor, view)
    assert esp_mode.name == "ESP MicroPython"
    assert esp_mode.description is not None
    assert esp_mode.icon == "esp"


def test_ESPMode_actions(esp_mode):
    """
    Sanity check for mode actions.
    """
    with mock.patch("mu.modes.esp.CHARTS", True):
        actions = esp_mode.actions()
    assert len(actions) == 4
    assert actions[0]["name"] == "run"
    assert actions[0]["handler"] == esp_mode.run
    assert actions[1]["name"] == "files"
    assert actions[1]["handler"] == esp_mode.toggle_files
    assert actions[2]["name"] == "repl"
    assert actions[2]["handler"] == esp_mode.toggle_repl
    assert actions[3]["name"] == "plotter"
    assert actions[3]["handler"] == esp_mode.toggle_plotter


def test_ESPMode_actions_no_charts(esp_mode):
    """
    Sanity check for mode actions.
    """
    with mock.patch("mu.modes.esp.CHARTS", False):
        actions = esp_mode.actions()
    assert len(actions) == 3
    assert actions[0]["name"] == "run"
    assert actions[0]["handler"] == esp_mode.run
    assert actions[1]["name"] == "files"
    assert actions[1]["handler"] == esp_mode.toggle_files
    assert actions[2]["name"] == "repl"
    assert actions[2]["handler"] == esp_mode.toggle_repl


def test_api(esp_mode):
    """
    Ensure the right thing comes back from the API.
    """
    api = esp_mode.api()
    assert api == SHARED_APIS + ESP_APIS


@mock.patch("mu.modes.esp.QThread")
@mock.patch("mu.modes.esp.FileManager")
def test_add_fs(fm, qthread, esp_mode):
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    esp_mode.view.current_tab = None
    esp_mode.find_device = mock.MagicMock(
        return_value=("COM0", "12345", "ESP8266")
    )
    esp_mode.add_fs()
    workspace = esp_mode.workspace_dir()
    esp_mode.view.add_filesystem.assert_called_once_with(
        workspace, esp_mode.file_manager, "ESP board"
    )
    assert esp_mode.fs


@mock.patch("mu.modes.esp.QThread")
@mock.patch("mu.modes.esp.FileManager")
def test_add_fs_project_path(fm, qthread, esp_mode):
    """
    It's possible to add the file system pane if the REPL is inactive.
    """
    esp_mode.view.current_tab.path = "foo"
    esp_mode.find_device = mock.MagicMock(
        return_value=("COM0", "12345", "ESP8266")
    )
    esp_mode.add_fs()
    workspace = os.path.dirname(os.path.abspath("foo"))
    esp_mode.view.add_filesystem.assert_called_once_with(
        workspace, esp_mode.file_manager, "ESP board"
    )
    assert esp_mode.fs


def test_add_fs_no_device(esp_mode):
    """
    If there's no device attached then ensure a helpful message is displayed.
    """
    esp_mode.editor.current_device = None
    esp_mode.add_fs()
    assert esp_mode.view.show_message.call_count == 1


def test_remove_fs(esp_mode):
    """
    Removing the file system results in the expected state.
    """
    esp_mode.fs = True
    esp_mode.remove_fs()
    assert esp_mode.view.remove_filesystem.call_count == 1
    assert esp_mode.fs is None


def test_toggle_repl_on(esp_mode):
    """
    Ensure the REPL is able to toggle on if there's no file system pane.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.fs = None
    esp_mode.repl = None
    event = mock.Mock()

    def side_effect(*args, **kwargs):
        esp_mode.repl = True

    with mock.patch(
        "mu.modes.esp.MicroPythonMode.toggle_repl", side_effect=side_effect
    ) as super_toggle_repl:
        esp_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    esp_mode.set_buttons.assert_called_once_with(files=False)
    assert esp_mode.repl


@mock.patch("mu.modes.esp.MicroPythonMode.toggle_repl")
def test_toggle_repl_fail(super_toggle_repl, esp_mode):
    """
    Ensure buttons are not disabled if enabling the REPL fails,
    and that the thread lock on file access is released.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.fs = None
    esp_mode.repl = None
    event = mock.Mock()

    esp_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    esp_mode.set_buttons.assert_not_called()
    assert not esp_mode.repl


def test_toggle_repl_off(esp_mode):
    """
    Ensure the file system button is enabled if the repl toggles off.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.fs = None
    esp_mode.repl = True
    event = mock.Mock()

    def side_effect(*args, **kwargs):
        esp_mode.repl = False

    with mock.patch(
        "mu.modes.esp.MicroPythonMode.toggle_repl", side_effect=side_effect
    ) as super_toggle_repl:
        esp_mode.toggle_repl(event)
    super_toggle_repl.assert_called_once_with(event)
    esp_mode.set_buttons.assert_called_once_with(files=True)


def test_toggle_repl_with_fs(esp_mode):
    """
    If the file system is active, show a helpful message instead.
    """
    esp_mode.remove_repl = mock.MagicMock()
    esp_mode.repl = None
    esp_mode.fs = True
    esp_mode.toggle_repl(None)
    assert esp_mode.view.show_message.call_count == 1


def test_toggle_files_on(esp_mode):
    """
    If the fs is off, toggle it on.
    """

    def side_effect(*args, **kwargs):
        esp_mode.fs = True

    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.add_fs = mock.MagicMock(side_effect=side_effect)
    esp_mode.repl = None
    esp_mode.fs = None
    event = mock.Mock()
    esp_mode.toggle_files(event)
    assert esp_mode.add_fs.call_count == 1
    esp_mode.set_buttons.assert_called_once_with(
        run=False, repl=False, plotter=False
    )


def test_toggle_files_off(esp_mode):
    """
    If the fs is on, toggle if off.
    """
    esp_mode.remove_fs = mock.MagicMock()
    esp_mode.repl = None
    esp_mode.fs = True
    event = mock.Mock()
    esp_mode.toggle_files(event)
    assert esp_mode.remove_fs.call_count == 1


def test_toggle_files_with_repl(esp_mode):
    """
    If the REPL is active, ensure a helpful message is displayed.
    """
    esp_mode.add_repl = mock.MagicMock()
    esp_mode.repl = True
    esp_mode.fs = None
    event = mock.Mock()
    esp_mode.toggle_files(event)
    assert esp_mode.view.show_message.call_count == 1


def test_run_no_editor(esp_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    without any text editor tabs open.
    """
    esp_mode.view.current_tab = None
    esp_mode.run()
    assert esp_mode.view.show_message.call_count == 1


def test_run_no_device(esp_mode):
    """
    Ensure an error message is displayed if attempting to run a script
    and no device is found.
    """
    esp_mode.editor.current_device = None
    esp_mode.run()
    assert esp_mode.view.show_message.call_count == 1


def test_run(esp_mode):
    """
    Ensure run/repl/files buttons are disabled while flashing.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.find_device = mock.MagicMock(
        return_value=("COM0", "12345", "ESP8266")
    )
    mock_connection_class = mock.MagicMock()
    with mock.patch("mu.modes.base.REPLConnection", mock_connection_class):
        esp_mode.run()
    esp_mode.set_buttons.assert_called_once_with(files=False)


def test_on_data_flood(esp_mode):
    """
    Ensure the "Files" button is re-enabled before calling the base method.
    """
    esp_mode.set_buttons = mock.MagicMock()
    with mock.patch("builtins.super") as mock_super:
        esp_mode.on_data_flood()
        esp_mode.set_buttons.assert_called_once_with(files=True)
        mock_super().on_data_flood.assert_called_once_with()


def test_toggle_plotter(esp_mode):
    """
    Ensure the plotter is toggled on if the file system pane is absent.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.view.show_message = mock.MagicMock()

    def side_effect(*args, **kwargs):
        esp_mode.plotter = True

    with mock.patch(
        "mu.modes.microbit.MicroPythonMode.toggle_plotter",
        side_effect=side_effect,
    ) as tp:
        esp_mode.plotter = None
        esp_mode.toggle_plotter(None)
        tp.assert_called_once_with(None)
        esp_mode.set_buttons.assert_called_once_with(files=False)


def test_toggle_plotter_no_repl_or_plotter(esp_mode):
    """
    Ensure the file system button is enabled if the plotter toggles off and the
    repl isn't active.
    """
    esp_mode.set_buttons = mock.MagicMock()
    esp_mode.view.show_message = mock.MagicMock()

    def side_effect(*args, **kwargs):
        esp_mode.plotter = False
        esp_mode.repl = False

    with mock.patch(
        "mu.modes.microbit.MicroPythonMode.toggle_plotter",
        side_effect=side_effect,
    ) as tp:
        esp_mode.plotter = None
        esp_mode.toggle_plotter(None)
        tp.assert_called_once_with(None)
        esp_mode.set_buttons.assert_called_once_with(files=True)


def test_toggle_plotter_with_fs(esp_mode):
    """
    If the file system is active, show a helpful message instead.
    """
    esp_mode.remove_plotter = mock.MagicMock()
    esp_mode.view.show_message = mock.MagicMock()
    esp_mode.plotter = None
    esp_mode.fs = True
    esp_mode.toggle_plotter(None)
    assert esp_mode.view.show_message.call_count == 1


def test_deactivate(esp_mode):
    """
    Ensure Filesystem pane is hidden, when MicroPython-mode is
    deactivated.
    """
    esp_mode.remove_fs = mock.MagicMock()
    esp_mode.activate()
    esp_mode.fs = True
    esp_mode.deactivate()
    esp_mode.remove_fs.assert_called_once_with()


@pytest.fixture()
def sparkfunESP32():
    return Device(
        0x0403,
        0x6015,
        "COM0",
        "123456",
        "Sparkfun ESP32 Thing",
        "ESP MicroPython",
        "esp",
    )


def test_device_changed(esp_mode, sparkfunESP32):
    """
    Ensure Filesystem pane is reconnected, when the user changes
    device.
    """
    esp_mode.add_fs = mock.MagicMock()
    esp_mode.remove_fs = mock.MagicMock()
    esp_mode.activate()
    esp_mode.fs = True
    esp_mode.device_changed(sparkfunESP32)
    esp_mode.remove_fs.assert_called_once_with()
    esp_mode.add_fs.assert_called_once_with()
