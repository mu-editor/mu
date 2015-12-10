import sys
import os
import os.path
import keyword

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QToolBar, QAction, QScrollArea,
    QSplitter, QFileDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont
from mu.resources import load_icon


# Directories
HOME_DIRECTORY = os.path.expanduser('~')
MICROPYTHON_DIRECTORY = os.path.join(HOME_DIRECTORY, 'micropython')
if not os.path.exists(MICROPYTHON_DIRECTORY):
    os.mkdir(MICROPYTHON_DIRECTORY)


# FONT related constants:
DEFAULT_FONT_SIZE = 11
DEFAULT_FONT = 'Bitstream Vera Sans Mono'
# Platform specific alternatives...
if sys.platform == 'win32':
    DEFAULT_FONT = 'Consolas'
elif sys.platform == 'darwin':
    DEFAULT_FONT = 'Monaco'


class Font:
    def __init__(self, color='black', paper='white', bold=False, italic=False):
        self.color = color
        self.paper = paper
        self.bold = bold
        self.italic = italic


ALL_STYLES = -1


class Theme:
    @classmethod
    def apply_to(cls, lexer):
        # Apply a font for all styles
        font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        font.setBold(False)
        font.setItalic(False)
        lexer.setFont(font, ALL_STYLES)

        for name, font in cls.__dict__.items():
            if not isinstance(font, Font):
                continue

            style_num = getattr(lexer, name)
            lexer.setColor(QColor(font.color), style_num)
            lexer.setEolFill(True, style_num)
            lexer.setPaper(QColor(font.paper), style_num)
            if font.bold or font.italic:
                f = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
                f.setBold(font.bold)
                f.setItalic(font.italic)
                lexer.setFont(f, style_num)


class PythonTheme(Theme):
    FunctionMethodName = ClassName = Font(color='#0000a0')
    UnclosedString = Font(paper='#00fd00')
    Comment = CommentBlock = Font(color='gray')
    Keyword = Font(color='#008080', bold=True)
    SingleQuotedString = DoubleQuotedString = Font(color='#800000')
    TripleSingleQuotedString = TripleDoubleQuotedString = Font(color='#060')
    Number = Font(color='#00008B')
    Decorator = Font(color='#cc6600')
    Default = Identifier = Font()
    Operator = Font(color='#400040')
    HighlightedIdentifier = Font(color='#0000a0')


class PythonLexer(QsciLexerPython):
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
        self.configure()

    def configure(self):
        """Set up the editor component."""
        # Font information
        font = QFont(DEFAULT_FONT)
        font.setFixedPitch(True)
        font.setPointSize(DEFAULT_FONT_SIZE)
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
        # Use the lexer defined above (and must save a reference to it)
        self.lexer = self.choose_lexer()
        self.setLexer(self.lexer)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

    def choose_lexer(self):
        _, ext = os.path.splitext(self.path)
        if ext == '.py':
            lex = PythonLexer()
            PythonTheme.apply_to(lex)
            return lex
        return None

    def needs_write(self):
        return self.isModified()


