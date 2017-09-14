"""
Copyright (c) 2015-2016 Nicholas H.Tollervey and others (see the AUTHORS file).

Based upon work done for Puppy IDE by Dan Pope, Nicholas Tollervey and Damien
George.

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
import platform
import logging
import os.path
from PyQt5.QtCore import (QSize, Qt, pyqtSignal, QIODevice, QProcess,
                          QTimer, QProcessEnvironment)
from PyQt5.QtWidgets import (QToolBar, QAction, QDesktopWidget, QWidget,
                             QVBoxLayout, QTabWidget, QFileDialog,
                             QMessageBox, QTextEdit, QFrame, QListWidget,
                             QGridLayout, QLabel, QMenu, QApplication,
                             QMainWindow, QStatusBar, QListWidgetItem, QDialog,
                             QDialogButtonBox, QPlainTextEdit, QDockWidget,
                             QTreeView)
from PyQt5.QtGui import (QKeySequence, QColor, QTextCursor, QFontDatabase,
                         QCursor, QStandardItemModel, QStandardItem)
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtSerialPort import QSerialPort
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from mu import __version__
from mu.contrib import microfs
from mu.resources import (load_icon, load_stylesheet, load_font_data,
                          load_pixmap)


#: The default font size.
DEFAULT_FONT_SIZE = 14
#: All editor windows use the same font
FONT_NAME = "Source Code Pro"
FONT_FILENAME_PATTERN = "SourceCodePro-{variant}.otf"
FONT_VARIANTS = ("Bold", "BoldIt", "It", "Regular", "Semibold", "SemiboldIt")
# Load the two themes from resources/css/[night|day].css
#: NIGHT_STYLE is a dark high contrast theme.
NIGHT_STYLE = load_stylesheet('night.css')
#: DAY_STYLE is a light conventional theme.
DAY_STYLE = load_stylesheet('day.css')
# Regular Expression for valid individual code 'words'
RE_VALID_WORD = re.compile('^[A-Za-z0-9_-]*$')


logger = logging.getLogger(__name__)


class Font:
    """
    Utility class that makes it easy to set font related values within the
    editor.
    """
    _DATABASE = None

    def __init__(self, color='black', paper='white', bold=False, italic=False):
        self.color = color
        self.paper = paper
        self.bold = bold
        self.italic = italic

    @classmethod
    def get_database(cls):
        """
        Create a font database and load the MU builtin fonts into it.
        This is a cached classmethod so the font files aren't re-loaded
        every time a font is refereced
        """
        if cls._DATABASE is None:
            cls._DATABASE = QFontDatabase()
            for variant in FONT_VARIANTS:
                filename = FONT_FILENAME_PATTERN.format(variant=variant)
                font_data = load_font_data(filename)
                cls._DATABASE.addApplicationFontFromData(font_data)
        return cls._DATABASE

    def load(self, size=DEFAULT_FONT_SIZE):
        """
        Load the font from the font database, using the correct size and style
        """
        return Font.get_database().font(FONT_NAME, self.stylename, size)

    @property
    def stylename(self):
        """
        Map the bold and italic boolean flags here to a relevant
        font style name.
        """
        if self.bold:
            if self.italic:
                return "Semibold Italic"
            return "Semibold"
        if self.italic:
            return "Italic"
        return "Regular"


class Theme:
    """
    Defines a font and other theme specific related information.
    """

    @classmethod
    def apply_to(cls, lexer):
        # Apply a font for all styles
        lexer.setFont(Font().load())

        for name, font in cls.__dict__.items():
            if not isinstance(font, Font):
                continue
            style_num = getattr(lexer, name)
            lexer.setColor(QColor(font.color), style_num)
            lexer.setEolFill(True, style_num)
            lexer.setPaper(QColor(font.paper), style_num)
            lexer.setFont(font.load(), style_num)


class DayTheme(Theme):
    """
    Defines a Python related theme including the various font colours for
    syntax highlighting.

    This is a light theme.
    """

    FunctionMethodName = ClassName = Font(color='#0000a0')
    UnclosedString = Font(paper='#FFDDDD')
    Comment = CommentBlock = Font(color='gray')
    Keyword = Font(color='#008080', bold=True)
    SingleQuotedString = DoubleQuotedString = Font(color='#800000')
    TripleSingleQuotedString = TripleDoubleQuotedString = Font(color='#060')
    Number = Font(color='#00008B')
    Decorator = Font(color='#cc6600')
    Default = Identifier = Font()
    Operator = Font(color='#400040')
    HighlightedIdentifier = Font(color='#0000a0')
    Paper = QColor('white')
    Caret = QColor('black')
    Margin = QColor('#EEE')
    IndicatorError = QColor('red')
    IndicatorStyle = QColor('blue')
    IndicatorWordMatch = QColor('lightGrey')
    BraceBackground = QColor('lightGrey')
    BraceForeground = QColor('blue')
    UnmatchedBraceBackground = QColor('#FFDDDD')
    UnmatchedBraceForeground = QColor('black')
    BreakpointMarker = QColor('#D80000')


class NightTheme(Theme):
    """
    Defines a Python related theme including the various font colours for
    syntax highlighting.

    This is the dark / high contrast theme.
    """

    FunctionMethodName = ClassName = Font(color='#AAA', paper='black')
    UnclosedString = Font(paper='#666')
    Comment = CommentBlock = Font(color='#AAA', paper='black')
    Keyword = Font(color='#EEE', bold=True, paper='black')
    SingleQuotedString = DoubleQuotedString = Font(color='#AAA', paper='black')
    TripleSingleQuotedString = TripleDoubleQuotedString = Font(color='#AAA',
                                                               paper='black')
    Number = Font(color='#AAA', paper='black')
    Decorator = Font(color='#cccccc', paper='black')
    Default = Identifier = Font(color='#fff', paper='black')
    Operator = Font(color='#CCC', paper='black')
    HighlightedIdentifier = Font(color='#ffffff', paper='black')
    Paper = QColor('black')
    Caret = QColor('white')
    Margin = QColor('#333')
    IndicatorError = QColor('white')
    IndicatorStyle = QColor('cyan')
    IndicatorWordMatch = QColor('grey')
    BraceBackground = QColor('white')
    BraceForeground = QColor('black')
    UnmatchedBraceBackground = QColor('#666')
    UnmatchedBraceForeground = QColor('black')
    BreakpointMarker = QColor('white')


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
            kws = keyword.kwlist + ['self', 'cls']
        elif flag == 2:
            kws = __builtins__.keys()
        else:
            return None
        return ' '.join(kws)


class EditorPane(QsciScintilla):
    """
    Represents the text editor.
    """

    def __init__(self, path, text):
        super().__init__()
        self.path = path
        self.setText(text)
        self.check_indicators = {  # IDs are arbitrary
            'error': {'id': 19, 'markers': {}},
            'style': {'id': 20, 'markers': {}}
        }
        self.MARKER_NUMBER = 22  # Also arbitrary
        self.BREAKPOINT_MARKER = 23  # Arbitrary
        self.search_indicators = {
            'selection': {'id': 21, 'positions': []}
        }
        self.previous_selection = {
            'line_start': 0, 'col_start': 0, 'line_end': 0, 'col_end': 0
        }
        self.lexer = PythonLexer()
        self.api = None
        self.setModified(False)
        self.breakpoint_lines = set()
        self.configure()

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
        self.markerDefine(self.RightArrow, self.MARKER_NUMBER)
        self.markerDefine(self.Circle, self.BREAKPOINT_MARKER)
        self.setMarginSensitivity(1, True)
        self.setIndicatorDrawUnder(True)
        for type_ in self.check_indicators:
            self.indicatorDefine(
                self.SquiggleIndicator, self.check_indicators[type_]['id'])
        for type_ in self.search_indicators:
            self.indicatorDefine(
                self.StraightBoxIndicator, self.search_indicators[type_]['id'])
        self.setAnnotationDisplay(self.AnnotationBoxed)
        self.marginClicked.connect(self.on_marker_clicked)
        self.selectionChanged.connect(self.selection_change_listener)

    def connect_margin(self, func):
        """
        Connect clicking the margin to the passed in handler function.
        """
        self.marginClicked.connect(func)

    def set_theme(self, theme=DayTheme):
        """
        Connect the theme to a lexer and return the lexer for the editor to
        apply to the script text.
        """
        theme.apply_to(self.lexer)
        self.lexer.setDefaultPaper(theme.Paper)
        self.setCaretForegroundColor(theme.Caret)
        self.setMarginsBackgroundColor(theme.Margin)
        self.setMarginsForegroundColor(theme.Caret)
        self.setIndicatorForegroundColor(theme.IndicatorError,
                                         self.check_indicators['error']['id'])
        self.setIndicatorForegroundColor(theme.IndicatorStyle,
                                         self.check_indicators['style']['id'])
        for type_ in self.search_indicators:
            self.setIndicatorForegroundColor(
                theme.IndicatorWordMatch, self.search_indicators[type_]['id'])
        self.setMarkerBackgroundColor(theme.IndicatorError, self.MARKER_NUMBER)
        self.setMarkerBackgroundColor(theme.BreakpointMarker,
                                      self.BREAKPOINT_MARKER)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setLexer(self.lexer)
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

    @property
    def label(self):
        """
        The label associated with this editor widget (usually the filename of
        the script we're editing).

        If the script has been modified since it was last saved, the label will
        end with an asterisk.
        """
        if self.path:
            label = os.path.basename(self.path)
        else:
            label = 'untitled'
        # Add an asterisk to indicate that the file remains unsaved.
        if self.isModified():
            return label + ' *'
        else:
            return label

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
            for _, markers in \
                    self.check_indicators[indicator]['markers'].items():
                line_no = markers[0]['line_no']  # All markers on same line.
                self.clearIndicatorRange(
                    line_no, 0, line_no, 999999,
                    self.check_indicators[indicator]['id'])
            self.check_indicators[indicator]['markers'] = {}

    def reset_search_indicators(self):
        """
        Clears all the text indicators from the search functionality.
        """
        for indicator in self.search_indicators:
            for position in self.search_indicators[indicator]['positions']:
                self.clearIndicatorRange(
                    position['line_start'], position['col_start'],
                    position['line_end'], position['col_end'],
                    self.search_indicators[indicator]['id'])
            self.search_indicators[indicator]['positions'] = []

    def annotate_code(self, feedback, annotation_type='error'):
        """
        Given a list of annotations add them to the editor pane so the user can
        act upon them.
        """
        indicator = self.check_indicators[annotation_type]
        for line_no, messages in feedback.items():
            marker_id = self.markerAdd(line_no, self.MARKER_NUMBER)
            indicator['markers'][marker_id] = messages
            for message in messages:
                col = message.get('column', 0)
                if col:
                    col_start = col - 1
                    col_end = col + 1
                    self.fillIndicatorRange(line_no, col_start, line_no,
                                            col_end, indicator['id'])

    def on_marker_clicked(self, margin, line, state):
        """
        Display something when the margin indicator is clicked.
        """
        marker_id = self.get_marker_at_line(line)
        if marker_id:
            if self.annotation(line):
                self.clearAnnotations(line)
            else:
                messages = []
                for indicator in self.check_indicators:
                    markers = self.check_indicators[indicator]['markers']
                    messages += [i['message'] for i in
                                 markers.get(marker_id, [])]
                text = '\n'.join(messages).strip()
                if text:
                    self.annotate(line, text, self.annotationDisplay())

    def get_marker_at_line(self, line):
        """
        Given a line, will return the marker if one exists. Otherwise, returns
        None.

        Required because the built in markersAtLine method is useless, misnamed
        and doesn't return anything useful. :-(
        """
        for indicator in self.check_indicators:
            for marker_id in self.check_indicators[indicator]['markers']:
                if self.markerLine(marker_id) == line:
                    return marker_id

    def find_next_match(self, text, from_line=-1, from_col=-1,
                        case_sensitive=True, wrap_around=True):
        """
        Finds the next text match from the current cursor, or the given
        position, and selects it (the automatic selection is the only available
        QsciScintilla behaviour).
        Returns True if match found, False otherwise.
        """
        return self.findFirst(
            text,            # Text to find,
            False,           # Treat as regular expression
            case_sensitive,  # Case sensitive search
            True,            # Whole word matches only
            wrap_around,     # Wrap search
            forward=True,    # Forward search
            line=from_line,  # -1 starts at current position
            index=from_col,  # -1 starts at current position
            show=False,      # Unfolds found text
            posix=False)     # More POSIX compatible RegEx

    def range_from_positions(self, start_position, end_position):
        """Given a start-end pair, such as are provided by a regex match,
        return the corresponding Scintilla line-offset pairs which are
        used for searches, indicators etc.

        FIXME: Not clear whether the Scintilla conversions are expecting
        bytes or characters (ie codepoints)
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
            QsciScintilla.SCI_WORDSTARTPOSITION, pos0, 1)
        _, start_offset = self.lineIndexFromPosition(word_start_pos)
        if col0 != start_offset:
            return

        pos1 = self.positionFromLineIndex(line1, col1)
        word_end_pos = self.SendScintilla(
            QsciScintilla.SCI_WORDENDPOSITION, pos1, 1)
        _, end_offset = self.lineIndexFromPosition(word_end_pos)
        if col1 != end_offset:
            return

        #
        # For each matching word within the editor text, add it to
        # the list of highlighted indicators and fill it according
        # to the current theme.
        #
        indicators = self.search_indicators['selection']
        text = self.text()
        for match in re.finditer(selected_text, text):
            range = self.range_from_positions(*match.span())
            #
            # Don't highlight the text we've selected
            #
            if range == selected_range:
                continue

            line_start, col_start, line_end, col_end = range
            indicators['positions'].append({
                'line_start': line_start, 'col_start': col_start,
                'line_end': line_end, 'col_end': col_end
            })
            self.fillIndicatorRange(line_start, col_start, line_end,
                                    col_end, indicators['id'])

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
        if self.previous_selection['col_end'] != index_to or \
                self.previous_selection['col_start'] != index_from or \
                self.previous_selection['line_start'] != line_from or \
                self.previous_selection['line_end'] != line_to:
            self.previous_selection['line_start'] = line_from
            self.previous_selection['col_start'] = index_from
            self.previous_selection['line_end'] = line_to
            self.previous_selection['col_end'] = index_to
            # Highlight matches
            self.reset_search_indicators()
            self.highlight_selected_matches()


