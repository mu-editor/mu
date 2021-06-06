# -*- coding: utf-8 -*-
"""
Tests for the QProcess-based Process class
"""
import sys
from unittest import mock
import uuid

import pytest

from PyQt5.QtCore import QTimer, QProcess

from mu import virtual_environment


def test_creation_environment():
    """Ensure that a process is always unbuffered & io-encoding of UTF-8"""
    p = virtual_environment.Process()
    #
    # Ensure we're always running unbuffered and with
    # an IO encoding of utf-8
    #
    assert p.environment.value("PYTHONUNBUFFERED") == "1"
    assert p.environment.value("PYTHONIOENCODING").lower() == "utf-8"


def test_set_up_run():
    """Ensure that the process is set up to run with additional env vars"""
    envvar = uuid.uuid1().hex
    p = virtual_environment.Process()
    p._set_up_run(envvar=envvar)
    environment = p.process.processEnvironment()
    assert environment.value("envvar") == envvar


def test_run_blocking():
    """Ensure that a process is run synchronously and returns its output"""
    p = virtual_environment.Process()
    expected_output = sys.executable
    output = p.run_blocking(
        sys.executable, ["-c", "import sys; print(sys.executable)"]
    ).strip()
    assert output == expected_output


def test_run_blocking_timeout():
    """Ensure that a process is run synchronously and times out"""
    p = virtual_environment.Process()
    #
    # If the process times out, it will raise a VirtualEnvironmentError
    # whose message arg will contain any stdout
    #
    expected_stdout = uuid.uuid1().hex
    expected_stderr = uuid.uuid1().hex
    try:
        p.run_blocking(
            sys.executable,
            [
                "-c",
                "import sys; sys.stdout.write('"
                + expected_stdout
                + "'); sys.stderr.write('"
                + expected_stderr
                + "'); time.sleep(2.0)",
            ],
            wait_for_s=1.0,
        ).strip()
    except virtual_environment.VirtualEnvironmentError as exc:
        assert expected_stdout in exc.message
        assert expected_stderr in exc.message


def test_run_blocking_error():
    """Ensure that a process raises a known exception on error"""
    p = virtual_environment.Process()
    #
    # If the process errors out, it will raise a VirtualEnvironmentError
    # whose message arg will contain any stdout and stderr
    #
    expected_stdout = uuid.uuid1().hex
    expected_stderr = uuid.uuid1().hex
    try:
        p.run_blocking(
            sys.executable,
            [
                "-c",
                "import sys; sys.stdout.write('"
                + expected_stdout
                + "'); sys.stderr.write('"
                + expected_stderr
                + "'); 1/0",
            ],
        ).strip()
    except virtual_environment.VirtualEnvironmentError as exc:
        assert expected_stdout in exc.message
        assert expected_stderr in exc.message


def _QTimer_singleshot(delay, partial):
    return partial.func(*partial.args, **partial.keywords)


def test_run():
    """Ensure that a QProcess is started with the relevant params"""
    command = sys.executable
    args = ["-c", "import sys; print(sys.executable)"]
    with mock.patch.object(
        QTimer, "singleShot", _QTimer_singleshot
    ), mock.patch.object(QProcess, "start") as mocked_start:
        p = virtual_environment.Process()
        p.run(command, args)

    mocked_start.assert_called_with(command, args)


def test_wait_shows_failure():
    """If QProcess fails, wait for raise an exception"""
    #
    # We have to do a *lot* of mocking to get this test to work:
    # - The process needs to be able to "run"
    # - The wait needs to complete
    # - And the result of the wait needs to indicate a failure
    #
    with mock.patch.object(
        QProcess, "waitForFinished", return_value=False
    ), mock.patch.object(
        QProcess, "exitStatus", return_value=QProcess.CrashExit
    ), mock.patch.object(
        QProcess, "start"
    ):
        p = virtual_environment.Process()
        p.run(None, None)
        with pytest.raises(virtual_environment.VirtualEnvironmentError):
            p.wait()
