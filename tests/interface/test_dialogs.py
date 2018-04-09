# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QApplication, QDialog
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
        ms = mu.interface.dialogs.ModeSelector()
        ms.setup(modes, current_mode, 'day')
    assert mock_item.call_count == 3


def test_ModeSelector_setup_night_theme():
    """
    Ensure the ModeSelector handles the night theme correctly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    modes = {
        'python': PythonMode(editor, view),
        'adafruit': AdafruitMode(editor, view),
        'microbit': MicrobitMode(editor, view),
    }
    current_mode = 'python'
    mock_item = mock.MagicMock()
    mock_css = mock.MagicMock()
    with mock.patch('mu.interface.dialogs.ModeItem', mock_item):
        ms = mu.interface.dialogs.ModeSelector()
        ms.setStyleSheet = mock_css
        ms.setup(modes, current_mode, 'night')
    assert mock_item.call_count == 3
    mock_css.assert_called_once_with(mu.interface.themes.NIGHT_STYLE)


def test_ModeSelector_setup_contrast_theme():
    """
    Ensure the ModeSelector handles the high contrast theme correctly.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    modes = {
        'python': PythonMode(editor, view),
        'adafruit': AdafruitMode(editor, view),
        'microbit': MicrobitMode(editor, view),
    }
    current_mode = 'python'
    mock_item = mock.MagicMock()
    mock_css = mock.MagicMock()
    with mock.patch('mu.interface.dialogs.ModeItem', mock_item):
        ms = mu.interface.dialogs.ModeSelector()
        ms.setStyleSheet = mock_css
        ms.setup(modes, current_mode, 'contrast')
    assert mock_item.call_count == 3
    mock_css.assert_called_once_with(mu.interface.themes.CONTRAST_STYLE)


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


def test_AdminDialog_setup():
    """
    Ensure the admin dialog is setup properly given the content of a log
    file and envars.
    """
    log = 'this is the contents of a log file'
    envars = 'name=value'
    ad = mu.interface.dialogs.AdminDialog()
    ad.setStyleSheet = mock.MagicMock()
    ad.setup(log, envars, 'day')
    assert ad.log_widget.log_text_area.toPlainText() == log
    assert ad.envars() == envars
    ad.setStyleSheet.assert_called_once_with(mu.interface.themes.DAY_STYLE)


def test_AdminDialog_setup_night():
    """
    Ensure the admin dialog can start with the night theme.
    """
    log = 'this is the contents of a log file'
    envars = 'name=value'
    ad = mu.interface.dialogs.AdminDialog()
    ad.setStyleSheet = mock.MagicMock()
    ad.setup(log, envars, 'night')
    ad.setStyleSheet.assert_called_once_with(mu.interface.themes.NIGHT_STYLE)


def test_LogDisplay_setup_contrast():
    """
    Ensure the log display dialog can start with the high contrast theme.
    """
    log = 'this is the contents of a log file'
    envars = 'name=value'
    ad = mu.interface.dialogs.AdminDialog()
    ad.setStyleSheet = mock.MagicMock()
    ad.setup(log, envars, 'contrast')
    ad.setStyleSheet.\
        assert_called_once_with(mu.interface.themes.CONTRAST_STYLE)