class ButtonBar(QToolBar):
    """
    Represents the bar of buttons across the top of the editor and defines
    their behaviour.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.setMovable(False)
        self.setIconSize(QSize(64, 64))
        self.setToolButtonStyle(3)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("StandardToolBar")
        self.reset()

    def reset(self):
        """
        Resets the button states.
        """
        self.slots = {}
        self.clear()

    def change_mode(self, mode):
        self.reset()
        self.addAction(name="new", display_name=_("New"),
                       tool_text=_("Create a new Python script."))
        self.addAction(name="load", display_name=_("Load"),
                       tool_text=_("Load a Python script."))
        self.addAction(name="save", display_name=_("Save"),
                       tool_text=_("Save the current Python script."))
        self.addSeparator()

        for action in mode.actions():
            self.addAction(name=action['name'],
                           display_name=action['display_name'],
                           tool_text=action['description'])

        self.addSeparator()
        self.addAction(name="zoom-in", display_name=_('Zoom-in'),
                       tool_text=_("Zoom in (to make the text bigger)."))
        self.addAction(name="zoom-out", display_name=_('Zoom-out'),
                       tool_text=_("Zoom out (to make the text smaller)."))
        self.addAction(name="theme", display_name=_('Theme'),
                       tool_text=_("Change theme between day or night."))
        self.addSeparator()
        self.addAction(name="check", display_name=_('Check'),
                       tool_text=_("Check your code for mistakes."))
        self.addAction(name="help", display_name=_('Help'),
                       tool_text=_("Show help about Mu in a browser."))
        self.addAction(name="quit", display_name=_('Quit'),
                       tool_text=_("Quit Mu."))

    def set_responsive_mode(self, width, height):
        """
        Compact button bar for when window is very small.
        """
        font_size = DEFAULT_FONT_SIZE
        if width < 940 and height > 600:
            self.setIconSize(QSize(48, 48))
        elif height < 600 and width < 940:
            font_size = 10
            self.setIconSize(QSize(32, 32))
        else:
            self.setIconSize(QSize(64, 64))
        stylesheet = "QWidget{font-size: " + str(font_size) + "px;}"
        self.setStyleSheet(stylesheet)

    def addAction(self, name, display_name, tool_text):
        """
        Creates an action associated with an icon and name and adds it to the
        widget's slots.
        """
        action = QAction(load_icon(name), display_name, self,
                         toolTip=tool_text)
        super().addAction(action)
        self.slots[name] = action

    def connect(self, name, handler, shortcut=None):
        """
        Connects a named slot to a handler function and optional hot-key
        shortcuts.
        """
        self.slots[name].pyqtConfigure(triggered=handler)
        if shortcut:
            self.slots[name].setShortcut(QKeySequence(shortcut))


class FileTabs(QTabWidget):
    """
    Extend the base class so we can override the removeTab behaviour.
    """

    def __init__(self):
        super(FileTabs, self).__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(self.change_tab)

    def removeTab(self, tab_id):
        """
        Ask the user before closing the file.
        """
        window = self.nativeParentWidget()
        modified = window.current_tab.isModified()
        if modified:
            msg = ('There is un-saved work, closing the tab will cause you '
                   'to lose it.')
            if window.show_confirmation(msg) == QMessageBox.Cancel:
                return
        super(FileTabs, self).removeTab(tab_id)

    def change_tab(self, tab_id):
        """
        Update the application title to reflect the name of the file in the
        currently selected tab.
        """
        current_tab = self.widget(tab_id)
        window = self.nativeParentWidget()
        if current_tab:
            window.update_title(current_tab.label)
        else:
            window.update_title(None)


class Window(QMainWindow):
    """
    Defines the look and characteristics of the application's main window.
    """

    title = _("Mu {}").format(__version__)
    icon = "icon"
    timer = None
    usb_checker = None

    _zoom_in = pyqtSignal(int)
    _zoom_out = pyqtSignal(int)

    def zoom_in(self):
        """
        Handles zooming in.
        """
        self._zoom_in.emit(2)

    def zoom_out(self):
        """
        Handles zooming out.
        """
        self._zoom_out.emit(2)

    def connect_zoom(self, widget):
        """
        Connects a referenced widget to the zoom related signals.
        """
        self._zoom_in.connect(widget.zoomIn)
        self._zoom_out.connect(widget.zoomOut)

    @property
    def current_tab(self):
        """
        Returns the currently focussed tab.
        """
        return self.tabs.currentWidget()

    def set_read_only(self, is_readonly):
        """
        Set all tabs read-only.
        """
        self.read_only_tabs = is_readonly
        for tab in self.widgets:
            tab.setReadOnly(is_readonly)

    def get_load_path(self, folder):
        """
        Displays a dialog for selecting a file to load. Returns the selected
        path. Defaults to start in the referenced folder.
        """
        path, _ = QFileDialog.getOpenFileName(self.widget, 'Open file', folder,
                                              '*.py *.hex')
        logger.debug('Getting load path: {}'.format(path))
        return path

    def get_save_path(self, folder):
        """
        Displays a dialog for selecting a file to save. Returns the selected
        path. Defaults to start in the referenced folder.
        """
        path, _ = QFileDialog.getSaveFileName(self.widget, 'Save file', folder)
        logger.debug('Getting save path: {}'.format(path))
        return path

    def get_microbit_path(self, folder):
        """
        Displays a dialog for locating the location of the BBC micro:bit in the
        host computer's filesystem. Returns the selected path. Defaults to
        start in the referenced folder.
        """
        path = QFileDialog.getExistingDirectory(self.widget,
                                                'Locate BBC micro:bit', folder,
                                                QFileDialog.ShowDirsOnly)
        logger.debug('Getting micro:bit path: {}'.format(path))
        return path

    def add_tab(self, path, text, api):
        """
        Adds a tab with the referenced path and text to the editor.
        """
        new_tab = EditorPane(path, text)
        new_tab.connect_margin(self.breakpoint_toggle)
        new_tab_index = self.tabs.addTab(new_tab, new_tab.label)
        new_tab.set_api(api)

        @new_tab.modificationChanged.connect
        def on_modified():
            modified_tab_index = self.tabs.currentIndex()
            self.tabs.setTabText(modified_tab_index, new_tab.label)
            self.update_title(new_tab.label)

        self.tabs.setCurrentIndex(new_tab_index)
        self.connect_zoom(new_tab)
        self.set_theme(self.theme)
        new_tab.setFocus()
        if self.read_only_tabs:
            new_tab.setReadOnly(self.read_only_tabs)

    def focus_tab(self, tab):
        index = self.tabs.indexOf(tab)
        self.tabs.setCurrentIndex(index)
        tab.setFocus()

    @property
    def tab_count(self):
        """
        Returns the number of active tabs.
        """
        return self.tabs.count()

    @property
    def widgets(self):
        """
        Returns a list of references to the widgets representing tabs in the
        editor.
        """
        return [self.tabs.widget(i) for i in range(self.tab_count)]

    @property
    def modified(self):
        """
        Returns a boolean indication if there are any modified tabs in the
        editor.
        """
        for widget in self.widgets:
            if widget.isModified():
                return True
        return False

    def add_filesystem(self, home):
        """
        Adds the file system pane to the application.
        """
        self.fs_pane = FileSystemPane(home)
        self.fs = QDockWidget(_('Filesystem on micro:bit'))
        self.fs.setWidget(self.fs_pane)
        self.fs.setFeatures(QDockWidget.DockWidgetMovable)
        self.fs.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.fs)
        self.fs_pane.setFocus()
        self.connect_zoom(self.fs_pane)

    def add_micropython_repl(self, repl, name):
        """
        Adds a MicroPython based REPL pane to the application.
        """
        repl_pane = MicroPythonREPLPane(port=repl.port, theme=self.theme)
        self.add_repl(repl_pane, name)

    def add_jupyter_repl(self, repl):
        """
        Adds a Jupyter based REPL pane to the application.
        """
        kernel = repl.kernel
        kernel.gui = 'qt4'
        kernel_client = repl.client()
        kernel_client.start_channels()
        ipython_widget = JupyterREPLPane(theme=self.theme)
        ipython_widget.kernel_manager = repl
        ipython_widget.kernel_client = kernel_client
        self.add_repl(ipython_widget, _('Python3 (Jupyter)'))

    def add_repl(self, repl_pane, name):
        """
        Adds the referenced REPL pane to the application.
        """
        self.repl_pane = repl_pane
        self.repl = QDockWidget(_('{} REPL').format(name))
        self.repl.setWidget(repl_pane)
        self.repl.setFeatures(QDockWidget.DockWidgetMovable)
        self.repl.setAllowedAreas(Qt.BottomDockWidgetArea |
                                  Qt.LeftDockWidgetArea |
                                  Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.repl)
        self.connect_zoom(self.repl_pane)
        self.repl_pane.setFocus()

    def add_python3_runner(self, name, path):
        """
        Display console output for the referenced running Python script.
        """
        self.process_runner = PythonProcessPane()
        self.runner = QDockWidget(name)
        self.runner.setWidget(self.process_runner)
        self.runner.setFeatures(QDockWidget.DockWidgetMovable)
        self.runner.setAllowedAreas(Qt.BottomDockWidgetArea |
                                    Qt.LeftDockWidgetArea |
                                    Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.runner)
        self.process_runner.start_process(path, name)
        self.process_runner.setFocus()
        self.connect_zoom(self.process_runner)
        return self.process_runner

    def add_debug_inspector(self):
        """
        Display a debug inspector to view the call stack.
        """
        self.debug_inspector = DebugInspector()
        self.debug_model = QStandardItemModel()
        self.debug_inspector.setModel(self.debug_model)
        self.debug_inspector.setUniformRowHeights(True)
        self.inspector = QDockWidget(_('Debug Inspector'))
        self.inspector.setWidget(self.debug_inspector)
        self.inspector.setFeatures(QDockWidget.DockWidgetMovable)
        self.inspector.setAllowedAreas(Qt.BottomDockWidgetArea |
                                       Qt.LeftDockWidgetArea |
                                       Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector)
        self.connect_zoom(self.debug_inspector)

    def update_debug_inspector(self, locals_dict):
        """
        Given the contents of a dict representation of the locals in the
        current stack frame, update the debug inspector with the new values.
        """
        excluded_names = ['__builtins__', '__debug_code__',
                          '__debug_script__', ]
        names = sorted([x for x in locals_dict if x not in excluded_names])
        self.debug_model.clear()
        self.debug_model.setHorizontalHeaderLabels([_('Name'), _('Value'), ])
        for name in names:
            try:
                # DANGER!
                val = eval(locals_dict[name])
            except Exception:
                val = None
            if isinstance(val, list):
                # Show a list consisting of rows of position/value
                list_item = QStandardItem(name)
                for i, i_val in enumerate(val):
                    list_item.appendRow([
                        QStandardItem(str(i)),
                        QStandardItem(repr(i_val))
                    ])
                self.debug_model.appendRow([
                    list_item,
                    QStandardItem(_('(A list of {} items.)').format(len(val)))
                ])
            elif isinstance(val, dict):
                # Show a dict consisting of rows of key/value pairs.
                dict_item = QStandardItem(name)
                for k, k_val in val.items():
                    dict_item.appendRow([
                        QStandardItem(repr(k)),
                        QStandardItem(repr(k_val))
                    ])
                self.debug_model.appendRow([
                    dict_item,
                    QStandardItem(_('(A dict of {} items.)').format(len(val)))
                ])
            else:
                self.debug_model.appendRow([
                    QStandardItem(name),
                    QStandardItem(locals_dict[name]),
                ])

    def remove_filesystem(self):
        """
        Removes the file system pane from the application.
        """
        if hasattr(self, 'fs') and self.fs:
            self.fs_pane = None
            self.fs.setParent(None)
            self.fs.deleteLater()
            self.fs = None

    def remove_repl(self):
        """
        Removes the REPL pane from the application.
        """
        if hasattr(self, 'repl') and self.repl:
            self.repl_pane = None
            self.repl.setParent(None)
            self.repl.deleteLater()
            self.repl = None

    def remove_python_runner(self):
        """
        Removes the runner pane from the application.
        """
        if hasattr(self, 'runner') and self.runner:
            self.process_runner = None
            self.runner.setParent(None)
            self.runner.deleteLater()
            self.runner = None

    def remove_debug_inspector(self):
        """
        Removes the debug inspector pane from the application.
        """
        if hasattr(self, 'inspector') and self.inspector:
            self.debug_inspector = None
            self.debug_model = None
            self.inspector.setParent(None)
            self.inspector.deleteLater()
            self.inspector = None

    def set_theme(self, theme):
        """
        Sets the theme for the REPL and editor tabs.
        """
        self.setStyleSheet(DAY_STYLE)
        self.theme = theme
        new_theme = DayTheme
        new_icon = 'theme'
        if theme == 'night':
            new_theme = NightTheme
            new_icon = 'theme_day'
            self.setStyleSheet(NIGHT_STYLE)
        for widget in self.widgets:
            widget.set_theme(new_theme)
        self.button_bar.slots['theme'].setIcon(load_icon(new_icon))
        if hasattr(self, 'repl') and self.repl:
            self.repl_pane.set_theme(theme)

    def show_logs(self, log, theme):
        """
        Display the referenced content of the log.
        """
        log_box = LogDisplay()
        log_box.setup(log, theme)
        log_box.exec()

    def show_message(self, message, information=None, icon=None):
        """
        Displays a modal message to the user.

        If information is passed in this will be set as the additional
        informative text in the modal dialog.

        Since this mechanism will be used mainly for warning users that
        something is awry the default icon is set to "Warning". It's possible
        to override the icon to one of the following settings: NoIcon,
        Question, Information, Warning or Critical.
        """
        message_box = QMessageBox(self)
        message_box.setText(message)
        message_box.setWindowTitle('Mu')
        if information:
            message_box.setInformativeText(information)
        if icon and hasattr(message_box, icon):
            message_box.setIcon(getattr(message_box, icon))
        else:
            message_box.setIcon(message_box.Warning)
        logger.debug(message)
        logger.debug(information)
        message_box.exec()

    def show_confirmation(self, message, information=None, icon=None):
        """
        Displays a modal message to the user to which they need to confirm or
        cancel.

        If information is passed in this will be set as the additional
        informative text in the modal dialog.

        Since this mechanism will be used mainly for warning users that
        something is awry the default icon is set to "Warning". It's possible
        to override the icon to one of the following settings: NoIcon,
        Question, Information, Warning or Critical.
        """
        message_box = QMessageBox()
        message_box.setText(message)
        message_box.setWindowTitle(_('Mu'))
        if information:
            message_box.setInformativeText(information)
        if icon and hasattr(message_box, icon):
            message_box.setIcon(getattr(message_box, icon))
        else:
            message_box.setIcon(message_box.Warning)
        message_box.setStandardButtons(message_box.Cancel | message_box.Ok)
        message_box.setDefaultButton(message_box.Cancel)
        logger.debug(message)
        logger.debug(information)
        return message_box.exec()

    def update_title(self, filename=None):
        """
        Updates the title bar of the application. If a filename (representing
        the name of the file currently the focus of the editor) is supplied,
        append it to the end of the title.
        """
        title = self.title
        if filename:
            title += ' - ' + filename
        self.setWindowTitle(title)

    def autosize_window(self):
        """
        Makes the editor 80% of the width*height of the screen and centres it.
        """
        screen = QDesktopWidget().screenGeometry()
        w = int(screen.width() * 0.8)
        h = int(screen.height() * 0.8)
        self.resize(w, h)
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def reset_annotations(self):
        """
        Resets the state of annotations on the current tab.
        """
        self.current_tab.reset_annotations()

    def annotate_code(self, feedback, annotation_type):
        """
        Given a list of annotations about the code in the current tab, add
        the annotations to the editor window so the user can make appropriate
        changes.
        """
        self.current_tab.annotate_code(feedback, annotation_type)

    def setup(self, breakpoint_toggle, theme):
        """
        Sets up the window.

        Defines the various attributes of the window and defines how the user
        interface is laid out.
        """
        self.theme = theme
        self.breakpoint_toggle = breakpoint_toggle
        # Give the window a default icon, title and minimum size.
        self.setWindowIcon(load_icon(self.icon))
        self.update_title()
        self.read_only_tabs = False
        self.setMinimumSize(800, 400)

        self.widget = QWidget()

        widget_layout = QVBoxLayout()
        self.widget.setLayout(widget_layout)
        self.button_bar = ButtonBar(self.widget)
        self.tabs = FileTabs()
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        self.addToolBar(self.button_bar)
        self.show()
        self.autosize_window()

    def resizeEvent(self, resizeEvent):
        """
        Respond to window getting too small for the button bar to fit well.
        """
        size = resizeEvent.size()
        self.button_bar.set_responsive_mode(size.width(), size.height())

    def select_mode(self, modes, current_mode, theme):
        """
        Display the mode selector dialog and return the result.
        """
        mode_select = ModeSelector()
        mode_select.setup(modes, current_mode, theme)
        mode_select.exec()
        try:
            return mode_select.get_mode()
        except Exception as ex:
            return None

    def change_mode(self, mode):
        """
        Given a an object representing a mode, recreates the button bar with
        the expected functionality.
        """
        self.button_bar.change_mode(mode)
        # Update the autocomplete / tooltip APIs for each tab to the new mode.
        api = mode.api()
        for widget in self.widgets:
            widget.set_api(api)

    def set_usb_checker(self, duration, callback):
        """
        Sets up a timer that polls for USB changes via the "callback" every
        "duration" seconds.
        """
        self.usb_checker = QTimer()
        self.usb_checker.timeout.connect(callback)
        self.usb_checker.start(duration * 1000)

    def set_timer(self, duration, callback):
        """
        Set a repeating timer to call "callback" every "duration" seconds.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(callback)
        self.timer.start(duration * 1000)  # Measured in milliseconds.

    def stop_timer(self):
        """
        Stop the repeating timer.
        """
        if self.timer:
            self.timer.stop()
            self.timer = None


