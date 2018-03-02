# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QAction, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QSize, QIODevice
from PyQt5.QtGui import QIcon, QKeySequence
from unittest import mock
from mu import __version__
import mu.interface.main
import mu.interface.themes
import mu.interface.editor
import pytest


def test_ButtonBar_init():
    """
    Ensure everything is set and configured given a new instance of the
    ButtonBar.
    """
    mock_movable = mock.MagicMock(return_value=None)
    mock_icon_size = mock.MagicMock(return_value=None)
    mock_tool_button_size = mock.MagicMock(return_value=None)
    mock_context_menu_policy = mock.MagicMock(return_value=None)
    mock_object_name = mock.MagicMock(return_value=None)
    mock_reset = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.main.ButtonBar.setMovable', mock_movable), \
            mock.patch('mu.interface.main.ButtonBar.setIconSize',
                       mock_icon_size), \
            mock.patch('mu.interface.main.ButtonBar.setToolButtonStyle',
                       mock_tool_button_size), \
            mock.patch('mu.interface.main.ButtonBar.setContextMenuPolicy',
                       mock_context_menu_policy), \
            mock.patch('mu.interface.main.ButtonBar.setObjectName',
                       mock_object_name), \
            mock.patch('mu.interface.main.ButtonBar.reset', mock_reset):
        mu.interface.main.ButtonBar(None)
        mock_movable.assert_called_once_with(False)
        mock_icon_size.assert_called_once_with(QSize(64, 64))
        mock_tool_button_size.assert_called_once_with(3)
        mock_context_menu_policy.assert_called_once_with(Qt.PreventContextMenu)
        mock_object_name.assert_called_once_with('StandardToolBar')
        assert mock_reset.call_count == 1


def test_ButtonBar_reset():
    """
    Ensure reset clears the slots and actions.
    """
    mock_clear = mock.MagicMock()
    with mock.patch('mu.interface.main.ButtonBar.clear', mock_clear):
        b = mu.interface.main.ButtonBar(None)
        mock_clear.reset_mock()
        b.slots = {'foo': 'bar'}
        b.reset()
        assert b.slots == {}
        mock_clear.assert_called_once_with()


def test_ButtonBar_change_mode():
    """
    Ensure the expected actions are added to the button bar when the mode is
    changed.
    """
    mock_reset = mock.MagicMock()
    mock_add_action = mock.MagicMock()
    mock_add_separator = mock.MagicMock()
    actions = [
        {
            'name': 'foo',
            'display_name': 'Foo',
            'description': 'bar',
        },
    ]
    mock_mode = mock.MagicMock()
    mock_mode.actions.return_value = actions
    with mock.patch('mu.interface.main.ButtonBar.reset', mock_reset), \
            mock.patch('mu.interface.main.ButtonBar.addAction',
                       mock_add_action), \
            mock.patch('mu.interface.main.ButtonBar.addSeparator',
                       mock_add_separator):
        b = mu.interface.main.ButtonBar(None)
        mock_reset.reset_mock()
        b.change_mode(mock_mode)
        mock_reset.assert_called_once_with()
        assert mock_add_action.call_count == 10
        assert mock_add_separator.call_count == 3


def test_ButtonBar_set_responsive_mode():
    """
    Does the button bar shrink in compact mode and grow out of it?
    """
    mock_icon_size = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.main.ButtonBar.setIconSize', mock_icon_size):
        bb = mu.interface.main.ButtonBar(None)
        bb.setStyleSheet = mock.MagicMock()
        bb.set_responsive_mode(1024, 800)
        mock_icon_size.assert_called_with(QSize(64, 64))
        default_font = str(mu.interface.themes.DEFAULT_FONT_SIZE)
        style = "QWidget{font-size: " + default_font + "px;}"
        bb.setStyleSheet.assert_called_with(style)
        bb.set_responsive_mode(939, 800)
        mock_icon_size.assert_called_with(QSize(48, 48))
        bb.setStyleSheet.assert_called_with(style)
        bb.set_responsive_mode(939, 599)
        mock_icon_size.assert_called_with(QSize(32, 32))
        style = "QWidget{font-size: " + str(10) + "px;}"
        bb.setStyleSheet.assert_called_with(style)


def test_ButtonBar_add_action():
    """
    Check the appropriately referenced QAction is created by a call to
    addAction.
    """
    bb = mu.interface.main.ButtonBar(None)
    with mock.patch('builtins.super') as mock_s:
        bb.addAction('save', 'Save', 'save stuff')
        mock_s.assert_called_once_with()
    assert 'save' in bb.slots
    assert isinstance(bb.slots['save'], QAction)


def test_ButtonBar_connect():
    """
    Check the named slot is connected to the slot handler.
    """
    bb = mu.interface.main.ButtonBar(None)
    bb.parentWidget = mock.MagicMock(return_value=QWidget())
    bb.addAction('save', 'Save', 'save stuff')
    bb.slots['save'].pyqtConfigure = mock.MagicMock(return_value=None)
    bb.slots['save'].setShortcut = mock.MagicMock()
    mock_handler = mock.MagicMock(return_value=None)
    bb.connect('save', mock_handler, 'Ctrl+S')
    slot = bb.slots['save']
    slot.pyqtConfigure.assert_called_once_with(triggered=mock_handler)
    slot.setShortcut.assert_called_once_with(QKeySequence('Ctrl+S'))


def test_FileTabs_init():
    """
    Ensure a FileTabs instance is initialised as expected.
    """
    with mock.patch('mu.interface.main.FileTabs.setTabsClosable') as mstc, \
            mock.patch('mu.interface.main.FileTabs.tabCloseRequested') as cr, \
            mock.patch('mu.interface.main.FileTabs.currentChanged') as mcc:
        qtw = mu.interface.main.FileTabs()
        mstc.assert_called_once_with(True)
        cr.connect.assert_called_once_with(qtw.removeTab)
        mcc.connect.assert_called_once_with(qtw.change_tab)


def test_FileTabs_removeTab_cancel():
    """
    Ensure removeTab asks the user for confirmation if there is a modification
    to the tab. If "cancel" is selected, the parent removeTab is NOT called.
    """
    qtw = mu.interface.main.FileTabs()
    mock_window = mock.MagicMock()
    mock_window.show_confirmation.return_value = QMessageBox.Cancel
    mock_window.current_tab.isModified.return_value = True
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    with mock.patch('mu.interface.main.QTabWidget.removeTab',
                    return_value='foo') as rt:
        qtw.removeTab(tab_id)
        msg = 'There is un-saved work, closing the tab will cause you to ' \
              'lose it.'
        mock_window.show_confirmation.assert_called_once_with(msg)
        assert rt.call_count == 0


