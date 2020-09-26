# -*- coding: utf-8 -*-
"""
Tests for the user interface elements of Mu.
"""
from unittest import mock
import mu.interface.themes
import mu.interface.editor


def test_patch_osx_mojave_font_issue_552():
    with mock.patch("platform.platform", return_value="Windows"):
        assert not mu.interface.themes.should_patch_osx_mojave_font()
    with mock.patch(
        "platform.platform", return_value="Darwin-18.0.0-x86_64-i386-64bit"
    ):
        assert mu.interface.themes.should_patch_osx_mojave_font()


def test_constants():
    """
    Ensure the expected constant values exist.
    """
    assert mu.interface.themes.NIGHT_STYLE
    assert mu.interface.themes.DAY_STYLE


def test_Font():
    """
    Ensure the Font class works as expected with default and passed in args.
    """
    f = mu.interface.themes.Font()
    # Defaults
    assert f.color == "#181818"
    assert f.paper == "#FEFEF7"
    assert f.bold is False
    assert f.italic is False
    # Passed in arguments
    f = mu.interface.themes.Font(
        color="pink", paper="black", bold=True, italic=True
    )
    assert f.color == "pink"
    assert f.paper == "black"
    assert f.bold
    assert f.italic


def test_theme_apply_to():
    """
    Ensure that the apply_to class method updates the passed in lexer with the
    expected font settings.
    """
    lexer = mu.interface.editor.PythonLexer()
    theme = mu.interface.themes.DayTheme()
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
    with mock.patch("mu.interface.themes.FONT_NAME", "Source Code Pro"):
        mu.interface.themes.Font._DATABASE = None
        try:
            with mock.patch("mu.interface.themes.QFontDatabase") as db:
                mu.interface.themes.Font().load()
                mu.interface.themes.Font(bold=True).load()
                mu.interface.themes.Font(italic=True).load()
                mu.interface.themes.Font(bold=True, italic=True).load()
        finally:
            mu.interface.themes.Font._DATABASE = None
        db.assert_called_once_with()
        db().font.assert_has_calls(
            [
                mock.call("Source Code Pro", "Regular", 14),
                mock.call("Source Code Pro", "Semibold", 14),
                mock.call("Source Code Pro", "Italic", 14),
                mock.call("Source Code Pro", "Semibold Italic", 14),
            ]
        )