class StatusBar(QStatusBar):
    """
    Defines the look and behaviour of the status bar along the bottom of the
    UI.
    """
    def __init__(self, parent=None, mode='python'):
        super().__init__(parent)
        self.mode = mode
        # Mode selector.
        self.mode_label = QLabel()
        self.mode_label.setToolTip(_("Select edit mode."))
        self.addPermanentWidget(self.mode_label)
        self.set_mode(mode)
        # Logs viewer
        self.logs_label = QLabel()
        self.logs_label.setPixmap(load_pixmap('logs').scaledToHeight(24))
        self.logs_label.setToolTip(_('View logs.'))
        self.addPermanentWidget(self.logs_label)

    def connect_logs(self, handler):
        """
        Connect the mouse press event for the log widget to the referenced
        handler function.
        """
        self.logs_label.mousePressEvent = handler

    def connect_mode(self, handler):
        """
        Connect the mouse press event for the mode widget to the referenced
        handler function.
        """
        self.mode_label.mousePressEvent = handler

    def set_message(self, message, pause=5000):
        """
        Displays a message in the status bar for a certain period of time.
        """
        self.showMessage(message, pause)

    def set_mode(self, mode):
        """
        Updates the mode label to the new mode.
        """
        self.mode_label.setText(mode.capitalize())