def test_FileTabs_removeTab_ok():
    """
    Ensure removeTab asks the user for confirmation if there is a modification
    to the tab. If user responds with "OK", the parent removeTab IS called.
    """
    qtw = mu.interface.main.FileTabs()
    mock_window = mock.MagicMock()
    mock_window.show_confirmation.return_value = QMessageBox.Ok
    mock_window.current_tab.isModified.return_value = True
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    with mock.patch('mu.interface.main.QTabWidget.removeTab',
                    return_value='foo') as rt:
        qtw.removeTab(tab_id)
        msg = 'There is un-saved work, closing the tab will cause you to ' \
              'lose it.'
        mock_window.show_confirmation.assert_called_once_with(msg)
        rt.assert_called_once_with(tab_id)


def test_FileTabs_change_tab():
    """
    Ensure change_tab updates the title of the application window with the
    label from the currently selected file.
    """
    qtw = mu.interface.main.FileTabs()
    mock_tab = mock.MagicMock()
    mock_tab.label = "foo"
    qtw.widget = mock.MagicMock(return_value=mock_tab)
    mock_window = mock.MagicMock()
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    qtw.change_tab(tab_id)
    mock_window.update_title.assert_called_once_with(mock_tab.label)


def test_FileTabs_change_tab_no_tabs():
    """
    If there are no tabs left, ensure change_tab updates the title of the
    application window with the default value (None).
    """
    qtw = mu.interface.main.FileTabs()
    qtw.widget = mock.MagicMock(return_value=None)
    mock_window = mock.MagicMock()
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    qtw.change_tab(0)
    mock_window.update_title.assert_called_once_with(None)


def test_Window_attributes():
    """
    Expect the title and icon to be set correctly.
    """
    w = mu.interface.main.Window()
    assert w.title == "Mu {}".format(__version__)
    assert w.icon == "icon"


def test_Window_resizeEvent():
    """
    Ensure resize events are passed along to the button bar.
    """
    resizeEvent = mock.MagicMock()
    size = mock.MagicMock()
    size.width.return_value = 1024
    size.height.return_value = 768
    resizeEvent.size.return_value = size
    w = mu.interface.main.Window()
    w.button_bar = mock.MagicMock()
    w.resizeEvent(resizeEvent)
    w.button_bar.set_responsive_mode.assert_called_with(1024, 768)


def test_Window_select_mode_selected():
    """
    Handle the selection of a new mode.
    """
    mock_mode_selector = mock.MagicMock()
    mock_selector = mock.MagicMock()
    mock_selector.get_mode.return_value = 'foo'
    mock_mode_selector.return_value = mock_selector
    mock_modes = mock.MagicMock()
    current_mode = 'python'
    with mock.patch('mu.interface.main.ModeSelector', mock_mode_selector):
        w = mu.interface.main.Window()
        result = w.select_mode(mock_modes, current_mode, 'day')
        assert result == 'foo'
        mock_selector.setup.assert_called_once_with(mock_modes, current_mode,
                                                    'day')
        mock_selector.exec.assert_called_once_with()


def test_Window_select_mode_cancelled():
    """
    Handle the selection of a new mode.
    """
    mock_mode_selector = mock.MagicMock()
    mock_selector = mock.MagicMock()
    mock_selector.get_mode.side_effect = ValueError()
    mock_mode_selector.return_value = mock_selector
    mock_modes = mock.MagicMock()
    current_mode = 'python'
    with mock.patch('mu.interface.main.ModeSelector', mock_mode_selector):
        w = mu.interface.main.Window()
        result = w.select_mode(mock_modes, current_mode, 'day')
        assert result is None


def test_Window_change_mode():
    """
    Ensure the change of mode is made by the button_bar.
    """
    mock_mode = mock.MagicMock()
    api = ['API details', ]
    mock_mode.api.return_value = api
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    tab1 = mock.MagicMock()
    tab2 = mock.MagicMock()
    w.tabs.widget = mock.MagicMock(side_effect=[tab1, tab2])
    w.button_bar = mock.MagicMock()
    w.change_mode(mock_mode)
    w.button_bar.change_mode.assert_called_with(mock_mode)
    tab1.set_api.assert_called_once_with(api)
    tab2.set_api.assert_called_once_with(api)


def test_Window_zoom_in():
    """
    Ensure the correct signal is emitted.
    """
    w = mu.interface.main.Window()
    w._zoom_in = mock.MagicMock()
    w._zoom_in.emit = mock.MagicMock()
    w.zoom_in()
    w._zoom_in.emit.assert_called_once_with(2)


def test_Window_zoom_out():
    """
    Ensure the correct signal is emitted.
    """
    w = mu.interface.main.Window()
    w._zoom_out = mock.MagicMock()
    w._zoom_out.emit = mock.MagicMock()
    w.zoom_out()
    w._zoom_out.emit.assert_called_once_with(2)


def test_Window_connect_zoom():
    """
    Ensure the zoom in/out signals are connected to the passed in widget's
    zoomIn and zoomOut handlers.
    """
    w = mu.interface.main.Window()
    w._zoom_in = mock.MagicMock()
    w._zoom_in.connect = mock.MagicMock()
    w._zoom_out = mock.MagicMock()
    w._zoom_out.connect = mock.MagicMock()
    widget = mock.MagicMock()
    widget.zoomIn = mock.MagicMock()
    widget.zoomOut = mock.MagicMock()
    w.connect_zoom(widget)
    assert w._zoom_in.connect.called_once_with(widget.zoomIn)
    assert w._zoom_out.connect.called_once_with(widget.zoomOut)


def test_Window_current_tab():
    """
    Ensure the correct tab is extracted from Window.tabs.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value='foo')
    assert w.current_tab == 'foo'


def test_Window_set_read_only():
    """
    Ensure all the tabs have the setReadOnly method set to the boolean passed
    into set_read_only.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    tab1 = mock.MagicMock()
    tab2 = mock.MagicMock()
    w.tabs.widget = mock.MagicMock(side_effect=[tab1, tab2])
    w.set_read_only(True)
    assert w.read_only_tabs
    tab1.setReadOnly.assert_called_once_with(True)
    tab2.setReadOnly.assert_called_once_with(True)


def test_Window_get_load_path():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = '/foo/bar.py'
    mock_fd.getOpenFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch('mu.interface.main.QFileDialog', mock_fd):
        assert w.get_load_path('micropython') == path
    mock_fd.getOpenFileName.assert_called_once_with(w.widget, 'Open file',
                                                    'micropython',
                                                    '*.py *.PY *.hex')


def test_Window_get_save_path():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = '/foo/bar.py'
    mock_fd.getSaveFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch('mu.interface.main.QFileDialog', mock_fd):
        assert w.get_save_path('micropython') == path
    mock_fd.getSaveFileName.assert_called_once_with(w.widget, 'Save file',
                                                    'micropython')


