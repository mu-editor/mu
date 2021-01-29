"""
Tests for the minimalist Lego Spike mode.
"""
import pytest
from unittest import mock
from mu.modes.lego import LegoMode
from mu.modes.api import LEGO_APIS, SHARED_APIS


@pytest.fixture
def lego_mode():
    editor = mock.MagicMock()
    view = mock.MagicMock()
    lego_mode = LegoMode(editor, view)
    return lego_mode


def test_api(lego_mode):
    """
    Ensure the right thing comes back from the API.
    """
    api = lego_mode.api()
    assert api == SHARED_APIS + LEGO_APIS
