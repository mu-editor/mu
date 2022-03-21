# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import QAction, QWidget, QFileDialog, QMessageBox, QMenu
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from unittest import mock
import pytest
from mu import __version__
from tests.test_app import DumSig
import mu.interface.main
import mu.interface.themes
import mu.interface.editor
from mu.interface.panes import CHARTS, PlotterPane
import sys


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
    with mock.patch(
        "mu.interface.main.ButtonBar.setMovable", mock_movable
    ), mock.patch(
        "mu.interface.main.ButtonBar.setIconSize", mock_icon_size
    ), mock.patch(
        "mu.interface.main.ButtonBar.setToolButtonStyle", mock_tool_button_size
    ), mock.patch(
        "mu.interface.main.ButtonBar.setContextMenuPolicy",
        mock_context_menu_policy,
    ), mock.patch(
        "mu.interface.main.ButtonBar.setObjectName", mock_object_name
    ), mock.patch(
        "mu.interface.main.ButtonBar.reset", mock_reset
    ):
        mu.interface.main.ButtonBar(None)
        mock_movable.assert_called_once_with(False)
        mock_icon_size.assert_called_once_with(QSize(64, 64))
        mock_tool_button_size.assert_called_once_with(3)
        mock_context_menu_policy.assert_called_once_with(Qt.PreventContextMenu)
        mock_object_name.assert_called_once_with("StandardToolBar")
        assert mock_reset.call_count == 1


def test_ButtonBar_reset():
    """
    Ensure reset clears the slots and actions.
    """
    mock_clear = mock.MagicMock()
    with mock.patch("mu.interface.main.ButtonBar.clear", mock_clear):
        b = mu.interface.main.ButtonBar(None)
        mock_clear.reset_mock()
        b.slots = {"foo": "bar"}
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
    actions = [{"name": "foo", "display_name": "Foo", "description": "bar"}]
    mock_mode = mock.MagicMock()
    mock_mode.actions.return_value = actions
    with mock.patch(
        "mu.interface.main.ButtonBar.reset", mock_reset
    ), mock.patch(
        "mu.interface.main.ButtonBar.addAction", mock_add_action
    ), mock.patch(
        "mu.interface.main.ButtonBar.addSeparator", mock_add_separator
    ):
        b = mu.interface.main.ButtonBar(None)
        mock_reset.reset_mock()
        b.change_mode(mock_mode)
        mock_reset.assert_called_once_with()
        if sys.version_info < (3, 6):
            assert mock_add_action.call_count == 11
        else:
            assert mock_add_action.call_count == 12
        assert mock_add_separator.call_count == 5


def test_ButtonBar_set_responsive_mode():
    """
    Does the button bar shrink in compact mode and grow out of it?
    """
    mock_icon_size = mock.MagicMock(return_value=None)
    with mock.patch("mu.interface.main.ButtonBar.setIconSize", mock_icon_size):
        bb = mu.interface.main.ButtonBar(None)
        bb.setStyleSheet = mock.MagicMock()
        bb.set_responsive_mode(1124, 800)
        mock_icon_size.assert_called_with(QSize(46, 46))
        style = (
            "QWidget{font-size: "
            + str(mu.interface.themes.DEFAULT_FONT_SIZE)
            + "px;}"
        )
        bb.setStyleSheet.assert_called_with(style)
        bb.set_responsive_mode(939, 800)
        mock_icon_size.assert_called_with(QSize(39, 39))
        style = "QWidget{font-size: " + str(11) + "px;}"
        bb.setStyleSheet.assert_called_with(style)
        bb.set_responsive_mode(939, 599)
        mock_icon_size.assert_called_with(QSize(39, 39))
        style = "QWidget{font-size: " + str(11) + "px;}"
        bb.setStyleSheet.assert_called_with(style)


def test_ButtonBar_add_action():
    """
    Check the appropriately referenced QAction is created by a call to
    addAction.
    """
    bb = mu.interface.main.ButtonBar(None)
    with mock.patch("builtins.super") as mock_s:
        bb.addAction("save", "Save", "save stuff")
        mock_s.assert_called_once_with()
    assert "save" in bb.slots
    assert isinstance(bb.slots["save"], QAction)


def test_ButtonBar_connect():
    """
    Check the named slot is connected to the slot handler.
    """
    bb = mu.interface.main.ButtonBar(None)
    bb.parentWidget = mock.MagicMock(return_value=QWidget())
    bb.addAction("save", "Save", "save stuff")
    bb.slots["save"].pyqtConfigure = mock.MagicMock(return_value=None)
    bb.slots["save"].setShortcut = mock.MagicMock()
    mock_handler = mock.MagicMock(return_value=None)
    bb.connect("save", mock_handler, "Ctrl+S")
    slot = bb.slots["save"]
    slot.pyqtConfigure.assert_called_once_with(triggered=mock_handler)
    slot.setShortcut.assert_called_once_with(QKeySequence("Ctrl+S"))


def test_FileTabs_init():
    """
    Ensure a FileTabs instance is initialised as expected.
    """
    with mock.patch(
        "mu.interface.main.FileTabs.setTabsClosable"
    ) as mstc, mock.patch(
        "mu.interface.main.FileTabs.setMovable"
    ) as mstm, mock.patch(
        "mu.interface.main.FileTabs.currentChanged"
    ) as mcc:
        qtw = mu.interface.main.FileTabs()
        mstc.assert_called_once_with(False)
        mstm.assert_called_once_with(True)
        mcc.connect.assert_called_once_with(qtw.change_tab)


def test_FileTabs_removeTab_cancel():
    """
    Ensure removeTab asks the user for confirmation if there is a modification
    to the tab. If "cancel" is selected, the parent removeTab is NOT called.
    """
    qtw = mu.interface.main.FileTabs()
    mock_tab = mock.MagicMock()
    mock_tab.isModified.return_value = True
    qtw.widget = mock.MagicMock(return_value=mock_tab)
    mock_window = mock.MagicMock()
    mock_window.show_confirmation.return_value = QMessageBox.Cancel
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    with mock.patch(
        "mu.interface.main.QTabWidget.removeTab", return_value="foo"
    ) as rt:
        qtw.removeTab(tab_id)
        msg = (
            "There is un-saved work, closing the tab will cause you to "
            "lose it."
        )
        mock_window.show_confirmation.assert_called_once_with(msg)
        assert rt.call_count == 0
        qtw.widget.assert_called_once_with(tab_id)
        assert mock_tab.isModified.call_count == 1


def test_FileTabs_removeTab_ok():
    """
    Ensure removeTab asks the user for confirmation if there is a modification
    to the tab. If user responds with "OK", the parent removeTab IS called.
    """
    qtw = mu.interface.main.FileTabs()
    mock_tab = mock.MagicMock()
    mock_tab.isModified.return_value = True
    qtw.widget = mock.MagicMock(return_value=mock_tab)
    mock_window = mock.MagicMock()
    mock_window.show_confirmation.return_value = QMessageBox.Ok
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    with mock.patch(
        "mu.interface.main.QTabWidget.removeTab", return_value="foo"
    ) as rt:
        qtw.removeTab(tab_id)
        msg = (
            "There is un-saved work, closing the tab will cause you to "
            "lose it."
        )
        mock_window.show_confirmation.assert_called_once_with(msg)
        rt.assert_called_once_with(tab_id)
        qtw.widget.assert_called_once_with(tab_id)
        assert mock_tab.isModified.call_count == 1


def test_FileTabs_change_tab():
    """
    Ensure change_tab updates the title of the application window with the
    label from the currently selected file.
    """
    qtw = mu.interface.main.FileTabs()
    mock_tab = mock.MagicMock()
    mock_tab.title = "foo"
    qtw.widget = mock.MagicMock(return_value=mock_tab)
    mock_window = mock.MagicMock()
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    qtw.change_tab(tab_id)
    mock_window.update_title.assert_called_once_with(mock_tab.title)


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