def test_Window_get_microbit_path():
    """
    Ensures the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = '/foo'
    ShowDirsOnly = QFileDialog.ShowDirsOnly
    mock_fd.getExistingDirectory = mock.MagicMock(return_value=path)
    mock_fd.ShowDirsOnly = ShowDirsOnly
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch('mu.interface.main.QFileDialog', mock_fd):
        assert w.get_microbit_path('micropython') == path
    title = 'Locate BBC micro:bit'
    mock_fd.getExistingDirectory.assert_called_once_with(w.widget, title,
                                                         'micropython',
                                                         ShowDirsOnly)


def test_Window_add_tab():
    """
    Ensure adding a tab works as expected and the expected on_modified handler
    is created.
    """
    w = mu.interface.main.Window()
    w.read_only_tabs = True
    new_tab_index = 999
    w.tabs = mock.MagicMock()
    w.tabs.addTab = mock.MagicMock(return_value=new_tab_index)
    w.tabs.currentIndex = mock.MagicMock(return_value=new_tab_index)
    w.tabs.setCurrentIndex = mock.MagicMock(return_value=None)
    w.tabs.setTabText = mock.MagicMock(return_value=None)
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.set_theme = mock.MagicMock(return_value=None)
    w.theme = mock.MagicMock()
    w.api = ['an api help text', ]
    ep = mu.interface.editor.EditorPane('/foo/bar.py', 'baz')
    ep.set_api = mock.MagicMock()
    ep.modificationChanged = mock.MagicMock()
    ep.modificationChanged.connect = mock.MagicMock(return_value=None)
    ep.connect_margin = mock.MagicMock()
    ep.setFocus = mock.MagicMock(return_value=None)
    ep.setReadOnly = mock.MagicMock()
    mock_ed = mock.MagicMock(return_value=ep)
    path = '/foo/bar.py'
    text = 'print("Hello, World!")'
    api = ['API definition', ]
    w.breakpoint_toggle = mock.MagicMock()
    with mock.patch('mu.interface.main.EditorPane', mock_ed):
        w.add_tab(path, text, api)
    mock_ed.assert_called_once_with(path, text)
    w.tabs.addTab.assert_called_once_with(ep, ep.label)
    w.tabs.setCurrentIndex.assert_called_once_with(new_tab_index)
    w.connect_zoom.assert_called_once_with(ep)
    w.set_theme.assert_called_once_with(w.theme)
    ep.connect_margin.assert_called_once_with(w.breakpoint_toggle)
    ep.set_api.assert_called_once_with(api)
    ep.setFocus.assert_called_once_with()
    ep.setReadOnly.assert_called_once_with(w.read_only_tabs)
    on_modified = ep.modificationChanged.connect.call_args[0][0]
    on_modified()
    w.tabs.setTabText.assert_called_once_with(new_tab_index, ep.label)


def test_Window_focus_tab():
    """
    Given a tab instance, ensure it has focus.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.indexOf.return_value = 1
    tab = mock.MagicMock()
    w.focus_tab(tab)
    w.tabs.setCurrentIndex.assert_called_once_with(1)
    tab.setFocus.assert_called_once_with()


def test_Window_tab_count():
    """
    Ensure the number from Window.tabs.count() is returned.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    assert w.tab_count == 2
    w.tabs.count.assert_called_once_with()


def test_Window_widgets():
    """
    Ensure a list derived from calls to Window.tabs.widget(i) is returned.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    tab1 = mock.MagicMock()
    tab2 = mock.MagicMock()
    w.tabs.widget = mock.MagicMock(side_effect=[tab1, tab2])
    result = w.widgets
    assert result == [tab1, tab2]
    w.tabs.count.assert_called_once_with()


def test_Window_modified():
    """
    Ensure the window's modified attribute is derived from the modified state
    of its tabs.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    widget1 = mock.MagicMock()
    widget1.isModified = mock.MagicMock(return_value=False)
    widget2 = mock.MagicMock()
    widget2.isModified = mock.MagicMock(return_value=False)
    w.tabs.widget = mock.MagicMock(side_effect=[widget1, widget2])
    assert w.modified is False
    widget2.isModified = mock.MagicMock(return_value=True)
    w.tabs.widget = mock.MagicMock(side_effect=[widget1, widget2])
    assert w.modified


def test_Window_on_serial_read():
    """
    When data is received the data_received signal should emit it.
    """
    w = mu.interface.main.Window()
    w.serial = mock.MagicMock()
    w.serial.readAll.return_value = b'hello'
    w.data_received = mock.MagicMock()
    w.on_serial_read()
    w.data_received.emit.assert_called_once_with(b'hello')


def test_Window_open_serial_link():
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
    with mock.patch('mu.interface.main.QSerialPort', mock_serial_class):
        w = mu.interface.main.Window()
        w.open_serial_link('COM0')
        assert w.input_buffer == []
    mock_serial.setPortName.assert_called_once_with('COM0')
    mock_serial.setBaudRate.assert_called_once_with(115200)
    mock_serial.open.assert_called_once_with(QIODevice.ReadWrite)
    mock_serial.readyRead.connect.assert_called_once_with(w.on_serial_read)


def test_Window_open_serial_link_unable_to_connect():
    """
    If serial.open fails raise an IOError.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=False)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.main.QSerialPort', mock_serial_class):
        with pytest.raises(IOError):
            w = mu.interface.main.Window()
            w.open_serial_link('COM0')


def test_Window_open_serial_link_DTR_unset():
    """
    If data terminal ready (DTR) is unset (as can be the case on some
    Windows / Qt combinations) then fall back to PySerial to correct. See
    issues #281 and #302 for details.
    """
    mock_qt_serial = mock.MagicMock()
    mock_qt_serial.isDataTerminalReady.return_value = False
    mock_py_serial = mock.MagicMock()
    mock_serial_class = mock.MagicMock(return_value=mock_qt_serial)
    with mock.patch('mu.interface.main.QSerialPort', mock_serial_class):
        with mock.patch('mu.interface.main.serial', mock_py_serial):
            w = mu.interface.main.Window()
            w.open_serial_link('COM0')
    mock_qt_serial.close.assert_called_once_with()
    assert mock_qt_serial.open.call_count == 2
    mock_py_serial.Serial.assert_called_once_with('COM0')
    mock_pyser = mock_py_serial.Serial('COM0')
    assert mock_pyser.dtr is True
    mock_pyser.close.assert_called_once_with()


def test_Window_close_serial_link():
    """
    Ensure the serial link is closed / cleaned up as expected.
    """
    mock_serial = mock.MagicMock()
    w = mu.interface.main.Window()
    w.serial = mock_serial
    w.close_serial_link()
    mock_serial.close.assert_called_once_with()
    assert w.serial is None


