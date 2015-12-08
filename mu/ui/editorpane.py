import sys
import keyword
import os.path
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont


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