def test_FileTabs_addTab():
    """
    Expect tabs to be added with the right label and a button
    """
    qtw = mu.interface.main.FileTabs()
    mock_tabbar = mock.MagicMock()
    mock_tabbar.setTabButton = mock.MagicMock()
    qtw.removeTab = mock.MagicMock()
    qtw.tabBar = mock.MagicMock(return_value=mock_tabbar)
    qtw.widget = mock.MagicMock(return_value=None)
    iconSize = QSize(12, 12)
    qtw.iconSize = mock.MagicMock(return_value=iconSize)
    mock_window = mock.MagicMock()
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    ep = mu.interface.editor.EditorPane("/foo/bar.py", "baz")
    ep.modificationChanged = DumSig()
    # Mocks for various classes
    mock_widget = mock.MagicMock()
    mock_widget_class = mock.MagicMock(return_value=mock_widget)
    mock_label = mock.MagicMock()
    mock_label.setPixmap = mock.MagicMock()
    mock_label_class = mock.MagicMock(return_value=mock_label)
    mock_button = mock.MagicMock()
    mock_button.clicked = DumSig()
    mock_button_class = mock.MagicMock(return_value=mock_button)
    mock_layout = mock.MagicMock()
    mock_layout.addWidget = mock.MagicMock()
    mock_layout.setContentsMargins = mock.MagicMock()
    mock_layout.setSpacing = mock.MagicMock()
    mock_layout_class = mock.MagicMock(return_value=mock_layout)
    mock_load_icon = mock.MagicMock()
    mock_load_pixmap = mock.MagicMock()
    # Patch half the world to check it was used
    with mock.patch(
        "mu.interface.main.QWidget", mock_widget_class
    ), mock.patch("mu.interface.main.QLabel", mock_label_class), mock.patch(
        "mu.interface.main.QPushButton", mock_button_class
    ), mock.patch(
        "mu.interface.main.QHBoxLayout", mock_layout_class
    ), mock.patch(
        "mu.interface.main.load_icon", mock_load_icon
    ), mock.patch(
        "mu.interface.main.load_pixmap", mock_load_pixmap
    ):
        qtw.addTab(ep, ep.label)
    # Various widgets were created
    mock_widget_class.assert_called_once_with()
    mock_label_class.assert_called_once_with(mock_widget)
    mock_button_class.assert_called_once_with(mock_widget)
    mock_layout_class.assert_called_once_with(mock_widget)
    # Widgets added to layout
    mock_layout.addWidget.assert_has_calls(
        [mock.call(mock_label), mock.call(mock_button)]
    )
    # Layout configured
    mock_layout.setContentsMargins.assert_called_once_with(0, 0, 0, 0)
    mock_layout.setSpacing.assert_called_once_with(6)
    # Check the icons were loaded
    mock_load_icon.assert_called_once_with("close-tab")
    mock_load_pixmap.assert_called_once_with("document", size=iconSize)
    # We assume the tab id is 0 based on looking at Qt's source
    # and the fact the bar was previously empty
    right = mu.interface.main.QTabBar.RightSide
    mock_tabbar.setTabButton.assert_called_once_with(0, right, mock_widget)
    # Check the page is removed when the button is clicked
    mock_button.clicked.emit()
    qtw.removeTab.assert_called_once_with(0)
    # Check icon is updated when modified
    ep.isModified = mock.MagicMock(side_effect=[True, False])
    with mock.patch("mu.interface.main.load_pixmap", mock_load_pixmap):
        ep.modificationChanged.emit()
        ep.modificationChanged.emit()
    assert ep.isModified.call_count == 2
    # Initial setup + two emits
    assert mock_load_pixmap.call_count == 3
    assert mock_label.setPixmap.call_count == 3


def test_Window_attributes():
    """
    Expect the title and icon to be set correctly.
    """
    w = mu.interface.main.Window()
    assert w.title == "Mu {}".format(__version__)
    assert w.icon == "icon"
    assert w.zoom_position == 2
    assert w.zooms == ("xs", "s", "m", "l", "xl", "xxl", "xxxl")


def test_Window_wheelEvent_zoom_in():
    """
    If the CTRL+scroll in a positive direction, zoom in.
    """
    w = mu.interface.main.Window()
    w.zoom_in = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.angleDelta().y.return_value = 1
    modifiers = Qt.ControlModifier
    with mock.patch(
        "mu.interface.main.QApplication.keyboardModifiers",
        return_value=modifiers,
    ):
        w.wheelEvent(mock_event)
        w.zoom_in.assert_called_once_with()
        mock_event.ignore.assert_called_once_with()


def test_Window_wheelEvent_zoom_out():
    """
    If the CTRL+scroll in a negative direction, zoom out.
    """
    w = mu.interface.main.Window()
    w.zoom_out = mock.MagicMock()
    mock_event = mock.MagicMock()
    mock_event.angleDelta().y.return_value = -1
    modifiers = Qt.ControlModifier
    with mock.patch(
        "mu.interface.main.QApplication.keyboardModifiers",
        return_value=modifiers,
    ):
        w.wheelEvent(mock_event)
        w.zoom_out.assert_called_once_with()
        mock_event.ignore.assert_called_once_with()


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
    mock_selector.get_mode.return_value = "foo"
    mock_mode_selector.return_value = mock_selector
    mock_modes = mock.MagicMock()
    current_mode = "python"
    with mock.patch("mu.interface.main.ModeSelector", mock_mode_selector):
        w = mu.interface.main.Window()
        result = w.select_mode(mock_modes, current_mode)
        assert result == "foo"
        mock_selector.setup.assert_called_once_with(mock_modes, current_mode)
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
    current_mode = "python"
    with mock.patch("mu.interface.main.ModeSelector", mock_mode_selector):
        w = mu.interface.main.Window()
        result = w.select_mode(mock_modes, current_mode)
        assert result is None


def test_Window_change_mode():
    """
    Ensure the change of mode is made by the button_bar.
    """
    mock_mode = mock.MagicMock()
    api = ["API details"]
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


def test_Window_set_zoom():
    """
    Ensure the correct signal is emitted.
    """
    w = mu.interface.main.Window()
    w._zoom_in = mock.MagicMock()
    w.set_zoom()
    w._zoom_in.emit.assert_called_once_with("m")


def test_Window_zoom_in():
    """
    Ensure the correct signal is emitted.
    """
    w = mu.interface.main.Window()
    w._zoom_in = mock.MagicMock()
    w.zoom_in()
    w._zoom_in.emit.assert_called_once_with("l")


def test_Window_zoom_out():
    """
    Ensure the correct signal is emitted.
    """
    w = mu.interface.main.Window()
    w._zoom_out = mock.MagicMock()
    w.zoom_out()
    w._zoom_out.emit.assert_called_once_with("s")


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
    w.tabs.currentWidget = mock.MagicMock(return_value="foo")
    assert w.current_tab == "foo"


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


def test_Window_get_load_path_no_previous():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/bar.py"
    mock_fd.getOpenFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_load_path(
            "micropython", "*.py *.hex *.PY *.HEX", allow_previous=True
        )
    assert returned_path == path
    assert w.previous_folder == "/foo"  # Note lack of filename.
    mock_fd.getOpenFileName.assert_called_once_with(
        w.widget, "Open file", "micropython", "*.py *.hex *.PY *.HEX"
    )


def test_Window_get_load_path_with_previous():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/bar.py"
    mock_fd.getOpenFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.previous_folder = "/previous"
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_load_path(
            "micropython", "*.py *.hex *.PY *.HEX", allow_previous=True
        )
    assert returned_path == path
    assert w.previous_folder == "/foo"  # Note lack of filename.
    mock_fd.getOpenFileName.assert_called_once_with(
        w.widget, "Open file", "/previous", "*.py *.hex *.PY *.HEX"
    )


def test_Window_get_load_path_force_path():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/bar.py"
    mock_fd.getOpenFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.previous_folder = "/previous"
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_load_path(
            "micropython", "*.py *.hex *.PY *.HEX", allow_previous=False
        )
    assert returned_path == path
    assert w.previous_folder == "/previous"  # Note lack of filename.
    mock_fd.getOpenFileName.assert_called_once_with(
        w.widget, "Open file", "micropython", "*.py *.hex *.PY *.HEX"
    )