def test_Window_add_filesystem():
    """
    Ensure the expected settings are updated when adding a file system pane.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.splitter = mock.MagicMock()
    w.addDockWidget = mock.MagicMock(return_value=None)
    w.connect_zoom = mock.MagicMock(return_value=None)
    mock_fs = mock.MagicMock()
    mock_fs.setFocus = mock.MagicMock(return_value=None)
    mock_fs_class = mock.MagicMock(return_value=mock_fs)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    mock_file_manager = mock.MagicMock()
    with mock.patch('mu.interface.main.FileSystemPane', mock_fs_class), \
            mock.patch('mu.interface.main.QDockWidget', mock_dock_class):
        result = w.add_filesystem('path/to/home', mock_file_manager)
    mock_fs_class.assert_called_once_with('path/to/home')
    assert result == mock_fs
    assert w.fs_pane == mock_fs
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)
    mock_fs.setFocus.assert_called_once_with()
    mock_file_manager.on_list_files.connect.\
        assert_called_once_with(mock_fs.on_ls)
    mock_fs.list_files.connect.assert_called_once_with(mock_file_manager.ls)
    mock_fs.microbit_fs.put.connect.\
        assert_called_once_with(mock_file_manager.put)
    mock_fs.microbit_fs.delete.connect.\
        assert_called_once_with(mock_file_manager.delete)
    mock_fs.microbit_fs.list_files.connect.\
        assert_called_once_with(mock_file_manager.ls)
    mock_fs.local_fs.get.connect.assert_called_once_with(mock_file_manager.get)
    mock_fs.local_fs.list_files.connect.\
        assert_called_once_with(mock_file_manager.ls)
    mock_file_manager.on_put_file.connect.\
        assert_called_once_with(mock_fs.microbit_fs.on_put)
    mock_file_manager.on_delete_file.connect.\
        assert_called_once_with(mock_fs.microbit_fs.on_delete)
    mock_file_manager.on_get_file.connect.\
        assert_called_once_with(mock_fs.local_fs.on_get)
    mock_file_manager.on_list_fail.connect.\
        assert_called_once_with(mock_fs.on_ls_fail)
    mock_file_manager.on_put_fail.connect.\
        assert_called_once_with(mock_fs.on_put_fail)
    mock_file_manager.on_delete_fail.connect.\
        assert_called_once_with(mock_fs.on_delete_fail)
    mock_file_manager.on_get_fail.connect.\
        assert_called_once_with(mock_fs.on_get_fail)
    w.connect_zoom.assert_called_once_with(mock_fs)


def test_Window_add_micropython_repl():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    MicroPython based REPL.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.add_repl = mock.MagicMock()

    def side_effect(self, w=w):
        w.serial = mock.MagicMock()

    w.open_serial_link = mock.MagicMock(side_effect=side_effect)
    w.data_received = mock.MagicMock()
    mock_repl = mock.MagicMock()
    mock_repl_class = mock.MagicMock(return_value=mock_repl)
    with mock.patch('mu.interface.main.MicroPythonREPLPane', mock_repl_class):
        w.add_micropython_repl('COM0', 'Test REPL')
    mock_repl_class.assert_called_once_with(serial=w.serial, theme=w.theme)
    w.open_serial_link.assert_called_once_with('COM0')
    w.serial.write.assert_called_once_with(b'\x03')
    w.data_received.connect.assert_called_once_with(mock_repl.process_bytes)
    w.add_repl.assert_called_once_with(mock_repl, 'Test REPL')


def test_Window_add_micropython_plotter():
    """
    Ensure the expected object is instantiated and add_plotter is called for
    a MicroPython based plotter.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.add_plotter = mock.MagicMock()

    def side_effect(self, w=w):
        w.serial = mock.MagicMock()

    w.open_serial_link = mock.MagicMock(side_effect=side_effect)
    w.data_received = mock.MagicMock()
    mock_plotter = mock.MagicMock()
    mock_plotter_class = mock.MagicMock(return_value=mock_plotter)
    with mock.patch('mu.interface.main.PlotterPane', mock_plotter_class):
        w.add_micropython_plotter('COM0', 'MicroPython Plotter')
    mock_plotter_class.assert_called_once_with(theme=w.theme)
    w.open_serial_link.assert_called_once_with('COM0')
    w.data_received.connect.assert_called_once_with(mock_plotter.process_bytes)
    w.add_plotter.assert_called_once_with(mock_plotter, 'MicroPython Plotter')


def test_Window_add_jupyter_repl():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    Jupyter based REPL.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.add_repl = mock.MagicMock()
    mock_kernel_manager = mock.MagicMock()
    mock_kernel_client = mock.MagicMock()
    mock_pane = mock.MagicMock()
    mock_pane_class = mock.MagicMock(return_value=mock_pane)
    with mock.patch('mu.interface.main.JupyterREPLPane', mock_pane_class):
        w.add_jupyter_repl(mock_kernel_manager, mock_kernel_client)
    mock_pane_class.assert_called_once_with(theme=w.theme)
    assert mock_pane.kernel_manager == mock_kernel_manager
    assert mock_pane.kernel_client == mock_kernel_client
    assert mock_kernel_manager.kernel.gui == 'qt4'
    w.add_repl.assert_called_once_with(mock_pane, 'Python3 (Jupyter)')


def test_Window_add_repl():
    """
    Ensure the expected settings are updated.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.addDockWidget = mock.MagicMock()
    mock_repl_pane = mock.MagicMock()
    mock_repl_pane.setFocus = mock.MagicMock(return_value=None)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch('mu.interface.main.QDockWidget', mock_dock_class):
        w.add_repl(mock_repl_pane, 'Test REPL')
    assert w.repl_pane == mock_repl_pane
    mock_repl_pane.setFocus.assert_called_once_with()
    w.connect_zoom.assert_called_once_with(mock_repl_pane)
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)


def test_Window_add_plotter():
    """
    Ensure the expected settings are updated.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.addDockWidget = mock.MagicMock()
    mock_plotter_pane = mock.MagicMock()
    mock_plotter_pane.setTheme = mock.MagicMock()
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch('mu.interface.main.QDockWidget', mock_dock_class):
        w.add_plotter(mock_plotter_pane, 'Test Plotter')
    assert w.plotter_pane == mock_plotter_pane
    mock_plotter_pane.setFocus.assert_called_once_with()
    mock_plotter_pane.set_theme.assert_called_once_with(w.theme)
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)