class ModeItem(QListWidgetItem):
    """
    Represents an available mode listed for selection.
    """

    def __init__(self, name, description, icon, parent=None):
        super().__init__(parent)
        self.name = name
        self.description = description
        self.icon = icon
        text = "{}\n{}".format(name, description)
        self.setText(text)
        self.setIcon(load_icon(self.icon))


class ModeSelector(QDialog):
    """
    Defines a UI for selecting the mode for Mu.
    """

    def setup(self, modes, current_mode, theme):
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        else:
            self.setStyleSheet(NIGHT_STYLE)
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_('Select Mode'))
        widget_layout = QVBoxLayout()
        label = QLabel(_('Please select the desired mode then click "OK". '
                         'Otherwise, click "Cancel".'))
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.setLayout(widget_layout)
        self.mode_list = QListWidget()
        widget_layout.addWidget(self.mode_list)
        self.mode_list.setIconSize(QSize(48, 48))
        for name, item in modes.items():
            if not item.is_debugger:
                ModeItem(item.name, item.description, item.icon,
                         self.mode_list)
        self.mode_list.sortItems()
        instructions = QLabel(_('You can change mode at any time by clicking '
                                'the name of the current mode shown in the '
                                ' bottom right-hand corner of Mu.'))
        instructions.setWordWrap(True)
        widget_layout.addWidget(instructions)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok |
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        widget_layout.addWidget(button_box)

    def get_mode(self):
        """
        Return details of the newly selected mode.
        """
        if self.result() == QDialog.Accepted:
            return self.mode_list.currentItem().icon
        else:
            raise RuntimeError('Mode change cancelled.')


