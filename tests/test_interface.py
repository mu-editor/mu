# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from PyQt5.QtWidgets import (QApplication, QAction, QWidget, QFileDialog,
                             QMessageBox, QLabel, QListWidget, QDialog)
from PyQt5.QtCore import QIODevice, Qt, QSize
from PyQt5.QtGui import QTextCursor, QIcon, QKeySequence
from unittest import mock
from mu import __version__
from mu.modes import PythonMode, AdafruitMode, MicrobitMode, DebugMode
import os
import platform
import mu.interface
import pytest
import keyword
import re

# Required so the QWidget tests don't abort with the message:
# "QWidget: Must construct a QApplication before a QWidget"
# The QApplication need only be instantiated once.
app = QApplication([])


def test_constants():
    """
    Ensure the expected constant values exist.
    """
    assert mu.interface.NIGHT_STYLE
    assert mu.interface.DAY_STYLE


def test_Font():
    """
    Ensure the Font class works as expected with default and passed in args.
    """
    f = mu.interface.Font()
    # Defaults
    assert f.color == 'black'
    assert f.paper == 'white'
    assert f.bold is False
    assert f.italic is False
    # Passed in arguments
    f = mu.interface.Font(color='pink', paper='black', bold=True, italic=True)
    assert f.color == 'pink'
    assert f.paper == 'black'
    assert f.bold
    assert f.italic


def test_theme_apply_to():
    """
    Ensure that the apply_to class method updates the passed in lexer with the
    expected font settings.
    """
    lexer = mu.interface.PythonLexer()
    theme = mu.interface.DayTheme()
    lexer.setFont = mock.MagicMock(return_value=None)
    lexer.setColor = mock.MagicMock(return_value=None)
    lexer.setEolFill = mock.MagicMock(return_value=None)
    lexer.setPaper = mock.MagicMock(return_value=None)
    theme.apply_to(lexer)
    assert lexer.setFont.call_count == 17
    assert lexer.setColor.call_count == 16
    assert lexer.setEolFill.call_count == 16
    assert lexer.setPaper.call_count == 16


def test_Font_loading():
    mu.interface.Font._DATABASE = None
    try:
        with mock.patch("mu.interface.QFontDatabase") as db:
            mu.interface.Font().load()
            mu.interface.Font(bold=True).load()
            mu.interface.Font(italic=True).load()
            mu.interface.Font(bold=True, italic=True).load()
    finally:
        mu.interface.Font._DATABASE = None
    db.assert_called_once_with()
    db().font.assert_has_calls([
        mock.call('Source Code Pro', 'Regular', 14),
        mock.call('Source Code Pro', 'Semibold', 14),
        mock.call('Source Code Pro', 'Italic', 14),
        mock.call('Source Code Pro', 'Semibold Italic', 14),
    ])


def test_pythonlexer_keywords():
    """
    Ensure both types of expected keywords are returned from the PythonLexer
    class.
    """
    lexer = mu.interface.PythonLexer()
    # 1 = return keywords.
    assert lexer.keywords(1) == ' '.join(keyword.kwlist + ['self', 'cls'])
    # 2 = built-in functions.
    assert lexer.keywords(2) == ' '.join(__builtins__.keys())
    # Anything else returns None.
    assert lexer.keywords(3) is None


def test_EditorPane_init():
    """
    Ensure everything is set and configured given a path and text passed into
    a new instance of the EditorPane.
    """
    mock_text = mock.MagicMock(return_value=None)
    mock_modified = mock.MagicMock(return_value=None)
    mock_configure = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.EditorPane.setText', mock_text), \
            mock.patch('mu.interface.EditorPane.setModified', mock_modified), \
            mock.patch('mu.interface.EditorPane.configure', mock_configure):
        path = '/foo/bar.py'
        text = 'print("Hello, World!")'
        mu.interface.EditorPane(path, text)
        mock_text.assert_called_once_with(text)
        mock_modified.assert_called_once_with(False)
        mock_configure.assert_called_once_with()


def test_EditorPane_configure():
    """
    Check the expected configuration takes place. NOTE - this is checking the
    expected attributes are configured, not what the actual configuration
    values may be. I.e. we're checking that, say, setIndentationWidth is
    called.
    """
    ep = mu.interface.EditorPane('/foo/bar.py', 'baz')
    ep.setFont = mock.MagicMock()
    ep.setUtf8 = mock.MagicMock()
    ep.setAutoIndent = mock.MagicMock()
    ep.setIndentationsUseTabs = mock.MagicMock()
    ep.setIndentationWidth = mock.MagicMock()
    ep.setTabWidth = mock.MagicMock()
    ep.setEdgeColumn = mock.MagicMock()
    ep.setMarginLineNumbers = mock.MagicMock()
    ep.setMarginWidth = mock.MagicMock()
    ep.setBraceMatching = mock.MagicMock()
    ep.SendScintilla = mock.MagicMock()
    ep.set_theme = mock.MagicMock()
    ep.markerDefine = mock.MagicMock()
    ep.indicatorDefine = mock.MagicMock()
    ep.setMarginSensitivity = mock.MagicMock()
    ep.setIndicatorDrawUnder = mock.MagicMock()
    ep.marginClicked = mock.MagicMock()
    ep.marginClicked.connect = mock.MagicMock()
    ep.setAnnotationDisplay = mock.MagicMock()
    ep.selectionChanged = mock.MagicMock()
    ep.selectionChanged.connect = mock.MagicMock()
    ep.configure()
    assert ep.api is None
    assert ep.setFont.call_count == 1
    assert ep.setUtf8.call_count == 1
    assert ep.setAutoIndent.call_count == 1
    assert ep.setIndentationsUseTabs.call_count == 1
    assert ep.setIndentationWidth.call_count == 1
    assert ep.setTabWidth.call_count == 1
    assert ep.setEdgeColumn.call_count == 1
    assert ep.setMarginLineNumbers.call_count == 1
    assert ep.setMarginWidth.call_count == 1
    assert ep.setBraceMatching.call_count == 1
    assert ep.SendScintilla.call_count == 1
    assert ep.set_theme.call_count == 1
    assert ep.markerDefine.call_count == 2
    assert ep.setMarginSensitivity.call_count == 2
    assert ep.setIndicatorDrawUnder.call_count == 1
    assert ep.marginClicked.connect.call_count == 1
    assert ep.setAnnotationDisplay.call_count == 1
    assert ep.selectionChanged.connect.call_count == 1
    ep.indicatorDefine.assert_has_calls(
        [mock.call(ep.SquiggleIndicator,
                   ep.check_indicators['error']['id']),
         mock.call(ep.SquiggleIndicator,
                   ep.check_indicators['style']['id']),
         mock.call(ep.StraightBoxIndicator,
                   ep.search_indicators['selection']['id'])],
        any_order=True)


def test_Editor_connect_margin():
    """
    Ensure that the passed in function is connected to the marginClick event.
    """
    mock_fn = mock.MagicMock()
    ep = mu.interface.EditorPane('/foo/bar.py', 'baz')
    ep.marginClicked = mock.MagicMock()
    ep.connect_margin(mock_fn)
    ep.marginClicked.connect.assert_called_once_with(mock_fn)


def test_EditorPane_set_theme():
    """
    Check all the expected configuration calls are made to ensure the widget's
    theme is updated.
    """
    api = ['api help text', ]
    ep = mu.interface.EditorPane('/foo/bar.py', 'baz')
    ep.lexer = mock.MagicMock()
    mock_api = mock.MagicMock()
    with mock.patch('mu.interface.QsciAPIs', return_value=mock_api) as mapi:
        ep.set_api(api)
        mapi.assert_called_once_with(ep.lexer)
        mock_api.add.assert_called_once_with('api help text')
        mock_api.prepare.assert_called_once_with()


def test_EditorPane_label():
    """
    Ensure the correct label is returned given a set of states:

    If there's a path, use the basename for the label. Otherwise it's
    "untitled".

    If the text is modified append an asterisk.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    assert ep.label == 'untitled'
    ep = mu.interface.EditorPane('/foo/bar.py', 'baz')
    assert ep.label == 'bar.py'
    ep.isModified = mock.MagicMock(return_value=True)
    assert ep.label == 'bar.py *'


def test_EditorPane_reset_annotations():
    """
    Ensure annotation state is reset.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.clearAnnotations = mock.MagicMock()
    ep.markerDeleteAll = mock.MagicMock()
    ep.reset_search_indicators = mock.MagicMock()
    ep.reset_check_indicators = mock.MagicMock()
    ep.reset_annotations()
    ep.clearAnnotations.assert_called_once_with()
    ep.markerDeleteAll.assert_called_once_with()
    ep.reset_search_indicators.assert_called_once_with()
    ep.reset_check_indicators.assert_called_once_with()


