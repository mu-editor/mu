"""
UI related capabilities for the text editor widget embedded in each tab in Mu.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import keyword
import os
import re
import logging
import os.path
from collections import defaultdict
from PyQt5.Qsci import (
    QsciScintilla,
    QsciLexerPython,
    QsciLexerHTML,
    QsciAPIs,
    QsciLexerCSS,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
from mu.interface.themes import Font, DayTheme
from mu.logic import NEWLINE


# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile(r"^\w+$")


logger = logging.getLogger(__name__)


class PythonLexer(QsciLexerPython):
    """
    A Python specific "lexer" that's used to identify keywords of the Python
    language so the editor can do syntax highlighting.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHighlightSubidentifiers(False)

    def keywords(self, flag):
        """
        Returns a list of Python keywords.
        """
        if flag == 1:
            kws = keyword.kwlist + ["self", "cls"]
        elif flag == 2:
            kws = __builtins__.keys()
        else:
            return None
        return " ".join(kws)


class CssLexer(QsciLexerCSS):
    """
    Fixes problems with comments in CSS.
    """

    def description(self, style):
        """
        Ensures "Comment" is returned when the lexer encounters a comment (this
        is due to a bug in the base class, for which this is a work around).
        """
        if style == QsciLexerCSS.Comment:
            return "Comment"
        return super().description(style)


