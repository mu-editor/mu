import sys
import os
import os.path
import keyword

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QToolBar, QAction, QScrollArea,
    QSplitter, QFileDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont

from mu.hybrid.repl import REPLPane
from mu.hybrid.repl import find_microbit
from mu.resources import load_icon
from mu.views import chrome


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
        self.setModified(False)
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
        self.lexer = self.python_lexer()
        self.setLexer(self.lexer)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

    def python_lexer(self):
        lex = PythonLexer()
        PythonTheme.apply_to(lex)
        return lex

    def get_label(self):
        if self.path:
            label = os.path.basename(self.path)
        else:
            label = 'untitled'

        if self.isModified():
            return label + ' *'
        else:
            return label

    def needs_write(self):
        return self.isModified()


class TabPane(QTabWidget):
    def __len__(self):
        return self.count()

    def __getitem__(self, index):
        t = self.widget(index)
        if not t:
            raise IndexError(index)
        return t


class Editor:
    """
    Represents the application.
    """

    project = None
    
    @property
    def iter_tabs(self):
        for index in range(self.tabs.count):
            tab = self.tabs.widget(index)
            if not tab:
                raise IndexError(index)
            else:
                yield tab

    def __init__(self, splitter, tabs):
        self.splitter = splitter
        self.tabs = tabs

        mb_port = find_microbit()
        if mb_port:
            port = '/dev/{}'.format(mb_port)
            # Todo - Refactor some of this to model and controller
            replpane = REPLPane(port=port, parent=self)
            self.add_repl(replpane)

    def add_repl(self, repl):
        self.repl = repl
        self.add_pane(repl)

    def add_pane(self, pane):
        self.splitter.addWidget(pane)

    def add_tab(self, path, text):
        editor = EditorPane(path, text)
        tab_ix = self.tabs.addTab(editor, editor.get_label())
        editor.modificationChanged.connect(lambda: self.mark_tab_modified(tab_ix))
        self.tabs.setCurrentIndex(tab_ix)

    def mark_tab_modified(self, tab_ix):
        assert tab_ix == self.tabs.currentIndex()
        ed = self.tabs.currentWidget()
        self.tabs.setTabText(tab_ix, ed.get_label())

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
        for tab in self.iter_tabs:
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
        self.add_tab(None, '')

    def save(self):
        """Save the Python script."""
        ed = self.tabs.currentWidget()

        if ed is None:
            return

        if ed.path is None:
            path, _ = QFileDialog.getSaveFileName(self, 'Save file',
                                                  MICROPYTHON_DIRECTORY)
            ed.path = path

        with open(ed.path, 'w') as f:
            f.write(ed.text())

        ed.setModified(False)

    def load(self):
        """Load a Python script."""
        path, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                              MICROPYTHON_DIRECTORY, '*.py')
        try:
            with open(path) as f:
                text = f.read()
        except FileNotFoundError:
            pass
        else:
            self.add_tab(path, text)

    def snippets(self):
        """Use code snippets."""
        pass

    def flash(self):
        """Flash the micro:bit."""
        pass

    def repl(self):
        """Toggle the REPL pane."""
        pass

    def quit(self):
        """Exit the application."""
        # TODO: check for unsaved work and prompt to save if required. Fix once
        # we can actually save the work!
        sys.exit(0)