def test_EditorPane_reset_check_indicators():
    """
    Ensure code check indicators are reset.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.clearIndicatorRange = mock.MagicMock()
    ep.check_indicators = {
        'error': {
            'id': 19,
            'markers': {
                1: [{'column': 0, 'line_no': 1, 'message': 'indicator detail'}]
            },
        },
        'style': {
            'id': 20,
            'markers': {
                2: [{'code': 'x', 'column': 0, 'line_no': 1,
                     'message': 'indicator detail'}]
            }
        }
    }
    ep.reset_check_indicators()
    ep.clearIndicatorRange.assert_has_calls(
        [mock.call(1, 0, 1, 999999, 19), mock.call(1, 0, 1, 999999, 20)],
        any_order=True)
    for indicator in ep.check_indicators:
        assert ep.check_indicators[indicator]['markers'] == {}
        assert ep.check_indicators[indicator]['markers'] == {}


def test_EditorPane_reset_search_indicators():
    """
    Ensure search indicators are reset.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.clearIndicatorRange = mock.MagicMock()
    ep.search_indicators = {
        'selection': {'id': 10, 'positions': [
            {'line_start': 1, 'col_start': 2, 'line_end': 3, 'col_end': 4},
            {'line_start': 5, 'col_start': 4, 'line_end': 3, 'col_end': 2}
        ]}
    }
    ep.reset_search_indicators()
    ep.clearIndicatorRange.assert_has_calls(
        [mock.call(1, 2, 3, 4, 10), mock.call(5, 4, 3, 2, 10)],
        any_order=True)
    for indicator in ep.search_indicators:
        assert ep.search_indicators[indicator]['positions'] == []
        assert ep.search_indicators[indicator]['positions'] == []


def test_EditorPane_annotate_code():
    """
    Given a dict containing representations of feedback on the code contained
    within the EditorPane instance, ensure the correct indicators and markers
    are set.
    """
    feedback = {
        17: [{'line_no': 17,
              'message': 'Syntax error',
              'source': 'for word, pitch in words\n',
              'column': 24},
             {'line_no': 17,
              'message': 'Too many blank lines (4) above this line',
              'column': 0,
              'code': 'E303'}],
        18: [{'line_no': 18,
              'message': 'Unexpected indentation',
              'column': 4,
              'code': 'E113'}],
        21: [{'line_no': 21,
              'message': 'No newline at end of file',
              'column': 50,
              'code': 'W292'}]}
    ep = mu.interface.EditorPane(None, 'baz')
    ep.markerAdd = mock.MagicMock()
    ep.fillIndicatorRange = mock.MagicMock()
    ep.annotate_code(feedback, 'error')
    assert ep.markerAdd.call_count == 3  # once for each affected line.
    assert ep.fillIndicatorRange.call_count == 3  # once for each message.


def test_EditorPane_on_marker_clicked_on():
    """
    Ensure the annotation is shown when the marker is clicked.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.check_indicators = {
        'error': {
            'markers': {
                1: [{'message': 'a message'}, {'message': 'another message'}]
            }
        }
    }
    ep.annotation = mock.MagicMock(return_value=None)
    ep.annotate = mock.MagicMock()
    ep.get_marker_at_line = mock.MagicMock(return_value=1)
    line_no = 1
    ep.on_marker_clicked(1, line_no, None)
    ep.get_marker_at_line.assert_called_once_with(line_no)
    ep.annotation.assert_called_once_with(line_no)
    ep.annotate.assert_called_once_with(line_no, 'a message\nanother message',
                                        ep.annotationDisplay())


def test_EditorPane_on_marker_clicked_off():
    """
    Ensure the annotation is removed when the marker is clicked again.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.clearAnnotations = mock.MagicMock()
    ep.get_marker_at_line = mock.MagicMock(return_value=1)
    ep.annotation = mock.MagicMock(return_value=1)
    line_no = 1
    ep.on_marker_clicked(1, line_no, None)
    ep.clearAnnotations.assert_called_once_with(line_no)


def test_EditorPane_get_marker_at_line():
    """
    Given a line with a marker on it, will return the marker_id for it.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.check_indicators = {
        'error': {
            'markers': {
                1: [{'message': 'a message'}, {'message': 'another message'}]
            }
        }
    }
    line_no = 22
    ep.markerLine = mock.MagicMock(return_value=line_no)
    assert ep.get_marker_at_line(line_no) == 1


def test_EditorPane_find_next_match():
    """
    Ensures that the expected arg values are passed through to QsciScintilla
    for highlighting matched text.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.findFirst = mock.MagicMock(return_value=True)
    assert ep.find_next_match('foo', from_line=10, from_col=5,
                              case_sensitive=True, wrap_around=False)
    ep.findFirst.assert_called_once_with('foo', False, True, True, False,
                                         forward=True, line=10, index=5,
                                         show=False, posix=False)


def _ranges_in_text(text, search_for):
    """Find any instances of `search_for` inside text and return the equivalent
    Scintilla Ranges of (line_start, column_start, line_end, column_end).
    For now, we'll ignore the possibility of multi-line ranges which are
    certainly supported within Scintilla.

    NB Scintilla appears to use exclusive bounds at both ends, so
    for the text 'foo bar', 'foo' will give (0, 0, 0, 3).
    """
    for n_line, line in enumerate(text.splitlines()):
        for match in re.finditer(search_for, line):
            yield n_line, match.start(), n_line, match.end()


def test_EditorPane_highlight_selected_matches_no_selection():
    """
    Ensure that if the current selection is empty then all highlights
    are cleared.

    There's no API for determining which highlighted regions are present
    in the edit control, so we use the selection indicators structure
    as a proxy for the indicators set.
    """
    text = "foo bar foo"

    ep = mu.interface.EditorPane(None, 'baz')
    ep.setText(text)
    ep.setSelection(-1, -1, -1, -1)
    assert ep.search_indicators['selection']['positions'] == []


def test_EditorPane_highlight_selected_spans_two_or_more_lines():
    """
    Ensure that if the current selection spans two or more lines then all
    highlights are cleared.

    There's no API for determining which highlighted regions are present
    in the edit control, so we use the selection indicators structure
    as a proxy for the indicators set.
    """
    text = "foo\nbar\nfoo"

    ep = mu.interface.EditorPane(None, 'baz')
    ep.setText(text)
    ep.setSelection(0, 0, 1, 1)
    assert ep.search_indicators['selection']['positions'] == []


def test_EditorPane_highlight_selected_matches_multi_word():
    """
    Ensure that if the current selection is not a single word then don't cause
    a search/highlight call.

    There's no API for determining which highlighted regions are present
    in the edit control, so we use the selection indicators structure
    as a proxy for the indicators set.
    """
    text = "foo bar foo"
    search_for = "foo bar"

    ep = mu.interface.EditorPane(None, 'baz')
    ep.setText(text)
    for range in _ranges_in_text(text, search_for):
        break

    ep.setSelection(*range)
    assert ep.search_indicators['selection']['positions'] == []


def test_EditorPane_highlight_selected_matches_with_match():
    """
    Ensure that if the current selection is a single word then it causes the
    expected search/highlight call.

    There appears to be no way to iterate over indicators within the editor.
    So we're using the search_indicators structure as a proxy
    """
    text = "foo bar foo baz foo"
    search_for = "foo"

    ep = mu.interface.EditorPane(None, 'baz')
    ep.setText(text)

    #
    # Determine what ranges would be found and highlighted and arbitrarily
    # use the last one for the selection
    #
    expected_ranges = []
    selected_range = None
    for range in _ranges_in_text(text, search_for):
        if selected_range is None:
            selected_range = range
        else:
            (line_start, col_start, line_end, col_end) = range
            expected_ranges.append(
                dict(
                    line_start=line_start, col_start=col_start,
                    line_end=line_end, col_end=col_end
                )
            )

    ep.setSelection(*selected_range)
    assert ep.search_indicators['selection']['positions'] == expected_ranges


def test_EditorPane_highlight_selected_matches_incomplete_word():
    """
    Ensure that if the current selection is not a complete word
    then no ranges are highlighted.

    There appears to be no way to iterate over indicators within the editor.
    So we're using the search_indicators structure as a proxy
    """
    text = "foo bar foo baz foo"
    search_for = "fo"

    ep = mu.interface.EditorPane(None, 'baz')
    ep.setText(text)
    for range in _ranges_in_text(text, search_for):
        ep.setSelection(*range)
        break

    assert ep.search_indicators['selection']['positions'] == []


def test_EditorPane_highlight_selected_matches_cursor_remains():
    """
    Ensure that if a selection is made, the text cursor remains in the
    same place after any matching terms have been highlighted.

    NB Since this is testing an interaction between our code and
    the QScintilla control, there is no way to mock this behaviour.
    """
    text = "foo bar foo"
    search_for = "foo"
    ep = mu.interface.EditorPane(None, 'baz')
    ep.setText(text)

    select_n_chars = 2

    #
    # Find the first of the matching words
    # Place the cursor at the right-hand end of the match
    # Extend the selection back a number of characters
    # Confirm that the cursor is correctly that many characters back from
    #   the end of the matching text (ie that it hasn't been reset)
    #
    for line0, index0, line1, index1 in _ranges_in_text(text, search_for):
        break
    ep.setCursorPosition(line1, index1)
    for i in range(select_n_chars):
        ep.SendScintilla(mu.interface.QsciScintilla.SCI_CHARLEFTEXTEND)
    assert ep.getCursorPosition() == (line1, index1 - select_n_chars)


