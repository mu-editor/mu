# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
import os

import pytest
import mu.interface.dialogs
from PyQt5.QtWidgets import QDialog, QWidget, QDialogButtonBox
from unittest import mock
from mu import virtual_environment
from mu.modes import (
    PythonMode,
    CircuitPythonMode,
    MicrobitMode,
    DebugMode,
    ESPMode,
)
from PyQt5.QtCore import QProcess


def test_ModeItem_init():
    """
    Ensure that ModeItem objects are setup correctly.
    """
    name = "item_name"
    description = "item_description"
    icon = "icon_name"
    mock_text = mock.MagicMock()
    mock_icon = mock.MagicMock()
    mock_load = mock.MagicMock(return_value=icon)
    with mock.patch(
        "mu.interface.dialogs.QListWidgetItem.setText", mock_text
    ), mock.patch(
        "mu.interface.dialogs.QListWidgetItem.setIcon", mock_icon
    ), mock.patch(
        "mu.interface.dialogs.load_icon", mock_load
    ):
        mi = mu.interface.dialogs.ModeItem(name, description, icon)
        assert mi.name == name
        assert mi.description == description
        assert mi.icon == icon
    mock_text.assert_called_once_with("{}\n{}".format(name, description))
    mock_load.assert_called_once_with(icon)
    mock_icon.assert_called_once_with(icon)