def test_Window_get_save_path():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/bar.py"
    mock_fd.getSaveFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_save_path("micropython")
    mock_fd.getSaveFileName.assert_called_once_with(
        w.widget,
        "Save file",
        "micropython",
        "Python (*.py);;Other (*.*)",
        "Python (*.py)",
    )
    assert w.previous_folder == "/foo"  # Note lack of filename.
    assert returned_path == path


def test_Window_get_save_path_missing_extension():
    """
    Ensure that if the user enters a file without an extension, then append a
    ".py" extension by default. See #1571.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/bar"  # Note lack of ".py" extension in path provided by user.
    mock_fd.getSaveFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_save_path("micropython")
    mock_fd.getSaveFileName.assert_called_once_with(
        w.widget,
        "Save file",
        "micropython",
        "Python (*.py);;Other (*.*)",
        "Python (*.py)",
    )
    assert w.previous_folder == "/foo"  # Note lack of filename.
    assert returned_path == path + ".py"  # Note addition of ".py" extension.


def test_Window_get_save_path_empty_path():
    """
    Avoid appending a ".py" extension if the path is empty. See #1880.
    """
    mock_fd = mock.MagicMock()
    path = ""  # Empty, as when user cancels Save As / Rename Tab.
    mock_fd.getSaveFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_save_path("micropython")
    assert returned_path == ""  # Note lack of addition of ".py" extension.


def test_Window_get_save_path_for_dot_file():
    """
    Ensure that if the user enters a dot file without an extension, then
    no extension is appended. See commentary in #1572 for context.
    """
    mock_fd = mock.MagicMock()
    path = "/foo/.bar"  # a dot file without an extension.
    mock_fd.getSaveFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        returned_path = w.get_save_path("micropython")
    mock_fd.getSaveFileName.assert_called_once_with(
        w.widget,
        "Save file",
        "micropython",
        "Python (*.py);;Other (*.*)",
        "Python (*.py)",
    )
    assert w.previous_folder == "/foo"  # Note lack of filename.
    assert returned_path == path  # Note lack of extension


def test_Window_get_microbit_path():
    """
    Ensures the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = "/foo"
    ShowDirsOnly = QFileDialog.ShowDirsOnly
    mock_fd.getExistingDirectory = mock.MagicMock(return_value=path)
    mock_fd.ShowDirsOnly = ShowDirsOnly
    w = mu.interface.main.Window()
    w.widget = mock.MagicMock()
    with mock.patch("mu.interface.main.QFileDialog", mock_fd):
        assert w.get_microbit_path("micropython") == path
    title = "Locate BBC micro:bit"
    mock_fd.getExistingDirectory.assert_called_once_with(
        w.widget, title, "micropython", ShowDirsOnly
    )


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
    w.tabs.indexOf = mock.MagicMock(return_value=new_tab_index)
    w.tabs.setCurrentIndex = mock.MagicMock(return_value=None)
    w.tabs.setTabText = mock.MagicMock(return_value=None)
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.set_theme = mock.MagicMock(return_value=None)
    w.theme = mock.MagicMock()
    w.api = ["an api help text"]
    ep = mu.interface.editor.EditorPane("/foo/bar.py", "baz")
    ep.set_api = mock.MagicMock()
    ep.modificationChanged = mock.MagicMock()
    ep.modificationChanged.connect = mock.MagicMock(return_value=None)
    ep.connect_margin = mock.MagicMock()
    ep.setFocus = mock.MagicMock(return_value=None)
    ep.setReadOnly = mock.MagicMock()
    mock_ed = mock.MagicMock(return_value=ep)
    path = "/foo/bar.py"
    text = 'print("Hello, World!")'
    api = ["API definition"]
    w.breakpoint_toggle = mock.MagicMock()
    with mock.patch("mu.interface.main.EditorPane", mock_ed):
        w.add_tab(path, text, api, "\n")
    mock_ed.assert_called_once_with(path, text, "\n")
    w.tabs.addTab.assert_called_once_with(ep, ep.label)
    w.tabs.setCurrentIndex.assert_called_once_with(new_tab_index)
    w.connect_zoom.assert_called_once_with(ep)
    w.set_theme.assert_called_once_with(w.theme)
    ep.connect_margin.assert_called_once_with(w.breakpoint_toggle)
    ep.set_api.assert_called_once_with(api)
    ep.setFocus.assert_called_once_with()
    ep.setReadOnly.assert_called_once_with(w.read_only_tabs)
    ep.isModified = mock.MagicMock(side_effect=[True, True, False, False])
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


def test_Window_on_context_menu_nothing_selected():
    """
    If the current tab has no selected text, there should be no QMenu created.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = -1, -1, -1, -1
    menu = QMenu()
    menu.insertAction = mock.MagicMock()
    menu.insertSeparator = mock.MagicMock()
    menu.exec_ = mock.MagicMock()
    mock_tab.createStandardContextMenu = mock.MagicMock(return_value=menu)
    w.on_context_menu()
    assert mock_tab.createStandardContextMenu.call_count == 1
    # No additional items added to the menu.
    assert menu.insertAction.call_count == 0
    assert menu.insertSeparator.call_count == 0
    assert menu.exec_.call_count == 1


def test_Window_on_context_menu_has_selection_but_no_repl():
    """
    If the current tab has selected text, but there is no active REPL, there
    should be no QMenu created.
    """
    w = mu.interface.main.Window()
    w.repl = None
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 10, 10
    menu = QMenu()
    menu.insertAction = mock.MagicMock()
    menu.insertSeparator = mock.MagicMock()
    menu.exec_ = mock.MagicMock()
    mock_tab.createStandardContextMenu = mock.MagicMock(return_value=menu)
    w.on_context_menu()
    assert mock_tab.createStandardContextMenu.call_count == 1
    # No additional items added to the menu.
    assert menu.insertAction.call_count == 0
    assert menu.insertSeparator.call_count == 0
    assert menu.exec_.call_count == 1


def test_Window_on_context_menu_has_selection_but_no_interactive_process():
    """
    If the current tab has selected text, but there is no process in
    interactive mode, there should be no QMenu created.
    """
    w = mu.interface.main.Window()
    w.process_runner = mock.MagicMock()
    w.process_runner.is_interactive = False
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 10, 10
    menu = QMenu()
    menu.insertAction = mock.MagicMock()
    menu.insertSeparator = mock.MagicMock()
    menu.exec_ = mock.MagicMock()
    mock_tab.createStandardContextMenu = mock.MagicMock(return_value=menu)
    w.on_context_menu()
    assert mock_tab.createStandardContextMenu.call_count == 1
    # No additional items added to the menu.
    assert menu.insertAction.call_count == 0
    assert menu.insertSeparator.call_count == 0
    assert menu.exec_.call_count == 1


def test_Window_on_context_menu_with_repl():
    """
    If the current tab has selected text, and there is an active REPL, there
    should be a QMenu created in the expected manner.
    """
    w = mu.interface.main.Window()
    w.repl = True
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 10, 10
    menu = QMenu()
    menu.insertAction = mock.MagicMock()
    menu.insertSeparator = mock.MagicMock()
    menu.exec_ = mock.MagicMock()
    menu.actions = mock.MagicMock(return_value=["foo"])
    mock_tab.createStandardContextMenu = mock.MagicMock(return_value=menu)
    w.on_context_menu()
    assert mock_tab.createStandardContextMenu.call_count == 1
    assert menu.insertAction.call_count == 1
    assert menu.insertSeparator.call_count == 1
    assert menu.exec_.call_count == 1


def test_Window_on_context_menu_with_process_runner():
    """
    If the current tab has selected text, and there is an active
    PythonProcessRunner, there should be a QMenu created in the expected
    manner.
    """
    w = mu.interface.main.Window()
    w.process_runner = mock.MagicMock()
    w.process_runner.is_interactive = True
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 10, 10
    menu = QMenu()
    menu.insertAction = mock.MagicMock()
    menu.insertSeparator = mock.MagicMock()
    menu.exec_ = mock.MagicMock()
    menu.actions = mock.MagicMock(return_value=["foo"])
    mock_tab.createStandardContextMenu = mock.MagicMock(return_value=menu)
    w.on_context_menu()
    assert mock_tab.createStandardContextMenu.call_count == 1
    assert menu.insertAction.call_count == 1
    assert menu.insertSeparator.call_count == 1
    assert menu.exec_.call_count == 1


def test_Window_copy_to_repl_fragment():
    """
    If a fragment of text from a single line is selected, only paste that into
    the REPL.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 0, 5
    mock_tab.text.return_value = "Hello world!"
    w.repl_pane = mock.MagicMock()
    with mock.patch("mu.interface.main.QApplication") as mock_app:
        w.copy_to_repl()
        mock_app.clipboard.assert_called_once_with()
        clipboard = mock_app.clipboard()
        clipboard.setText.assert_called_once_with("Hello")
        w.repl_pane.paste.assert_called_once_with()
        w.repl_pane.setFocus.assert_called_once_with()