def test_EditorPane_selection_change_listener():
    """
    Enusure that is there is a change to the selected text then controll is
    passed to highlight_selected_matches.
    """
    ep = mu.interface.EditorPane(None, 'baz')
    ep.getSelection = mock.MagicMock(return_value=(1, 1, 2, 2))
    ep.highlight_selected_matches = mock.MagicMock()
    ep.selection_change_listener()
    assert ep.previous_selection['line_start'] == 1
    assert ep.previous_selection['col_start'] == 1
    assert ep.previous_selection['line_end'] == 2
    assert ep.previous_selection['col_end'] == 2
    assert ep.highlight_selected_matches.call_count == 1


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
    with mock.patch('mu.interface.ButtonBar.setMovable', mock_movable), \
            mock.patch('mu.interface.ButtonBar.setIconSize', mock_icon_size), \
            mock.patch('mu.interface.ButtonBar.setToolButtonStyle',
                       mock_tool_button_size), \
            mock.patch('mu.interface.ButtonBar.setContextMenuPolicy',
                       mock_context_menu_policy), \
            mock.patch('mu.interface.ButtonBar.setObjectName',
                       mock_object_name), \
            mock.patch('mu.interface.ButtonBar.reset', mock_reset):
        mu.interface.ButtonBar(None)
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
    with mock.patch('mu.interface.ButtonBar.clear', mock_clear):
        b = mu.interface.ButtonBar(None)
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
    with mock.patch('mu.interface.ButtonBar.reset', mock_reset), \
            mock.patch('mu.interface.ButtonBar.addAction', mock_add_action), \
            mock.patch('mu.interface.ButtonBar.addSeparator',
                       mock_add_separator):
        b = mu.interface.ButtonBar(None)
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
    with mock.patch('mu.interface.ButtonBar.setIconSize', mock_icon_size):
        bb = mu.interface.ButtonBar(None)
        bb.setStyleSheet = mock.MagicMock()
        bb.set_responsive_mode(1024, 800)
        mock_icon_size.assert_called_with(QSize(64, 64))
        default_font = str(mu.interface.DEFAULT_FONT_SIZE)
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
    bb = mu.interface.ButtonBar(None)
    with mock.patch('builtins.super') as mock_s:
        bb.addAction('save', 'Save', 'save stuff')
        mock_s.assert_called_once_with()
    assert 'save' in bb.slots
    assert isinstance(bb.slots['save'], QAction)


def test_ButtonBar_connect():
    """
    Check the named slot is connected to the slot handler.
    """
    bb = mu.interface.ButtonBar(None)
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
    with mock.patch('mu.interface.FileTabs.setTabsClosable') as mstc, \
            mock.patch('mu.interface.FileTabs.tabCloseRequested') as mtcr, \
            mock.patch('mu.interface.FileTabs.currentChanged') as mcc:
        qtw = mu.interface.FileTabs()
        mstc.assert_called_once_with(True)
        mtcr.connect.assert_called_once_with(qtw.removeTab)
        mcc.connect.assert_called_once_with(qtw.change_tab)


def test_FileTabs_removeTab_cancel():
    """
    Ensure removeTab asks the user for confirmation if there is a modification
    to the tab. If "cancel" is selected, the parent removeTab is NOT called.
    """
    qtw = mu.interface.FileTabs()
    mock_window = mock.MagicMock()
    mock_window.show_confirmation.return_value = QMessageBox.Cancel
    mock_window.current_tab.isModified.return_value = True
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    with mock.patch('mu.interface.QTabWidget.removeTab',
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
    qtw = mu.interface.FileTabs()
    mock_window = mock.MagicMock()
    mock_window.show_confirmation.return_value = QMessageBox.Ok
    mock_window.current_tab.isModified.return_value = True
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    tab_id = 1
    with mock.patch('mu.interface.QTabWidget.removeTab',
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
    qtw = mu.interface.FileTabs()
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
    qtw = mu.interface.FileTabs()
    qtw.widget = mock.MagicMock(return_value=None)
    mock_window = mock.MagicMock()
    qtw.nativeParentWidget = mock.MagicMock(return_value=mock_window)
    qtw.change_tab(0)
    mock_window.update_title.assert_called_once_with(None)


def test_Window_attributes():
    """
    Expect the title and icon to be set correctly.
    """
    w = mu.interface.Window()
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
    w = mu.interface.Window()
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
    with mock.patch('mu.interface.ModeSelector', mock_mode_selector):
        w = mu.interface.Window()
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
    with mock.patch('mu.interface.ModeSelector', mock_mode_selector):
        w = mu.interface.Window()
        result = w.select_mode(mock_modes, current_mode, 'day')
        assert result is None


def test_Window_change_mode():
    """
    Ensure the change of mode is made by the button_bar.
    """
    mock_mode = mock.MagicMock()
    api = ['API details', ]
    mock_mode.api.return_value = api
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    w._zoom_in = mock.MagicMock()
    w._zoom_in.emit = mock.MagicMock()
    w.zoom_in()
    w._zoom_in.emit.assert_called_once_with(2)


def test_Window_zoom_out():
    """
    Ensure the correct signal is emitted.
    """
    w = mu.interface.Window()
    w._zoom_out = mock.MagicMock()
    w._zoom_out.emit = mock.MagicMock()
    w.zoom_out()
    w._zoom_out.emit.assert_called_once_with(2)


def test_Window_connect_zoom():
    """
    Ensure the zoom in/out signals are connected to the passed in widget's
    zoomIn and zoomOut handlers.
    """
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value='foo')
    assert w.current_tab == 'foo'


def test_Window_set_read_only():
    """
    Ensure all the tabs have the setReadOnly method set to the boolean passed
    into set_read_only.
    """
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    w.widget = mock.MagicMock()
    with mock.patch('mu.interface.QFileDialog', mock_fd):
        assert w.get_load_path('micropython') == path
    mock_fd.getOpenFileName.assert_called_once_with(w.widget, 'Open file',
                                                    'micropython',
                                                    '*.py *.hex')


def test_Window_get_save_path():
    """
    Ensure the QFileDialog is called with the expected arguments and the
    resulting path is returned.
    """
    mock_fd = mock.MagicMock()
    path = '/foo/bar.py'
    mock_fd.getSaveFileName = mock.MagicMock(return_value=(path, True))
    w = mu.interface.Window()
    w.widget = mock.MagicMock()
    with mock.patch('mu.interface.QFileDialog', mock_fd):
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
    w = mu.interface.Window()
    w.widget = mock.MagicMock()
    with mock.patch('mu.interface.QFileDialog', mock_fd):
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
    w = mu.interface.Window()
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
    ep = mu.interface.EditorPane('/foo/bar.py', 'baz')
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
    with mock.patch('mu.interface.EditorPane', mock_ed):
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
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    assert w.tab_count == 2
    w.tabs.count.assert_called_once_with()


def test_Window_widgets():
    """
    Ensure a list derived from calls to Window.tabs.widget(i) is returned.
    """
    w = mu.interface.Window()
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
    w = mu.interface.Window()
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


def test_Window_add_filesystem():
    """
    Ensure the expected settings are updated when adding a file system pane.
    """
    w = mu.interface.Window()
    w.theme = mock.MagicMock()
    w.splitter = mock.MagicMock()
    w.addDockWidget = mock.MagicMock(return_value=None)
    w.connect_zoom = mock.MagicMock(return_value=None)
    mock_fs = mock.MagicMock()
    mock_fs.setFocus = mock.MagicMock(return_value=None)
    mock_fs_class = mock.MagicMock(return_value=mock_fs)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch('mu.interface.FileSystemPane', mock_fs_class), \
            mock.patch('mu.interface.QDockWidget', mock_dock_class):
        w.add_filesystem('path/to/home')
    mock_fs_class.assert_called_once_with('path/to/home')
    assert w.fs_pane == mock_fs
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)
    mock_fs.setFocus.assert_called_once_with()
    w.connect_zoom.assert_called_once_with(mock_fs)