class LogDisplay(QDialog):
    """
    Defines the UI for displaying the logs produced by Mu.
    """

    def setup(self, log, theme):
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        else:
            self.setStyleSheet(NIGHT_STYLE)
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_('Mu Debug Log'))
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        label = QLabel(_('When reporting a bug, copy and paste the content of '
                         'the following log file.'))
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.log_text_area = QPlainTextEdit()
        self.log_text_area.setReadOnly(True)
        self.log_text_area.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.log_text_area.setPlainText(log)
        widget_layout.addWidget(self.log_text_area)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        widget_layout.addWidget(button_box)


class JupyterREPLPane(RichJupyterWidget):
    """
    REPL = Read, Evaluate, Print, Loop.

    Displays a Jupyter iPython session.
    """

    def __init__(self, theme='day', parent=None):
        super().__init__(parent)
        self.set_theme(theme)
        self.console_height = 10

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        stylesheet = ("QWidget{font-size: " + str(new_size) +
                      "pt; font-family: Monospace;}")
        self.setStyleSheet(stylesheet)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font.pointSize()
        new_size = min(old_size + delta, 34)
        self.set_font_size(new_size)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font.pointSize()
        new_size = max(old_size - delta, 4)
        self.set_font_size(new_size)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.set_default_style()
            self.setStyleSheet(DAY_STYLE)
        else:
            self.set_default_style(colors='nocolor')
            self.setStyleSheet(NIGHT_STYLE)