def test_Window_copy_to_repl_with_python_runner():
    """
    If a fragment of text from a single line is selected, only paste that into
    the active PythonProcessRunner.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 0, 5
    mock_tab.text.return_value = "Hello world!"
    w.process_runner = mock.MagicMock()
    with mock.patch("mu.interface.main.QApplication") as mock_app:
        w.copy_to_repl()
        mock_app.clipboard.assert_called_once_with()
        clipboard = mock_app.clipboard()
        clipboard.setText.assert_called_once_with("Hello")
        w.process_runner.paste.assert_called_once_with()
        w.process_runner.setFocus.assert_called_once_with()


def test_Window_copy_to_repl_multi_line():
    """
    If multiple lines are selected, ensure whitespace is corrected and paste
    them all into the REPL.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 3, 17
    mock_tab.text.return_value = """    def hello():
        return "Hello"

    print(hello())
    """
    w.repl_pane = mock.MagicMock()
    with mock.patch("mu.interface.main.QApplication") as mock_app:
        w.copy_to_repl()
        mock_app.clipboard.assert_called_once_with()
        clipboard = mock_app.clipboard()
        expected = """def hello():
    return "Hello"

print(hello())"""
        clipboard.setText.assert_called_once_with(expected)
        w.repl_pane.paste.assert_called_once_with()
        w.repl_pane.setFocus.assert_called_once_with()


def test_Window_on_stdout_write():
    """
    Ensure the data_received signal is emitted with the data.
    """
    w = mu.interface.main.Window()
    w.data_received = mock.MagicMock()
    w.on_stdout_write(b"hello")
    w.data_received.emit.assert_called_once_with(b"hello")


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
    with mock.patch(
        "mu.interface.main.FileSystemPane", mock_fs_class
    ), mock.patch("mu.interface.main.QDockWidget", mock_dock_class):
        result = w.add_filesystem("path/to/home", mock_file_manager)
    mock_fs_class.assert_called_once_with("path/to/home")
    assert result == mock_fs
    assert w.fs_pane == mock_fs
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)
    mock_fs.setFocus.assert_called_once_with()
    mock_file_manager.on_list_files.connect.assert_called_once_with(
        mock_fs.on_ls
    )
    mock_fs.list_files.connect.assert_called_once_with(mock_file_manager.ls)
    mock_fs.microbit_fs.put.connect.assert_called_once_with(
        mock_file_manager.put
    )
    mock_fs.microbit_fs.delete.connect.assert_called_once_with(
        mock_file_manager.delete
    )
    mock_fs.microbit_fs.list_files.connect.assert_called_once_with(
        mock_file_manager.ls
    )
    mock_fs.local_fs.get.connect.assert_called_once_with(mock_file_manager.get)
    mock_fs.local_fs.list_files.connect.assert_called_once_with(
        mock_file_manager.ls
    )
    mock_file_manager.on_put_file.connect.assert_called_once_with(
        mock_fs.microbit_fs.on_put
    )
    mock_file_manager.on_delete_file.connect.assert_called_once_with(
        mock_fs.microbit_fs.on_delete
    )
    mock_file_manager.on_get_file.connect.assert_called_once_with(
        mock_fs.local_fs.on_get
    )
    mock_file_manager.on_list_fail.connect.assert_called_once_with(
        mock_fs.on_ls_fail
    )
    mock_file_manager.on_put_fail.connect.assert_called_once_with(
        mock_fs.on_put_fail
    )
    mock_file_manager.on_delete_fail.connect.assert_called_once_with(
        mock_fs.on_delete_fail
    )
    mock_file_manager.on_get_fail.connect.assert_called_once_with(
        mock_fs.on_get_fail
    )
    w.connect_zoom.assert_called_once_with(mock_fs)


def test_Window_add_filesystem_open_signal():
    w = mu.interface.main.Window()
    w.open_file = mock.MagicMock()
    mock_open_emit = mock.MagicMock()
    w.open_file.emit = mock_open_emit
    pane = w.add_filesystem("homepath", mock.MagicMock())
    pane.open_file.emit("test")
    mock_open_emit.assert_called_once_with("test")


def test_Window_add_micropython_repl():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    MicroPython based REPL.
    """
    w = mu.interface.main.Window()
    w.add_repl = mock.MagicMock()
    mock_connection = mock.MagicMock()

    mock_repl = mock.MagicMock()
    mock_repl_class = mock.MagicMock(return_value=mock_repl)
    with mock.patch("mu.interface.main.MicroPythonREPLPane", mock_repl_class):
        w.add_micropython_repl("Test REPL", mock_connection)
    mock_repl_class.assert_called_once_with(mock_connection)

    mock_connection.data_received.connect.assert_called_once_with(
        mock_repl.process_tty_data
    )
    w.add_repl.assert_called_once_with(mock_repl, "Test REPL")


def test_Window_add_micropython_plotter():
    """
    Ensure the expected object is instantiated and add_plotter is called for
    a MicroPython based plotter.
    """
    w = mu.interface.main.Window()
    w.add_plotter = mock.MagicMock()
    mock_connection = mock.MagicMock()

    mock_plotter = mock.MagicMock()
    mock_plotter_class = mock.MagicMock(return_value=mock_plotter)
    mock_data_flood_handler = mock.MagicMock()
    with mock.patch("mu.interface.main.PlotterPane", mock_plotter_class):
        w.add_micropython_plotter(
            "MicroPython Plotter", mock_connection, mock_data_flood_handler
        )
    mock_plotter_class.assert_called_once_with()
    mock_connection.data_received.connect.assert_called_once_with(
        mock_plotter.process_tty_data
    )
    mock_plotter.data_flood.connect.assert_called_once_with(
        mock_data_flood_handler
    )
    w.add_plotter.assert_called_once_with(mock_plotter, "MicroPython Plotter")


def test_Window_add_snek_repl():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    Snek based REPL.
    """
    w = mu.interface.main.Window()
    w.add_repl = mock.MagicMock()
    mock_connection = mock.MagicMock()

    mock_repl = mock.MagicMock()
    mock_repl_class = mock.MagicMock(return_value=mock_repl)
    with mock.patch("mu.interface.main.SnekREPLPane", mock_repl_class):
        w.add_snek_repl("Test REPL", mock_connection)
    mock_repl_class.assert_called_once_with(mock_connection)

    mock_connection.data_received.connect.assert_called_once_with(
        mock_repl.process_bytes
    )
    w.add_repl.assert_called_once_with(mock_repl, "Test REPL")