def test_Window_add_micropython_repl():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    MicroPython based REPL.
    """
    w = mu.interface.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.add_repl = mock.MagicMock()
    mock_repl = mock.MagicMock()
    mock_repl_class = mock.MagicMock(return_value=mock_repl)
    mock_repl_arg = mock.MagicMock()
    mock_repl_arg.port = mock.MagicMock('COM0')
    with mock.patch('mu.interface.MicroPythonREPLPane', mock_repl_class):
        w.add_micropython_repl(mock_repl_arg, 'Test REPL')
    mock_repl_class.assert_called_once_with(port=mock_repl_arg.port,
                                            theme=w.theme)
    w.add_repl.assert_called_once_with(mock_repl, 'Test REPL')


def test_Window_add_jupyter_repl():
    """
    Ensure the expected object is instantiated and add_repl is called for a
    Jupyter based REPL.
    """
    w = mu.interface.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.add_repl = mock.MagicMock()
    mock_repl = mock.MagicMock()
    mock_kernel = mock.MagicMock()
    mock_kernel_client = mock.MagicMock()
    mock_repl.kernel = mock_kernel
    mock_repl.client.return_value = mock_kernel_client
    mock_pane = mock.MagicMock()
    mock_pane_class = mock.MagicMock(return_value=mock_pane)
    with mock.patch('mu.interface.JupyterREPLPane', mock_pane_class):
        w.add_jupyter_repl(mock_repl)
    mock_pane_class.assert_called_once_with(theme=w.theme)
    assert mock_pane.kernel_manager == mock_repl
    assert mock_pane.kernel_client == mock_kernel_client
    assert mock_kernel.gui == 'qt4'
    w.add_repl.assert_called_once_with(mock_pane, 'Python3 (Jupyter)')


def test_Window_add_repl():
    """
    Ensure the expected settings are updated.
    """
    w = mu.interface.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.addDockWidget = mock.MagicMock()
    mock_repl_pane = mock.MagicMock()
    mock_repl_pane.setFocus = mock.MagicMock(return_value=None)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    with mock.patch('mu.interface.QDockWidget'), \
            mock.patch('mu.interface.QDockWidget', mock_dock_class):
        w.add_repl(mock_repl_pane, 'Test REPL')
    assert w.repl_pane == mock_repl_pane
    mock_repl_pane.setFocus.assert_called_once_with()
    w.connect_zoom.assert_called_once_with(mock_repl_pane)
    w.addDockWidget.assert_called_once_with(Qt.BottomDockWidgetArea, mock_dock)


def test_Window_add_python3_runner():
    """
    Ensure a Python 3 runner (to capture stdin/out/err) is displayed correctly.
    """
    w = mu.interface.Window()
    w.theme = mock.MagicMock()
    w.connect_zoom = mock.MagicMock(return_value=None)
    w.addDockWidget = mock.MagicMock()
    mock_process_runner = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process_runner)
    mock_dock = mock.MagicMock()
    mock_dock_class = mock.MagicMock(return_value=mock_dock)
    name = 'foo'
    path = 'bar'
    with mock.patch('mu.interface.PythonProcessPane', mock_process_class), \
            mock.patch('mu.interface.QDockWidget', mock_dock_class):
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
    w = mu.interface.Window()
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
    with mock.patch('mu.interface.DebugInspector',
                    mock_debug_inspector_class), \
            mock.patch('mu.interface.QStandardItemModel', mock_model_class), \
            mock.patch('mu.interface.QDockWidget', mock_dock_class):
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
    w = mu.interface.Window()
    w.debug_model = mock.MagicMock()
    mock_standard_item = mock.MagicMock()
    with mock.patch('mu.interface.QStandardItem', mock_standard_item):
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
    w = mu.interface.Window()
    w.debug_model = mock.MagicMock()
    mock_standard_item = mock.MagicMock()
    mock_eval = mock.MagicMock(side_effect=Exception('BOOM!'))
    with mock.patch('mu.interface.QStandardItem', mock_standard_item), \
            mock.patch('mu.interface.eval', mock_eval):
        w.update_debug_inspector(locals_dict)
    # You just have to believe this is correct. I checked! :-)
    assert mock_standard_item.call_count == 2


def test_Window_remove_filesystem():
    """
    Check all the necessary calls to remove / reset the file system pane are
    made.
    """
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    mock_repl = mock.MagicMock()
    mock_repl.setParent = mock.MagicMock(return_value=None)
    mock_repl.deleteLater = mock.MagicMock(return_value=None)
    w.repl = mock_repl
    w.remove_repl()
    mock_repl.setParent.assert_called_once_with(None)
    mock_repl.deleteLater.assert_called_once_with()
    assert w.repl is None


def test_Window_remove_python_runner():
    """
    Check all the necessary calls to remove / reset the Python3 runner are
    made.
    """
    w = mu.interface.Window()
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
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    w.setStyleSheet = mock.MagicMock(return_value=None)
    w.tabs = mock.MagicMock()
    w.tabs.count = mock.MagicMock(return_value=2)
    tab1 = mock.MagicMock()
    tab1.set_theme = mock.MagicMock()
    tab2 = mock.MagicMock()
    tab2.set_theme = mock.MagicMock()
    w.tabs.widget = mock.MagicMock(side_effect=[tab1, tab2])
    w.button_bar = mock.MagicMock()
    w.button_bar.slots = {
        'theme': mock.MagicMock()
    }
    w.button_bar.slots['theme'].setIcon = mock.MagicMock(return_value=None)
    w.repl = mock.MagicMock()
    w.repl_pane = mock.MagicMock()
    w.repl_pane.set_theme = mock.MagicMock()
    w.set_theme('night')
    assert w.setStyleSheet.call_count == 2
    assert w.theme == 'night'
    tab1.set_theme.assert_called_once_with(mu.interface.NightTheme)
    tab2.set_theme.assert_called_once_with(mu.interface.NightTheme)
    w.button_bar.slots['theme'].setIcon.asser_called_once()
    assert isinstance(w.button_bar.slots['theme'].setIcon.call_args[0][0],
                      QIcon)
    w.repl_pane.set_theme.assert_called_once_with('night')


def test_Window_show_logs():
    """
    Ensure the modal widget for showing the log file is correctly configured.
    """
    mock_log_display = mock.MagicMock()
    mock_log_box = mock.MagicMock()
    mock_log_display.return_value = mock_log_box
    with mock.patch('mu.interface.LogDisplay', mock_log_display):
        w = mu.interface.Window()
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
    w = mu.interface.Window()
    message = 'foo'
    information = 'bar'
    icon = 'Information'
    with mock.patch('mu.interface.QMessageBox', mock_qmb_class):
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
    w = mu.interface.Window()
    message = 'foo'
    with mock.patch('mu.interface.QMessageBox', mock_qmb_class):
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
    w = mu.interface.Window()
    message = 'foo'
    information = 'bar'
    icon = 'Information'
    with mock.patch('mu.interface.QMessageBox', mock_qmb_class):
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
    w = mu.interface.Window()
    message = 'foo'
    with mock.patch('mu.interface.QMessageBox', mock_qmb_class):
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
    w = mu.interface.Window()
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
    w = mu.interface.Window()
    w.resize = mock.MagicMock(return_value=None)
    mock_size = mock.MagicMock()
    mock_size.width = mock.MagicMock(return_value=819)
    mock_size.height = mock.MagicMock(return_value=614)
    w.geometry = mock.MagicMock(return_value=mock_size)
    w.move = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.QDesktopWidget', mock_qdw):
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
    w = mu.interface.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value=tab)
    w.reset_annotations()
    tab.reset_annotations.assert_called_once_with()


def test_Window_annotate_code():
    """
    Ensure the current tab is annotated with the passed in feedback.
    """
    tab = mock.MagicMock()
    w = mu.interface.Window()
    w.tabs = mock.MagicMock()
    w.tabs.currentWidget = mock.MagicMock(return_value=tab)
    feedback = 'foo'
    w.annotate_code(feedback, 'error')
    tab.annotate_code.assert_called_once_with(feedback, 'error')


def test_Window_setup():
    """
    Ensures the various default attributes of the window are set to the
    expected value.
    """
    w = mu.interface.Window()
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
    with mock.patch('mu.interface.QWidget', mock_widget_class), \
            mock.patch('mu.interface.ButtonBar', mock_button_bar_class), \
            mock.patch('mu.interface.FileTabs', mock_qtw_class):
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
    w = mu.interface.Window()
    mock_timer = mock.MagicMock()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_callback = mock.MagicMock()
    with mock.patch('mu.interface.QTimer', mock_timer_class):
        w.set_usb_checker(1, mock_callback)
        assert w.usb_checker == mock_timer
        w.usb_checker.timeout.connect.assert_called_once_with(mock_callback)
        w.usb_checker.start.assert_called_once_with(1000)


def test_Window_set_timer():
    """
    Ensure a repeating timer with the referenced callback is created.
    """
    w = mu.interface.Window()
    mock_timer = mock.MagicMock()
    mock_timer_class = mock.MagicMock(return_value=mock_timer)
    mock_callback = mock.MagicMock()
    with mock.patch('mu.interface.QTimer', mock_timer_class):
        w.set_timer(5, mock_callback)
        assert w.timer == mock_timer
        w.timer.timeout.connect.assert_called_once_with(mock_callback)
        w.timer.start.assert_called_once_with(5 * 1000)


def test_Window_stop_timer():
    """
    Ensure the timer is stopped and destroyed.
    """
    mock_timer = mock.MagicMock()
    w = mu.interface.Window()
    w.timer = mock_timer
    w.stop_timer()
    assert w.timer is None
    mock_timer.stop.assert_called_once_with()


def test_MicroPythonREPLPane_init_default_args():
    """
    Ensure the MicroPython REPLPane object is instantiated as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
    assert mock_serial_class.call_count == 1
    mock_serial.setPortName.assert_called_once_with('COM0')
    mock_serial.setBaudRate.assert_called_once_with(115200)
    mock_serial.open.assert_called_once_with(QIODevice.ReadWrite)
    mock_serial.readyRead.connect.assert_called_once_with(rp.on_serial_read)
    mock_serial.write.assert_called_once_with(b'\x03')