def test_Window_add_python3_runner():
    """
    Ensure a Python 3 runner (to capture stdin/out/err) is displayed correctly.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.addDockWidget = mock.MagicMock()
    mock_process_runner = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process_runner)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    name = 'foo'
    path = 'bar'
    with mock.patch('mu.interface.main.PythonProcessPane',
                    mock_process_class), \
            mock.patch('mu.interface.main.QDockWidget', mock_dock_class):
        result = w.add_python3_runner(name, path)
        assert result == mock_process_runner
    assert w.process_runner == mock_process_runner
    assert w.runner == mock_dock
    w.runner.setWidget.assert_called_once_with(w.process_runner)
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)


def test_Window_add_debug_inspector():
    """
    Ensure a debug inspector (to display local variables) is displayed
    correctly.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.addDockWidget = mock.MagicMock()
    mock_debug_inspector = mock.MagicMock()
    mock_debug_inspector_class = mock.MagicMock(
        return_value=mock_debug_inspector)
    mock_model = mock.MagicMock()
    mock_model_class = mock.MagicMock(return_value=mock_model)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch('mu.interface.main.DebugInspector',
                    mock_debug_inspector_class), \
            mock.patch('mu.interface.main.QStandardItemModel',
                       mock_model_class), \
            mock.patch('mu.interface.main.QDockWidget', mock_dock_class):
        w.add_debug_inspector()
    assert w.debug_inspector == mock_debug_inspector
    assert w.debug_model == mock_model
    mock_debug_inspector.setModel.assert_called_once_with(mock_model)
    mock_dock.setWidget.assert_called_once_with(mock_debug_inspector)
    w.addDockWidget.assert_called_once_with(Qt.RightDockWidgetArea, mock_dock)


def test_Window_update_debug_inspector():
    """
    Given a representation of the local objects in the debug runner's call
    stack. Ensure the debug inspector's model is populated in the correct way
    to show the different types of value.
    """
    locals_dict = {
        '__builtins__': ['some', 'builtin', 'methods', ],
        '__debug_code__': '<debug code details>',
        '__debug_script__': '<debug script details',
        '__file__': "'/path/to/script.py'",
        '__name__': "'__main__'",
        'foo': "'hello'",
        'bar': "['this', 'is', 'a', 'list']",
        'baz': "{'this': 'is', 'a': 'dict'}",
    }
    w = mu.interface.main.Window()
    w.debug_model = mock.MagicMock()
    mock_standard_item = mock.MagicMock()
    with mock.patch('mu.interface.main.QStandardItem', mock_standard_item):
        w.update_debug_inspector(locals_dict)
    w.debug_model.clear.assert_called_once_with()
    w.debug_model.setHorizontalHeaderLabels(['Name', 'Value', ])
    # You just have to believe this is correct. I checked! :-)
    assert mock_standard_item.call_count == 22


def test_Window_update_debug_inspector_with_exception():
    """
    If an exception is encountered when working out the type of the value,
    make sure it just reverts to the repr of the object.
    """
    locals_dict = {
        'bar': "['this', 'is', 'a', 'list']",
    }
    w = mu.interface.main.Window()
    w.debug_model = mock.MagicMock()
    mock_standard_item = mock.MagicMock()
    mock_eval = mock.MagicMock(side_effect=Exception('BOOM!'))
    with mock.patch('mu.interface.main.QStandardItem', mock_standard_item), \
            mock.patch('builtins.eval', mock_eval):
        w.update_debug_inspector(locals_dict)
    # You just have to believe this is correct. I checked! :-)
    assert mock_standard_item.call_count == 2


def test_Window_remove_filesystem():
    """
    Check all the necessary calls to remove / reset the file system pane are
    made.
    """
    w = mu.interface.main.Window()
    mock_fs = mock.MagicMock()
    mock_fs.setParent = mock.MagicMock(return_value=None)
    mock_fs.deleteLater = mock.MagicMock(return_value=None)
    w.fs = mock_fs
    w.remove_filesystem()
    mock_fs.setParent.assert_called_once_with(None)
    mock_fs.deleteLater.assert_called_once_with()
    assert w.fs is None


def test_Window_remove_repl():
    """
    Check all the necessary calls to remove / reset the REPL are made.
    """
    w = mu.interface.main.Window()
    mock_repl = mock.MagicMock()
    mock_repl.setParent = mock.MagicMock(return_value=None)
    mock_repl.deleteLater = mock.MagicMock(return_value=None)
    w.repl = mock_repl
    w.serial = mock.MagicMock()
    w.remove_repl()
    mock_repl.setParent.assert_called_once_with(None)
    mock_repl.deleteLater.assert_called_once_with()
    assert w.repl is None
    assert w.serial is None


def test_Window_remove_repl_active_plotter():
    """
    When removing the repl, if the plotter is active, retain the serial
    connection.
    """
    w = mu.interface.main.Window()
    w.repl = mock.MagicMock()
    w.plotter = mock.MagicMock()
    w.serial = mock.MagicMock()
    w.remove_repl()
    assert w.repl is None
    assert w.serial


def test_Window_remove_plotter():
    """
    Check all the necessary calls to remove / reset the plotter are made.
    """
    w = mu.interface.main.Window()
    mock_plotter = mock.MagicMock()
    mock_plotter.setParent = mock.MagicMock(return_value=None)
    mock_plotter.deleteLater = mock.MagicMock(return_value=None)
    w.plotter = mock_plotter
    w.serial = mock.MagicMock()
    w.remove_plotter()
    mock_plotter.setParent.assert_called_once_with(None)
    mock_plotter.deleteLater.assert_called_once_with()
    assert w.plotter is None
    assert w.serial is None


def test_Window_remove_plotter_active_repl():
    """
    When removing the plotter, if the repl is active, retain the serial
    connection.
    """
    w = mu.interface.main.Window()
    w.repl = mock.MagicMock()
    w.plotter = mock.MagicMock()
    w.serial = mock.MagicMock()
    w.remove_plotter()
    assert w.plotter is None
    assert w.serial


def test_Window_remove_python_runner():
    """
    Check all the necessary calls to remove / reset the Python3 runner are
    made.
    """
    w = mu.interface.main.Window()
    mock_runner = mock.MagicMock()
    mock_runner.setParent = mock.MagicMock(return_value=None)
    mock_runner.deleteLater = mock.MagicMock(return_value=None)
    w.runner = mock_runner
    w.remove_python_runner()
    mock_runner.setParent.assert_called_once_with(None)
    mock_runner.deleteLater.assert_called_once_with()
    assert w.process_runner is None
    assert w.runner is None


def test_Window_remove_debug_inspector():
    """
    Check all the necessary calls to remove / reset the debug inspector are
    made.
    """
    w = mu.interface.main.Window()
    mock_inspector = mock.MagicMock()
    mock_model = mock.MagicMock()
    mock_debug_inspector = mock.MagicMock()
    w.inspector = mock_inspector
    w.debug_inspector = mock_debug_inspector
    w.debug_model = mock_model
    w.remove_debug_inspector()
    assert w.debug_inspector is None
    assert w.debug_model is None
    assert w.inspector is None
    mock_inspector.setParent.assert_called_once_with(None)
    mock_inspector.deleteLater.assert_called_once_with()