def test_Window_add_snek_repl_no_interrupt():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    Snek based REPL.
    """
    w = mu.interface.main.Window()
    w.add_repl = mock.MagicMock()
    mock_connection = mock.MagicMock()

    mock_repl = mock.MagicMock()
    mock_repl_class = mock.MagicMock(return_value=mock_repl)
    with mock.patch("mu.interface.main.SnekREPLPane", mock_repl_class):
        w.add_snek_repl("Test REPL", mock_connection, force_interrupt=False)
    mock_repl_class.assert_called_once_with(mock_connection)

    assert mock_connection.send_interrupt.call_count == 0
    mock_connection.data_received.connect.assert_called_once_with(
        mock_repl.process_bytes
    )
    w.add_repl.assert_called_once_with(mock_repl, "Test REPL")


def test_Window_add_python3_plotter():
    """
    Ensure the plotter is created correctly when in Python 3 mode.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    w.add_plotter = mock.MagicMock()
    w.data_received = mock.MagicMock()
    mock_plotter = mock.MagicMock()
    mock_plotter_class = mock.MagicMock(return_value=mock_plotter)
    mock_mode = mock.MagicMock()
    with mock.patch("mu.interface.main.PlotterPane", mock_plotter_class):
        w.add_python3_plotter(mock_mode)
    w.data_received.connect.assert_called_once_with(
        mock_plotter.process_tty_data
    )
    mock_plotter.data_flood.connect.assert_called_once_with(
        mock_mode.on_data_flood
    )
    w.add_plotter.assert_called_once_with(mock_plotter, "Python3 data tuple")


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
    with mock.patch("mu.interface.main.JupyterREPLPane", mock_pane_class):
        w.add_jupyter_repl(mock_kernel_manager, mock_kernel_client)
    mock_pane_class.assert_called_once_with()
    assert mock_pane.kernel_manager == mock_kernel_manager
    assert mock_pane.kernel_client == mock_kernel_client
    assert mock_kernel_manager.kernel.gui == "qt4"
    w.add_repl.assert_called_once_with(mock_pane, "Python3 (Jupyter)")


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
    with mock.patch("mu.interface.main.QDockWidget", mock_dock_class):
        w.add_repl(mock_repl_pane, "Test REPL")
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
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch("mu.interface.main.QDockWidget", mock_dock_class):
        w.add_plotter(mock_plotter_pane, "Test Plotter")
    assert w.plotter_pane == mock_plotter_pane
    mock_plotter_pane.setFocus.assert_called_once_with()
    mock_plotter_pane.set_theme.assert_called_once_with(w.theme)
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)


@pytest.mark.skipif(not CHARTS, reason="QtChart unavailable")
def test_Window_remember_plotter_position():
    """
    Check that opening plotter, changing the area it's docked to, then closing
    it makes the next plotter open at the same area.
    """
    w = mu.interface.main.Window()
    w.theme = mock.MagicMock()
    pane = PlotterPane()
    w.add_plotter(pane, "Test Plotter")
    dock_area = w.dockWidgetArea(w.plotter)
    assert dock_area == 8  # Bottom
    w.removeDockWidget(w.plotter)
    w.addDockWidget(Qt.LeftDockWidgetArea, w.plotter)
    dock_area = w.dockWidgetArea(w.plotter)
    assert dock_area == 1  # Left
    w.remove_plotter()
    assert w.plotter is None
    pane2 = PlotterPane()
    w.add_plotter(pane2, "Test Plotter 2")
    dock_area = w.dockWidgetArea(w.plotter)
    assert dock_area == 1  # Reopened on left


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
    name = "foo"
    path = "bar"
    with mock.patch(
        "mu.interface.main.PythonProcessPane", mock_process_class
    ), mock.patch("mu.interface.main.QDockWidget", mock_dock_class):
        result = w.add_python3_runner(name, path, ".")
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
        return_value=mock_debug_inspector
    )
    mock_model = mock.MagicMock()
    mock_model_class = mock.MagicMock(return_value=mock_model)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch(
        "mu.interface.main.DebugInspector", mock_debug_inspector_class
    ), mock.patch(
        "mu.interface.main.QStandardItemModel", mock_model_class
    ), mock.patch(
        "mu.interface.main.QDockWidget", mock_dock_class
    ):
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
        "__builtins__": ["some", "builtin", "methods"],
        "__debug_code__": "<debug code details>",
        "__debug_script__": "<debug script details",
        "__file__": "'/path/to/script.py'",
        "__name__": "'__main__'",
        "foo": "'hello'",
        "bar": "['this', 'is', 'a', 'list']",
        "baz": "{'this': 'is', 'a': 'dict'}",
    }
    w = mu.interface.main.Window()
    w.debug_model = mock.MagicMock()
    w.debug_model.rowCount.return_value = 0
    mock_standard_item = mock.MagicMock()
    with mock.patch(
        "mu.interface.main.DebugInspectorItem", mock_standard_item
    ):
        w.update_debug_inspector(locals_dict)
    w.debug_model.rowCount.assert_called_once_with()
    w.debug_model.setHorizontalHeaderLabels(["Name", "Value"])
    # You just have to believe this is correct. I checked! :-)
    assert mock_standard_item.call_count == 22


def test_Window_update_debug_inspector_with_exception():
    """
    If an exception is encountered when working out the type of the value,
    make sure it just reverts to the repr of the object.
    """
    locals_dict = {"bar": "['this', 'is', 'a', 'list']"}
    w = mu.interface.main.Window()
    w.debug_model = mock.MagicMock()
    w.debug_model.rowCount.return_value = 0
    mock_standard_item = mock.MagicMock()
    mock_eval = mock.MagicMock(side_effect=Exception("BOOM!"))
    with mock.patch(
        "mu.interface.main.DebugInspectorItem", mock_standard_item
    ), mock.patch("builtins.eval", mock_eval):
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
    w.dockWidgetArea = mock.MagicMock()
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
    w.dockWidgetArea = mock.MagicMock()
    w.remove_repl()
    mock_repl.setParent.assert_called_once_with(None)
    mock_repl.deleteLater.assert_called_once_with()
    assert w.dockWidgetArea.call_count == 1
    assert w.repl is None


def test_Window_remove_plotter():
    """
    Check all the necessary calls to remove / reset the plotter are made.
    """
    w = mu.interface.main.Window()
    mock_plotter = mock.MagicMock()
    mock_plotter.setParent = mock.MagicMock(return_value=None)
    mock_plotter.deleteLater = mock.MagicMock(return_value=None)
    w.dockWidgetArea = mock.MagicMock()
    w.plotter = mock_plotter
    w.remove_plotter()
    mock_plotter.setParent.assert_called_once_with(None)
    mock_plotter.deleteLater.assert_called_once_with()
    assert w.dockWidgetArea.call_count == 1
    assert w.plotter is None


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
    w.process_runner = mock.MagicMock()
    w.dockWidgetArea = mock.MagicMock()
    w.remove_python_runner()
    mock_runner.setParent.assert_called_once_with(None)
    mock_runner.deleteLater.assert_called_once_with()
    assert w.dockWidgetArea.call_count == 1
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
    w.dockWidgetArea = mock.MagicMock()
    w.remove_debug_inspector()
    assert w.debug_inspector is None
    assert w.debug_model is None
    assert w.inspector is None
    mock_inspector.setParent.assert_called_once_with(None)
    mock_inspector.deleteLater.assert_called_once_with()
    assert w.dockWidgetArea.call_count == 1