def test_MicroPythonREPLPane_init_cannot_open():
    """
    If serial.open fails raise an IOError.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=False)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        with pytest.raises(IOError):
            mu.interface.MicroPythonREPLPane('COM0')


def test_MicroPythonREPLPane_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = 'paste me!'
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        with mock.patch('mu.interface.QApplication', mock_application):
            rp = mu.interface.MicroPythonREPLPane('COM0')
            mock_serial.write.reset_mock()
            rp.paste()
    mock_serial.write.assert_called_once_with(bytes('paste me!', 'utf8'))


def test_MicroPythonREPLPane_paste_only_works_if_there_is_something_to_paste():
    """
    Pasting into the REPL should send bytes via the serial connection.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_clipboard = mock.MagicMock()
    mock_clipboard.text.return_value = ''
    mock_application = mock.MagicMock()
    mock_application.clipboard.return_value = mock_clipboard
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        with mock.patch('mu.interface.QApplication', mock_application):
            rp = mu.interface.MicroPythonREPLPane('COM0')
            mock_serial.write.reset_mock()
            rp.paste()
    assert mock_serial.write.call_count == 0


def test_MicroPythonREPLPane_context_menu():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'WinNT'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class), \
            mock.patch('mu.interface.platform', mock_platform), \
            mock.patch('mu.interface.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.QCursor'):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == 'Copy'
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == 'Ctrl+Shift+C'
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == 'Paste'
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == 'Ctrl+Shift+V'
    assert mock_qmenu.exec_.call_count == 1


def test_MicroPythonREPLPane_context_menu_darwin():
    """
    Ensure the context menu for the REPL is configured correctly for non-OSX
    platforms.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readyRead = mock.MagicMock()
    mock_serial.readyRead.connect = mock.MagicMock(return_value=None)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_platform = mock.MagicMock()
    mock_platform.system.return_value = 'Darwin'
    mock_qmenu = mock.MagicMock()
    mock_qmenu_class = mock.MagicMock(return_value=mock_qmenu)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class), \
            mock.patch('mu.interface.platform', mock_platform), \
            mock.patch('mu.interface.QMenu', mock_qmenu_class), \
            mock.patch('mu.interface.QCursor'):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.context_menu()
    assert mock_qmenu.addAction.call_count == 2
    copy_action = mock_qmenu.addAction.call_args_list[0][0]
    assert copy_action[0] == 'Copy'
    assert copy_action[1] == rp.copy
    assert copy_action[2].toString() == 'Ctrl+C'
    paste_action = mock_qmenu.addAction.call_args_list[1][0]
    assert paste_action[0] == 'Paste'
    assert paste_action[1] == rp.paste
    assert paste_action[2].toString() == 'Ctrl+V'
    assert mock_qmenu.exec_.call_count == 1


def test_MicroPythonREPLPane_cursor_to_end():
    """
    Ensure the cursor is set to the very end of the available text using the
    appropriate Qt related magic.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_text_cursor = mock.MagicMock()
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.textCursor = mock.MagicMock(return_value=mock_text_cursor)
        rp.setTextCursor = mock.MagicMock()
        rp.cursor_to_end()
        mock_text_cursor.movePosition.assert_called_once_with(QTextCursor.End)
        rp.setTextCursor.assert_called_once_with(mock_text_cursor)


def test_MicroPythonREPLPane_set_theme():
    """
    Ensure the set_theme toggles as expected.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.setStyleSheet = mock.MagicMock(return_value=None)
        rp.set_theme('day')
        rp.setStyleSheet.assert_called_once_with(mu.interface.DAY_STYLE)
        rp.setStyleSheet.reset_mock()
        rp.set_theme('night')
        rp.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_MicroPythonREPLPane_on_serial_read():
    """
    Ensure the method calls process_bytes.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.readAll = mock.MagicMock(return_value='abc'.encode('utf-8'))
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.process_bytes = mock.MagicMock()
        rp.on_serial_read()
        rp.process_bytes.assert_called_once_with(bytes('abc'.encode('utf-8')))


def test_MicroPythonREPLPane_keyPressEvent():
    """
    Ensure key presses in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_A)
        data.text = mock.MagicMock(return_value='a')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(bytes('a', 'utf-8'))


def test_MicroPythonREPLPane_keyPressEvent_backspace():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
        data.text = mock.MagicMock(return_value='\b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\b')


def test_MicroPythonREPLPane_keyPressEvent_up():
    """
    Ensure up arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Up)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[A')


def test_MicroPythonREPLPane_keyPressEvent_down():
    """
    Ensure down arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Down)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[B')


def test_MicroPythonREPLPane_keyPressEvent_right():
    """
    Ensure right arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Right)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[C')


def test_MicroPythonREPLPane_keyPressEvent_left():
    """
    Ensure left arrows in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Left)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[D')


def test_MicroPythonREPLPane_keyPressEvent_home():
    """
    Ensure home key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_Home)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[H')


def test_MicroPythonREPLPane_keyPressEvent_end():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_End)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers = mock.MagicMock(return_value=None)
        rp.keyPressEvent(data)
        mock_serial.write.assert_called_once_with(b'\x1B[F')


def test_MicroPythonREPLPane_keyPressEvent_CTRL_C_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.copy = mock.MagicMock()
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_C)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
        rp.keyPressEvent(data)
        rp.copy.assert_called_once_with()


def test_MicroPythonREPLPane_keyPressEvent_CTRL_V_Darwin():
    """
    Ensure end key in the REPL is handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.paste = mock.MagicMock()
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_V)
        data.text = mock.MagicMock(return_value='1b')
        data.modifiers.return_value = Qt.ControlModifier | Qt.ShiftModifier
        rp.keyPressEvent(data)
        rp.paste.assert_called_once_with()


def test_MicroPythonREPLPane_keyPressEvent_meta():
    """
    Ensure backspaces in the REPL are handled correctly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial.write = mock.MagicMock(return_value=None)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        mock_serial.write.reset_mock()  # write is called during __init__()
        data = mock.MagicMock
        data.key = mock.MagicMock(return_value=Qt.Key_M)
        data.text = mock.MagicMock(return_value='a')
        if platform.system() == 'Darwin':
            data.modifiers = mock.MagicMock(return_value=Qt.MetaModifier)
        else:
            data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier)
        rp.keyPressEvent(data)
        expected = 1 + Qt.Key_M - Qt.Key_A
        mock_serial.write.assert_called_once_with(bytes([expected]))


def test_MicroPythonREPLPane_process_bytes():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. Backspace is enacted, carriage-return is ignored, newline moves
    the cursor position to the end of the line before enacted and all others
    are simply inserted.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(side_effect=[True, False, True,
                                                       True])
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.textCursor = mock.MagicMock(return_value=mock_tc)
        rp.setTextCursor = mock.MagicMock(return_value=None)
        rp.insertPlainText = mock.MagicMock(return_value=None)
        rp.ensureCursorVisible = mock.MagicMock(return_value=None)
        bs = bytes([8, 13, 10, 65, ])  # \b, \r, \n, 'A'
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