def test_ModeSelector_setup():
    """
    Ensure the ModeSelector dialog is setup properly given a list of modes.

    If a mode has debugger = True it is ignored since debug mode is not a mode
    to be selected by users.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    modes = {
        "python": PythonMode(editor, view),
        "circuitpython": CircuitPythonMode(editor, view),
        "microbit": MicrobitMode(editor, view),
        "debugger": DebugMode(editor, view),
    }
    current_mode = "python"
    mock_item = mock.MagicMock()
    with mock.patch("mu.interface.dialogs.ModeItem", mock_item):
        with mock.patch("mu.interface.dialogs.QVBoxLayout"):
            with mock.patch("mu.interface.dialogs.QListWidget"):
                ms = mu.interface.dialogs.ModeSelector()
                ms.setLayout = mock.MagicMock()
                ms.setup(modes, current_mode)
                assert ms.setLayout.call_count == 1
    assert mock_item.call_count == 3


def test_ModeSelector_select_and_accept():
    """
    Ensure the accept slot is fired when this event handler is called.
    """
    ms = mu.interface.dialogs.ModeSelector()
    ms.accept = mock.MagicMock()
    ms.select_and_accept()
    ms.accept.assert_called_once_with()


def test_ModeSelector_get_mode():
    """
    Ensure that the ModeSelector will correctly return a selected mode (or
    raise the expected exception if cancelled).
    """
    ms = mu.interface.dialogs.ModeSelector()
    ms.result = mock.MagicMock(return_value=QDialog.Accepted)
    item = mock.MagicMock()
    item.icon = "name"
    ms.mode_list = mock.MagicMock()
    ms.mode_list.currentItem.return_value = item
    result = ms.get_mode()
    assert result == "name"
    ms.result.return_value = None
    with pytest.raises(RuntimeError):
        ms.get_mode()


def test_LogWidget_setup():
    """
    Ensure the log widget displays the referenced log file string in the
    expected way.
    """
    log = "this is the contents of a log file"
    lw = mu.interface.dialogs.LogWidget()
    lw.setup(log)
    assert lw.log_text_area.toPlainText() == log
    assert lw.log_text_area.isReadOnly()


def test_EnvironmentVariablesWidget_setup():
    """
    Ensure the widget for editing user defined environment variables displays
    the referenced string in the expected way.
    """
    envars = "name=value"
    evw = mu.interface.dialogs.EnvironmentVariablesWidget()
    evw.setup(envars)
    assert evw.text_area.toPlainText() == envars
    assert not evw.text_area.isReadOnly()


def test_MicrobitSettingsWidget_setup():
    """
    Ensure the widget for editing settings related to the BBC microbit
    displays the referenced settings data in the expected way.
    """
    minify = True
    custom_runtime_path = "/foo/bar"
    mbsw = mu.interface.dialogs.MicrobitSettingsWidget()
    mbsw.setup(minify, custom_runtime_path)
    assert mbsw.minify.isChecked()
    assert mbsw.runtime_path.text() == "/foo/bar"


def test_PackagesWidget_setup():
    """
    Ensure the widget for editing settings related to third party packages
    displays the referenced data in the expected way.
    """
    packages = "foo\nbar\nbaz"
    pw = mu.interface.dialogs.PackagesWidget()
    pw.setup(packages)
    assert pw.text_area.toPlainText() == packages


@pytest.fixture
def microbit():
    device = mu.logic.Device(
        0x0D28,
        0x0204,
        "COM1",
        123456,
        "ARM",
        "BBC micro:bit",
        "microbit",
        None,
    )
    return device


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_setup(esptool_is_installed, microbit):
    """
    Ensure the widget for editing settings related to the ESP Firmware Flasher
    displays the referenced settings data in the expected way.
    """
    mode = mock.MagicMock()
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    espff.venv = mock.Mock()
    with mock.patch("os.path.exists", return_value=False):
        espff.setup(mode, device_list)

    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mode, device_list)


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_show_folder_dialog(
    esptool_is_installed, microbit
):
    """
    Ensure the widget for editing settings related to the ESP Firmware Flasher
    displays the referenced settings data in the expected way.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/bar.py"
    mock_fd.getOpenFileName = mock.MagicMock(return_value=(path, True))
    mode = mock.MagicMock()
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mode, device_list)
    with mock.patch("mu.interface.dialogs.QFileDialog", mock_fd):
        espff.show_folder_dialog()
    assert espff.txtFolder.text() == path.replace("/", os.sep)


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_update_firmware(
    esptool_is_installed, microbit
):
    """
    Ensure the widget for editing settings related to the ESP Firmware Flasher
    displays the referenced settings data in the expected way.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = ESPMode(editor, view)
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    espff.venv = mock.Mock()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mm, device_list)

    espff.mode.repl = True
    espff.mode.plotter = True
    espff.mode.fs = True
    espff.device_type.setCurrentIndex(0)
    espff.update_firmware()

    espff.device_type.setCurrentIndex(1)
    espff.update_firmware()


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_update_firmware_no_device(
    esptool_is_installed,
):
    """
    Ensure that we don't try to flash, when no device is connected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    mm = ESPMode(editor, view)
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mm, device_list)

    espff.run_esptool = mock.MagicMock()
    espff.device_type.setCurrentIndex(0)
    espff.update_firmware()

    espff.run_esptool.assert_not_called()


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_esptool_error(
    esptool_is_installed, microbit
):
    """
    Ensure the widget for editing settings related to the ESP Firmware Flasher
    displays the referenced settings data in the expected way.
    """
    mode = mock.MagicMock()
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mode, device_list)
    espff.esptool_error(0)


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_esptool_finished(
    esptool_is_installed, microbit
):
    """
    Ensure the widget for editing settings related to the ESP Firmware Flasher
    displays the referenced settings data in the expected way.
    """
    mode = mock.MagicMock()
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mode, device_list)
    espff.esptool_finished(1, 0)

    espff.commands = ["foo", "bar"]
    espff.esptool_finished(0, QProcess.CrashExit + 1)


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_read_process(esptool_is_installed, microbit):
    """
    Ensure the widget for editing settings related to the ESP Firmware Flasher
    displays the referenced settings data in the expected way.
    """
    mode = mock.MagicMock()
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mode, device_list)

    espff.process = mock.MagicMock()
    espff.process.readAll().data.return_value = b"halted"
    espff.read_process()

    data = "𠜎Hello, World!".encode("utf-8")  # Contains a multi-byte char.
    data = data[1:]  # Split the muti-byte character (cause UnicodeDecodeError)
    espff.process.readAll().data.return_value = data
    espff.read_process()


@mock.patch(
    "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
    return_value=True,
)
def test_ESPFirmwareFlasherWidget_firmware_path_changed(
    esptool_is_installed, microbit
):
    """
    Ensure the widget for editing settings related to the ESP Firmware
    Flasher displays the referenced settings data in the expected way.
    """
    mode = mock.MagicMock()
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    device_list.add_device(microbit)
    espff = mu.interface.dialogs.ESPFirmwareFlasherWidget()
    with mock.patch("os.path.exists", return_value=True):
        espff.setup(mode, device_list)
    espff.txtFolder.setText("foo")
    assert espff.btnExec.isEnabled()
    espff.txtFolder.setText("")
    assert not espff.btnExec.isEnabled()