def test_Window_set_theme():
    """
    Check the theme is correctly applied to the window.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    tab1 = mock.MagicMock()
    tab1.set_theme = mock.MagicMock()
    tab2 = mock.MagicMock()
    tab2.set_theme = mock.MagicMock()
    w.tabs.widget = mock.MagicMock(
        side_effect=[tab1, tab2, tab1, tab2, tab1, tab2]
    )
    w.button_bar = mock.MagicMock()
    w.button_bar.slots = {"theme": mock.MagicMock()}
    w.button_bar.slots["theme"].setIcon = mock.MagicMock(return_value=None)
    w.repl = mock.MagicMock()
    w.repl_pane = mock.MagicMock()
    w.repl_pane.set_theme = mock.MagicMock()
    w.plotter = mock.MagicMock()
    w.plotter_pane = mock.MagicMock()
    w.plotter_pane.set_theme = mock.MagicMock()
    w.load_theme = mock.MagicMock()
    w.load_theme.emit = mock.MagicMock()
    w.set_theme("night")
    w.load_theme.emit.assert_called_once_with("night")
    assert w.theme == "night"
    tab1.set_theme.assert_called_once_with(mu.interface.themes.NightTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.themes.NightTheme)
    assert 1 == w.button_bar.slots["theme"].setIcon.call_count
    assert isinstance(
        w.button_bar.slots["theme"].setIcon.call_args[0][0], QIcon
    )
    w.repl_pane.set_theme.assert_called_once_with("night")
    w.plotter_pane.set_theme.assert_called_once_with("night")
    w.load_theme.emit.reset_mock()
    tab1.set_theme.reset_mock()
    tab2.set_theme.reset_mock()
    w.button_bar.slots["theme"].setIcon.reset_mock()
    w.repl_pane.set_theme.reset_mock()
    w.plotter_pane.set_theme.reset_mock()
    w.set_theme("contrast")
    w.load_theme.emit.assert_called_once_with("contrast")
    assert w.theme == "contrast"
    tab1.set_theme.assert_called_once_with(mu.interface.themes.ContrastTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.themes.ContrastTheme)
    assert 1 == w.button_bar.slots["theme"].setIcon.call_count
    assert isinstance(
        w.button_bar.slots["theme"].setIcon.call_args[0][0], QIcon
    )
    w.repl_pane.set_theme.assert_called_once_with("contrast")
    w.plotter_pane.set_theme.assert_called_once_with("contrast")
    w.load_theme.emit.reset_mock()
    tab1.set_theme.reset_mock()
    tab2.set_theme.reset_mock()
    w.button_bar.slots["theme"].setIcon.reset_mock()
    w.repl_pane.set_theme.reset_mock()
    w.plotter_pane.set_theme.reset_mock()
    w.set_theme("day")
    w.load_theme.emit.assert_called_once_with("day")
    assert w.theme == "day"
    tab1.set_theme.assert_called_once_with(mu.interface.themes.DayTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.themes.DayTheme)
    assert 1 == w.button_bar.slots["theme"].setIcon.call_count
    assert isinstance(
        w.button_bar.slots["theme"].setIcon.call_args[0][0], QIcon
    )
    w.repl_pane.set_theme.assert_called_once_with("day")
    w.plotter_pane.set_theme.assert_called_once_with("day")


def test_Window_set_checker_icon():
    w = mu.interface.main.Window()
    w.button_bar = mock.MagicMock()
    w.button_bar.slots = {"check": mock.MagicMock()}
    w.button_bar.slots["check"].setIcon = mock.MagicMock()
    mock_timer = mock.MagicMock()
    mock_timer.start = mock.MagicMock()
    mock_timer.stop = mock.MagicMock()
    mock_timer.timeout = DumSig()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_load_icon = mock.MagicMock()
    with mock.patch("mu.interface.main.QTimer", mock_timer_class), mock.patch(
        "mu.interface.main.load_icon", mock_load_icon
    ):
        w.set_checker_icon("check-good")
        # Fake a timeout
        mock_timer.timeout.emit()
    mock_timer_class.assert_called_once_with()
    mock_timer.start.assert_called_once_with(500)
    mock_timer.stop.assert_called_once_with()
    mock_load_icon.assert_has_calls(
        [mock.call("check-good"), mock.call("check")]
    )
    assert w.button_bar.slots["check"].setIcon.call_count == 2


def test_Window_show_admin():
    """
    Ensure the modal widget for showing the admin features is correctly
    configured.
    """
    mock_admin_display = mock.MagicMock()
    mock_admin_box = mock.MagicMock()
    mock_admin_box.settings.return_value = "this is the expected result"
    mock_admin_display.return_value = mock_admin_box
    with mock.patch("mu.interface.main.AdminDialog", mock_admin_display):
        w = mu.interface.main.Window()
        result = w.show_admin("log", "envars", "packages", "mode", "devices")
        mock_admin_display.assert_called_once_with(w)
        mock_admin_box.setup.assert_called_once_with(
            "log", "envars", "packages", "mode", "devices"
        )
        mock_admin_box.exec.assert_called_once_with()
        assert result == "this is the expected result"


def test_Window_show_admin_cancelled():
    """
    If the modal dialog for the admin functions is cancelled, ensure an
    empty dictionary (indicating a "falsey" no change) is returned.
    """
    mock_admin_display = mock.MagicMock()
    mock_admin_box = mock.MagicMock()
    mock_admin_box.exec.return_value = False
    mock_admin_display.return_value = mock_admin_box
    with mock.patch("mu.interface.main.AdminDialog", mock_admin_display):
        w = mu.interface.main.Window()
        result = w.show_admin("log", "envars", "packages", "mode", "devices")
        mock_admin_display.assert_called_once_with(w)
        mock_admin_box.setup.assert_called_once_with(
            "log", "envars", "packages", "mode", "devices"
        )
        mock_admin_box.exec.assert_called_once_with()
        assert result == {}


def test_Window_sync_packages():
    """
    Ensure the expected modal dialog indicating progress of third party package
    add/removal is displayed with the expected settings.
    """
    mock_package_dialog = mock.MagicMock()
    with mock.patch("mu.interface.main.PackageDialog", mock_package_dialog):
        w = mu.interface.main.Window()
        to_remove = {"foo"}
        to_add = {"bar"}
        w.sync_packages(to_remove, to_add)
        dialog = mock_package_dialog()
        dialog.setup.assert_called_once_with(to_remove, to_add)
        dialog.exec.assert_called_once_with()


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
    message = "foo"
    information = "bar"
    icon = "Information"
    with mock.patch("mu.interface.main.QMessageBox", mock_qmb_class):
        w.show_message(message, information, icon)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with("Mu")
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
    message = "foo"
    with mock.patch("mu.interface.main.QMessageBox", mock_qmb_class):
        w.show_message(message)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with("Mu")
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
    message = "foo"
    information = "bar"
    icon = "Information"
    with mock.patch("mu.interface.main.QMessageBox", mock_qmb_class):
        w.show_confirmation(message, information, icon)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with("Mu")
    mock_qmb.setInformativeText.assert_called_once_with(information)
    mock_qmb.setIcon.assert_called_once_with(mock_qmb.Information)
    mock_qmb.setStandardButtons.assert_called_once_with(
        mock_qmb.Cancel | mock_qmb.Ok
    )
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
    message = "foo"
    with mock.patch("mu.interface.main.QMessageBox", mock_qmb_class):
        w.show_confirmation(message)
    mock_qmb.setText.assert_called_once_with(message)
    mock_qmb.setWindowTitle.assert_called_once_with("Mu")
    assert mock_qmb.setInformativeText.call_count == 0
    mock_qmb.setIcon.assert_called_once_with(mock_qmb.Warning)
    mock_qmb.setStandardButtons.assert_called_once_with(
        mock_qmb.Cancel | mock_qmb.Ok
    )
    mock_qmb.setDefaultButton.assert_called_once_with(mock_qmb.Cancel)
    mock_qmb.exec.assert_called_once_with()


def test_Window_update_title():
    """
    Ensure a passed in title results in the correct call to setWindowTitle.
    """
    w = mu.interface.main.Window()
    w.title = "Mu"
    w.setWindowTitle = mock.MagicMock(return_value=None)
    w.update_title("foo.py")
    w.setWindowTitle.assert_called_once_with("Mu - foo.py")


def _qdesktopwidget_mock(width, height):
    """
    Create and return a usable mock for QDesktopWidget that supports the
    QDesktopWidget().screenGeometry() use case: it returns a mocked QRect
    responding to .width() and .height() per the passed in arguments.
    """
    mock_sg = mock.MagicMock()
    mock_screen = mock.MagicMock()
    mock_screen.width = mock.MagicMock(return_value=width)
    mock_screen.height = mock.MagicMock(return_value=height)
    mock_sg.screenGeometry = mock.MagicMock(return_value=mock_screen)
    return mock.MagicMock(return_value=mock_sg)


def test_Window_autosize_window():
    """
    Check the correct calculations take place and methods are called so the
    window is resized and positioned correctly.
    """
    mock_qdw = _qdesktopwidget_mock(1024, 768)
    w = mu.interface.main.Window()
    w.resize = mock.MagicMock(return_value=None)
    mock_size = mock.MagicMock()
    mock_size.width = mock.MagicMock(return_value=819)
    mock_size.height = mock.MagicMock(return_value=614)
    w.geometry = mock.MagicMock(return_value=mock_size)
    w.move = mock.MagicMock(return_value=None)
    with mock.patch("mu.interface.main.QDesktopWidget", mock_qdw):
        w.size_window()
    mock_qdw.assert_called_once_with()
    w.resize.assert_called_once_with(int(1024 * 0.8), int(768 * 0.8))
    w.geometry.assert_called_once_with()
    x = (1024 - 819) // 2
    y = (768 - 614) // 2
    w.move.assert_called_once_with(x, y)


def test_Window_autosize_window_off_screen():
    """
    Check the correct calculations take place and methods are called so the
    window is resized and positioned correctly even if the passed in X/Y
    coordinates would put the window OFF the screen. See issue #1613 for
    context.
    """
    mock_qdw = _qdesktopwidget_mock(1024, 768)
    w = mu.interface.main.Window()
    w.resize = mock.MagicMock(return_value=None)
    mock_size = mock.MagicMock()
    mock_size.width = mock.MagicMock(return_value=819)
    mock_size.height = mock.MagicMock(return_value=614)
    w.geometry = mock.MagicMock(return_value=mock_size)
    w.move = mock.MagicMock(return_value=None)
    with mock.patch("mu.interface.main.QDesktopWidget", mock_qdw):
        w.size_window(x=-20, y=9999)
    mock_qdw.assert_called_once_with()
    w.resize.assert_called_once_with(int(1024 * 0.8), int(768 * 0.8))
    w.geometry.assert_called_once_with()
    x = (1024 - 819) // 2
    y = (768 - 614) // 2
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
    feedback = "foo"
    w.annotate_code(feedback, "error")
    tab.annotate_code.assert_called_once_with(feedback, "error")


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
    w.size_window = mock.MagicMock(return_value=None)
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
    theme = "night"
    breakpoint_toggle = mock.MagicMock()
    mock_qdw = _qdesktopwidget_mock(1000, 600)
    with mock.patch(
        "mu.interface.main.QWidget", mock_widget_class
    ), mock.patch(
        "mu.interface.main.ButtonBar", mock_button_bar_class
    ), mock.patch(
        "mu.interface.main.FileTabs", mock_qtw_class
    ), mock.patch(
        "mu.interface.main.QDesktopWidget", mock_qdw
    ):
        w.setup(breakpoint_toggle, theme)
    assert w.breakpoint_toggle == breakpoint_toggle
    assert w.theme == theme
    assert w.setWindowIcon.call_count == 1
    assert isinstance(w.setWindowIcon.call_args[0][0], QIcon)
    w.update_title.assert_called_once_with()
    w.setMinimumSize.assert_called_once_with(500, 300)
    assert w.widget == mock_widget
    assert w.button_bar == mock_button_bar
    assert w.tabs == mock_qtw
    w.show.assert_called_once_with()
    w.setCentralWidget.call_count == 1
    w.addToolBar.call_count == 1
    assert w.size_window.call_count == 0


def test_Window_set_usb_checker():
    """
    Ensure the callback for checking for connected devices is set as expected.
    """
    w = mu.interface.main.Window()
    mock_timer = mock.MagicMock()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_callback = mock.MagicMock()
    with mock.patch("mu.interface.main.QTimer", mock_timer_class):
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
    with mock.patch("mu.interface.main.QTimer", mock_timer_class):
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
    with mock.patch("mu.interface.main.QShortcut", mock_shortcut), mock.patch(
        "mu.interface.main.QKeySequence", mock_sequence
    ):
        w.connect_tab_rename(mock_handler, "Ctrl-Shift-S")
    w.tabs.tabBarDoubleClicked.connect.assert_called_once_with(mock_handler)
    mock_shortcut.assert_called_once_with(mock_sequence("Ctrl-Shift-S"), w)
    mock_shortcut().activated.connect.assert_called_once_with(mock_handler)


def test_Window_open_directory_from_os_windows():
    """
    Ensure the file explorer for Windows is called for the expected path.
    """
    w = mu.interface.main.Window()
    with mock.patch("mu.interface.main.sys") as mock_sys, mock.patch(
        "mu.interface.main.os"
    ) as mock_os:
        path = "c:\\a\\path\\"
        mock_sys.platform = "win32"
        w.open_directory_from_os(path)
        mock_os.startfile.assert_called_once_with(path)


def test_Window_open_directory_from_os_darwin():
    """
    Ensure the file explorer for OSX is called for the expected path.
    """
    w = mu.interface.main.Window()
    with mock.patch("mu.interface.main.sys") as mock_sys, mock.patch(
        "mu.interface.main.os.system"
    ) as mock_system:
        path = "/home/user/mu_code/images/"
        mock_sys.platform = "darwin"
        w.open_directory_from_os(path)
        mock_system.assert_called_once_with('open "{}"'.format(path))


def test_Window_open_directory_from_os_freedesktop():
    """
    Ensure the file explorer for FreeDesktop (Linux) is called for the
    expected path.
    """
    w = mu.interface.main.Window()
    with mock.patch("mu.interface.main.sys") as mock_sys, mock.patch(
        "mu.interface.main.os.system"
    ) as mock_system:
        path = "/home/user/mu_code/images/"
        mock_sys.platform = "linux"
        w.open_directory_from_os(path)
        mock_system.assert_called_once_with('xdg-open "{}"'.format(path))


def test_Window_open_file_event():
    """
    Ensure the open_file event is emitted when a tab's open_file is
    triggered.
    """
    editor = mu.interface.editor.EditorPane("/foo/bar.py", "baz")
    window = mu.interface.main.Window()
    window.breakpoint_toggle = mock.MagicMock()
    window.tabs = mock.MagicMock()
    window.theme = "day"
    window.button_bar = mock.MagicMock()
    window.read_only_tabs = False

    mock_emit = mock.MagicMock()
    window.open_file = mock.MagicMock()
    window.open_file.emit = mock_emit

    path = "/foo/bar.py"
    text = 'print("Hello, World!")'
    api = ["API definition"]

    mock_editor = mock.MagicMock(return_value=editor)
    with mock.patch("mu.interface.main.EditorPane", mock_editor):
        window.add_tab(path, text, api, "\n")
    mock_editor.assert_called_once_with(path, text, "\n")
    editor.open_file.emit("/foo/bar.py")
    mock_emit.assert_called_once_with("/foo/bar.py")


def test_Window_connect_find_replace():
    """
    Ensure a shortcut is created with teh expected shortcut and handler
    function.
    """
    window = mu.interface.main.Window()
    mock_handler = mock.MagicMock()
    mock_shortcut = mock.MagicMock()
    mock_sequence = mock.MagicMock()
    with mock.patch("mu.interface.main.QShortcut", mock_shortcut), mock.patch(
        "mu.interface.main.QKeySequence", mock_sequence
    ):
        window.connect_find_replace(mock_handler, "Ctrl+F")
    mock_sequence.assert_called_once_with("Ctrl+F")
    ks = mock_sequence("Ctrl+F")
    mock_shortcut.assert_called_once_with(ks, window)
    shortcut = mock_shortcut(ks, window)
    shortcut.activated.connect.assert_called_once_with(mock_handler)


def test_Window_connect_find_again():
    """
    Ensure a shortcut is created with the expected shortcut and handler
    function.
    """
    window = mu.interface.main.Window()
    mock_handlers = mock.MagicMock(), mock.MagicMock()
    mock_shortcut = mock.MagicMock()
    mock_sequence = mock.MagicMock()
    ksf = mock.MagicMock("F3")
    # ksb = mock.MagicMock("Shift+F3")
    with mock.patch("mu.interface.main.QShortcut", mock_shortcut), mock.patch(
        "mu.interface.main.QKeySequence", mock_sequence
    ):
        window.connect_find_again(mock_handlers, "F3")
    mock_sequence.assert_has_calls((mock.call("F3"), mock.call("Shift+F3")))
    shortcut = mock_shortcut(ksf, window)
    shortcut.activated.connect.assert_called_with(mock_handlers[1])
    assert shortcut.activated.connect.call_count == 2


def test_Window_show_find_replace():
    """
    The find/replace dialog is setup with the right arguments and, if
    successfully closed, returns the expected result.
    """
    window = mu.interface.main.Window()
    mock_dialog = mock.MagicMock()
    mock_dialog.find.return_value = "foo"
    mock_dialog.replace.return_value = "bar"
    mock_dialog.replace_flag.return_value = True
    mock_FRDialog = mock.MagicMock(return_value=mock_dialog)
    mock_FRDialog.exec.return_value = True
    with mock.patch("mu.interface.main.FindReplaceDialog", mock_FRDialog):
        result = window.show_find_replace("", "", False)
    mock_dialog.setup.assert_called_once_with("", "", False)
    assert result == ("foo", "bar", True)


def test_Window_replace_text_not_current_tab():
    """
    If there is currently no open tab in which to search, return 0 (to indicate
    no changes have been made).
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = None
    assert w.replace_text("foo", "bar", False) == 0


