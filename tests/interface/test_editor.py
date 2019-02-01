# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from unittest import mock
import mu.interface.editor
import keyword
import re
from PyQt5.QtCore import Qt, QMimeData, QUrl, QPointF
from PyQt5.QtGui import QDropEvent

import pytest


def test_pythonlexer_keywords():
    """
    Ensure both types of expected keywords are returned from the PythonLexer
    class.
    """
    lexer = mu.interface.editor.PythonLexer()
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
    with mock.patch('mu.interface.editor.EditorPane.setText', mock_text), \
            mock.patch('mu.interface.editor.EditorPane.setModified',
                       mock_modified), \
            mock.patch('mu.interface.editor.EditorPane.configure',
                       mock_configure):
        path = '/foo/bar.py'
        text = 'print("Hello, World!")'
        editor = mu.interface.editor.EditorPane(path, text, '\r\n')
        mock_text.assert_called_once_with(text)
        mock_modified.assert_called_once_with(False)
        mock_configure.assert_called_once_with()
        assert editor.isUtf8()
        assert editor.newline == '\r\n'


def test_EditorPane_configure():
    """
    Check the expected configuration takes place. NOTE - this is checking the
    expected attributes are configured, not what the actual configuration
    values may be. I.e. we're checking that, say, setIndentationWidth is
    called.
    """
    ep = mu.interface.editor.EditorPane('/foo/bar.py', 'baz')
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
    ep.set_zoom = mock.MagicMock()
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
    assert ep.markerDefine.call_count == 1
    assert ep.setMarginSensitivity.call_count == 2
    assert ep.setIndicatorDrawUnder.call_count == 1
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
    assert ep.set_zoom.call_count == 1


def test_Editor_connect_margin():
    """
    Ensure that the passed in function is connected to the marginClick event.
    """
    mock_fn = mock.MagicMock()
    ep = mu.interface.editor.EditorPane('/foo/bar.py', 'baz')
    ep.marginClicked = mock.MagicMock()
    ep.connect_margin(mock_fn)
    ep.marginClicked.connect.assert_called_once_with(mock_fn)


def test_EditorPane_set_theme():
    """
    Check all the expected configuration calls are made to ensure the widget's
    theme is updated.
    """
    api = ['api help text', ]
    ep = mu.interface.editor.EditorPane('/foo/bar.py', 'baz')
    ep.lexer = mock.MagicMock()
    mock_api = mock.MagicMock()
    with mock.patch('mu.interface.editor.QsciAPIs',
                    return_value=mock_api) as mapi:
        ep.set_api(api)
        mapi.assert_called_once_with(ep.lexer)
        mock_api.add.assert_called_once_with('api help text')
        mock_api.prepare.assert_called_once_with()


def test_EditorPane_set_zoom():
    """
    Ensure the t-shirt size is turned into a call to parent's zoomTo.
    """
    ep = mu.interface.editor.EditorPane('/foo/bar.py', 'baz')
    ep.zoomTo = mock.MagicMock()
    ep.set_zoom('xl')
    ep.zoomTo.assert_called_once_with(8)


def test_EditorPane_label():
    """
    Ensure the correct label is returned given a set of states:

    If there's a path, use the basename for the label. Otherwise it's
    "untitled".

    If the text is modified append an asterisk.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    assert ep.label == 'untitled'
    ep = mu.interface.editor.EditorPane('/foo/bar.py', 'baz')
    assert ep.label == 'bar.py'
    ep.isModified = mock.MagicMock(return_value=True)
    assert ep.label == 'bar.py *'


def test_EditorPane_reset_annotations():
    """
    Ensure annotation state is reset.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
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
    ep = mu.interface.editor.EditorPane(None, 'baz')
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
    ep = mu.interface.editor.EditorPane(None, 'baz')
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
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.markerAdd = mock.MagicMock()
    ep.ensureLineVisible = mock.MagicMock()
    ep.fillIndicatorRange = mock.MagicMock()
    ep.annotate_code(feedback, 'error')
    assert ep.fillIndicatorRange.call_count == 3  # once for each message.
    ep.ensureLineVisible.assert_called_once_with(17)  # first problem visible


