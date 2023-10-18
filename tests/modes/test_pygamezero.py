# -*- coding: utf-8 -*-
"""
Tests for the PyGameZero mode.
"""
import os.path
from mu.modes.pygamezero import PyGameZeroMode
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, PI_APIS, PYGAMEZERO_APIS
from mu.virtual_environment import venv
from unittest import mock
import tempfile


def test_pgzero_mode():
    """
    Sanity check for setting up of the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    assert pm.name == "Pygame Zero"
    assert pm.description is not None
    assert pm.icon == "pygamezero"
    assert pm.is_debugger is False
    assert pm.editor == editor
    assert pm.view == view
    assert pm.builtins

    actions = pm.actions()
    assert len(actions) == 5
    assert actions[0]["name"] == "play"
    assert actions[0]["handler"] == pm.play_toggle
    assert actions[1]["name"] == "images"
    assert actions[1]["handler"] == pm.show_images
    assert actions[2]["name"] == "fonts"
    assert actions[2]["handler"] == pm.show_fonts
    assert actions[3]["name"] == "sounds"
    assert actions[3]["handler"] == pm.show_sounds
    assert actions[4]["name"] == "music"
    assert actions[4]["handler"] == pm.show_music


def test_pgzero_api():
    """
    Make sure the API definition is as expected.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    result = pm.api()
    assert result == SHARED_APIS + PYTHON3_APIS + PI_APIS + PYGAMEZERO_APIS


def test_pgzero_play_toggle_on():
    """
    Check the handler for clicking play starts the new process and updates the
    UI state.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    pm.runner = None

    def runner(pm=pm):
        pm.runner = True

    pm.run_game = mock.MagicMock(side_effect=runner)
    pm.set_buttons = mock.MagicMock()
    pm.play_toggle(None)
    pm.run_game.assert_called_once_with()
    slot = pm.view.button_bar.slots["play"]
    assert slot.setIcon.call_count == 1
    slot.setText.assert_called_once_with("Stop")
    slot.setToolTip.assert_called_once_with("Stop your Pygame Zero game.")
    pm.set_buttons.assert_called_once_with(modes=False)


def test_pgzero_play_toggle_on_cancelled():
    """
    Ensure the button states are correct if playing an unsaved script is
    cancelled before the process is allowed to start.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    pm.runner = None
    pm.run_game = mock.MagicMock()
    pm.play_toggle(None)
    pm.run_game.assert_called_once_with()
    slot = pm.view.button_bar.slots["play"]
    assert slot.setIcon.call_count == 0


def test_pgzero_play_toggle_off():
    """
    Check the handler for clicking play stops the process and reverts the UI
    state.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    pm.runner = True
    pm.stop_game = mock.MagicMock()
    pm.set_buttons = mock.MagicMock()
    pm.play_toggle(None)
    pm.stop_game.assert_called_once_with()
    slot = pm.view.button_bar.slots["play"]
    assert slot.setIcon.call_count == 1
    slot.setText.assert_called_once_with("Play")
    slot.setToolTip.assert_called_once_with("Play your Pygame Zero game.")
    pm.set_buttons.assert_called_once_with(modes=True)


def test_pgzero_run_game():
    """
    Ensure that running the game launches the process as expected.
    """
    editor = mock.MagicMock()
    editor.envars = [["name", "value"]]
    view = mock.MagicMock()
    view.current_tab.path = "/foo/bar"
    view.current_tab.isModified.return_value = True
    mock_runner = mock.MagicMock()
    view.add_python3_runner.return_value = mock_runner
    pm = PyGameZeroMode(editor, view)
    py_args = ["-m", "pgzero"]
    with mock.patch.object(venv, "interpreter", "interpreter"):
        pm.run_game()

    editor.save_tab_to_file.assert_called_once_with(view.current_tab)
    view.add_python3_runner.assert_called_once_with(
        interpreter="interpreter",
        script_name="/foo/bar",
        working_directory="/foo",
        interactive=False,
        envars=editor.envars,
        python_args=py_args,
    )
    mock_runner.process.waitForStarted.assert_called_once_with()


def test_pgzero_run_game_no_editor():
    """
    If there's no active tab, there can be no runner either.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PyGameZeroMode(editor, view)
    pm.stop_game = mock.MagicMock()
    pm.run_game()
    assert pm.runner is None
    pm.stop_game.assert_called_once_with()