def test_Window_set_theme():
    """
    Check the theme is correctly applied to the window.
    """
    w = mu.interface.main.Window()
    w.setStyleSheet = mock.MagicMock(return_value=None)
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    tab1 = mock.MagicMock()
    tab1.set_theme = mock.MagicMock()
    tab2 = mock.MagicMock()
    tab2.set_theme = mock.MagicMock()
    w.tabs.widget = mock.MagicMock(side_effect=[tab1, tab2, tab1, tab2, tab1,
                                                tab2])
    w.button_bar = mock.MagicMock()
    w.button_bar.slots = {
        'theme': mock.MagicMock()
    }
    w.button_bar.slots['theme'].setIcon = mock.MagicMock(return_value=None)
    w.repl = mock.MagicMock()
    w.repl_pane = mock.MagicMock()
    w.repl_pane.set_theme = mock.MagicMock()
    w.plotter = mock.MagicMock()
    w.plotter_pane = mock.MagicMock()
    w.plotter_pane.set_theme = mock.MagicMock()
    w.set_theme('night')
    assert w.setStyleSheet.call_count == 1
    assert w.theme == 'night'
    tab1.set_theme.assert_called_once_with(mu.interface.themes.NightTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.themes.NightTheme)
    assert 1 == w.button_bar.slots['theme'].setIcon.call_count
    assert isinstance(w.button_bar.slots['theme'].setIcon.call_args[0][0],
                      QIcon)
    w.repl_pane.set_theme.assert_called_once_with('night')
    w.plotter_pane.set_theme.assert_called_once_with('night')
    w.setStyleSheet.reset_mock()
    tab1.set_theme.reset_mock()
    tab2.set_theme.reset_mock()
    w.button_bar.slots['theme'].setIcon.reset_mock()
    w.repl_pane.set_theme.reset_mock()
    w.plotter_pane.set_theme.reset_mock()
    w.set_theme('contrast')
    assert w.setStyleSheet.call_count == 1
    assert w.theme == 'contrast'
    tab1.set_theme.assert_called_once_with(mu.interface.themes.ContrastTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.themes.ContrastTheme)
    assert 1 == w.button_bar.slots['theme'].setIcon.call_count
    assert isinstance(w.button_bar.slots['theme'].setIcon.call_args[0][0],
                      QIcon)
    w.repl_pane.set_theme.assert_called_once_with('contrast')
    w.plotter_pane.set_theme.assert_called_once_with('contrast')
    w.setStyleSheet.reset_mock()
    tab1.set_theme.reset_mock()
    tab2.set_theme.reset_mock()
    w.button_bar.slots['theme'].setIcon.reset_mock()
    w.repl_pane.set_theme.reset_mock()
    w.plotter_pane.set_theme.reset_mock()
    w.set_theme('day')
    assert w.setStyleSheet.call_count == 1
    assert w.theme == 'day'
    tab1.set_theme.assert_called_once_with(mu.interface.themes.DayTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.themes.DayTheme)
    assert 1 == w.button_bar.slots['theme'].setIcon.call_count
    assert isinstance(w.button_bar.slots['theme'].setIcon.call_args[0][0],
                      QIcon)
    w.repl_pane.set_theme.assert_called_once_with('day')
    w.plotter_pane.set_theme.assert_called_once_with('day')


def test_Window_show_logs():
    """
    Ensure the modal widget for showing the log file is correctly configured.
    """
    mock_log_display = mock.MagicMock()
    mock_log_box = mock.MagicMock()
    mock_log_display.return_value = mock_log_box
    with mock.patch('mu.interface.main.LogDisplay', mock_log_display):
        w = mu.interface.main.Window()
        w.show_logs('foo', 'day')
        mock_log_display.assert_called_once_with()
        mock_log_box.setup.assert_called_once_with('foo', 'day')
        mock_log_box.exec.assert_called_once_with()


def test_Window_show_message():
    """
    Ensure the show_message method configures a QMessageBox in the expected
    manner.
    """
    mock_qmb = mock.MagicMock()
    mock_qmb.setText = mock.MagicMock(return_value=None)
    mock_qmb.setWindowTitle = mock.MagicMock(return_value=None)
    mock_qmb.setInformativeText = mock.MagicMock(return_value=None)
    mock_qmb.setIcon = mock.MagicMock(return_value=None)
    mock_qmb.Information = mock.MagicMock()
    mock_qmb.exec = mock.MagicMock(return_value=None)
    mock_qmb_class = mock.MagicMock(return_value=mock_qmb)
    w = mu.interface.main.Window()
    message = 'foo'
    information = 'bar'
    icon = 'Information'
    with mock.patch('mu.interface.main.QMessageBox', mock_qmb_class):
        w.show_message(message, information, icon)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with('Mu')
    mock_qmb.setInformativeText.assert_called_once_with(information)
    mock_qmb.setIcon.assert_called_once_with(mock_qmb.Information)
    mock_qmb.exec.assert_called_once_with()


def test_Window_show_message_default():
    """
    Ensure the show_message method configures a QMessageBox in the expected
    manner with default args.
    """
    mock_qmb = mock.MagicMock()
    mock_qmb.setText = mock.MagicMock(return_value=None)
    mock_qmb.setWindowTitle = mock.MagicMock(return_value=None)
    mock_qmb.setInformativeText = mock.MagicMock(return_value=None)
    mock_qmb.setIcon = mock.MagicMock(return_value=None)
    mock_qmb.Warning = mock.MagicMock()
    mock_qmb.exec = mock.MagicMock(return_value=None)
    mock_qmb_class = mock.MagicMock(return_value=mock_qmb)
    w = mu.interface.main.Window()
    message = 'foo'
    with mock.patch('mu.interface.main.QMessageBox', mock_qmb_class):
        w.show_message(message)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with('Mu')
    assert mock_qmb.setInformativeText.call_count == 0
    mock_qmb.setIcon.assert_called_once_with(mock_qmb.Warning)
    mock_qmb.exec.assert_called_once_with()