def test_EditorPane_debugger_at_line():
    """
    Ensure the right calls are made to highlight the referenced line with the
    DEBUG_INDICATOR.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.text = mock.MagicMock(return_value='baz')
    ep.reset_debugger_highlight = mock.MagicMock()
    ep.fillIndicatorRange = mock.MagicMock()
    ep.ensureLineVisible = mock.MagicMock()
    ep.debugger_at_line(99)
    ep.reset_debugger_highlight.assert_called_once_with()
    ep.text.assert_called_once_with(99)
    ep.fillIndicatorRange.assert_called_once_with(99, 0, 99, 3,
                                                  ep.DEBUG_INDICATOR)
    ep.ensureLineVisible.assert_called_once_with(99)


def test_EditorPane_debugger_at_line_windows_line_endings():
    """
    Ensure the right calls are made to highlight the referenced line with the
    DEBUG_INDICATOR.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.text = mock.MagicMock(return_value='baz\r\n')
    ep.reset_debugger_highlight = mock.MagicMock()
    ep.fillIndicatorRange = mock.MagicMock()
    ep.ensureLineVisible = mock.MagicMock()
    ep.debugger_at_line(99)
    ep.reset_debugger_highlight.assert_called_once_with()
    ep.text.assert_called_once_with(99)
    ep.fillIndicatorRange.assert_called_once_with(99, 0, 99, 3,
                                                  ep.DEBUG_INDICATOR)
    ep.ensureLineVisible.assert_called_once_with(99)


def test_EditorPane_reset_debugger_highlight():
    """
    Ensure all DEBUG_INDICATORs are removed from the editor.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.lines = mock.MagicMock(return_value=3)
    ep.text = mock.MagicMock(return_value='baz')
    ep.clearIndicatorRange = mock.MagicMock()
    ep.reset_debugger_highlight()
    assert ep.clearIndicatorRange.call_count == 3
    assert ep.clearIndicatorRange.call_args_list[0][0] == (0, 0, 0, 3,
                                                           ep.DEBUG_INDICATOR)


def test_EditorPane_show_annotations():
    """
    Ensure the annotations are shown in "sentence" case and with an arrow to
    indicate the line to which they refer.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.check_indicators = {
        'error': {
            'markers': {
                1: [
                    {'message': 'message 1', 'line_no': 1},
                    {'message': 'message 2', 'line_no': 1},
                ]
            }
        }
    }
    ep.annotate = mock.MagicMock()
    ep.show_annotations()
    ep.annotate.assert_called_once_with(1,
                                        '\u2191 message 1\n\u2191 message 2',
                                        ep.annotationDisplay())


def test_EditorPane_find_next_match():
    """
    Ensures that the expected arg values are passed through to QsciScintilla
    for highlighting matched text.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
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

    ep = mu.interface.editor.EditorPane(None, 'baz')
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

    ep = mu.interface.editor.EditorPane(None, 'baz')
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

    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.setText(text)
    for range in _ranges_in_text(text, search_for):
        break
    ep.setSelection(*range)
    assert ep.search_indicators['selection']['positions'] == []


@pytest.mark.parametrize('text, search_for', [
    ("foo bar foo baz foo", "foo"),
    ("résumé foo bar foo baz foo", "foo"),
    ("résumé bar résumé baz résumé", "résumé"),
])
def test_EditorPane_highlight_selected_matches_with_match(text, search_for):
    """
    Ensure that if the current selection is a single word then it causes the
    expected search/highlight call.

    There appears to be no way to iterate over indicators within the editor.
    So we're using the search_indicators structure as a proxy
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
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

    ep = mu.interface.editor.EditorPane(None, 'baz')
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
    ep = mu.interface.editor.EditorPane(None, 'baz')
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
        ep.SendScintilla(mu.interface.editor.QsciScintilla.SCI_CHARLEFTEXTEND)
    assert ep.getCursorPosition() == (line1, index1 - select_n_chars)


def test_EditorPane_selection_change_listener():
    """
    Enusure that is there is a change to the selected text then controll is
    passed to highlight_selected_matches.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.getSelection = mock.MagicMock(return_value=(1, 1, 2, 2))
    ep.highlight_selected_matches = mock.MagicMock()
    ep.selection_change_listener()
    assert ep.previous_selection['line_start'] == 1
    assert ep.previous_selection['col_start'] == 1
    assert ep.previous_selection['line_end'] == 2
    assert ep.previous_selection['col_end'] == 2
    assert ep.highlight_selected_matches.call_count == 1


def test_EditorPane_drop_event():
    """
    If there's a drop event associated with files, cause them to be passed into
    Mu's existing file loading code.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    m = mock.MagicMock()
    ep.open_file = mock.MagicMock()
    ep.open_file.emit = m
    data = QMimeData()
    data.setUrls([QUrl('file://test/path.py'), QUrl('file://test/path.hex'),
                  QUrl('file://test/path.txt')])
    evt = QDropEvent(QPointF(0, 0), Qt.CopyAction, data,
                     Qt.LeftButton, Qt.NoModifier)
    ep.dropEvent(evt)
    # Upstream _load will handle invalid file type (.txt).
    assert m.call_count == 3


