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
import logging
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QIODevice
from PyQt5.QtWidgets import (QToolBar, QAction, QStackedWidget, QDesktopWidget,
                             QWidget, QVBoxLayout, QShortcut, QSplitter,
                             QTabWidget, QFileDialog, QMessageBox, QTextEdit,
                             QFrame, QListWidget, QGridLayout, QLabel, QMenu)
from PyQt5.QtGui import QKeySequence, QColor, QTextCursor, QFontDatabase
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtSerialPort import QSerialPort
from mu.contrib import microfs
from mu.resources import load_icon, load_stylesheet, load_font_data


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
    Indicator = QColor('red')


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
    Indicator = QColor('white')


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

    def __init__(self, path, text, api=None):
        super().__init__()
        self.path = path
        self.setText(text)
        self.indicators = {}
        self.INDICATOR_NUMBER = 19  # arbitrary
        self.MARKER_NUMBER = 22  # also arbitrary
        self.api = api if api else []
        self.setModified(False)
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
        self.setTabWidth(4)
        self.setEdgeColumn(79)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, 50)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.set_theme()
        self.markerDefine(self.RightArrow, self.MARKER_NUMBER)
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_marker_clicked)
        self.setAnnotationDisplay(self.AnnotationBoxed)

    def set_theme(self, theme=DayTheme):
        """
        Connect the theme to a lexer and return the lexer for the editor to
        apply to the script text.
        """
        self.lexer = PythonLexer()
        theme.apply_to(self.lexer)
        self.lexer.setDefaultPaper(theme.Paper)
        self.setCaretForegroundColor(theme.Caret)
        self.setMarginsBackgroundColor(theme.Margin)
        self.setMarginsForegroundColor(theme.Caret)
        self.setIndicatorForegroundColor(theme.Indicator)
        self.setMarkerBackgroundColor(theme.Indicator, self.MARKER_NUMBER)

        api = QsciAPIs(self.lexer)
        for entry in self.api:
            api.add(entry)
        api.prepare()
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)

        self.setLexer(self.lexer)

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
        Clears all the assets (indicators, annotations and markers) associated
        with last code check.
        """
        self.clearAnnotations()
        self.markerDeleteAll()
        for line_no in self.indicators:
            self.clearIndicatorRange(line_no, 0, line_no, 999999,
                                     self.INDICATOR_NUMBER)
        self.indicators = {}

    def annotate_code(self, feedback):
        """
        Given a list of annotations add them to the editor pane so the user
        can act upon them.
        """
        self.indicatorDefine(self.SquiggleIndicator, self.INDICATOR_NUMBER)
        self.setIndicatorDrawUnder(True)
        for line_no, messages in feedback.items():
            marker_id = self.markerAdd(line_no, self.MARKER_NUMBER)
            col_start = 0
            col_end = 0
            self.indicators[marker_id] = messages
            for message in messages:
                col = message.get('column', 0)
                if col:
                    col_start = col - 1
                    col_end = col + 1
                    self.fillIndicatorRange(line_no, col_start, line_no,
                                            col_end, self.INDICATOR_NUMBER)

    def on_marker_clicked(self, margin, line, state):
        """
        Display something when the margin indicator is clicked.
        """
        marker_id = self.get_marker_at_line(line)
        if marker_id:
            if self.annotation(line):
                self.clearAnnotations(line)
            else:
                messages = [i['message'] for i in
                            self.indicators.get(marker_id, [])]
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
        for marker_id in self.indicators:
            if self.markerLine(marker_id) == line:
                return marker_id


class ButtonBar(QToolBar):
    """
    Represents the bar of buttons across the top of the editor and defines
    their behaviour.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.slots = {}

        self.setMovable(False)
        self.setIconSize(QSize(64, 64))
        self.setToolButtonStyle(3)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("StandardToolBar")

        self.addAction(name="new",
                       tool_text="Create a new MicroPython script.")
        self.addAction(name="load", tool_text="Load a MicroPython script.")
        self.addAction(name="save",
                       tool_text="Save the current MicroPython script.")
        self.addSeparator()
        self.addAction(name="flash",
                       tool_text="Flash your code onto the micro:bit.")
        self.addAction(name="files",
                       tool_text="Access the file system on the micro:bit.")
        self.addAction(name="repl",
                       tool_text="Use the REPL to live code the micro:bit.")
        self.addSeparator()
        self.addAction(name="zoom-in",
                       tool_text="Zoom in (to make the text bigger).")
        self.addAction(name="zoom-out",
                       tool_text="Zoom out (to make the text smaller).")
        self.addAction(name="theme",
                       tool_text="Change theme between day or night.")
        self.addSeparator()
        self.addAction(name="check",
                       tool_text="Check your code for mistakes.")
        self.addAction(name="help",
                       tool_text="Show help about Mu in a browser.")
        self.addAction(name="quit", tool_text="Quit Mu.")

    def addAction(self, name, tool_text):
        """
        Creates an action associated with an icon and name and adds it to the
        widget's slots.
        """
        action = QAction(load_icon(name), name.capitalize(), self,
                         toolTip=tool_text)
        super().addAction(action)
        self.slots[name] = action

    def connect(self, name, handler, *shortcuts):
        """
        Connects a named slot to a handler function and optional hot-key
        shortcuts.
        """
        self.slots[name].pyqtConfigure(triggered=handler)
        for shortcut in shortcuts:
            QShortcut(QKeySequence(shortcut),
                      self.parentWidget()).activated.connect(handler)


