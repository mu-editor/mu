# -*- coding: utf-8 -*-
"""
Tests for the file-reading logic
"""
import os
import codecs
import locale
import re
from unittest import mock

import pytest

import mu.logic
from PyQt5.QtWidgets import QMessageBox

from . import support

#
# Tests for newline detection
# Mu should detect the majority newline convention
# in a loaded file and use that convention when writing
# the file out again. Internally all newlines are MU_NEWLINE
#

def test_read_newline_no_text():
    """If the file being loaded is empty, use the platform default newline
    """
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            text, newline = mu.logic.read_and_decode(filepath)
            assert text.count("\r\n") == 0
            assert newline == os.linesep

def test_read_newline_all_unix():
    """If the file being loaded has only the Unix convention, use that
    """
    with support.generate_python_files(["abc\ndef"]) as filepaths:
        for filepath in filepaths:
            text, newline = mu.logic.read_and_decode(filepath)
            assert text.count("\r\n") == 0
            assert newline == "\n"

def test_read_newline_all_windows():
    """If the file being loaded has only the Windows convention, use that
    """
    with support.generate_python_files(["abc\r\ndef"]) as filepaths:
        for filepath in filepaths:
            text, newline = mu.logic.read_and_decode(filepath)
            assert text.count("\r\n") == 0
            assert newline == "\r\n"

def test_read_newline_most_unix():
    """If the file being loaded has mostly the Unix convention, use that
    """
    with support.generate_python_files(["\nabc\r\ndef\n"]) as filepaths:
        for filepath in filepaths:
            text, newline = mu.logic.read_and_decode(filepath)
            assert text.count("\r\n") == 0
            assert newline == "\n"

def test_read_newline_most_windows():
    """If the file being loaded has mostly the Windows convention, use that
    """
    with support.generate_python_files(["\r\nabc\ndef\r\n"]) as filepaths:
        for filepath in filepaths:
            text, newline = mu.logic.read_and_decode(filepath)
            assert text.count("\r\n") == 0
            assert newline == "\r\n"

def test_read_newline_equal_match():
    """If the file being loaded has an equal number of Windows and
    Unix newlines, use the platform default
    """
    with support.generate_python_files(["\r\nabc\ndef"]) as filepaths:
        for filepath in filepaths:
            text, newline = mu.logic.read_and_decode(filepath)
            assert text.count("\r\n") == 0
            assert newline == os.linesep

#
# When writing Mu should honour the line-ending convention found inbound
#
def test_write_newline_to_unix():
    """If the file had Unix newlines it should be saved with Unix newlines

    (In principle this check is unnecessary as Unix newlines are currently
    the Mu internal default; but we leave it here in case that situation
    changes)
    """
    with support.generate_python_files([""]) as filepaths:
        test_string = "\r\n".join("the cat sat on the mat".split())
        for filepath in filepaths:
            mu.logic.save_and_encode(test_string, filepath, "\n")
        with open(filepath, newline="") as f:
            text = f.read()
            assert text.count("\r\n") == 0
            #
            # There will be one more line-ending because of the encoding cookie prefix
            #
            assert text.count("\n") == 1 + test_string.count("\r\n")

def test_write_newline_to_windows():
    """If the file had Windows newlines it should be saved with Windows newlines
    """
    with support.generate_python_files([""]) as filepaths:
        test_string = "\n".join("the cat sat on the mat".split())
        for filepath in filepaths:
            mu.logic.save_and_encode(test_string, filepath, "\r\n")
        with open(filepath, newline="") as f:
            text = f.read()
            assert len(re.findall("[^\r]\n", text)) == 0
            #
            # There will be one more line-ending because of the encoding cookie prefix
            #
            assert text.count("\r\n") == 1 + test_string.count("\n")


