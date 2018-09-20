# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QApplication, QDialog, QWidget
from unittest import mock
from mu.modes import PythonMode, AdafruitMode, MicrobitMode, DebugMode
import mu.interface.dialogs
import pytest


# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


def test_ModeItem_init():
    """
    Ensure that ModeItem objects are setup correctly.
    """
    name = 'item_name'
    description = 'item_description'
    icon = 'icon_name'
    mock_text = mock.MagicMock()
    mock_icon = mock.MagicMock()
    mock_load = mock.MagicMock(return_value=icon)
    with mock.patch('mu.interface.dialogs.QListWidgetItem.setText',
                    mock_text), \
            mock.patch('mu.interface.dialogs.QListWidgetItem.setIcon',
                       mock_icon), \
            mock.patch('mu.interface.dialogs.load_icon', mock_load):
        mi = mu.interface.dialogs.ModeItem(name, description, icon)
        assert mi.name == name
        assert mi.description == description
        assert mi.icon == icon
    mock_text.assert_called_once_with('{}\n{}'.format(name, description))
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
        'python': PythonMode(editor, view),
        'adafruit': AdafruitMode(editor, view),
        'microbit': MicrobitMode(editor, view),
        'debugger': DebugMode(editor, view),
    }
    current_mode = 'python'
    mock_item = mock.MagicMock()
    with mock.patch('mu.interface.dialogs.ModeItem', mock_item):
        with mock.patch('mu.interface.dialogs.QVBoxLayout'):
            with mock.patch('mu.interface.dialogs.QListWidget'):
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
    item.icon = 'name'
    ms.mode_list = mock.MagicMock()
    ms.mode_list.currentItem.return_value = item
    result = ms.get_mode()
    assert result == 'name'
    ms.result.return_value = None
    with pytest.raises(RuntimeError):
        ms.get_mode()


def test_LogWidget_setup():
    """
    Ensure the log widget displays the referenced log file string in the
    expected way.
    """
    log = 'this is the contents of a log file'
    lw = mu.interface.dialogs.LogWidget()
    lw.setup(log)
    assert lw.log_text_area.toPlainText() == log
    assert lw.log_text_area.isReadOnly()


def test_EnvironmentVariablesWidget_setup():
    """
    Ensure the widget for editing user defined environment variables displays
    the referenced string in the expected way.
    """
    envars = 'name=value'
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
    custom_runtime_path = '/foo/bar'
    mbsw = mu.interface.dialogs.MicrobitSettingsWidget()
    mbsw.setup(minify, custom_runtime_path)
    assert mbsw.minify.isChecked()
    assert mbsw.runtime_path.text() == '/foo/bar'


def test_AdafruitSettingsWidget_setup():
    """
    Ensure the widget for editing settings related to adafruit mode
    displays the referenced settings data in the expected way.
    """
    adafruit_run = True
    mbsw = mu.interface.dialogs.AdafruitSettingsWidget()
    mbsw.setup(adafruit_run)
    assert mbsw.adafruit_run.isChecked()


def test_AdminDialog_setup():
    """
    Ensure the admin dialog is setup properly given the content of a log
    file and envars.
    """
    log = 'this is the contents of a log file'
    settings = {
        'envars': 'name=value',
        'minify': True,
        'microbit_runtime': '/foo/bar',
        'adafruit_run': True
    }
    mock_window = QWidget()
    ad = mu.interface.dialogs.AdminDialog(mock_window)
    ad.setup(log, settings)
    assert ad.log_widget.log_text_area.toPlainText() == log
    assert ad.settings() == settings


def test_FindReplaceDialog_setup():
    """
    Ensure the find/replace dialog is setup properly given only the theme
    as an argument.
    """
    frd = mu.interface.dialogs.FindReplaceDialog()
    frd.setup()
    assert frd.find() == ''
    assert frd.replace() == ''
    assert frd.replace_flag() is False


def test_FindReplaceDialog_setup_with_args():
    """
    Ensure the find/replace dialog is setup properly given only the theme
    as an argument.
    """
    find = 'foo'
    replace = 'bar'
    flag = True
    frd = mu.interface.dialogs.FindReplaceDialog()
    frd.setup(find, replace, flag)
    assert frd.find() == find
    assert frd.replace() == replace
    assert frd.replace_flag()
