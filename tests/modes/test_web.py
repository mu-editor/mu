# -*- coding: utf-8 -*-
"""
Tests for the flask based web mode.
"""
import os
import signal
from mu.modes.web import WebMode, CODE_TEMPLATE
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, FLASK_APIS
from unittest import mock


def test_init():
    """
    Ensure the web mode has the expected default settings. Tested so these
    cannot be accidentally changed..!
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    assert wm.name == "Web"
    assert wm.icon == "web"
    assert wm.runner is None
    assert wm.save_timeout == 0
    assert wm.file_extensions == ["css", "html"]
    assert wm.code_template == CODE_TEMPLATE
    actions = wm.actions()
    assert len(actions) == 5
    assert actions[0]["name"] == "run"
    assert actions[0]["handler"] == wm.run_toggle
    assert actions[1]["name"] == "browse"
    assert actions[1]["handler"] == wm.browse
    assert actions[2]["name"] == "templates"
    assert actions[2]["handler"] == wm.load_templates
    assert actions[3]["name"] == "css"
    assert actions[3]["handler"] == wm.load_css
    assert actions[4]["name"] == "static"
    assert actions[4]["handler"] == wm.show_images


def test_web_api():
    """
    Ensure the API documentation is correct.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    result = wm.api()
    assert result == SHARED_APIS + PYTHON3_APIS + FLASK_APIS


def test_run_toggle_on():
    """
    Check the handler for running the local server starts the sub-process and
    updates the UI state.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    wm.runner = None

    def runner(wm=wm):
        wm.runner = True

    wm.start_server = mock.MagicMock(side_effect=runner)
    wm.set_buttons = mock.MagicMock()
    wm.run_toggle(None)
    wm.start_server.assert_called_once_with()
    slot = wm.view.button_bar.slots["run"]
    assert slot.setIcon.call_count == 1
    slot.setText.assert_called_once_with("Stop")
    slot.setToolTip.assert_called_once_with("Stop the web server.")
    wm.set_buttons.assert_called_once_with(modes=False)


def test_run_toggle_off():
    """
    Check the handler for toggling the local server stops the process and
    reverts the UI state.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    wm.runner = True
    wm.stop_server = mock.MagicMock()
    wm.set_buttons = mock.MagicMock()
    wm.run_toggle(None)
    wm.stop_server.assert_called_once_with()
    slot = wm.view.button_bar.slots["play"]
    assert slot.setIcon.call_count == 1
    slot.setText.assert_called_once_with("Run")
    slot.setToolTip.assert_called_once_with("Run the web server.")
    wm.set_buttons.assert_called_once_with(modes=True)


def test_start_server_no_tab():
    """
    If there's no tab, the resver isn't started.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    wm = WebMode(editor, view)
    wm.stop_server = mock.MagicMock()
    wm.start_server()
    wm.stop_server.assert_called_once_with()
    assert view.add_python3_runner.call_count == 0


def test_start_server_unsaved_tab():
    """
    If there's a tab, but no associated path, then call the save method on
    the editor to get one. If none is returned no further action is taken.
    """
    editor = mock.MagicMock()
    editor.save.return_value = None
    view = mock.MagicMock()
    view.current_tab.path = None
    wm = WebMode(editor, view)
    wm.start_server()
    assert editor.save.call_count == 1
    assert view.add_python3_runner.call_count == 0


def test_start_server_not_python_file():
    """
    If the user attempts to start the server from not-a-Python-file, then
    complain and abort.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = "foo.html"
    wm = WebMode(editor, view)
    wm.stop_server = mock.MagicMock()
    wm.start_server()
    assert view.show_message.call_count == 1
    wm.stop_server.assert_called_once_with()
    assert view.add_python3_runner.call_count == 0


def test_start_server_no_templates():
    """
    If the user attempts to start the server from a location without a
    templates directory, then complain and abort.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = "foo.py"
    wm = WebMode(editor, view)
    wm.stop_server = mock.MagicMock()
    with mock.patch("os.path.isdir", return_value=False):
        wm.start_server()
    assert view.show_message.call_count == 1
    wm.stop_server.assert_called_once_with()
    assert view.add_python3_runner.call_count == 0


def test_start_server():
    """
    The server is started and stored as the runner associated with the mode.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab.path = "foo.py"
    view.current_tab.isModified.return_value = True
    wm = WebMode(editor, view)
    wm.stop_server = mock.MagicMock()
    with mock.patch("os.path.isdir", return_value=True):
        wm.start_server()
    assert view.add_python3_runner.call_count == 1
    view.add_python3_runner().process.waitForStarted.assert_called_once_with()