#
# Generate a Unicode test string which includes all the usual
# 7-bit characters but also an 8th-bit range which tends to
# trip things up between encodings
#
UNICODE_TEST_STRING = (bytes(range(0x20, 0x80)) + bytes(range(0xa0, 0xff))).decode("iso-8859-1")

#
# Tests for encoding detection
# Mu should detect:
# - BOM (UTF8/16)
# - Encoding cooke, eg # -*- coding: utf-8 -*-
# - fallback to the platform default (locale.getpreferredencoding())
#
def test_read_utf8bom():
    """Successfully decode from utf-8 encoded with BOM
    """
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            with open(filepath, "w", encoding="utf-8-sig") as f:
                f.write(UNICODE_TEST_STRING)
            text, _ = mu.logic.read_and_decode(filepath)
            assert text == UNICODE_TEST_STRING

def test_read_utf16bebom():
    """Successfully decode from utf-16 BE encoded with BOM
    """
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            with open(filepath, "wb") as f:
                f.write(codecs.BOM_UTF16_BE)
                f.write(UNICODE_TEST_STRING.encode("utf-16-be"))
            text, _ = mu.logic.read_and_decode(filepath)
            assert text == UNICODE_TEST_STRING

def test_read_utf16lebom():
    """Successfully decode from utf-16 LE encoded with BOM
    """
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            with open(filepath, "wb") as f:
                f.write(codecs.BOM_UTF16_LE)
                f.write(UNICODE_TEST_STRING.encode("utf-16-le"))
            text, _ = mu.logic.read_and_decode(filepath)
            assert text == UNICODE_TEST_STRING

def test_read_encoding_cookie():
    """Successfully decode from iso-8859-1 with an encoding cookie
    """
    encoding_cookie = mu.logic.ENCODING_COOKIE.replace(mu.logic.ENCODING, "iso-8859-1")
    test_string = encoding_cookie + UNICODE_TEST_STRING
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            with open(filepath, "wb") as f:
                f.write(test_string.encode("iso-8859-1"))
            text, _ = mu.logic.read_and_decode(filepath)
            assert text == test_string

def test_read_encoding_default():
    """Successfully decode from the default locale
    """
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            with open(filepath, "wb") as f:
                f.write(UNICODE_TEST_STRING.encode(locale.getpreferredencoding()))
            text, _ = mu.logic.read_and_decode(filepath)
            assert text == UNICODE_TEST_STRING

#
# When writing, Mu should use utf-8 (without a BOM) and ensure the text is
# prefixed with a PEP 263 encoding cookie
# If the file already has an encoding cookie it should be replaced by the Mu cookie
#
def test_write_utf8():
    """The text should be saved encoded as utf8
    """
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            mu.logic.save_and_encode(UNICODE_TEST_STRING, filepath)
            with open(filepath, encoding="utf-8") as f:
                text = f.read()
                assert text == mu.logic.ENCODING_COOKIE + UNICODE_TEST_STRING

def test_write_encoding_cookie_no_cookie():
    """If the text has no cookie of its own the first line of the saved
    file will be the Mu encoding cookie
    """
    test_string = "This is a test"
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            mu.logic.save_and_encode(test_string, filepath)
            with open(filepath, encoding="utf-8") as f:
                for line in f:
                    assert line == mu.logic.ENCODING_COOKIE
                    break
                else:
                    assert False, "No cookie found"

def test_write_encoding_cookie_existing_cookie():
    """If the text has a cookie of its own it will be replaced by the Mu cookie
    """
    cookie = mu.logic.ENCODING_COOKIE.replace(mu.logic.ENCODING, "iso-8859-1")
    test_string = cookie + "This is a test"
    with support.generate_python_files([""]) as filepaths:
        for filepath in filepaths:
            mu.logic.save_and_encode(test_string, filepath)
            with open(filepath, encoding="utf-8") as f:
                for line in f:
                    assert line == mu.logic.ENCODING_COOKIE
                    break
                else:
                    assert False, "No cookie found"