def test_MicroPythonREPLPane_process_bytes_VT100():
    """
    Ensure bytes coming from the device to the application are processed as
    expected. In this case, make sure VT100 related codes are handled properly.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    mock_tc = mock.MagicMock()
    mock_tc.movePosition = mock.MagicMock(return_value=False)
    mock_tc.removeSelectedText = mock.MagicMock()
    mock_tc.deleteChar = mock.MagicMock(return_value=None)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.textCursor = mock.MagicMock(return_value=mock_tc)
        rp.setTextCursor = mock.MagicMock(return_value=None)
        rp.insertPlainText = mock.MagicMock(return_value=None)
        rp.ensureCursorVisible = mock.MagicMock(return_value=None)
        bs = bytes([
            27, 91, ord('1'), ord('A'),  # <Esc>[1A
            27, 91, ord('1'), ord('B'),  # <Esc>[1B
            27, 91, ord('1'), ord('C'),  # <Esc>[1C
            27, 91, ord('1'), ord('D'),  # <Esc>[1D
            27, 91, ord('K'),  # <Esc>[K
        ])
        rp.process_bytes(bs)
        rp.textCursor.assert_called_once_with()
        assert mock_tc.movePosition.call_count == 6
        assert mock_tc.movePosition.call_args_list[0][0][0] == QTextCursor.Down
        assert mock_tc.movePosition.call_args_list[1][0][0] == QTextCursor.Up
        assert mock_tc.movePosition.call_args_list[2][0][0] == QTextCursor.Down
        assert mock_tc.movePosition.call_args_list[3][0][0] == \
            QTextCursor.Right
        assert mock_tc.movePosition.call_args_list[4][0][0] == QTextCursor.Left
        assert mock_tc.movePosition.call_args_list[5][0][0] == \
            QTextCursor.EndOfLine
        assert mock_tc.movePosition.call_args_list[5][1]['mode'] == \
            QTextCursor.KeepAnchor
        assert rp.setTextCursor.call_count == 5
        assert rp.setTextCursor.call_args_list[0][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[1][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[2][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[3][0][0] == mock_tc
        assert rp.setTextCursor.call_args_list[4][0][0] == mock_tc
        mock_tc.removeSelectedText.assert_called_once_with()
        rp.ensureCursorVisible.assert_called_once_with()


def test_MicroPythonREPLPane_clear():
    """
    Ensure setText is called with an empty string.
    """
    mock_serial = mock.MagicMock()
    mock_serial.setPortName = mock.MagicMock(return_value=None)
    mock_serial.setBaudRate = mock.MagicMock(return_value=None)
    mock_serial.open = mock.MagicMock(return_value=True)
    mock_serial_class = mock.MagicMock(return_value=mock_serial)
    with mock.patch('mu.interface.QSerialPort', mock_serial_class):
        rp = mu.interface.MicroPythonREPLPane('COM0')
        rp.setText = mock.MagicMock(return_value=None)
        rp.clear()
        rp.setText.assert_called_once_with('')


def test_MuFileList_disable():
    """
    Disable and block drops on the current and sibling MuFileList.
    """
    mock_sibling = mock.MagicMock()
    mfl = mu.interface.MuFileList()
    mfl.setDisabled = mock.MagicMock(return_value=True)
    mfl.setAcceptDrops = mock.MagicMock(return_value=True)
    mfl.disable(mock_sibling)
    mfl.setDisabled.assert_called_once_with(True)
    mock_sibling.setDisabled.assert_called_once_with(True)
    mfl.setAcceptDrops.assert_called_once_with(False)
    mock_sibling.setAcceptDrops.assert_called_once_with(False)


def test_MuFileList_enable():
    """
    Allow drops and interactions with current and sibling MuFileList.
    """
    mock_sibling = mock.MagicMock()
    mfl = mu.interface.MuFileList()
    mfl.setDisabled = mock.MagicMock(return_value=True)
    mfl.setAcceptDrops = mock.MagicMock(return_value=True)
    mfl.enable(mock_sibling)
    mfl.setDisabled.assert_called_once_with(False)
    mock_sibling.setDisabled.assert_called_once_with(False)
    mfl.setAcceptDrops.assert_called_once_with(True)
    mock_sibling.setAcceptDrops.assert_called_once_with(True)


def test_MuFileList_show_confirm_overwrite_dialog():
    """
    """
    mfl = mu.interface.MuFileList()
    mock_qmb = mock.MagicMock()
    mock_qmb.setIcon = mock.MagicMock(return_value=None)
    mock_qmb.setText = mock.MagicMock(return_value=None)
    mock_qmb.setWindowTitle = mock.MagicMock(return_value=None)
    mock_qmb.exec_ = mock.MagicMock(return_value=QMessageBox.Ok)
    mock_qmb_class = mock.MagicMock(return_value=mock_qmb)
    mock_qmb_class.Ok = QMessageBox.Ok
    mock_qmb_class.Information = QMessageBox.Information
    with mock.patch('mu.interface.QMessageBox', mock_qmb_class):
        assert mfl.show_confirm_overwrite_dialog()
    msg = 'File already exists; overwrite it?'
    mock_qmb.setText.assert_called_once_with(msg)
    mock_qmb.setWindowTitle.assert_called_once_with('File already exists')
    mock_qmb.setIcon.assert_called_once_with(QMessageBox.Information)


def test_MicrobitFileList_init():
    """
    Check the widget references the user's home and allows drag and drop.
    """
    mfs = mu.interface.MicrobitFileList('home/path')
    assert mfs.home == 'home/path'
    assert mfs.dragDropMode() == mfs.DragDrop


def test_MicrobitFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.LocalFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mfs = mu.interface.MicrobitFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.enable = mock.MagicMock()
    mfs.parent = mock.MagicMock()
    with mock.patch('mu.interface.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.MuFileList.dropEvent',
                       return_value=None) as mock_dropEvent, \
            mock.patch('mu.interface.microfs.put',
                       return_value=True) as mock_put:
        mfs.dropEvent(mock_event)
        mfs.disable.assert_called_once_with(source)
        home = os.path.join('homepath', 'foo.py')
        mock_put.assert_called_once_with(mock_serial, home)
        mock_dropEvent.assert_called_once_with(mock_event)
        mfs.enable.assert_called_once_with(source)
        mfs.parent().ls.assert_called_once_with()


def test_MicrobitFileList_dropEvent_error():
    """
    Ensure that if an error occurs there is no change in the file list state.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.LocalFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mfs = mu.interface.MicrobitFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.enable = mock.MagicMock()
    ex = IOError('BANG')
    with mock.patch('mu.interface.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.microfs.put', side_effect=ex), \
            mock.patch('mu.interface.logger.error', return_value=None) as log:
        mfs.dropEvent(mock_event)
        log.assert_called_once_with(ex)
        mfs.disable.assert_called_once_with(source)
        mfs.enable.assert_called_once_with(source)


def test_MicrobitFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    mfs = mu.interface.MicrobitFileList('homepath')
    mfs.disable = mock.MagicMock()
    mfs.enable = mock.MagicMock()
    with mock.patch('mu.interface.microfs.put', return_value=None) as mp:
        mfs.dropEvent(mock_event)
        assert mp.call_count == 0
    mfs.disable.assert_called_once_with(source)
    mfs.enable.assert_called_once_with(source)


def test_MicrobitFileList_contextMenuEvent():
    """
    Ensure that the menu displayed when a file on the micro:bit is
    right-clicked works as expected when activated.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.MicrobitFileList('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.mapToGlobal = mock.MagicMock(return_value=None)
    mfs.setDisabled = mock.MagicMock(return_value=None)
    mfs.setAcceptDrops = mock.MagicMock(return_value=None)
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mock_event = mock.MagicMock()
    with mock.patch('mu.interface.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.microfs.rm',
                       return_value=None) as mock_rm, \
            mock.patch('mu.interface.QMenu', return_value=mock_menu):
        mfs.contextMenuEvent(mock_event)
        mock_rm.assert_called_once_with(mock_serial, 'foo.py')
        assert mfs.setDisabled.call_count == 2
        assert mfs.setAcceptDrops.call_count == 2


def test_MicrobitFileList_contextMenuEvent_error():
    """
    Ensure that if there's an error while preparing for the rm operation that
    it aborts without enacting.
    """
    mock_menu = mock.MagicMock()
    mock_action = mock.MagicMock()
    mock_menu.addAction.return_value = mock_action
    mock_menu.exec_.return_value = mock_action
    mfs = mu.interface.MicrobitFileList('homepath')
    mock_current = mock.MagicMock()
    mock_current.text.return_value = 'foo.py'
    mfs.currentItem = mock.MagicMock(return_value=mock_current)
    mfs.mapToGlobal = mock.MagicMock(return_value=None)
    mfs.setDisabled = mock.MagicMock(return_value=None)
    mfs.setAcceptDrops = mock.MagicMock(return_value=None)
    mfs.takeItem = mock.MagicMock(return_value=None)
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    mock_event = mock.MagicMock()
    ex = IOError('BANG')
    with mock.patch('mu.interface.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.microfs.rm', side_effect=ex), \
            mock.patch('mu.interface.QMenu', return_value=mock_menu), \
            mock.patch('mu.interface.logger.error', return_value=None) as log:
        mfs.contextMenuEvent(mock_event)
        log.assert_called_once_with(ex)
        assert mfs.takeItem.call_count == 0
        assert mfs.setDisabled.call_count == 2
        assert mfs.setAcceptDrops.call_count == 2


def test_LocalFileList_init():
    """
    Ensure the class instantiates with the expected state.
    """
    lfl = mu.interface.LocalFileList('home/path')
    assert lfl.home == 'home/path'
    assert lfl.dragDropMode() == lfl.DragDrop


def test_LocalFileList_dropEvent():
    """
    Ensure a valid drop event is handled as expected.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.MicrobitFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    lfs = mu.interface.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.enable = mock.MagicMock()
    lfs.parent = mock.MagicMock()
    with mock.patch('mu.interface.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.MuFileList.dropEvent',
                       return_value=None) as mock_dropEvent, \
            mock.patch('mu.interface.microfs.get',
                       return_value=True) as mock_get:
        lfs.dropEvent(mock_event)
        lfs.disable.assert_called_once_with(source)
        home = os.path.join('homepath', 'foo.py')
        mock_get.assert_called_once_with(mock_serial, 'foo.py', home)
        mock_dropEvent.assert_called_once_with(mock_event)
        lfs.enable.assert_called_once_with(source)
        lfs.parent().ls.assert_called_once_with()


