# -*- coding: utf-8 -*-
"""
Tests for the resources sub-module.
"""
import mu.resources
from unittest import mock
from PyQt5.QtGui import QIcon, QPixmap


def test_path():
    """
    Ensure the resource_filename function is called with the expected args and
    the path function under test returns its result.
    """
    with mock.patch("mu.resources.resource_filename", return_value="bar") as r:
        assert mu.resources.path("foo") == "bar"
        r.assert_called_once_with(mu.resources.__name__, "images/foo")


def test_load_icon():
    """
    Check the load_icon function returns the expected QIcon object.
    """
    result = mu.resources.load_icon("icon")
    assert isinstance(result, QIcon)


def test_load_pixmap():
    """
    Check the load_pixmap function returns the expected QPixmap object.
    """
    result = mu.resources.load_pixmap("icon")
    assert isinstance(result, QPixmap)


def test_stylesheet():
    """
    Ensure the resource_string function is called with the expected args and
    the load_stylesheet function returns its result.
    """
    with mock.patch("mu.resources.resource_string", return_value=b"foo") as rs:
        assert "foo" == mu.resources.load_stylesheet("foo")
        rs.assert_called_once_with(mu.resources.__name__, "css/foo")


def test_load_font_data():
    """
    Ensure font data can be loaded
    """
    with mock.patch("mu.resources.resource_string", return_value=b"foo") as rs:
        assert b"foo" == mu.resources.load_font_data("foo")
        rs.assert_called_once_with(mu.resources.__name__, "fonts/foo")