def test_Window_show_confirmation():
    """
    Ensure the show_confirmation method configures a QMessageBox in the
    expected manner.
    """
    mock_qmb = mock.MagicMock()
    mock_qmb.setText = mock.MagicMock(return_value=None)
    mock_qmb.setWindowTitle = mock.MagicMock(return_value=None)
    mock_qmb.setInformativeText = mock.MagicMock(return_value=None)
    mock_qmb.setIcon = mock.MagicMock(return_value=None)
    mock_qmb.Information = mock.MagicMock()
    mock_qmb.setStandardButtons = mock.MagicMock(return_value=None)
    mock_qmb.Cancel = mock.MagicMock()
    mock_qmb.Ok = mock.MagicMock()
    mock_qmb.setDefaultButton = mock.MagicMock(return_value=None)
    mock_qmb.exec = mock.MagicMock(return_value=None)
    mock_qmb_class = mock.MagicMock(return_value=mock_qmb)
    w = mu.interface.main.Window()
    message = 'foo'
    information = 'bar'
    icon = 'Information'
    with mock.patch('mu.interface.main.QMessageBox', mock_qmb_class):
        w.show_confirmation(message, information, icon)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with('Mu')
    mock_qmb.setInformativeText.assert_called_once_with(information)
    mock_qmb.setIcon.assert_called_once_with(mock_qmb.Information)
    mock_qmb.setStandardButtons.assert_called_once_with(mock_qmb.Cancel |
                                                        mock_qmb.Ok)
    mock_qmb.setDefaultButton.assert_called_once_with(mock_qmb.Cancel)
    mock_qmb.exec.assert_called_once_with()


def test_Window_show_confirmation_default():
    """
    Ensure the show_confirmation method configures a QMessageBox in the
    expected manner with default args.
    """
    mock_qmb = mock.MagicMock()
    mock_qmb.setText = mock.MagicMock(return_value=None)
    mock_qmb.setWindowTitle = mock.MagicMock(return_value=None)
    mock_qmb.setInformativeText = mock.MagicMock(return_value=None)
    mock_qmb.setIcon = mock.MagicMock(return_value=None)
    mock_qmb.Warning = mock.MagicMock()
    mock_qmb.setStandardButtons = mock.MagicMock(return_value=None)
    mock_qmb.Cancel = mock.MagicMock()
    mock_qmb.Ok = mock.MagicMock()
    mock_qmb.setDefaultButton = mock.MagicMock(return_value=None)
    mock_qmb.exec = mock.MagicMock(return_value=None)
    mock_qmb_class = mock.MagicMock(return_value=mock_qmb)
    w = mu.interface.main.Window()
    message = 'foo'
    with mock.patch('mu.interface.main.QMessageBox', mock_qmb_class):
        w.show_confirmation(message)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with('Mu')
    assert mock_qmb.setInformativeText.call_count == 0
    mock_qmb.setIcon.assert_called_once_with(mock_qmb.Warning)
    mock_qmb.setStandardButtons.assert_called_once_with(mock_qmb.Cancel |
                                                        mock_qmb.Ok)
    mock_qmb.setDefaultButton.assert_called_once_with(mock_qmb.Cancel)
    mock_qmb.exec.assert_called_once_with()


def test_Window_update_title():
    """
    Ensure a passed in title results in the correct call to setWindowTitle.
    """
    w = mu.interface.main.Window()
    w.title = 'Mu'
    w.setWindowTitle = mock.MagicMock(return_value=None)
    w.update_title('foo.py')
    w.setWindowTitle.assert_called_once_with('Mu - foo.py')


def test_Window_autosize_window():
    """
    Check the correct calculations take place and methods are called so the
    window is resized and positioned correctly.
    """
    mock_sg = mock.MagicMock()
    mock_screen = mock.MagicMock()
    mock_screen.width = mock.MagicMock(return_value=1024)
    mock_screen.height = mock.MagicMock(return_value=768)
    mock_sg.screenGeometry = mock.MagicMock(return_value=mock_screen)
    mock_qdw = mock.MagicMock(return_value=mock_sg)
    w = mu.interface.main.Window()
    w.resize = mock.MagicMock(return_value=None)
    mock_size = mock.MagicMock()
    mock_size.width = mock.MagicMock(return_value=819)
    mock_size.height = mock.MagicMock(return_value=614)
    w.geometry = mock.MagicMock(return_value=mock_size)
    w.move = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.main.QDesktopWidget', mock_qdw):
        w.autosize_window()
    mock_qdw.assert_called_once_with()
    w.resize.assert_called_once_with(int(1024 * 0.8), int(768 * 0.8))
    w.geometry.assert_called_once_with()
    x = (1024 - 819) / 2
    y = (768 - 614) / 2
    w.move.assert_called_once_with(x, y)


def test_Window_reset_annotations():
    """
    Ensure the current tab has its annotations reset.
    """
    tab = mock.MagicMock()
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value=tab)
    w.reset_annotations()
    tab.reset_annotations.assert_called_once_with()


def test_Window_annotate_code():
    """
    Ensure the current tab is annotated with the passed in feedback.
    """
    tab = mock.MagicMock()
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value=tab)
    feedback = 'foo'
    w.annotate_code(feedback, 'error')
    tab.annotate_code.assert_called_once_with(feedback, 'error')


def test_Window_show_annotations():
    """
    Ensure the current tab displays its annotations.
    """
    tab = mock.MagicMock()
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value=tab)
    w.show_annotations()
    tab.show_annotations.assert_called_once_with()


def test_Window_setup():
    """
    Ensures the various default attributes of the window are set to the
    expected value.
    """
    w = mu.interface.main.Window()
    w.setWindowIcon = mock.MagicMock(return_value=None)
    w.update_title = mock.MagicMock(return_value=None)
    w.setMinimumSize = mock.MagicMock(return_value=None)
    w.addWidget = mock.MagicMock(return_value=None)
    w.setCurrentWidget = mock.MagicMock(return_value=None)
    w.set_theme = mock.MagicMock(return_value=None)
    w.show = mock.MagicMock(return_value=None)
    w.setCentralWidget = mock.MagicMock(return_value=None)
    w.addToolBar = mock.MagicMock(return_value=None)
    w.autosize_window = mock.MagicMock(return_value=None)
    mock_widget = mock.MagicMock()
    mock_widget.setLayout = mock.MagicMock(return_value=None)
    mock_widget_class = mock.MagicMock(return_value=mock_widget)
    mock_button_bar = mock.MagicMock()
    mock_button_bar_class = mock.MagicMock(return_value=mock_button_bar)
    mock_qtw = mock.MagicMock()
    mock_qtw.setTabsClosable = mock.MagicMock(return_value=None)
    mock_qtw.tabCloseRequested = mock.MagicMock()
    mock_qtw.tabCloseRequested.connect = mock.MagicMock(return_value=None)
    mock_qtw.removeTab = mock.MagicMock
    mock_qtw_class = mock.MagicMock(return_value=mock_qtw)
    theme = 'night'
    breakpoint_toggle = mock.MagicMock()
    with mock.patch('mu.interface.main.QWidget', mock_widget_class), \
            mock.patch('mu.interface.main.ButtonBar', mock_button_bar_class), \
            mock.patch('mu.interface.main.FileTabs', mock_qtw_class):
        w.setup(breakpoint_toggle, theme)
    assert w.breakpoint_toggle == breakpoint_toggle
    assert w.theme == theme
    assert w.setWindowIcon.call_count == 1
    assert isinstance(w.setWindowIcon.call_args[0][0], QIcon)
    w.update_title.assert_called_once_with()
    w.setMinimumSize.assert_called_once_with(800, 400)
    assert w.widget == mock_widget
    assert w.button_bar == mock_button_bar
    assert w.tabs == mock_qtw
    w.show.assert_called_once_with()
    w.setCentralWidget.call_count == 1
    w.addToolBar.call_count == 1
    w.autosize_window.assert_called_once_with()