def test_LocalFileList_dropEvent_error():
    """
    Ensure that if an error occurs there is no change in the file list state.
    """
    mock_event = mock.MagicMock()
    source = mu.interface.MicrobitFileList('homepath')
    mock_item = mock.MagicMock()
    mock_item.text.return_value = 'foo.py'
    source.currentItem = mock.MagicMock(return_value=mock_item)
    mock_event.source.return_value = source
    mock_context = mock.MagicMock()
    mock_serial = mock.MagicMock()
    mock_serial.port = 'COM0'
    mock_context.__enter__.return_value = mock_serial
    lfs = mu.interface.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.enable = mock.MagicMock()
    ex = IOError('BANG')
    with mock.patch('mu.interface.microfs.get_serial',
                    return_value=mock_context), \
            mock.patch('mu.interface.microfs.get', side_effect=ex), \
            mock.patch('mu.interface.logger.error', return_value=None) as log:
        lfs.dropEvent(mock_event)
        log.assert_called_once_with(ex)
        lfs.disable.assert_called_once_with(source)
        lfs.enable.assert_called_once_with(source)


def test_LocalFileList_dropEvent_wrong_source():
    """
    Ensure that only drop events whose origins are LocalFileList objects are
    handled.
    """
    mock_event = mock.MagicMock()
    source = mock.MagicMock()
    mock_event.source.return_value = source
    lfs = mu.interface.LocalFileList('homepath')
    lfs.disable = mock.MagicMock()
    lfs.enable = mock.MagicMock()
    with mock.patch('mu.interface.microfs.put', return_value=None) as mp:
        lfs.dropEvent(mock_event)
        assert mp.call_count == 0
    lfs.disable.assert_called_once_with(source)
    lfs.enable.assert_called_once_with(source)


def test_FileSystemPane_init():
    """
    Check things are set up as expected.
    """
    with mock.patch('mu.interface.FileSystemPane.ls',
                    return_value=None) as mock_ls:
        fsp = mu.interface.FileSystemPane('homepath')
    mock_ls.assert_called_once_with()
    assert isinstance(fsp.microbit_label, QLabel)
    assert isinstance(fsp.local_label, QLabel)
    assert isinstance(fsp.microbit_fs, QListWidget)
    assert isinstance(fsp.local_fs, QListWidget)


def test_FileSystemPane_ls():
    """
    Ensure the ls method works as expected.
    """
    microbit_files = ['foo.py', 'bar.py', 'baz.py']
    local_files = ['spam.py', 'eggs.py']
    # MOCK ALL TEH THIGNS!
    with mock.patch('mu.interface.MicrobitFileList.clear',
                    return_value=None) as mfs_clear, \
            mock.patch('mu.interface.LocalFileList.clear',
                       return_value=None) as lfs_clear, \
            mock.patch('mu.interface.microfs.ls',
                       return_value=microbit_files), \
            mock.patch('mu.interface.microfs.get_serial', return_value=None), \
            mock.patch('mu.interface.os.listdir', return_value=local_files), \
            mock.patch('mu.interface.os.path.isfile', return_value=True), \
            mock.patch('mu.interface.os.path.join', return_value=None):
        fsp = mu.interface.FileSystemPane('homepath')
        mfs_clear.assert_called_once_with()
        lfs_clear.assert_called_once_with()
        assert fsp.microbit_fs.count() == 3
        assert fsp.local_fs.count() == 2


def test_FileSystemPane_set_theme_day():
    """
    Ensures the day theme is set.
    """
    with mock.patch('mu.interface.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.FileSystemPane('homepath')
    fsp.setStyleSheet = mock.MagicMock()
    fsp.set_theme('day')
    fsp.setStyleSheet.assert_called_once_with(mu.interface.DAY_STYLE)


def test_FileSystemPane_set_theme_night():
    """
    Ensures the night theme is set.
    """
    with mock.patch('mu.interface.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.FileSystemPane('homepath')
    fsp.setStyleSheet = mock.MagicMock()
    fsp.set_theme('night')
    fsp.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_FileSystemPane_set_font_size():
    """
    Ensure the right size is set as the point size and the text based UI child
    widgets are updated.
    """
    with mock.patch('mu.interface.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.FileSystemPane('homepath')
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


def test_FileSystemPane_zoom_in():
    """
    Ensure the font is re-set bigger when zooming in.
    """
    with mock.patch('mu.interface.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.FileSystemPane('homepath')
    fsp.set_font_size = mock.MagicMock()
    fsp.zoomIn()
    expected = mu.interface.DEFAULT_FONT_SIZE + 2
    fsp.set_font_size.assert_called_once_with(expected)


def test_FileSystemPane_zoom_out():
    """
    Ensure the font is re-set smaller when zooming out.
    """
    with mock.patch('mu.interface.FileSystemPane.ls', return_value=None):
        fsp = mu.interface.FileSystemPane('homepath')
    fsp.set_font_size = mock.MagicMock()
    fsp.zoomOut()
    expected = mu.interface.DEFAULT_FONT_SIZE - 2
    fsp.set_font_size.assert_called_once_with(expected)


def test_StatusBar_init():
    """
    Ensure the status bar is set up as expected.
    """
    sb = mu.interface.StatusBar()
    # Default mode is set.
    assert sb.mode == 'python'

    sb = mu.interface.StatusBar(mode='foo')
    # Pass in the default mode.
    assert sb.mode == 'foo'

    # Expect two widgets for logs and mode.
    assert sb.mode_label
    assert sb.logs_label


def test_StatusBar_connect_logs():
    """
    Ensure the event handler for viewing logs is correctly set.
    """
    sb = mu.interface.StatusBar()

    def handler():
        pass

    sb.connect_logs(handler)
    assert sb.logs_label.mousePressEvent == handler


def test_StatusBar_connect_mode():
    """
    Ensure the event handler for selecting the new mode is correctly set.
    """
    sb = mu.interface.StatusBar()

    def handler():
        pass

    sb.connect_mode(handler)
    assert sb.mode_label.mousePressEvent == handler


def test_StatusBar_set_message():
    """
    Ensure the default pause for displaying a message in the status bar is
    used.
    """
    sb = mu.interface.StatusBar()
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
    sb = mu.interface.StatusBar()
    sb.mode_label.setText = mock.MagicMock()
    sb.set_mode(mode)
    sb.mode_label.setText.assert_called_once_with(mode.capitalize())


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
    with mock.patch('mu.interface.QListWidgetItem.setText', mock_text), \
            mock.patch('mu.interface.QListWidgetItem.setIcon', mock_icon), \
            mock.patch('mu.interface.load_icon', mock_load):
        mi = mu.interface.ModeItem(name, description, icon)
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
    with mock.patch('mu.interface.ModeItem', mock_item):
        ms = mu.interface.ModeSelector()
        ms.setup(modes, current_mode, 'day')
    assert mock_item.call_count == 3


def test_ModeSelector_setup_night_theme():
    """
    Ensure the ModeSelector can cope with theme.
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
    with mock.patch('mu.interface.ModeItem', mock_item):
        ms = mu.interface.ModeSelector()
        ms.setStyleSheet = mock_css
        ms.setup(modes, current_mode, 'night')
    assert mock_item.call_count == 3
    mock_css.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_ModeSelector_get_mode():
    """
    Ensure that the ModeSelector will correctly return a selected mode (or
    raise the expected exception if cancelled).
    """
    ms = mu.interface.ModeSelector()
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


def test_LogDisplay_setup():
    """
    Ensure the log display dialog is setup properly given the content of a log
    file.
    """
    log = 'this is the contents of a log file'
    ld = mu.interface.LogDisplay()
    ld.setup(log, 'day')
    assert ld.log_text_area.toPlainText() == log


def test_LogDisplay_setup_night():
    """
    Ensure the log display dialog can be themed.
    """
    log = 'this is the contents of a log file'
    ld = mu.interface.LogDisplay()
    ld.setStyleSheet = mock.MagicMock()
    ld.setup(log, 'night')
    assert ld.log_text_area.toPlainText() == log
    ld.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_JupyterREPLPane_init():
    """
    Ensure the widget is setup with the correct defaults.
    """
    jw = mu.interface.JupyterREPLPane()
    assert jw.console_height == 10


def test_JupyterREPLPane_set_font_size():
    """
    Check the correct stylesheet values are being set.
    """
    jw = mu.interface.JupyterREPLPane()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_font_size(16)
    style = jw.setStyleSheet.call_args[0][0]
    assert 'font-size: 16pt;' in style
    assert 'font-family: Monospace;' in style


def test_JupyterREPLPane_zoomIn():
    """
    Ensure zooming in increases the font size.
    """
    jw = mu.interface.JupyterREPLPane()
    jw.set_font_size = mock.MagicMock()
    old_size = jw.font.pointSize()
    jw.zoomIn(delta=4)
    jw.set_font_size.assert_called_once_with(old_size + 4)


def test_JupyterREPLPane_zoomOut():
    """
    Ensure zooming out decreases the font size.
    """
    jw = mu.interface.JupyterREPLPane()
    jw.set_font_size = mock.MagicMock()
    old_size = jw.font.pointSize()
    jw.zoomOut(delta=4)
    jw.set_font_size.assert_called_once_with(old_size - 4)


def test_JupyterREPLPane_set_theme_day():
    """
    Make sure the theme is correctly set for day.
    """
    jw = mu.interface.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_theme('day')
    jw.set_default_style.assert_called_once_with()
    jw.setStyleSheet.assert_called_once_with(mu.interface.DAY_STYLE)


def test_JupyterREPLPane_set_theme_night():
    """
    Make sure the theme is correctly set for night.
    """
    jw = mu.interface.JupyterREPLPane()
    jw.set_default_style = mock.MagicMock()
    jw.setStyleSheet = mock.MagicMock()
    jw.set_theme('night')
    jw.set_default_style.assert_called_once_with(colors='nocolor')
    jw.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_PythonProcessPane_init():
    """
    Check the font and input_buffer is set.
    """
    ppp = mu.interface.PythonProcessPane()
    assert ppp.font()
    assert ppp.input_buffer == []


def test_PythonProcessPane_start_process():
    """
    Ensure the widget is created as expected.
    """
    mock_process = mock.MagicMock()
    mock_process_class = mock.MagicMock(return_value=mock_process)
    mock_merge_chans = mock.MagicMock()
    mock_process_class.MergedChannels = mock_merge_chans
    with mock.patch('mu.interface.QProcess', mock_process_class):
        ppp = mu.interface.PythonProcessPane()
        ppp.start_process('workspace', 'script.py')
    assert mock_process_class.call_count == 1
    assert ppp.process == mock_process
    ppp.process.setProcessChannelMode.assert_called_once_with(mock_merge_chans)
    ppp.process.setWorkingDirectory.assert_called_once_with('workspace')
    ppp.process.readyRead.connect.assert_called_once_with(ppp.read)
    ppp.process.finished.connect.assert_called_once_with(ppp.finished)
    expected_script = os.path.abspath(os.path.normcase('script.py'))
    ppp.process.start.assert_called_once_with('mu-debug', [expected_script])


def test_PythonProcessPane_finished():
    """
    Check the functionality to handle the process finishing is correct.
    """
    ppp = mu.interface.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.insertText = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.setReadOnly = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.finished(0, 1)
    assert mock_cursor.insertText.call_count == 2
    assert 'exit code: 0' in mock_cursor.insertText.call_args[0][0]
    assert 'status: 1' in mock_cursor.insertText.call_args[0][0]
    ppp.setReadOnly.assert_called_once_with(True)
    ppp.setTextCursor.assert_called_once_with(ppp.textCursor())


def test_PythonProcessPane_append():
    """
    Ensure the referenced byte_stream is added to the textual content of the
    QTextEdit.
    """
    ppp = mu.interface.PythonProcessPane()
    mock_cursor = mock.MagicMock()
    mock_cursor.insertText = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.append(b'hello')
    mock_cursor.insertText.assert_called_once_with('hello')


def test_PythonProcessPane_delete():
    """
    Make sure that removing a character from the QTextEdit works as expected.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.input_buffer = ['a', 'b', ]
    mock_cursor = mock.MagicMock()
    mock_cursor.deletePreviousChar = mock.MagicMock()
    ppp.setTextCursor = mock.MagicMock()
    ppp.textCursor = mock.MagicMock(return_value=mock_cursor)
    ppp.delete()
    assert ppp.input_buffer == ['a', ]
    mock_cursor.deletePreviousChar.assert_called_once_with()


def test_PythonProcessPane_read():
    """
    Ensure incoming bytes from sub-process's stout are processed correctly.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.append = mock.MagicMock()
    ppp.process = mock.MagicMock()
    ppp.read()
    assert ppp.append.call_count == 1
    assert ppp.process.readAll().data.call_count == 1


def test_PythonProcessPane_keyPressEvent_a():
    """
    A "regular" character is typed.
    """
    ppp = mu.interface.PythonProcessPane()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_A)
    data.text = mock.MagicMock(return_value='a')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    assert ppp.input_buffer == [b'a', ]


def test_PythonProcessPane_keyPressEvent_backspace():
    """
    A backspace is typed.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.input_buffer = [b'a', 'b', ]
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Backspace)
    data.text = mock.MagicMock(return_value='\b')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    assert ppp.input_buffer == [b'a', ]


def test_PythonProcessPane_keyPressEvent_paste():
    """
    Control-V (paste)  character is typed.
    """
    ppp = mu.interface.PythonProcessPane()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_V)
    data.text = mock.MagicMock(return_value='')
    data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier |
                                    Qt.ShiftModifier)
    ppp.paste = mock.MagicMock()
    ppp.keyPressEvent(data)
    ppp.paste.assert_called_once_with()


def test_PythonProcessPane_keyPressEvent_copy():
    """
    A "regular" character is typed.
    """
    ppp = mu.interface.PythonProcessPane()
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_C)
    data.text = mock.MagicMock(return_value='')
    data.modifiers = mock.MagicMock(return_value=Qt.ControlModifier |
                                    Qt.ShiftModifier)
    ppp.copy = mock.MagicMock()
    ppp.keyPressEvent(data)
    ppp.copy.assert_called_once_with()