class MicroPythonREPLPane(QTextEdit):
    """
    REPL = Read, Evaluate, Print, Loop.

    This widget represents a REPL client connected to a BBC micro:bit running
    MicroPython.

    The device MUST be flashed with MicroPython for this to work.
    """

    def __init__(self, port, theme='day', parent=None):
        super().__init__(parent)
        self.setFont(Font().load())
        self.setAcceptRichText(False)
        self.setReadOnly(False)
        self.setUndoRedoEnabled(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.setObjectName('replpane')
        # open the serial port
        self.serial = QSerialPort(self)
        self.serial.setPortName(port)
        if self.serial.open(QIODevice.ReadWrite):
            self.serial.setBaudRate(115200)
            self.serial.readyRead.connect(self.on_serial_read)
            # clear the text
            self.clear()
            # Send a Control-C
            self.serial.write(b'\x03')
        else:
            raise IOError("Cannot connect to device on port {}".format(port))
        self.set_theme(theme)

    def paste(self):
        """
        Grabs clipboard contents then sends down the serial port.
        """
        clipboard = QApplication.clipboard()
        if clipboard and clipboard.text():
            self.serial.write(bytes(clipboard.text(), 'utf8'))

    def context_menu(self):
        """"
        Creates custom context menu with just copy and paste.
        """
        menu = QMenu(self)
        if platform.system() == 'Darwin':
            copy_keys = QKeySequence(Qt.CTRL + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.Key_V)
        else:
            copy_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_C)
            paste_keys = QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_V)

        menu.addAction("Copy", self.copy, copy_keys)
        menu.addAction("Paste", self.paste, paste_keys)
        menu.exec_(QCursor.pos())

    def cursor_to_end(self):
        """
        Moves the cursor to the very end of the available text.
        """
        tc = self.textCursor()
        tc.movePosition(QTextCursor.End)
        self.setTextCursor(tc)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        else:
            self.setStyleSheet(NIGHT_STYLE)

    def on_serial_read(self):
        """
        Called when the application gets data from the connected device.
        """
        self.process_bytes(bytes(self.serial.readAll()))

    def keyPressEvent(self, data):
        """
        Called when the user types something in the REPL.

        Correctly encodes it and sends it to the connected device.
        """
        key = data.key()
        msg = bytes(data.text(), 'utf8')
        if key == Qt.Key_Backspace:
            msg = b'\b'
        elif key == Qt.Key_Up:
            msg = b'\x1B[A'
        elif key == Qt.Key_Down:
            msg = b'\x1B[B'
        elif key == Qt.Key_Right:
            msg = b'\x1B[C'
        elif key == Qt.Key_Left:
            msg = b'\x1B[D'
        elif key == Qt.Key_Home:
            msg = b'\x1B[H'
        elif key == Qt.Key_End:
            msg = b'\x1B[F'
        elif (platform.system() == 'Darwin' and
                data.modifiers() == Qt.MetaModifier) or \
             (platform.system() != 'Darwin' and
                data.modifiers() == Qt.ControlModifier):
            # Handle the Control key. On OSX/macOS/Darwin (python calls this
            # platform Darwin), this is handled by Qt.MetaModifier. Other
            # platforms (Linux, Windows) call this Qt.ControlModifier. Go
            # figure. See http://doc.qt.io/qt-5/qt.html#KeyboardModifier-enum
            if Qt.Key_A <= key <= Qt.Key_Z:
                # The microbit treats an input of \x01 as Ctrl+A, etc.
                msg = bytes([1 + key - Qt.Key_A])
        elif (data.modifiers() == Qt.ControlModifier | Qt.ShiftModifier) or \
                (platform.system() == 'Darwin' and
                    data.modifiers() == Qt.ControlModifier):
            # Command-key on Mac, Ctrl-Shift on Win/Lin
            if key == Qt.Key_C:
                self.copy()
                msg = b''
            elif key == Qt.Key_V:
                self.paste()
                msg = b''
        self.serial.write(msg)

    def process_bytes(self, data):
        """
        Given some incoming bytes of data, work out how to handle / display
        them in the REPL widget.
        """
        tc = self.textCursor()
        # The text cursor must be on the last line of the document. If it isn't
        # then move it there.
        while tc.movePosition(QTextCursor.Down):
            pass
        i = 0
        while i < len(data):
            if data[i] == 8:  # \b
                tc.movePosition(QTextCursor.Left)
                self.setTextCursor(tc)
            elif data[i] == 13:  # \r
                pass
            elif data[i] == 27 and data[i + 1] == 91:  # VT100 cursor: <Esc>[
                i += 2  # move index to after the [
                m = re.search(r'(?P<count>[\d]*)(?P<action>[ABCDK])',
                              data[i:].decode('utf-8'))

                # move to (almost) after control seq (will ++ at end of loop)
                i += m.end() - 1

                if m.group("count") == '':
                    count = 1
                else:
                    count = int(m.group("count"))

                if m.group("action") == "A":  # up
                    tc.movePosition(QTextCursor.Up, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "B":  # down
                    tc.movePosition(QTextCursor.Down, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "C":  # right
                    tc.movePosition(QTextCursor.Right, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "D":  # left
                    tc.movePosition(QTextCursor.Left, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "K":  # delete things
                    if m.group("count") == "":  # delete to end of line
                        tc.movePosition(QTextCursor.EndOfLine,
                                        mode=QTextCursor.KeepAnchor)
                        tc.removeSelectedText()
                        self.setTextCursor(tc)
            elif data[i] == 10:  # \n
                tc.movePosition(QTextCursor.End)
                self.setTextCursor(tc)
                self.insertPlainText(chr(data[i]))
            else:
                tc.deleteChar()
                self.setTextCursor(tc)
                self.insertPlainText(chr(data[i]))
            i += 1
        self.ensureCursorVisible()

    def clear(self):
        """
        Clears the text of the REPL.
        """
        self.setText('')


class MuFileList(QListWidget):
    """
    Contains shared methods for the two types of file listing used in Mu.
    """

    def disable(self, sibling):
        """
        Stops interaction with the list widgets.
        """
        self.setDisabled(True)
        sibling.setDisabled(True)
        self.setAcceptDrops(False)
        sibling.setAcceptDrops(False)

    def enable(self, sibling):
        """
        Allows interaction with the list widgets.
        """
        self.setDisabled(False)
        sibling.setDisabled(False)
        self.setAcceptDrops(True)
        sibling.setAcceptDrops(True)

    def show_confirm_overwrite_dialog(self):
        """
        Display a dialog to check if an existing file should be overwritten.

        Returns a boolean indication of the user's decision.
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(_("File already exists; overwrite it?"))
        msg.setWindowTitle(_("File already exists"))
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec_() == QMessageBox.Ok


class MicrobitFileList(MuFileList):
    """
    Represents a list of files on the micro:bit.
    """

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.setDragDropMode(QListWidget.DragDrop)

    def dropEvent(self, event):
        source = event.source()
        self.disable(source)
        if isinstance(source, LocalFileList):
            file_exists = self.findItems(source.currentItem().text(),
                                         Qt.MatchExactly)
            if not file_exists or \
                    file_exists and self.show_confirm_overwrite_dialog():
                local_filename = os.path.join(self.home,
                                              source.currentItem().text())
                logger.info("Putting {}".format(local_filename))
                try:
                    with microfs.get_serial() as serial:
                        logger.info(serial.port)
                        microfs.put(serial, local_filename)
                    super().dropEvent(event)
                except Exception as ex:
                    logger.error(ex)
        self.enable(source)
        if self.parent() is not None:
            self.parent().ls()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        delete_action = menu.addAction(_("Delete (cannot be undone)"))
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == delete_action:
            self.setDisabled(True)
            self.setAcceptDrops(False)
            microbit_filename = self.currentItem().text()
            logger.info("Deleting {}".format(microbit_filename))
            try:
                with microfs.get_serial() as serial:
                    logger.info(serial.port)
                    microfs.rm(serial, microbit_filename)
                self.takeItem(self.currentRow())
            except Exception as ex:
                logger.error(ex)
            self.setDisabled(False)
            self.setAcceptDrops(True)


class LocalFileList(MuFileList):
    """
    Represents a list of files in the Mu directory on the local machine.
    """

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.setDragDropMode(QListWidget.DragDrop)

    def dropEvent(self, event):
        source = event.source()
        self.disable(source)
        if isinstance(source, MicrobitFileList):
            file_exists = self.findItems(source.currentItem().text(),
                                         Qt.MatchExactly)
            if not file_exists or \
                    file_exists and self.show_confirm_overwrite_dialog():
                microbit_filename = source.currentItem().text()
                local_filename = os.path.join(self.home,
                                              microbit_filename)
                logger.debug("Getting {} to {}".format(microbit_filename,
                                                       local_filename))
                try:
                    with microfs.get_serial() as serial:
                        logger.info(serial.port)
                        microfs.get(serial, microbit_filename, local_filename)
                    super().dropEvent(event)
                except Exception as ex:
                    logger.error(ex)
        self.enable(source)
        if self.parent() is not None:
            self.parent().ls()


class FileSystemPane(QFrame):
    """
    Contains two QListWidgets representing the micro:bit and the user's code
    directory. Users transfer files by dragging and dropping. Highlighted files
    can be selected for deletion.
    """

    def __init__(self, home):
        super().__init__()
        self.home = home
        self.font = Font().load()
        microbit_fs = MicrobitFileList(home)
        local_fs = LocalFileList(home)
        layout = QGridLayout()
        self.setLayout(layout)
        microbit_label = QLabel()
        microbit_label.setText(_('Files on your micro:bit:'))
        local_label = QLabel()
        local_label.setText(_('Files on your computer:'))
        self.microbit_label = microbit_label
        self.local_label = local_label
        self.microbit_fs = microbit_fs
        self.local_fs = local_fs
        self.set_font_size()
        layout.addWidget(microbit_label, 0, 0)
        layout.addWidget(local_label, 0, 1)
        layout.addWidget(microbit_fs, 1, 0)
        layout.addWidget(local_fs, 1, 1)
        self.ls()

    def ls(self):
        """
        Gets a list of the files on the micro:bit.

        Naive implementation for simplicity's sake.
        """
        self.microbit_fs.clear()
        self.local_fs.clear()
        microbit_files = microfs.ls(microfs.get_serial())
        for f in microbit_files:
            self.microbit_fs.addItem(f)
        local_files = [f for f in os.listdir(self.home)
                       if os.path.isfile(os.path.join(self.home, f))]
        local_files.sort()
        for f in local_files:
            self.local_fs.addItem(f)

    def set_theme(self, theme):
        """
        Sets the theme / look for the FileSystemPane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        else:
            self.setStyleSheet(NIGHT_STYLE)

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        self.font.setPointSize(new_size)
        self.microbit_label.setFont(self.font)
        self.local_label.setFont(self.font)
        self.microbit_fs.setFont(self.font)
        self.local_fs.setFont(self.font)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font.pointSize()
        new_size = min(old_size + delta, 34)
        self.set_font_size(new_size)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font.pointSize()
        new_size = max(old_size - delta, 4)
        self.set_font_size(new_size)


class PythonProcessPane(QTextEdit):
    """
    Captures, displays and works with the stdin, stdout and stderr of a Python
    process.

    Used for running / debugging standard Python3 scripts.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(Font().load())
        self.input_buffer = []

    def start_process(self, workspace, script):
        """
        Start the child process from the workspace with the script.
        """
        self.script = os.path.abspath(os.path.normcase(script))
        logger.info('Running script: {}'.format(script))
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        # Force buffers to flush immediately.
        env = QProcessEnvironment.systemEnvironment()
        env.insert('PYTHONUNBUFFERED', '1')
        self.process.setProcessEnvironment(env)
        logger.info('Working directory: {}'.format(workspace))
        self.process.setWorkingDirectory(workspace)
        self.process.readyRead.connect(self.read)
        self.process.finished.connect(self.finished)
        self.process.start('mu-debug', [self.script])

    def finished(self, code, status):
        """
        Called when the process is finished.
        """
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(_('\n\n---------- FINISHED ----------\n'))
        msg = _('exit code: {} status: {}').format(code, status)
        cursor.insertText(msg)
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.setReadOnly(True)

    def append(self, byte_stream):
        """
        Append text to the text area.
        """
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(byte_stream.decode('utf-8'))
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    def delete(self):
        """
        Removes a character from the end of the text (to facilitate when a
        user presses the delete button).
        """
        if self.input_buffer:
            self.input_buffer.pop()
            cursor = self.textCursor()
            cursor.movePosition(cursor.End)
            cursor.deletePreviousChar()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)

    def read(self):
        """
        From the process's stdout.
        """
        self.input_buffer = []
        self.append(self.process.readAll().data())

    def keyPressEvent(self, data):
        """
        Called when the user types something in the REPL.

        Correctly encodes it and sends it to the connected process.
        """
        key = data.key()
        msg = bytes(data.text(), 'utf8')
        if key == Qt.Key_Backspace:
            msg = b'\b'
        elif (data.modifiers() == Qt.ControlModifier | Qt.ShiftModifier) or \
                (platform.system() == 'Darwin' and
                    data.modifiers() == Qt.ControlModifier):
            # Command-key on Mac, Ctrl-Shift on Win/Lin
            if key == Qt.Key_C:
                self.copy()
                msg = b''
            elif key == Qt.Key_V:
                self.paste()
                msg = b''
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            msg = b'\n'
        if key == Qt.Key_Backspace:
            self.delete()
        else:
            self.input_buffer.append(msg)
            if not self.isReadOnly():
                self.append(msg)
        if self.input_buffer and self.input_buffer[-1] == b'\n':
            if hasattr(self, 'process') and self.process:
                self.process.write(b''.join(self.input_buffer))
            self.input_buffer = []

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font().pointSize()
        new_size = old_size + delta
        if new_size <= 34:
            super().zoomIn(delta)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font().pointSize()
        new_size = old_size - delta
        if new_size >= 4:
            super().zoomOut(delta)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        else:
            self.setStyleSheet(NIGHT_STYLE)


class DebugInspector(QTreeView):
    """
    Presents a tree like representation of the current state of the call stack
    to the user.
    """

    def set_font_size(self, new_size=DEFAULT_FONT_SIZE):
        """
        Sets the font size for all the textual elements in this pane.
        """
        stylesheet = ("QWidget{font-size: " + str(new_size) +
                      "pt; font-family: Monospace;}")
        self.setStyleSheet(stylesheet)

    def zoomIn(self, delta=2):
        """
        Zoom in (increase) the size of the font by delta amount difference in
        point size upto 34 points.
        """
        old_size = self.font().pointSize()
        new_size = min(old_size + delta, 34)
        self.set_font_size(new_size)

    def zoomOut(self, delta=2):
        """
        Zoom out (decrease) the size of the font by delta amount difference in
        point size down to 4 points.
        """
        old_size = self.font().pointSize()
        new_size = max(old_size - delta, 4)
        self.set_font_size(new_size)

    def set_theme(self, theme):
        """
        Sets the theme / look for the REPL pane.
        """
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        else:
            self.setStyleSheet(NIGHT_STYLE)
