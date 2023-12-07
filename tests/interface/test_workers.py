# -*- coding: utf-8 -*-
"""
Tests for UI workers to be run in separate threads.
"""
import os
from unittest import mock
from mu.interface import workers


def test_pythonanywhereworker_init():
    """
    Ensure the worker is initialised with the expected generated paths to be
    used when uploading files to PythonAnywhere.
    """
    instance = "www"
    username = "test_user"
    token = "a_test_token"
    files = {
        "app.py": "app.py",
    }
    app_name = "app"
    progress = mock.MagicMock()  # Instance of a modal progress indicator.
    paw = workers.PythonAnywhereWorker(
        instance, username, token, files, app_name, progress
    )
    assert paw.instance == instance
    assert paw.username == username
    assert paw.token == token
    assert paw.files == files
    assert paw.app_name == app_name
    assert paw.progress == progress
    assert (
        paw.url
        == "https://{instance}.pythonanywhere.com/api/v0/user/{username}/".format(
            instance=instance, username=username
        )
    )
    assert paw.files_path == "files/path/home/{username}/{app_name}/".format(
        username=username, app_name=app_name
    )
    assert (
        paw.wsgi_path
        == "/files/path/var/www/{username}_pythonanywhere_com_wsgi.py".format(
            username=username
        )
    )
    assert paw.static_path == "/home/{username}/{app_name}/static/".format(
        username=username, app_name=app_name
    )
    assert paw.wsgi_config == workers.WSGI.format(
        username=username, app_name=app_name
    )


def test_pythonanywhereworker_run_with_failure():
    """
    If an exception is raised in the "run" method, the error signal is emitted.
    """
    instance = "www"
    username = "test_user"
    token = "a_test_token"
    files = {
        "app.py": "app.py",
    }
    app_name = "app"
    progress = mock.MagicMock()  # Instance of a modal progress indicator.
    paw = workers.PythonAnywhereWorker(
        instance, username, token, files, app_name, progress
    )
    paw.error = mock.MagicMock()
    paw.finished = mock.MagicMock()
    ex = Exception("Boom!")
    with mock.patch("mu.interface.workers.requests.get", side_effect=ex):
        paw.run()
    paw.error.emit.assert_called_once_with(repr(ex))
    assert paw.finished.emit.call_count == 0


def test_pythonanywhereworker_run_to_deploy_to_main_instance():
    """
    Ensure the expected calls are made via, the requests module, to the
    PythonAnywhere API in order to deploy the application.
    """
    instance = "www"
    username = "test_user"
    token = "a_test_token"
    files = {
        # attempt to upload this test file :-)
        "app.py": os.path.abspath(__file__),
    }
    app_name = "app"
    progress = mock.MagicMock()  # Instance of a modal progress indicator.
    paw = workers.PythonAnywhereWorker(
        instance, username, token, files, app_name, progress
    )
    paw.error = mock.MagicMock()
    paw.finished = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_response.json.return_value = []  # assuming no existing app.
    mock_requests = mock.MagicMock()
    mock_requests.get.return_value = mock_response
    mock_requests.post.return_value = mock_response
    mock_requests.put.return_value = mock_response
    with mock.patch("mu.interface.workers.requests", mock_requests):
        paw.run()
    progress.setMaximum.assert_called_once_with(len(files) + 5)
    assert progress.setValue.call_count == len(files) + 5
    paw.finished.emit.assert_called_once_with("test_user.pythonanywhere.com")
    assert paw.error.emit.call_count == 0
    # Expected number of calls to API take place.
    assert mock_requests.get.call_count == 1
    assert mock_requests.put.call_count == 1
    assert mock_requests.post.call_count == 5


def test_pythonanywhereworker_run_to_deploy_to_eu_instance():
    """
    Ensure the expected calls are made via, the requests module, to the
    PythonAnywhere API in order to deploy the application to the EU zone.
    """
    instance = "eu"
    username = "test_user"
    token = "a_test_token"
    files = {
        # attempt to upload this test file :-)
        "app.py": os.path.abspath(__file__),
    }
    app_name = "app"
    progress = mock.MagicMock()  # Instance of a modal progress indicator.
    paw = workers.PythonAnywhereWorker(
        instance, username, token, files, app_name, progress
    )
    paw.error = mock.MagicMock()
    paw.finished = mock.MagicMock()
    mock_response = mock.MagicMock()
    mock_response.json.return_value = [
        # An existing domain, so no need to create app via API.
        {
            "domain_name": "test_user.eu.pythonanywhere.com",
        },
    ]
    mock_requests = mock.MagicMock()
    mock_requests.get.return_value = mock_response
    mock_requests.post.return_value = mock_response
    mock_requests.put.return_value = mock_response
    with mock.patch("mu.interface.workers.requests", mock_requests):
        paw.run()
    progress.setMaximum.assert_called_once_with(len(files) + 5)
    assert progress.setValue.call_count == len(files) + 5
    paw.finished.emit.assert_called_once_with(
        "test_user.eu.pythonanywhere.com"
    )
    assert paw.error.emit.call_count == 0
    # Expected number of calls to API take place.
    assert mock_requests.get.call_count == 1
    assert mock_requests.put.call_count == 1
    assert mock_requests.post.call_count == 3  # No need to create fresh app.