class FileTabs(QTabWidget):
    """
    Extend the base class so we can override the removeTab behaviour.
    """

    def __init__(self):
        super(FileTabs, self).__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)

    def removeTab(self, tab_id):
        """
        Ask the user before closing the file.
        """
        window = self.nativeParentWidget()
        modified = window.current_tab.isModified()
        if (modified):
            msg = 'There is un-saved work, closing the tab will cause you ' \
                  'to lose it.'
            if window.show_confirmation(msg) == QMessageBox.Cancel:
                return
        super(FileTabs, self).removeTab(tab_id)


class Window(QStackedWidget):
    """
    Defines the look and characteristics of the application's main window.
    """

    title = "Mu"
    icon = "icon"

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

    def add_tab(self, path, text):
        """
        Adds a tab with the referenced path and text to the editor.
        """
        new_tab = EditorPane(path, text, self.api)
        new_tab_index = self.tabs.addTab(new_tab, new_tab.label)

        @new_tab.modificationChanged.connect
        def on_modified():
            self.tabs.setTabText(new_tab_index, new_tab.label)

        self.tabs.setCurrentIndex(new_tab_index)
        self.connect_zoom(new_tab)
        self.set_theme(self.theme)
        new_tab.setFocus()

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
        self.fs = FileSystemPane(self.splitter, home)
        self.splitter.addWidget(self.fs)
        self.splitter.setSizes([66, 33])
        self.fs.setFocus()
        self.connect_zoom(self.fs)

    def add_repl(self, repl):
        """
        Adds the REPL pane to the application.
        """
        self.repl = REPLPane(port=repl.port, theme=self.theme)
        self.splitter.addWidget(self.repl)
        self.splitter.setSizes([66, 33])
        self.repl.setFocus()
        self.connect_zoom(self.repl)

    def remove_filesystem(self):
        """
        Removes the file system pane from the application.
        """
        self.fs.setParent(None)
        self.fs.deleteLater()
        self.fs = None

    def remove_repl(self):
        """
        Removes the REPL pane from the application.
        """
        self.repl.setParent(None)
        self.repl.deleteLater()
        self.repl = None

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
            self.repl.set_theme(theme)

    def show_message(self, message, information=None, icon=None, parent=None):
        """
        Displays a modal message to the user.

        If information is passed in this will be set as the additional
        informative text in the modal dialog.

        Since this mechanism will be used mainly for warning users that
        something is awry the default icon is set to "Warning". It's possible
        to override the icon to one of the following settings: NoIcon,
        Question, Information, Warning or Critical.
        """
        message_box = QMessageBox(parent)
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

    def show_confirmation(self, message, information=None, icon=None, parent=None):
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
        message_box = QMessageBox(parent)
        message_box.setText(message)
        message_box.setWindowTitle('Mu')
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

    def annotate_code(self, feedback):
        """
        Given a list of annotations about the code in the current tab, add
        the annotations to the editor window so the user can make appropriate
        changes.
        """
        self.current_tab.annotate_code(feedback)

    def setup(self, theme, api=None):
        """
        Sets up the window.

        Defines the various attributes of the window and defines how the user
        interface is laid out.
        """
        self.theme = theme
        self.api = api if api else []
        # Give the window a default icon, title and minimum size.
        self.setWindowIcon(load_icon(self.icon))
        self.update_title()
        self.setMinimumSize(926, 600)

        self.widget = QWidget()
        self.splitter = QSplitter(Qt.Vertical)

        widget_layout = QVBoxLayout()
        self.widget.setLayout(widget_layout)

        self.button_bar = ButtonBar(self.widget)

        widget_layout.addWidget(self.button_bar)
        widget_layout.addWidget(self.splitter)
        self.tabs = FileTabs()
        self.splitter.addWidget(self.tabs)

        self.addWidget(self.widget)
        self.setCurrentWidget(self.widget)

        self.set_theme(theme)
        self.show()
        self.autosize_window()


