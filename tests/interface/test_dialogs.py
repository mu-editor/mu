# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
import sys
import os
import pytest
import mu.interface.dialogs
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QDialogButtonBox
from unittest import mock
from mu.modes import PythonMode, CircuitPythonMode, MicrobitMode, DebugMode


# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


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
    mock_window = QWidget()
    ms = mu.interface.dialogs.ModeSelector(mock_window)
    ms.accept = mock.MagicMock()
    ms.select_and_accept()
    ms.accept.assert_called_once_with()


def test_ModeSelector_get_mode():
    """
    Ensure that the ModeSelector will correctly return a selected mode (or
    raise the expected exception if cancelled).
    """
    mock_window = QWidget()
    ms = mu.interface.dialogs.ModeSelector(mock_window)
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


def test_CircuitPythonSettingsWidget_setup():
    """
    Ensure the widget for editing settings related to adafruit mode
    displays the referenced settings data in the expected way.
    """
    circuitpython_run = True
    circuitpython_lib = True
    mbsw = mu.interface.dialogs.CircuitPythonSettingsWidget()
    mbsw.setup(circuitpython_run, circuitpython_lib)
    assert mbsw.circuitpython_run.isChecked()
    assert mbsw.circuitpython_lib.isChecked()


def test_PackagesWidget_setup():
    """
    Ensure the widget for editing settings related to third party packages
    displays the referenced data in the expected way.
    """
    packages = "foo\nbar\nbaz"
    pw = mu.interface.dialogs.PackagesWidget()
    pw.setup(packages)
    assert pw.text_area.toPlainText() == packages


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
        "circuitpython_run": True,
        "circuitpython_lib": True,
    }
    packages = "foo\nbar\nbaz\n"
    mock_window = QWidget()
    ad = mu.interface.dialogs.AdminDialog(mock_window)
    ad.setup(log, settings, packages)
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
    pd.run_pip = mock.MagicMock()
    to_remove = {"foo"}
    to_add = {"bar"}
    module_dir = "baz"
    pd.setup(to_remove, to_add, module_dir)
    pd.remove_packages.assert_called_once_with()
    pd.run_pip.assert_called_once_with()
    assert pd.button_box.button(QDialogButtonBox.Ok).isEnabled() is False
    assert pd.pkg_dirs == {}


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


def test_PackageDialog_run_pip():
    """
    Ensure the expected package to be installed is done so via the expected
    correct call to "pip" in a new process (as per the recommended way to
    us "pip").
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.to_add = {"foo"}
    pd.module_dir = "bar"
    mock_process = mock.MagicMock()
    with mock.patch("mu.interface.dialogs.QProcess", mock_process):
        pd.run_pip()
        assert pd.to_add == set()
        pd.process.readyRead.connect.assert_called_once_with(pd.read_process)
        pd.process.finished.connect.assert_called_once_with(pd.finished)
        args = [
            "-m",  # run the module
            "pip",  # called pip
            "install",  # to install
            "foo",  # a package called "foo"
            "--target",  # and the target directory for package assets is...
            "bar",  # ...this directory
        ]
        pd.process.start.assert_called_once_with(sys.executable, args)


def test_PackageDialog_finished_with_more_to_remove():
    """
    When the pip process is finished, check if there are more packages to
    install and run again.
    """
    pd = mu.interface.dialogs.PackageDialog()
    pd.to_add = {"foo"}
    pd.run_pip = mock.MagicMock()
    pd.process = mock.MagicMock()
    pd.finished()
    assert pd.process is None
    pd.run_pip.assert_called_once_with()


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