def test_Window_replace_text_not_global_found():
    """
    If the text to be replaced is found in the source, and the global_replace
    flag is false, return 1 (to indicate the number of changes made).
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.findFirst.return_value = True
    assert w.replace_text("foo", "bar", False) == 1
    mock_tab.replace.assert_called_once_with("bar")


def test_Window_replace_text_not_global_missing():
    """
    If the text to be replaced is missing in the source, and the global_replace
    flag is false, return 0 (to indicate no change made).
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    mock_tab.findFirst.return_value = False
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    assert w.replace_text("foo", "bar", False) == 0


def test_Window_replace_text_global_found():
    """
    If the text to be replaced is found several times in the source, and the
    global_replace flag is true, return X (to indicate X changes made) -- where
    X is some integer.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    mock_tab.findFirst.return_value = True
    mock_tab.findNext.side_effect = [True, False]
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    assert w.replace_text("foo", "bar", True) == 2
    assert mock_tab.replace.call_count == 2


def test_Window_replace_text_global_missing():
    """
    If the text to be replaced is missing in the source, and the global_replace
    flag is true, return 0 (to indicate no change made).
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    mock_tab.findFirst.return_value = False
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    assert w.replace_text("foo", "bar", True) == 0


def test_Window_replace_text_highlight_text_correct_selection():
    """
    Check that replace_text and highlight_text are actually highlighting text
    without regex matching.
    """
    view = mu.interface.main.Window()
    text = "ofafefifoof."
    tab = mu.interface.editor.EditorPane("path", text)
    with mock.patch("mu.interface.Window.current_tab") as current:
        current.findFirst = tab.findFirst
        view.highlight_text("f.")
        assert tab.selectedText() == "f."
        assert view.replace_text("of.", "", False)
        assert tab.selectedText() == "of."