class REPLPane(QTextEdit):
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
        elif data.modifiers() == Qt.ControlModifier:
        #     # Handle the Control key.  I would've expected us to have to test
        #     # for Qt.ControlModifier, but on (my!) OSX Qt.MetaModifier does
        #     # correspond to the Control key.  I've read something that suggests
        #     # that it's different on other platforms.
        #     # see http://doc.qt.io/qt-5/qt.html#KeyboardModifier-enum
             if Qt.Key_A <= key <= Qt.Key_Z:
        #         # The microbit treats an input of \x01 as Ctrl+A, etc.
                 msg = bytes([1 + key - Qt.Key_A])
        self.serial.write(msg)

    def process_bytes(self, bs):
        """
        Given some incoming bytes of data, work out how to handle / display
        them in the REPL widget.
        """
        tc = self.textCursor()
        logger.debug(bs)
        # The text cursor must be on the last line of the document. If it isn't
        # then move it there.
        while tc.movePosition(QTextCursor.Down):
            pass
        i = 0
        while i < len(bs):
            if bs[i] == 8:  # \b
                tc.movePosition(QTextCursor.Left)
                self.setTextCursor(tc)
            elif bs[i] == ord('\r'):
                pass
            elif bs[i] == 0x1b and bs[i+1] == ord('['):  #VT100 cursor control
                i += 2  # move index to after the [
                m = re.search(r'(?P<count>[\d]*)(?P<action>[ABCDK])', bs[i:].decode('ascii', errors='ignore'))
                i += m.end() - 1  #move to (almost) after the control seq (will increment at end of loop)

                if m.group("count") == '':
                    count = 1
                else:
                    count = int(m.group("count"))

                if m.group("action") == "A":  #up
                    tc.movePosition(QTextCursor.Up, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "B":  #down
                    tc.movePosition(QTextCursor.Down, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "C":  #right
                    tc.movePosition(QTextCursor.Right, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "D":  #left
                    tc.movePosition(QTextCursor.Left, n=count)
                    self.setTextCursor(tc)
                elif m.group("action") == "K":  #delete things
                    if m.group("count") == "":  #delete to end of line
                        tc.movePosition(QTextCursor.EndOfLine, mode=QTextCursor.KeepAnchor)
                        tc.removeSelectedText()
                        self.setTextCursor(tc)
            elif bs[i] == ord('\n'):
                tc.movePosition(QTextCursor.End)
                self.setTextCursor(tc)
                self.insertPlainText(chr(bs[i]))
            else:
                tc.deleteChar()
                self.setTextCursor(tc)
                self.insertPlainText(chr(bs[i]))
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

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete (cannot be undone)")
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


class FileSystemPane(QFrame):
    """
    Contains two QListWidgets representing the micro:bit and the user's code
    directory. Users transfer files by dragging and dropping. Highlighted files
    can be selected for deletion.
    """

    def __init__(self, parent, home):
        super().__init__(parent)
        self.home = home
        self.font = Font().load()
        microbit_fs = MicrobitFileList(home)
        local_fs = LocalFileList(home)
        layout = QGridLayout()
        self.setLayout(layout)
        microbit_label = QLabel()
        microbit_label.setText('Files on your micro:bit:')
        local_label = QLabel()
        local_label.setText('Files on your computer:')
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