def test_AdminDialog_setup():
    """
    Ensure the admin dialog is setup properly given the content of a log
    file and envars.
    """
    log = "this is the contents of a log file"
    settings = {
        "envars": "name=value",
        "minify": True,
        "microbit_runtime": "/foo/bar",
    }
    packages = "foo\nbar\nbaz\n"
    mock_window = QWidget()
    mode = mock.MagicMock()
    mode.short_name = "esp"
    mode.name = "ESP MicroPython"
    modes = mock.MagicMock()
    device_list = mu.logic.DeviceList(modes)
    ad = mu.interface.dialogs.AdminDialog(mock_window)
    with mock.patch(
        "mu.interface.dialogs.ESPFirmwareFlasherWidget.esptool_is_installed",
        return_value=True,
    ):
        ad.setup(log, settings, packages, mode, device_list)
        assert ad.log_widget.log_text_area.toPlainText() == log
        s = ad.settings()
        assert s["packages"] == packages
        del s["packages"]
        assert s == settings


def test_FindReplaceDialog_setup():
    """
    Ensure the find/replace dialog is setup properly given only the theme
    as an argument.
    """
    frd = mu.interface.dialogs.FindReplaceDialog()
    frd.setup()
    assert frd.find() == ""
    assert frd.replace() == ""
    assert frd.replace_flag() is False


def test_FindReplaceDialog_setup_with_args():
    """
    Ensure the find/replace dialog is setup properly given only the theme
    as an argument.
    """
    find = "foo"
    replace = "bar"
    flag = True
    frd = mu.interface.dialogs.FindReplaceDialog()
    frd.setup(find, replace, flag)
    assert frd.find() == find
    assert frd.replace() == replace
    assert frd.replace_flag()