def test_PythonProcessPane_keyPressEvent_newline():
    """
    A "regular" character is typed.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.process = mock.MagicMock()
    ppp.input_buffer = [b'a', ]
    data = mock.MagicMock
    data.key = mock.MagicMock(return_value=Qt.Key_Enter)
    data.text = mock.MagicMock(return_value='\r')
    data.modifiers = mock.MagicMock(return_value=None)
    ppp.keyPressEvent(data)
    assert ppp.input_buffer == []
    ppp.process.write.assert_called_once_with(b'a\n')


def test_PythonProcessPane_zoomIn():
    """
    Check ZoomIn increases point size.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 12
    with mock.patch('mu.interface.QTextEdit.zoomIn') as mock_zoom:
        ppp.zoomIn(8)
        mock_zoom.assert_called_once_with(8)


def test_PythonProcessPane_zoomIn_max():
    """
    Check ZoomIn only works up to point size of 34
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 34
    with mock.patch('mu.interface.QTextEdit.zoomIn') as mock_zoom:
        ppp.zoomIn(8)
        assert mock_zoom.call_count == 0


def test_PythonProcessPane_zoomOut():
    """
    Check ZoomOut decreases point size.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 12
    with mock.patch('mu.interface.QTextEdit.zoomOut') as mock_zoom:
        ppp.zoomOut(6)
        mock_zoom.assert_called_once_with(6)


def test_PythonProcessPane_zoomOut_min():
    """
    Check ZoomOut decreases point size down to 4
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.font = mock.MagicMock()
    ppp.font().pointSize.return_value = 4
    with mock.patch('mu.interface.QTextEdit.zoomOut') as mock_zoom:
        ppp.zoomOut(8)
        assert mock_zoom.call_count == 0


def test_PythonProcessPane_set_theme_day():
    """
    Set the theme to day.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.setStyleSheet = mock.MagicMock()
    ppp.set_theme('day')
    ppp.setStyleSheet.assert_called_once_with(mu.interface.DAY_STYLE)


def test_PythonProcessPane_set_theme_night():
    """
    Set the theme to night.
    """
    ppp = mu.interface.PythonProcessPane()
    ppp.setStyleSheet = mock.MagicMock()
    ppp.set_theme('night')
    ppp.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)


def test_DebugInspector_set_font_size():
    """
    Check the correct stylesheet values are being set.
    """
    di = mu.interface.DebugInspector()
    di.setStyleSheet = mock.MagicMock()
    di.set_font_size(16)
    style = di.setStyleSheet.call_args[0][0]
    assert 'font-size: 16pt;' in style
    assert 'font-family: Monospace;' in style


def test_DebugInspector_zoomIn():
    """
    Ensure zooming in increases the font size.
    """
    di = mu.interface.DebugInspector()
    di.set_font_size = mock.MagicMock()
    old_size = di.font().pointSize()
    di.zoomIn(delta=4)
    di.set_font_size.assert_called_once_with(old_size + 4)


def test_DebugInspector_zoomOut():
    """
    Ensure zooming out decreases the font size.
    """
    di = mu.interface.DebugInspector()
    di.set_font_size = mock.MagicMock()
    old_size = di.font().pointSize()
    di.zoomOut(delta=4)
    di.set_font_size.assert_called_once_with(old_size - 4)


def test_DebugInspector_set_theme_day():
    """
    Make sure the theme is correctly set for day.
    """
    di = mu.interface.DebugInspector()
    di.set_default_style = mock.MagicMock()
    di.setStyleSheet = mock.MagicMock()
    di.set_theme('day')
    di.setStyleSheet.assert_called_once_with(mu.interface.DAY_STYLE)


def test_DebugInspector_set_theme_night():
    """
    Make sure the theme is correctly set for night.
    """
    di = mu.interface.DebugInspector()
    di.set_default_style = mock.MagicMock()
    di.setStyleSheet = mock.MagicMock()
    di.set_theme('night')
    di.setStyleSheet.assert_called_once_with(mu.interface.NIGHT_STYLE)