def test_Window_set_usb_checker():
    """
    Ensure the callback for checking for connected devices is set as expected.
    """
    w = mu.interface.main.Window()
    mock_timer = mock.MagicMock()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_callback = mock.MagicMock()
    with mock.patch('mu.interface.main.QTimer', mock_timer_class):
        w.set_usb_checker(1, mock_callback)
        assert w.usb_checker == mock_timer
        w.usb_checker.timeout.connect.assert_called_once_with(mock_callback)
        w.usb_checker.start.assert_called_once_with(1000)


def test_Window_set_timer():
    """
    Ensure a repeating timer with the referenced callback is created.
    """
    w = mu.interface.main.Window()
    mock_timer = mock.MagicMock()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_callback = mock.MagicMock()
    with mock.patch('mu.interface.main.QTimer', mock_timer_class):
        w.set_timer(5, mock_callback)
        assert w.timer == mock_timer
        w.timer.timeout.connect.assert_called_once_with(mock_callback)
        w.timer.start.assert_called_once_with(5 * 1000)


def test_Window_stop_timer():
    """
    Ensure the timer is stopped and destroyed.
    """
    mock_timer = mock.MagicMock()
    w = mu.interface.main.Window()
    w.timer = mock_timer
    w.stop_timer()
    assert w.timer is None
    mock_timer.stop.assert_called_once_with()


def test_Window_connect_tab_rename():
    """
    Ensure the referenced handler and shortcuts are set up to fire when
    the tab is double-clicked.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    mock_handler = mock.MagicMock()
    mock_shortcut = mock.MagicMock()
    mock_sequence = mock.MagicMock()
    with mock.patch('mu.interface.main.QShortcut', mock_shortcut), \
            mock.patch('mu.interface.main.QKeySequence', mock_sequence):
        w.connect_tab_rename(mock_handler, 'Ctrl-Shift-S')
    w.tabs.tabBarDoubleClicked.connect.assert_called_once_with(mock_handler)
    mock_shortcut.assert_called_once_with(mock_sequence('Ctrl-Shift-S'), w)
    mock_shortcut().activated.connect.assert_called_once_with(mock_handler)


def test_Window_open_directory_from_os_windows():
    """
    Ensure the file explorer for Windows is called for the expected path.
    """
    w = mu.interface.main.Window()
    with mock.patch('mu.interface.main.sys') as mock_sys, \
            mock.patch('mu.interface.main.os') as mock_os:
        path = 'c:\\a\\path\\'
        mock_sys.platform = 'win32'
        w.open_directory_from_os(path)
        mock_os.startfile.assert_called_once_with(path)


def test_Window_open_directory_from_os_darwin():
    """
    Ensure the file explorer for OSX is called for the expected path.
    """
    w = mu.interface.main.Window()
    with mock.patch('mu.interface.main.sys') as mock_sys, \
            mock.patch('mu.interface.main.os.system') as mock_system:
        path = '/home/user/mu_code/images/'
        mock_sys.platform = 'darwin'
        w.open_directory_from_os(path)
        mock_system.assert_called_once_with('open "{}"'.format(path))


def test_Window_open_directory_from_os_freedesktop():
    """
    Ensure the file explorer for FreeDesktop (Linux) is called for the
    expected path.
    """
    w = mu.interface.main.Window()
    with mock.patch('mu.interface.main.sys') as mock_sys, \
            mock.patch('mu.interface.main.os.system') as mock_system:
        path = '/home/user/mu_code/images/'
        mock_sys.platform = 'linux'
        w.open_directory_from_os(path)
        mock_system.assert_called_once_with('xdg-open "{}"'.format(path))


def test_StatusBar_init():
    """
    Ensure the status bar is set up as expected.
    """
    sb = mu.interface.main.StatusBar()
    # Default mode is set.
    assert sb.mode == 'python'

    sb = mu.interface.main.StatusBar(mode='foo')
    # Pass in the default mode.
    assert sb.mode == 'foo'

    # Expect two widgets for logs and mode.
    assert sb.mode_label
    assert sb.logs_label


def test_StatusBar_connect_logs():
    """
    Ensure the event handler / shortcut for viewing logs is correctly set.
    """
    sb = mu.interface.main.StatusBar()

    def handler():
        pass

    mock_shortcut = mock.MagicMock()
    mock_sequence = mock.MagicMock()
    with mock.patch('mu.interface.main.QShortcut', mock_shortcut), \
            mock.patch('mu.interface.main.QKeySequence', mock_sequence):
        sb.connect_logs(handler, 'Ctrl+X')
    assert sb.logs_label.mousePressEvent == handler
    mock_shortcut.assert_called_once_with(mock_sequence('Ctrl-X'), sb.parent())
    mock_shortcut().activated.connect.assert_called_once_with(handler)


def test_StatusBar_connect_mode():
    """
    Ensure the event handler / shortcut for selecting the new mode is
    correctly set.
    """
    sb = mu.interface.main.StatusBar()

    def handler():
        pass

    mock_shortcut = mock.MagicMock()
    mock_sequence = mock.MagicMock()
    with mock.patch('mu.interface.main.QShortcut', mock_shortcut), \
            mock.patch('mu.interface.main.QKeySequence', mock_sequence):
        sb.connect_mode(handler, 'Ctrl-X')
    assert sb.mode_label.mousePressEvent == handler
    mock_shortcut.assert_called_once_with(mock_sequence('Ctrl-X'), sb.parent())
    mock_shortcut().activated.connect.assert_called_once_with(handler)


def test_StatusBar_set_message():
    """
    Ensure the default pause for displaying a message in the status bar is
    used.
    """
    sb = mu.interface.main.StatusBar()
    sb.showMessage = mock.MagicMock()
    sb.set_message('Hello')
    sb.showMessage.assert_called_once_with('Hello', 5000)
    sb.showMessage.reset_mock()
    sb.set_message('Hello', 1000)
    sb.showMessage.assert_called_once_with('Hello', 1000)


def test_StatusBar_set_mode():
    """
    Ensure the mode displayed in the status bar is correctly updated.
    """
    mode = 'python'
    sb = mu.interface.main.StatusBar()
    sb.mode_label.setText = mock.MagicMock()
    sb.set_mode(mode)
    sb.mode_label.setText.assert_called_once_with(mode.capitalize())