def test_Window_highlight_text():
    """
    Given target_text, highlights the first instance via Scintilla's findFirst
    method.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    mock_tab.findFirst.return_value = True
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 0, 0
    assert w.highlight_text("foo")
    mock_tab.findFirst.assert_called_once_with(
        "foo", False, True, False, True, forward=True, index=-1, line=-1
    )


def test_Window_highlight_text_backward():
    """
    Given target_text, highlights the first instance via Scintilla's findFirst
    method.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    mock_tab.findFirst.return_value = True
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    mock_tab.getSelection.return_value = 0, 0, 0, 0
    assert w.highlight_text("foo", forward=False)
    mock_tab.findFirst.assert_called_once_with(
        "foo", False, True, False, True, forward=False, index=0, line=0
    )


def test_Window_highlight_text_no_tab():
    """
    If there's no current tab, just return False.
    """
    w = mu.interface.main.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = None
    w.tabs.currentWidget.getSelection.return_value = 0, 0, 0, 0
    assert w.highlight_text("foo") is False


def test_Window_connect_toggle_comments():
    """
    Ensure the passed in handler is connected to a shortcut triggered by the
    shortcut.
    """
    window = mu.interface.main.Window()
    mock_handler = mock.MagicMock()
    mock_shortcut = mock.MagicMock()
    mock_sequence = mock.MagicMock()
    with mock.patch("mu.interface.main.QShortcut", mock_shortcut), mock.patch(
        "mu.interface.main.QKeySequence", mock_sequence
    ):
        window.connect_toggle_comments(mock_handler, "Ctrl+K")
    mock_sequence.assert_called_once_with("Ctrl+K")
    ks = mock_sequence("Ctrl+K")
    mock_shortcut.assert_called_once_with(ks, window)
    shortcut = mock_shortcut(ks, window)
    shortcut.activated.connect.assert_called_once_with(mock_handler)


def test_Window_toggle_comments():
    """
    If there's a current tab, call its toggle_comments method.
    """
    w = mu.interface.main.Window()
    mock_tab = mock.MagicMock()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget.return_value = mock_tab
    w.toggle_comments()
    mock_tab.toggle_comments.assert_called_once_with()


def test_Window_show_hide_device_selector():
    """
    Ensure that the device_selector is shown as expected.
    """
    window = mu.interface.main.Window()
    theme = "night"
    breakpoint_toggle = mock.MagicMock()
    window.setup(breakpoint_toggle, theme)

    window.show_device_selector()
    assert not (window.status_bar.device_selector.isHidden())
    window.hide_device_selector()
    assert window.status_bar.device_selector.isHidden()
    window.show_device_selector()
    assert not (window.status_bar.device_selector.isHidden())


def test_StatusBar_init():
    """
    Ensure the status bar is set up as expected.
    """
    sb = mu.interface.main.StatusBar()
    # Default mode is set.
    assert sb.mode == "python"

    sb = mu.interface.main.StatusBar(mode="foo")
    # Pass in the default mode.
    assert sb.mode == "foo"

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
    with mock.patch("mu.interface.main.QShortcut", mock_shortcut), mock.patch(
        "mu.interface.main.QKeySequence", mock_sequence
    ):
        sb.connect_logs(handler, "Ctrl+X")
    assert sb.logs_label.mousePressEvent == handler
    mock_shortcut.assert_called_once_with(mock_sequence("Ctrl-X"), sb.parent())
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
    with mock.patch("mu.interface.main.QShortcut", mock_shortcut), mock.patch(
        "mu.interface.main.QKeySequence", mock_sequence
    ):
        sb.connect_mode(handler, "Ctrl-X")
    assert sb.mode_label.mousePressEvent == handler
    mock_shortcut.assert_called_once_with(mock_sequence("Ctrl-X"), sb.parent())
    mock_shortcut().activated.connect.assert_called_once_with(handler)


def test_StatusBar_set_message():
    """
    Ensure the default pause for displaying a message in the status bar is
    used.
    """
    sb = mu.interface.main.StatusBar()
    sb.showMessage = mock.MagicMock()
    sb.set_message("Hello")
    sb.showMessage.assert_called_once_with("Hello", 5000)
    sb.showMessage.reset_mock()
    sb.set_message("Hello", 1000)
    sb.showMessage.assert_called_once_with("Hello", 1000)


def test_StatusBar_set_mode():
    """
    Ensure the mode displayed in the status bar is correctly updated.
    """
    mode = "python"
    sb = mu.interface.main.StatusBar()
    sb.mode_label.setText = mock.MagicMock()
    sb.set_mode(mode)
    sb.mode_label.setText.assert_called_once_with(mode)


@pytest.fixture
def microbit():
    """
    Fixture for easy setup of microbit device in tests
    """
    microbit = mu.logic.Device(
        0x0D28,
        0x0204,
        "COM1",
        123456,
        "ARM",
        "BBC micro:bit",
        "microbit",
        None,
    )
    return microbit


@pytest.fixture
def adafruit_feather():
    """
    Fixture for easy setup of adafruit feather device in tests
    """
    adafruit_feather = mu.logic.Device(
        0x239A,
        0x800B,
        "COM1",
        123456,
        "ARM",
        "CircuitPython",
        "circuitpython",
        "Adafruit Feather",
    )
    return adafruit_feather


def test_StatusBar_device_connected_microbit(microbit):
    """
    Test that a message is displayed when a new device is connected
    (with no board_name set)
    """
    sb = mu.interface.main.StatusBar()
    sb.set_message = mock.MagicMock()
    sb.device_connected(microbit)
    assert sb.set_message.call_count == 1


def test_StatusBar_device_connected_adafruit_feather(adafruit_feather):
    """
    Test that a message is displayed when a new device is connected
    (with board_name set)
    """
    sb = mu.interface.main.StatusBar()
    sb.set_message = mock.MagicMock()
    sb.device_connected(adafruit_feather)
    assert sb.set_message.call_count == 1