def test_PackageDialog_setup():
    """
    Ensure the PackageDialog is set up correctly and kicks off the process of
    removing and adding packages.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.remove_packages = mock.MagicMock()

    to_remove = {"foo"}
    to_add = {"bar"}
    with mock.patch.object(pd, "pip_queue") as pip_queue:
        pip_queue.append = mock.Mock()
        pd.setup(to_remove, to_add)

    queue_called_with = pip_queue.append.call_args_list
    [args0], _ = queue_called_with[0]
    assert args0 == ("install", to_add)
    [args1], _ = queue_called_with[1]
    assert args1 == ("remove", to_remove)
    assert pd.button_box.button(QDialogButtonBox.Ok).isEnabled() is False


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_packages():
    """
    Ensure the pkg_dirs of to-be-removed packages is correctly filled and the
    remove_package method is scheduled.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.to_remove = {"foo", "bar-baz", "Quux"}
    pd.module_dir = "wibble"
    dirs = [
        "foo-1.0.0.dist-info",
        "foo",
        "bar_baz-1.0.0.dist-info",
        "bar_baz",
        "quux-1.0.0.dist-info",
        "quux",
    ]
    with mock.patch(
        "mu.interface.dialogs.os.listdir", return_value=dirs
    ), mock.patch("mu.interface.dialogs.QTimer") as mock_qtimer:
        pd.remove_packages()
        assert pd.pkg_dirs == {
            "foo": os.path.join("wibble", "foo-1.0.0.dist-info"),
            "bar-baz": os.path.join("wibble", "bar_baz-1.0.0.dist-info"),
            "Quux": os.path.join("wibble", "quux-1.0.0.dist-info"),
        }
        mock_qtimer.singleShot.assert_called_once_with(2, pd.remove_package)


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_package_dist_info():
    """
    Ensures that if there are packages remaining to be deleted, then the next
    one is deleted as expected.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.append_data = mock.MagicMock()
    pd.pkg_dirs = {"foo": os.path.join("bar", "foo-1.0.0.dist-info")}
    pd.module_dir = "baz"
    files = [["filename1", ""], ["filename2", ""], ["filename3", ""]]
    mock_remove = mock.MagicMock()
    mock_shutil = mock.MagicMock()
    mock_qtimer = mock.MagicMock()
    with mock.patch("builtins.open"), mock.patch(
        "mu.interface.dialogs.csv.reader", return_value=files
    ), mock.patch("mu.interface.dialogs.os.remove", mock_remove), mock.patch(
        "mu.interface.dialogs.shutil", mock_shutil
    ), mock.patch(
        "mu.interface.dialogs.QTimer", mock_qtimer
    ):
        pd.remove_package()
        assert pd.pkg_dirs == {}
        assert mock_remove.call_count == 3
        assert mock_shutil.rmtree.call_count == 3
        pd.append_data.assert_called_once_with("Removed foo\n")
        mock_qtimer.singleShot.assert_called_once_with(2, pd.remove_package)


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_package_dist_info_cannot_delete():
    """
    Ensures that if there are packages remaining to be deleted, then the next
    one is deleted and any failures are logged.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.append_data = mock.MagicMock()
    pd.pkg_dirs = {"foo": os.path.join("bar", "foo-1.0.0.dist-info")}
    pd.module_dir = "baz"
    files = [["filename1", ""], ["filename2", ""], ["filename3", ""]]
    mock_remove = mock.MagicMock(side_effect=Exception("Bang"))
    mock_shutil = mock.MagicMock()
    mock_qtimer = mock.MagicMock()
    mock_log = mock.MagicMock()
    with mock.patch("builtins.open"), mock.patch(
        "mu.interface.dialogs.csv.reader", return_value=files
    ), mock.patch("mu.interface.dialogs.os.remove", mock_remove), mock.patch(
        "mu.interface.dialogs.logger.error", mock_log
    ), mock.patch(
        "mu.interface.dialogs.shutil", mock_shutil
    ), mock.patch(
        "mu.interface.dialogs.QTimer", mock_qtimer
    ):
        pd.remove_package()
        assert pd.pkg_dirs == {}
        assert mock_remove.call_count == 3
        assert mock_log.call_count == 6
        assert mock_shutil.rmtree.call_count == 3
        pd.append_data.assert_called_once_with("Removed foo\n")
        mock_qtimer.singleShot.assert_called_once_with(2, pd.remove_package)


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_package_egg_info():
    """
    Ensures that if there are packages remaining to be deleted, then the next
    one is deleted as expected.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.append_data = mock.MagicMock()
    pd.pkg_dirs = {"foo": os.path.join("bar", "foo-1.0.0.egg-info")}
    pd.module_dir = "baz"
    files = "".join(["filename1\n", "filename2\n", "filename3\n"])
    mock_remove = mock.MagicMock()
    mock_shutil = mock.MagicMock()
    mock_qtimer = mock.MagicMock()
    with mock.patch(
        "builtins.open", mock.mock_open(read_data=files)
    ), mock.patch("mu.interface.dialogs.os.remove", mock_remove), mock.patch(
        "mu.interface.dialogs.shutil", mock_shutil
    ), mock.patch(
        "mu.interface.dialogs.QTimer", mock_qtimer
    ):
        pd.remove_package()
        assert pd.pkg_dirs == {}
        assert mock_remove.call_count == 3
        assert mock_shutil.rmtree.call_count == 3
        pd.append_data.assert_called_once_with("Removed foo\n")
        mock_qtimer.singleShot.assert_called_once_with(2, pd.remove_package)


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_package_egg_info_cannot_delete():
    """
    Ensures that if there are packages remaining to be deleted, then the next
    one is deleted and any failures are logged.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.append_data = mock.MagicMock()
    pd.pkg_dirs = {"foo": os.path.join("bar", "foo-1.0.0.egg-info")}
    pd.module_dir = "baz"
    files = "".join(["filename1\n", "filename2\n", "filename3\n"])
    mock_remove = mock.MagicMock(side_effect=Exception("Bang"))
    mock_shutil = mock.MagicMock()
    mock_qtimer = mock.MagicMock()
    mock_log = mock.MagicMock()
    with mock.patch(
        "builtins.open", mock.mock_open(read_data=files)
    ), mock.patch("mu.interface.dialogs.os.remove", mock_remove), mock.patch(
        "mu.interface.dialogs.logger.error", mock_log
    ), mock.patch(
        "mu.interface.dialogs.shutil", mock_shutil
    ), mock.patch(
        "mu.interface.dialogs.QTimer", mock_qtimer
    ):
        pd.remove_package()
        assert pd.pkg_dirs == {}
        assert mock_remove.call_count == 3
        assert mock_log.call_count == 6
        assert mock_shutil.rmtree.call_count == 3
        pd.append_data.assert_called_once_with("Removed foo\n")
        mock_qtimer.singleShot.assert_called_once_with(2, pd.remove_package)


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_package_egg_info_cannot_open_record():
    """
    If the installed-files.txt file is not available (sometimes the case), then
    simply raise an exception and communicate this to the user.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.append_data = mock.MagicMock()
    pd.pkg_dirs = {"foo": os.path.join("bar", "foo-1.0.0.egg-info")}
    pd.module_dir = "baz"
    mock_qtimer = mock.MagicMock()
    mock_log = mock.MagicMock()
    with mock.patch(
        "builtins.open", mock.MagicMock(side_effect=Exception("boom"))
    ), mock.patch("mu.interface.dialogs.logger.error", mock_log), mock.patch(
        "mu.interface.dialogs.QTimer", mock_qtimer
    ):
        pd.remove_package()
        assert pd.pkg_dirs == {}
        assert mock_log.call_count == 2
        msg = (
            "UNABLE TO REMOVE PACKAGE: foo (check the logs for "
            "more information.)"
        )
        pd.append_data.assert_called_once_with(msg)
        mock_qtimer.singleShot.assert_called_once_with(2, pd.remove_package)


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_remove_package_end_state():
    """
    If there are no more packages to remove and there's nothing to be done for
    adding packages, then ensure all directories that do not contain files are
    deleted and the expected end-state is called.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.module_dir = "foo"
    pd.pkg_dirs = {}
    pd.to_add = {}
    pd.process = None
    pd.end_state = mock.MagicMock()
    with mock.patch(
        "mu.interface.dialogs.os.listdir", return_value=["bar", "baz"]
    ), mock.patch(
        "mu.interface.dialogs.os.walk",
        side_effect=[[("bar", [], [])], [("baz", [], ["x"])]],
    ), mock.patch(
        "mu.interface.dialogs.shutil"
    ) as mock_shutil:
        pd.remove_package()
        assert mock_shutil.rmtree.call_count == 2
        call_args = mock_shutil.rmtree.call_args_list
        assert call_args[0][0][0] == os.path.join("foo", "bar")
        assert call_args[1][0][0] == os.path.join("foo", "bin")
    pd.end_state.assert_called_once_with()


