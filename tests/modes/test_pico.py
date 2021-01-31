"""
Tests for the minimalist Pico mode.
"""
import pytest
from unittest import mock
from mu.modes.pico import PicoMode
from mu.modes.api import SHARED_APIS


@pytest.fixture
def pico_mode():
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pico_mode = PicoMode(editor, view)
    return pico_mode


def test_api(pico_mode):
    """
    Ensure the right thing comes back from the API.
    """
    api = pico_mode.api()
    assert api == SHARED_APIS