class ButtonBar(QToolBar):
    """
    Represents the bar of buttons across the top of the editor and defines
    their behaviour.
    """

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.configure()

    def configure(self):
        """Set up the buttons"""
        self.setMovable(False)
        self.setIconSize(QSize(64, 64))
        self.setToolButtonStyle(3)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("StandardToolBar")
        # Create actions to be added to the button bar.
        self.new_script_act = QAction(
            load_icon("new"),
            "New", self,
            statusTip="Create a new MicroPython script.",
            triggered=self.editor.new)

        self.load_python_file_act = QAction(
            load_icon("load"),
            "Load", self,
            statusTip="Load a MicroPython script.",
            triggered=self.editor.load)

        self.save_python_file_act = QAction(
            load_icon("save"),
            "Save", self,
            statusTip="Save the current MicroPython script.",
            triggered=self.editor.save)

        self.snippets_act = QAction(
            load_icon("snippets"),
            "Snippets", self,
            statusTip="Use code snippets to help you program.",
            triggered=self.editor.snippets)

        self.flash_act = QAction(
            load_icon("flash"),
            "Flash", self,
            statusTip="Flash your MicroPython script onto the micro:bit.",
            triggered=self.editor.flash)

        self.repl_act = QAction(
            load_icon("repl"),
            "REPL", self,
            statusTip="Connect to the MicroPython REPL for live coding of the micro:bit.",
            triggered=self.editor.repl)

        self.zoom_in_act = QAction(
            load_icon("zoom-in"),
            "Zoom In", self,
            statusTip="Zoom in (to make the text bigger).",
            triggered=self.editor.zoom_in)

        self.zoom_out_act = QAction(
            load_icon("zoom-out"),
            "Zoom Out", self,
            statusTip="Zoom out (to make the text smaller).",
            triggered=self.editor.zoom_out)
        # Add the actions to the button bar.
        self.addAction(self.new_script_act)
        self.addAction(self.load_python_file_act)
        self.addAction(self.save_python_file_act)
        self.addSeparator()
        self.addAction(self.snippets_act)
        self.addAction(self.flash_act)
        self.addAction(self.repl_act)
        self.addSeparator()
        self.addAction(self.zoom_in_act)
        self.addAction(self.zoom_out_act)


class TabPane(QTabWidget):
    def __len__(self):
        return self.count()

    def __getitem__(self, index):
        t = self.widget(index)
        if not t:
            raise IndexError(index)
        return t


class Editor(QWidget):
    """
    Represents the application.
    """
    def __init__(self, project, parent=None):
        super().__init__(parent)
        self.project = project

        # Vertical box layout.
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # The application has two aspects to it: buttons and the editor.
        self.buttons = ButtonBar(self)
        self.tabs = TabPane(parent=self)

        self.splitter = QSplitter(Qt.Vertical)
        # Add the buttons and editor to the user inteface.
        self.layout.addWidget(self.buttons)
        self.layout.addWidget(self.splitter)
        self.splitter.addWidget(self.tabs)
        # Ensure we have a minimal sensible size for the application.
        self.setMinimumSize(800, 600)

    def add_repl(self, repl):
        self.repl = repl
        self.add_pane(repl)

    def add_pane(self, pane):
        self.splitter.addWidget(pane)

    def add_tab(self, path, text):
        editor = EditorPane(path, text)
        self.tabs.addTab(editor, path)

    def add_svg(self, title, data):
        svg = QSvgWidget()
        svg.load(data)
        scrollpane = QScrollArea()
        scrollpane.setWidget(svg)
        self.tabs.addTab(scrollpane, title)

    def close(self):
        """Close this project."""
        self.save_all()
        self.parentWidget().close_project(self.project)

    def zoom_in(self):
        """Make the text BIGGER."""
        for tab in self.tabs:
            if hasattr(tab, 'zoomIn'):
                tab.zoomIn(2)
        if self.repl:
            self.repl.zoomIn(2)

    def zoom_out(self):
        """Make the text smaller."""
        for tab in self.tabs:
            if hasattr(tab, 'zoomOut'):
                tab.zoomOut(2)
        if self.repl:
            self.repl.zoomOut(2)

    def new(self):
        """New Python script."""
        pass

    def save(self):
        """Save the Python script."""
        pass

    def load(self):
        """Load a Python script."""
        filename, filetype = QFileDialog.getOpenFileName(self, 'Open file',
                                                         MICROPYTHON_DIRECTORY,
                                                         '*.py')
        try:
            with open(filename) as f:
                data = f.read()
        except FileNotFoundError:
            pass
        else:
            self.add_tab(filename, data)

    def snippets(self):
        """Use code snippets."""
        pass

    def flash(self):
        """Flash the micro:bit."""
        pass

    def repl(self):
        """Toggle the REPL pane."""
        pass