def test_stop_server():
    """
    Stopping the server will send SIGINT to the child process and remove the
    Python runner pane from the UI.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    mock_runner = mock.MagicMock()
    mock_runner.process.processId.return_value = 666  # ;-)
    wm.runner = mock_runner
    with mock.patch("os.kill") as mock_kill:
        wm.stop_server()
        mock_kill.assert_called_once_with(666, signal.SIGINT)
    mock_runner.process.waitForFinished.assert_called_once_with()
    assert wm.runner is None
    view.remove_python_runner.assert_called_once_with()


def test_stop_server_with_error():
    """
    If killing the server's child process encounters a problem (perhaps the
    process is already dead), then log this and tidy up.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    mock_runner = mock.MagicMock()
    mock_runner.process.processId.return_value = 666  # ;-)
    wm.runner = mock_runner
    with mock.patch(
        "os.kill", side_effect=Exception("Bang")
    ) as mock_kill, mock.patch("mu.modes.web.logger.error") as mock_log:
        wm.stop_server()
        mock_kill.assert_called_once_with(666, signal.SIGINT)
        assert mock_log.call_count == 2
    mock_runner.process.waitForFinished.assert_called_once_with()
    assert wm.runner is None
    view.remove_python_runner.assert_called_once_with()


def test_stop():
    """
    Ensure that this method, called when Mu is quitting, stops the local
    web server.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    wm.stop_server = mock.MagicMock()
    wm.stop()
    wm.stop_server.assert_called_once_with()


def test_open_file():
    """
    The open_file method is used to deal with files that are not Python
    source files. In this case, ensure it just returns the content of the
    referenced file.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    with mock.patch(
        "mu.modes.web.read_and_decode", return_value=("foo", "\n")
    ) as m:
        text, newline = wm.open_file("file.html")
        m.assert_called_once_with("file.html")
        assert text == "foo"
        assert newline == "\n"


def test_load_templates():
    """
    The OS's file system explorer is opened in the correct location for the
    templates / views used by the web application.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    view.current_tab.path = os.path.join(wm.workspace_dir(), "foo.py")
    wm.load_templates(None)
    expected_path = os.path.join(wm.workspace_dir(), "templates")
    editor.load.assert_called_once_with(default_path=expected_path)


def test_load_templates_no_file():
    """
    The OS's file system explorer is opened in the correct location for the
    templates / views used by the web application.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    wm = WebMode(editor, view)
    wm.load_templates(None)
    expected_path = os.path.join(wm.workspace_dir(), "templates")
    editor.load.assert_called_once_with(default_path=expected_path)


def test_load_css():
    """
    The OS's file system explorer is opened in the correct location for the
    web application's CSS files.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    view.current_tab.path = os.path.join(wm.workspace_dir(), "foo.py")
    wm.load_css(None)
    expected_path = os.path.join(wm.workspace_dir(), "static", "css")
    editor.load.assert_called_once_with(default_path=expected_path)


def test_load_css_no_file():
    """
    The OS's file system explorer is opened in the correct location for the
    web application's CSS files.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    wm = WebMode(editor, view)
    wm.load_css(None)
    expected_path = os.path.join(wm.workspace_dir(), "static", "css")
    editor.load.assert_called_once_with(default_path=expected_path)


def test_show_images():
    """
    The OS's file system explorer is opened in the correct location for the
    web application's CSS files.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    view.current_tab.path = os.path.join(wm.workspace_dir(), "foo.py")
    wm.show_images(None)
    expected_path = os.path.join(wm.workspace_dir(), "static", "img")
    view.open_directory_from_os.assert_called_once_with(expected_path)


def test_show_images_no_file():
    """
    The OS's file system explorer is opened in the correct location for the
    web application's CSS files.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    view.current_tab = None
    wm = WebMode(editor, view)
    wm.show_images(None)
    expected_path = os.path.join(wm.workspace_dir(), "static", "img")
    view.open_directory_from_os.assert_called_once_with(expected_path)


def test_browse():
    """
    The user's default web browser is opened to the correct URL for the root
    endpoint of the site served from localhost.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    wm.runner = True
    with mock.patch("mu.modes.web.webbrowser") as mock_browser:
        wm.browse(None)
        expected = "http://127.0.0.1:5000/"
        mock_browser.open.assert_called_once_with(expected)


def test_browse_not_serving():
    """
    If the user attempts to open their browser at their website, but the local
    web server isn't running, then display a friendly message explaining so.
    """
    editor = mock.MagicMock()
    view = mock.MagicMock()
    wm = WebMode(editor, view)
    wm.runner = None
    with mock.patch("mu.modes.web.webbrowser") as mock_browser:
        wm.browse(None)
        assert mock_browser.open.call_count == 0
        assert view.show_message.call_count == 1
