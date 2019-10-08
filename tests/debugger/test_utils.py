# -*- coding: utf-8 -*-
"""
Tests for the debug utils.
"""
from mu.debugger.utils import is_breakpoint_line


def test_is_breakpoint_line_valid_code():
    """
    A simple check to ensure a valid line of Python returns True.
    """
    code = 'print("Hello")'
    assert is_breakpoint_line(code)


def test_is_breakpoint_line_valid_code_with_whitespace():
    """
    If the line of code is indented with whitespace, ensure it returns True.
    """
    code = '    print("Hello")'
    assert is_breakpoint_line(code)


def test_is_breakpoint_line_valid_blank_line():
    """
    If the line is blank, you can't set a breakpoint.
    """
    assert is_breakpoint_line("        ") is False


def test_is_breakpoint_line_comment():
    """
    You can't set a breakpoint on a line that is a comment.
    """
    assert is_breakpoint_line("# A comment") is False
    assert is_breakpoint_line('""" A comment """') is False
    assert is_breakpoint_line("''' A comment'''") is False


def test_is_breakpoint_line_opening_collection():
    """
    It's common to write things like:

    foo = [
        'a',
        'b',
        'c',
    ]

    Breakpoints cannot be set on the first line of this statement (for all
    collection types).
    """
    assert is_breakpoint_line("foo = [") is False
    assert is_breakpoint_line("foo = {") is False
    assert is_breakpoint_line("foo = (") is False


def test_is_breakpoint_line_closing_collection():
    """
    It's common to write things like:

    foo = [
        'a',
        'b',
        'c',
    ]

    Breakpoints cannot be set on the final line of this statement (for all
    collection types).
    """
    assert is_breakpoint_line("]") is False
    assert is_breakpoint_line("}") is False
    assert is_breakpoint_line(")") is False