class EditorPane(QsciScintilla):
    """
    Represents the text editor.
    """

    # Signal fired when a script or hex is droped on this editor
    open_file = pyqtSignal(str)

    def __init__(self, path, text, newline=NEWLINE):
        super().__init__()
        self.setUtf8(True)
        self.path = path
        self.setText(text)
        self.newline = newline
        self.check_indicators = {  # IDs are arbitrary
            "error": {"id": 19, "markers": {}},
            "style": {"id": 20, "markers": {}},
        }
        self.search_indicators = {"selection": {"id": 21, "positions": []}}
        self.DEBUG_INDICATOR = 22  # Arbitrary
        self.BREAKPOINT_MARKER = 23  # Arbitrary
        self.previous_selection = {
            "line_start": 0,
            "col_start": 0,
            "line_end": 0,
            "col_end": 0,
        }
        if self.path:
            if self.path.endswith(".css"):
                self.lexer = CssLexer()
            elif self.path.endswith(".html") or self.path.endswith(".htm"):
                self.lexer = QsciLexerHTML()
                self.lexer.setDjangoTemplates(True)
            else:
                self.lexer = PythonLexer()
        else:
            self.lexer = PythonLexer()
        self.api = None
        self.has_annotations = False
        self.setModified(False)
        self.breakpoint_handles = set()
        self.configure()

    def wheelEvent(self, event):
        """
        Stops QScintilla from doing the wrong sort of zoom handling.
        """
        if not QApplication.keyboardModifiers():
            super().wheelEvent(event)

    def dropEvent(self, event):
        """
        Run by Qt when *something* is dropped on this editor
        """

        # Does the drag event have any urls?
        # Files are transfered as a url (by path not value)
        if event.mimeData().hasUrls():
            # Qt doesn't seem to have an 'open' action,
            # this seems the most appropriate
            event.setDropAction(Qt.CopyAction)
            # Valid links
            links = []
            # Iterate over each of the urls attached to the event
            for url in event.mimeData().urls():
                # Check the url is to a local file
                # (not a webpage for example)
                if url.isLocalFile():
                    # Grab a 'real' path from the url
                    path = url.toLocalFile()
                    # Add it to the list of valid links
                    links.append(path)

            # Did we get any?
            if len(links) > 0:
                # Only accept now we actually know we can do
                # something with the drop event
                event.accept()
                for link in links:
                    # Start bubbling an open file request
                    self.open_file.emit(link)

        # If the event wasn't handled let QsciScintilla have a go
        if not event.isAccepted():
            super().dropEvent(event)

    def configure(self):
        """
        Set up the editor component.
        """
        # Font information
        font = Font().load()
        self.setFont(font)
        # Generic editor settings
        self.setUtf8(True)
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)
        self.setEdgeColumn(79)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 50)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.set_theme()
        # Markers and indicators
        self.setMarginSensitivity(0, True)
        self.markerDefine(self.Circle, self.BREAKPOINT_MARKER)
        self.setMarginSensitivity(1, True)
        # Additional dummy margin to prevent accidental breakpoint toggles when
        # trying to position the edit cursor to the left of the first column,
        # using the mouse and not being 100% accurate. This margin needs to be
        # set with "sensitivity on": otherwise clicking it would select the
        # whole text line, per QsciScintilla's behaviour. It is up to the
        # click handler to ignore clicks on this margin: self.connect_margin.
        self.setMarginWidth(4, 8)
        self.setMarginSensitivity(4, True)
        # Indicators
        self.setIndicatorDrawUnder(True)
        for type_ in self.check_indicators:
            self.indicatorDefine(
                self.SquiggleIndicator, self.check_indicators[type_]["id"]
            )
        for type_ in self.search_indicators:
            self.indicatorDefine(
                self.StraightBoxIndicator, self.search_indicators[type_]["id"]
            )
        self.indicatorDefine(self.FullBoxIndicator, self.DEBUG_INDICATOR)
        self.setAnnotationDisplay(self.AnnotationBoxed)
        self.selectionChanged.connect(self.selection_change_listener)
        self.set_zoom()

    def connect_margin(self, func):
        """
        Connect clicking the margin to the passed in handler function, via a
        filtering handler that ignores clicks on margin 4.
        """
        # Margin 4 motivation in self.configure comments.
        def func_ignoring_margin_4(margin, line, modifiers):
            if margin != 4:
                func(margin, line, modifiers)

        self.marginClicked.connect(func_ignoring_margin_4)

    def set_theme(self, theme=DayTheme):
        """
        Connect the theme to a lexer and return the lexer for the editor to
        apply to the script text.
        """
        theme.apply_to(self.lexer)
        self.lexer.setDefaultPaper(theme.Paper)
        self.setCaretForegroundColor(theme.Caret)
        self.setIndicatorForegroundColor(
            theme.IndicatorError, self.check_indicators["error"]["id"]
        )
        self.setIndicatorForegroundColor(
            theme.IndicatorStyle, self.check_indicators["style"]["id"]
        )
        self.setIndicatorForegroundColor(
            theme.DebugStyle, self.DEBUG_INDICATOR
        )
        for type_ in self.search_indicators:
            self.setIndicatorForegroundColor(
                theme.IndicatorWordMatch, self.search_indicators[type_]["id"]
            )
        self.setMarkerBackgroundColor(
            theme.BreakpointMarker, self.BREAKPOINT_MARKER
        )
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setLexer(self.lexer)
        self.setMarginsBackgroundColor(theme.Margin)
        self.setMarginsForegroundColor(theme.Caret)
        self.setMatchedBraceBackgroundColor(theme.BraceBackground)
        self.setMatchedBraceForegroundColor(theme.BraceForeground)
        self.setUnmatchedBraceBackgroundColor(theme.UnmatchedBraceBackground)
        self.setUnmatchedBraceForegroundColor(theme.UnmatchedBraceForeground)

    def set_api(self, api_definitions):
        """
        Sets the API entries for tooltips, calltips and the like.
        """
        self.api = QsciAPIs(self.lexer)
        for entry in api_definitions:
            self.api.add(entry)
        self.api.prepare()

    def set_zoom(self, size="m"):
        """
        Sets the font zoom to the specified base point size for all fonts given
        a t-shirt size.
        """
        sizes = {
            "xs": -4,
            "s": -2,
            "m": 1,
            "l": 4,
            "xl": 8,
            "xxl": 16,
            "xxxl": 48,
        }
        self.zoomTo(sizes[size])
        margins = {
            "xs": 30,
            "s": 35,
            "m": 45,
            "l": 50,
            "xl": 60,
            "xxl": 75,
            "xxxl": 85,
        }
        # Make the margin left of line numbers follow zoom level
        self.setMarginWidth(0, margins[size])
        # Make margins around debugger-marker follow zoom level
        self.setMarginWidth(1, margins[size] * 0.25)
        self.setMarginWidth(4, margins[size] * 0.1)

    @property
    def label(self):
        """
        The label associated with this editor widget (usually the filename of
        the script we're editing).
        """
        if self.path:
            label = os.path.basename(self.path)
        else:
            label = _("untitled")
        return label

    @property
    def title(self):
        """
        The title associated with this editor widget (usually the filename of
        the script we're editing).

        If the script has been modified since it was last saved, the label will
        end with an asterisk.
        """
        if self.isModified():
            return self.label + " •"
        return self.label

    def reset_annotations(self):
        """
        Clears all the assets (indicators, annotations and markers).
        """
        self.clearAnnotations()
        self.markerDeleteAll()
        self.reset_search_indicators()
        self.reset_check_indicators()

    def reset_check_indicators(self):
        """
        Clears all the text indicators related to the check code functionality.
        """
        for indicator in self.check_indicators:
            for _, markers in self.check_indicators[indicator][
                "markers"
            ].items():
                line_no = markers[0]["line_no"]  # All markers on same line.
                self.clearIndicatorRange(
                    line_no,
                    0,
                    line_no,
                    999999,
                    self.check_indicators[indicator]["id"],
                )
            self.check_indicators[indicator]["markers"] = {}

    def reset_search_indicators(self):
        """
        Clears all the text indicators from the search functionality.
        """
        for indicator in self.search_indicators:
            for position in self.search_indicators[indicator]["positions"]:
                self.clearIndicatorRange(
                    position["line_start"],
                    position["col_start"],
                    position["line_end"],
                    position["col_end"],
                    self.search_indicators[indicator]["id"],
                )
            self.search_indicators[indicator]["positions"] = []

    def annotate_code(self, feedback, annotation_type="error"):
        """
        Given a list of annotations add them to the editor pane so the user can
        act upon them.
        """
        indicator = self.check_indicators[annotation_type]
        for line_no, messages in feedback.items():
            indicator["markers"][line_no] = messages
            for message in messages:
                col = message.get("column", 0)
                if col:
                    col_start = col - 1
                    col_end = col + 1
                    self.fillIndicatorRange(
                        line_no, col_start, line_no, col_end, indicator["id"]
                    )
        if feedback:
            # Ensure the first line with a problem is visible.
            first_problem_line = sorted(feedback.keys())[0]
            self.ensureLineVisible(first_problem_line)

    def debugger_at_line(self, line):
        """
        Set the line to be highlighted with the DEBUG_INDICATOR.
        """
        self.reset_debugger_highlight()
        # Calculate the line length & account for \r\n giving ObOE.
        line_length = len(self.text(line).rstrip())
        self.fillIndicatorRange(
            line, 0, line, line_length, self.DEBUG_INDICATOR
        )
        self.ensureLineVisible(line)

    def reset_debugger_highlight(self):
        """
        Reset all the lines so the DEBUG_INDICATOR is no longer displayed.

        We need to check each line since there's no way to tell what the
        currently highlighted line is. This approach also has the advantage of
        resetting the *whole* editor pane.
        """
        for i in range(self.lines()):
            line_length = len(self.text(i))
            self.clearIndicatorRange(
                i, 0, i, line_length, self.DEBUG_INDICATOR
            )

    def show_annotations(self):
        """
        Display all the messages to be annotated to the code.
        """
        lines = defaultdict(list)
        for indicator in self.check_indicators:
            markers = self.check_indicators[indicator]["markers"]
            for k, marker_list in markers.items():
                for m in marker_list:
                    lines[m["line_no"]].append("\u2191 " + m["message"])
        for line, messages in lines.items():
            text = "\n".join(messages).strip()
            if text:
                self.annotate(line, text, self.annotationDisplay())

    def find_next_match(
        self,
        text,
        from_line=-1,
        from_col=-1,
        case_sensitive=True,
        wrap_around=True,
    ):
        """
        Finds the next text match from the current cursor, or the given
        position, and selects it (the automatic selection is the only available
        QsciScintilla behaviour).
        Returns True if match found, False otherwise.
        """
        return self.findFirst(
            text,  # Text to find,
            False,  # Treat as regular expression
            case_sensitive,  # Case sensitive search
            True,  # Whole word matches only
            wrap_around,  # Wrap search
            forward=True,  # Forward search
            line=from_line,  # -1 starts at current position
            index=from_col,  # -1 starts at current position
            show=False,  # Unfolds found text
            posix=False,
        )  # More POSIX compatible RegEx

    def range_from_positions(self, start_position, end_position):
        """Given a start-end pair, such as are provided by a regex match,
        return the corresponding Scintilla line-offset pairs which are
        used for searches, indicators etc.

        NOTE: Arguments must be byte offsets into the underlying text bytes.
        """
        start_line, start_offset = self.lineIndexFromPosition(start_position)
        end_line, end_offset = self.lineIndexFromPosition(end_position)
        return start_line, start_offset, end_line, end_offset

    def highlight_selected_matches(self):
        """
        Checks the current selection, if it is a single word it then searches
        and highlights all matches.

        Since we're interested in exactly one word:
        * Ignore an empty selection
        * Ignore anything which spans more than one line
        * Ignore more than one word
        * Ignore anything less than one word
        """
        selected_range = line0, col0, line1, col1 = self.getSelection()
        #
        # If there's no selection, do nothing
        #
        if selected_range == (-1, -1, -1, -1):
            return

        #
        # Ignore anything which spans two or more lines
        #
        if line0 != line1:
            return

        #
        # Ignore if no text is selected or the selected text is not at most one
        # valid identifier-type word.
        #
        selected_text = self.selectedText()
        if not RE_VALID_WORD.match(selected_text):
            return

        #
        # Ignore anything which is not a whole word.
        # NB Although Scintilla defines a SCI_ISRANGEWORD message,
        # it's not exposed by QSciScintilla. Instead, we
        # ask Scintilla for the start end end position of
        # the word we're in and test whether our range end points match
        # those or not.
        #
        pos0 = self.positionFromLineIndex(line0, col0)
        word_start_pos = self.SendScintilla(
            QsciScintilla.SCI_WORDSTARTPOSITION, pos0, 1
        )
        _, start_offset = self.lineIndexFromPosition(word_start_pos)
        if col0 != start_offset:
            return

        pos1 = self.positionFromLineIndex(line1, col1)
        word_end_pos = self.SendScintilla(
            QsciScintilla.SCI_WORDENDPOSITION, pos1, 1
        )
        _, end_offset = self.lineIndexFromPosition(word_end_pos)
        if col1 != end_offset:
            return

        #
        # For each matching word within the editor text, add it to
        # the list of highlighted indicators and fill it according
        # to the current theme.
        #
        indicators = self.search_indicators["selection"]
        encoding = "utf8" if self.isUtf8() else "latin1"
        text_bytes = self.text().encode(encoding)
        selected_text_bytes = selected_text.encode(encoding)
        for match in re.finditer(selected_text_bytes, text_bytes):
            range = self.range_from_positions(*match.span())
            #
            # Don't highlight the text we've selected
            #
            if range == selected_range:
                continue

            line_start, col_start, line_end, col_end = range
            indicators["positions"].append(
                {
                    "line_start": line_start,
                    "col_start": col_start,
                    "line_end": line_end,
                    "col_end": col_end,
                }
            )
            self.fillIndicatorRange(
                line_start, col_start, line_end, col_end, indicators["id"]
            )

    def selection_change_listener(self):
        """
        Runs every time the text selection changes. This could get triggered
        multiple times while the mouse click is down, even if selection has not
        changed in itself.
        If there is a new selection is passes control to
        highlight_selected_matches.
        """
        # Get the current selection, exit if it has not changed
        line_from, index_from, line_to, index_to = self.getSelection()
        if (
            self.previous_selection["col_end"] != index_to
            or self.previous_selection["col_start"] != index_from
            or self.previous_selection["line_start"] != line_from
            or self.previous_selection["line_end"] != line_to
        ):
            self.previous_selection["line_start"] = line_from
            self.previous_selection["col_start"] = index_from
            self.previous_selection["line_end"] = line_to
            self.previous_selection["col_end"] = index_to
            # Highlight matches
            self.reset_search_indicators()
            self.highlight_selected_matches()

    def toggle_line(self, raw_line):
        """
        Given a raw_line, will return the toggled version of it.
        """
        clean_line = raw_line.strip()
        if not clean_line or clean_line.startswith("##"):
            # Ignore whitespace-only lines and compact multi-commented lines
            return raw_line

        if clean_line.startswith("#"):
            # It's a comment line, so replace only the first "# " or "#":
            if clean_line.startswith("# "):
                return raw_line.replace("# ", "", 1)
            else:
                return raw_line.replace("#", "", 1)
        else:
            # It's a normal line of code.
            return "# " + raw_line

    def toggle_comments(self):
        """
        Iterate through the selected lines and toggle their comment/uncomment
        state. So, lines that are not comments become comments and vice versa.
        """
        if self.hasSelectedText():
            # Toggle currently selected text.
            logger.info("Toggling comments")
            line_from, index_from, line_to, index_to = self.getSelection()
            selected_text = self.selectedText()
            lines = selected_text.split("\n")
            toggled_lines = []
            for line in lines:
                toggled_lines.append(self.toggle_line(line))
            new_text = "\n".join(toggled_lines)
            self.replaceSelectedText(new_text)
            # Ensure the new text is also selected.
            last_newline = toggled_lines[-1]
            last_oldline = lines[-1]

            # Adjust the selection based on whether the last line got
            # longer, shorter, or stayed the same
            delta = len(last_newline) - len(last_oldline)
            index_to += delta
            self.setSelection(line_from, index_from, line_to, index_to)
        else:
            # Toggle the line currently containing the cursor.
            line_number, column = self.getCursorPosition()
            logger.info("Toggling line {}".format(line_number))
            line_content = self.text(line_number)
            new_line = self.toggle_line(line_content)
            self.setSelection(line_number, 0, line_number, len(line_content))
            self.replaceSelectedText(new_line)
            self.setSelection(line_number, 0, line_number, len(new_line) - 1)