def test_pgzero_run_game_needs_saving():
    """
    If the file hasn't been saved yet (it's unnamed), prompt the user to save
    it.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = None
    pm = PyGameZeroMode(editor, view)
    pm.stop_game = mock.MagicMock()
    pm.run_game()
    editor.save.assert_called_once_with()


def test_pgzero_stop_game():
    """
    Check that the child process is killed, the runner cleaned up and UI
    is reset.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    mock_runner = mock.MagicMock()
    pm.runner = mock_runner
    pm.stop_game()
    mock_runner.stop_process.assert_called_once_with()
    assert pm.runner is None
    view.remove_python_runner.assert_called_once_with()


def test_pgzero_stop_game_no_runner():
    """
    If the game is cancelled before the child process is created ensure
    nothing breaks and the UI is reset.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    pm = PyGameZeroMode(editor, view)
    pm.runner = None
    pm.stop_game()
    view.remove_python_runner.assert_called_once_with()


def test_pgzero_show_images():
    """
    The view is called to run the OS's file explorer for the given images path.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = os.path.join(tempfile.gettempdir(), "abc.py")
    pm = PyGameZeroMode(editor, view)
    pm.show_images(None)
    image_dir = os.path.join(os.path.dirname(view.current_tab.path), "images")
    view.open_directory_from_os.assert_called_once_with(image_dir)


def test_pgzero_show_images_no_file():
    """
    Run the OS file explorer for the workspace if no file is current.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PyGameZeroMode(editor, view)
    pm.show_images(None)
    image_dir = os.path.join(pm.workspace_dir(), "images")
    view.open_directory_from_os.assert_called_once_with(image_dir)


def test_pgzero_show_fonts():
    """
    The view is called to run the OS's file explorer for the given fonts path.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = os.path.join(tempfile.gettempdir(), "abc.py")
    pm = PyGameZeroMode(editor, view)
    pm.show_fonts(None)
    fonts_dir = os.path.join(os.path.dirname(view.current_tab.path), "fonts")
    view.open_directory_from_os.assert_called_once_with(fonts_dir)


def test_pgzero_show_fonts_no_file():
    """
    Run the OS file explorer for the workspace if no file is current.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PyGameZeroMode(editor, view)
    pm.show_fonts(None)
    font_dir = os.path.join(pm.workspace_dir(), "fonts")
    view.open_directory_from_os.assert_called_once_with(font_dir)


def test_pgzero_show_sounds():
    """
    The view is called to run the OS's file explorer for the given sounds path.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = os.path.join(tempfile.gettempdir(), "abc.py")
    pm = PyGameZeroMode(editor, view)
    pm.show_sounds(None)
    sounds_dir = os.path.join(os.path.dirname(view.current_tab.path), "sounds")
    view.open_directory_from_os.assert_called_once_with(sounds_dir)


def test_pgzero_show_sounds_no_file():
    """
    Run the OS file explorer for the workspace if no file is current.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PyGameZeroMode(editor, view)
    pm.show_sounds(None)
    sound_dir = os.path.join(pm.workspace_dir(), "sounds")
    view.open_directory_from_os.assert_called_once_with(sound_dir)


def test_pgzero_show_music():
    """
    The view is called to run the OS's file explorer for the given music path.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = os.path.join(tempfile.gettempdir(), "abc.py")
    pm = PyGameZeroMode(editor, view)
    pm.show_music(None)
    music_dir = os.path.join(os.path.dirname(view.current_tab.path), "music")
    view.open_directory_from_os.assert_called_once_with(music_dir)


def test_pgzero_show_music_no_file():
    """
    Run the OS file explorer for the workspace if no file is current.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    pm = PyGameZeroMode(editor, view)
    pm.show_music(None)
    music_dir = os.path.join(pm.workspace_dir(), "music")
    view.open_directory_from_os.assert_called_once_with(music_dir)
