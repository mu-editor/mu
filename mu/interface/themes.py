"""
Theme and presentation related code for the Mu editor.

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
import logging
import platform

from PyQt5.QtGui import QColor, QFontDatabase
from mu.resources import load_stylesheet, load_font_data


logger = logging.getLogger(__name__)


def should_patch_osx_mojave_font():
    """
    OSX mojave and qt5/qtscintilla has a bug where non-system installed fonts
    are always rendered as black, regardless of the theme color.

    This is inconvenient for light themes, but makes dark themes unusable.

    Using a system-installed font doesn't exhibit this behaviour, so
    update FONT_NAME to use the default terminal font in OSX on mojave.

    This patch should be removed once the underlying issue has been resolved

    github issue #552
    """
    return platform.platform().startswith("Darwin-18.")


# The default font size.
DEFAULT_FONT_SIZE = 14
# All editor windows use the same font
if should_patch_osx_mojave_font():  # pragma: no cover
    logger.warn("Overriding built-in editor font due to Issue #552")
    FONT_NAME = "Monaco"
else:  # pragma: no cover
    FONT_NAME = "Source Code Pro"

FONT_FILENAME_PATTERN = "SourceCodePro-{variant}.otf"
FONT_VARIANTS = ("Bold", "BoldIt", "It", "Regular", "Semibold", "SemiboldIt")
# Load the two themes from resources/css/[night|day].css
# NIGHT_STYLE is a dark theme.
NIGHT_STYLE = load_stylesheet('night.css')
# DAY_STYLE is a light conventional theme.
DAY_STYLE = load_stylesheet('day.css')
# CONTRAST_STYLE is a high contrast theme.
CONTRAST_STYLE = load_stylesheet('contrast.css')


logger = logging.getLogger(__name__)


class Font:
    """
    Utility class that makes it easy to set font related values within the
    editor.
    """
    _DATABASE = None

    def __init__(self, color='#181818', paper='#FEFEF7', bold=False,
                 italic=False):
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
    Keyword = Font(color='#005050', bold=True)
    SingleQuotedString = DoubleQuotedString = Font(color='#800000')
    TripleSingleQuotedString = TripleDoubleQuotedString = Font(color='#060')
    Number = Font(color='#00008B')
    Decorator = Font(color='#cc6600')
    Default = Identifier = Font()
    Operator = Font(color='#400040')
    HighlightedIdentifier = Font(color='#0000a0')
    Paper = QColor('#FEFEF7')
    Caret = QColor('#181818')
    Margin = QColor('#EEE')
    IndicatorError = QColor('red')
    IndicatorStyle = QColor('blue')
    DebugStyle = QColor('#ffcc33')
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

    This is the dark theme.
    """

    FunctionMethodName = ClassName = Font(color='#81a2be', paper='#222')
    UnclosedString = Font(paper='#c93827')
    Comment = CommentBlock = Font(color='#969896', paper='#222')
    Keyword = Font(color='#73a46a', bold=True, paper='#222')
    SingleQuotedString = DoubleQuotedString = Font(color='#f0c674',
                                                   paper='#222')
    TripleSingleQuotedString = TripleDoubleQuotedString = Font(color='#f0c674',
                                                               paper='#222')
    Number = Font(color='#b5bd68', paper='#222')
    Decorator = Font(color='#cc6666', paper='#222')
    Default = Identifier = Font(color='#DDD', paper='#222')
    Operator = Font(color='#b294bb', paper='#222')
    HighlightedIdentifier = Font(color='#de935f', paper='#222')
    Paper = QColor('#222')
    Caret = QColor('#c6c6c6')
    Margin = QColor('#424446')
    IndicatorError = QColor('#c93827')
    IndicatorStyle = QColor('#2f5692')
    DebugStyle = QColor('#444')
    IndicatorWordMatch = QColor('#f14721')
    BraceBackground = QColor('#ed1596')
    BraceForeground = QColor('#222')
    UnmatchedBraceBackground = QColor('#c93827')
    UnmatchedBraceForeground = QColor('#222')
    BreakpointMarker = QColor('#c93827')


class ContrastTheme(Theme):
    """
    Defines a Python related theme including the various font colours for
    syntax highlighting.

    This is the high contrast theme.
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
    DebugStyle = QColor('#666')
    IndicatorWordMatch = QColor('grey')
    BraceBackground = QColor('white')
    BraceForeground = QColor('black')
    UnmatchedBraceBackground = QColor('#666')
    UnmatchedBraceForeground = QColor('black')
    BreakpointMarker = QColor('lightGrey')