def test_EditorPane_drop_event_not_file():
    """
    If the drop event isn't for files (for example, it may be for dragging and
    dropping text into the editor), then pass the handling up to QScintilla.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    event = mock.MagicMock()
    event.mimeData().hasUrls.return_value = False
    event.isAccepted.return_value = False
    with mock.patch('mu.interface.editor.QsciScintilla.dropEvent') as mock_de:
        ep.dropEvent(event)
        mock_de.assert_called_once_with(event)


def test_EditorPane_toggle_line_starts_with_hash():
    """
    If the line starts with a hash ("#") immediately followed by code, then
    uncomment it.

    e.g.

    #foo

    becomes:

    foo
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    assert ep.toggle_line('    #foo') == '    foo'


def test_EditorPane_toggle_line_starts_with_hash_space():
    """
    If the line starts with a PEP-8 compliant hash followed by a space ("# ")
    then uncomment it.

    e.g.

    # foo

    becomes:

    foo

    (Note the space is dropped.)
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    assert ep.toggle_line('    # foo') == '    foo'


def test_EditorPane_toggle_line_normal_line():
    """
    If the line is an uncommented line of text, then comment it with hash-space
    ("# ").

    e.g.

    foo

    becomes

    # foo
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    assert ep.toggle_line('    foo') == '#     foo'


def test_EditorPane_toggle_line_whitespace_line():
    """
    If the line is simply empty or contains only whitespace, then ignore it and
    return as-is.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    assert ep.toggle_line('    ') == '    '


def test_EditorPane_toggle_comments_no_selection():
    """
    If no text is selected, toggle the line currently containing the cursor.
    """
    ep = mu.interface.editor.EditorPane(None, 'baz')
    ep.hasSelectedText = mock.MagicMock(return_value=False)
    ep.getCursorPosition = mock.MagicMock(return_value=(1, 0))
    ep.text = mock.MagicMock(return_value='foo')
    ep.setSelection = mock.MagicMock()
    ep.replaceSelectedText = mock.MagicMock()
    ep.toggle_comments()
    assert ep.setSelection.call_count == 2
    # Final setSelection call re-selects the changed line.
    assert mock.call(1, 0, 1, 4) == ep.setSelection.call_args_list[1]
    ep.replaceSelectedText.assert_called_once_with('# foo')


def test_EditorPane_toggle_comments_selected_normal_lines():
    """
    Check normal lines of code are properly commented and subsequently
    highlighted.
    """
    ep = mu.interface.editor.EditorPane(None, 'foo\nbar\nbaz')
    ep.hasSelectedText = mock.MagicMock(return_value=True)
    ep.getSelection = mock.MagicMock(return_value=(0, 0, 2, 2))
    ep.selectedText = mock.MagicMock(return_value='foo\nbar\nbaz')
    ep.replaceSelectedText = mock.MagicMock()
    ep.setSelection = mock.MagicMock()
    ep.toggle_comments()
    ep.replaceSelectedText.assert_called_once_with('# foo\n# bar\n# baz')
    ep.setSelection.assert_called_once_with(0, 0, 2, 4)


def test_EditorPane_toggle_comments_selected_hash_comment_lines():
    """
    Check commented lines starting with "#" are now uncommented.
    """
    ep = mu.interface.editor.EditorPane(None, '#foo\n#bar\n#baz')
    ep.hasSelectedText = mock.MagicMock(return_value=True)
    ep.getSelection = mock.MagicMock(return_value=(0, 0, 2, 3))
    ep.selectedText = mock.MagicMock(return_value='#foo\n#bar\n#baz')
    ep.replaceSelectedText = mock.MagicMock()
    ep.setSelection = mock.MagicMock()
    ep.toggle_comments()
    ep.replaceSelectedText.assert_called_once_with('foo\nbar\nbaz')
    ep.setSelection.assert_called_once_with(0, 0, 2, 2)


def test_EditorPane_toggle_comments_selected_hash_space_comment_lines():
    """
    Check commented lines starting with "# " are now uncommented.
    """
    ep = mu.interface.editor.EditorPane(None, '# foo\n# bar\n# baz')
    ep.hasSelectedText = mock.MagicMock(return_value=True)
    ep.getSelection = mock.MagicMock(return_value=(0, 0, 2, 4))
    ep.selectedText = mock.MagicMock(return_value='# foo\n# bar\n# baz')
    ep.replaceSelectedText = mock.MagicMock()
    ep.setSelection = mock.MagicMock()
    ep.toggle_comments()
    ep.replaceSelectedText.assert_called_once_with('foo\nbar\nbaz')
    ep.setSelection.assert_called_once_with(0, 0, 2, 2)