@pytest.mark.skip(
    reason="Superseded probably by ntoll's previous work on venv"
)
def test_PackageDialog_end_state():
    """
    Ensure the expected end-state is correctly cofigured (for when all tasks
    relating to third party packages have finished).
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.append_data = mock.MagicMock()
    pd.button_box = mock.MagicMock()
    pd.end_state()
    pd.append_data.assert_called_once_with("\nFINISHED")
    pd.button_box.button().setEnabled.assert_called_once_with(True)


@pytest.mark.skip(reason="Superseded probably by virtual environment work")
def test_PackageDialog_run_pip():
    """
    Ensure the expected package to be installed is done so via the expected
    correct call to "pip" in a new process (as per the recommended way to
    us "pip").
    """
    pd = mu.interface.dialogs.PackageDialog()
    venv = virtual_environment.VirtualEnvironment(".")
    mock_process = mock.MagicMock()
    with mock.patch("mu.interface.dialogs.QProcess", mock_process):
        pd.setup({}, {"foo"})
        pd.process.readyRead.connect.assert_called_once_with(pd.read_process)
        pd.process.finished.connect.assert_called_once_with(pd.finished)
        args = [
            "-m",  # run the module
            "pip",  # called pip
            "install",  # to install
            "foo",  # a package called "foo"
        ]
        pd.process.start.assert_called_once_with(venv.interpreter, args)


@pytest.mark.skip(reason="Superseded probably by virtual environment work")
def test_PackageDialog_finished_with_more_to_remove():
    """
    When the pip process is finished, check if there are more packages to
    install and run again.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.run_pip = mock.MagicMock()
    pd.process = mock.MagicMock()
    venv = virtual_environment.VirtualEnvironment(".")
    pd.setup({}, {"foo"}, venv)
    pd.finished()
    assert pd.process is None
    pd.run_pip.assert_called_once_with()


@pytest.mark.skip(reason="Superseded probably by virtual environment work")
def test_PackageDialog_finished_to_end_state():
    """
    When the pip process is finished, if there are no more packages to install
    and there's no more activity for removing packages, move to the end state.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.to_add = set()
    pd.pkg_dirs = {}
    pd.end_state = mock.MagicMock()
    pd.finished()
    pd.end_state.assert_called_once_with()


@pytest.mark.skip(reason="Superseded probably by virtual environment work")
def test_PackageDialog_read_process():
    """
    Ensure any data from the subprocess running "pip" is read and appended to
    the text area.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.process = mock.MagicMock()
    pd.process.readAll().data.return_value = b"hello"
    pd.append_data = mock.MagicMock()
    mock_timer = mock.MagicMock()
    with mock.patch("mu.interface.dialogs.QTimer", mock_timer):
        pd.read_process()
        pd.append_data.assert_called_once_with("hello")
        mock_timer.singleShot.assert_called_once_with(2, pd.read_process)


@pytest.mark.skip(reason="Superseded probably by virtual environment work")
def test_PackageDialog_append_data():
    """
    Ensure that when data is appended, it's added to the end of the text area!
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.text_area = mock.MagicMock()
    pd.append_data("hello")
    c = pd.text_area.textCursor()
    assert c.movePosition.call_count == 2
    c.insertText.assert_called_once_with("hello")
    pd.text_area.setTextCursor.assert_called_once_with(c)
