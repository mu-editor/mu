# -*- coding: utf-8 -*-
"""
Tests for the virtual_environment module pip support
"""
import os
import random
import logging
from unittest.mock import patch

import pytest

import mu.virtual_environment

HERE = os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def cleanup_logger():
    """
    This function will always be called for each test in this module.

    It first yields to the test function and then ensures the logger no longer
    references and SplashLogHandler instances.

    Why do this..?

    The SplashLogHandler was not garbage collected but the PyQt signal used
    by this handler was destroyed by Qt. This appeared to result in a core dump
    at random times, depending on the order in which the tests were run.

    This fix ensures no such log handler exists after these tests are run.
    """
    logger = logging.getLogger(mu.virtual_environment.__name__)
    # Clean up the logger from an unknown "dirty" state.
    while logger.hasHandlers() and logger.handlers:
        handler = logger.handlers[0]
        if isinstance(handler, mu.virtual_environment.SplashLogHandler):
            logger.removeHandler(handler)

    yield  # Run the test function.

    # Now clean up the logging.
    while logger.hasHandlers() and logger.handlers:
        handler = logger.handlers[0]
        if isinstance(handler, mu.virtual_environment.SplashLogHandler):
            logger.removeHandler(handler)


def rstring(length=10, characters="abcdefghijklmnopqrstuvwxyz"):
    letters = list(characters)
    random.shuffle(letters)
    return "".join(letters[:length])


def rrange(limit=10):
    return range(random.randint(1, limit))


def test_pip_creation():
    """Ensure we can create a pip object which retains the pip executable"""
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    assert pip.executable == pip_executable


def test_pip_run():
    """Ensure we are calling out to pip with whatever parameters"""
    command = rstring()
    params = [rstring() for _ in rrange(3)]
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.run(command, *params)
        expected_args = (
            pip_executable,
            [command, "--disable-pip-version-check"] + list(params),
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_run_with_kwargs():
    """Ensure we are calling out to pip with whatever keyword parameters"""
    command = rstring()
    params = dict(a=1, b=False, c=True, d_e=2)
    #
    # All keyword params become "--xxx" switches to the command
    # Keywords with values are followed by their value
    # Keywords with the value False become "--no-<keyword>"
    # Keywords with the value none become standalone switches
    # Underscores are replaced by dashes
    #
    expected_parameters = ["--a", "1", "--no-b", "--c", "--d-e", "2"]
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.run(command, **params)
        args, _ = mock_run.call_args
        #
        # NB presumably because of non-ordered dicts, Python 3.5 can produce
        # arguments in a different order.
        #
        output_command, output_args = args
        expected_command = pip_executable
        expected_args = [
            command,
            "--disable-pip-version-check",
        ] + expected_parameters
        assert output_command == expected_command
        assert set(output_args) == set(expected_args)


def pip_install_testing(
    label,
    command,
    package_or_packages,
    input_switches={},
    expected_switches=[],
):
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    expected_command = pip_executable
    expected_args = [command, "--disable-pip-version-check"]
    if isinstance(package_or_packages, list):
        expected_args.extend(package_or_packages)
    else:
        expected_args.append(package_or_packages)
    if expected_switches:
        expected_args.extend(expected_switches)
    if command == "uninstall":
        expected_args.append("--yes")

    with patch.object(pip.process, "run_blocking") as mock_run:
        function = getattr(pip, command)
        function(package_or_packages, **input_switches)
        args, _ = mock_run.call_args
        output_command, output_args = args
        #
        # NB presumably because of non-ordered dicts, Python 3.5 can produce
        # arguments in a different order.
        #
        assert output_command == expected_command
        assert set(output_args) == set(expected_args)


#
# pip install
#


def test_pip_install_single_package():
    """Ensure that installing a single package results in:
    "pip install <package>"
    """
    pip_install_testing(
        "test_pip_install_single_package", "install", rstring()
    )


def test_pip_install_several_packages():
    """Ensure that installing several package results in
    "pip install <packageA> <packageB>"
    """
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip_install_testing(
        "test_pip_install_several_packages", "install", package_names
    )


def test_pip_install_single_package_with_flag():
    """Ensure that installing a single package with upgrade=True
    "pip install --upgrade <package>"
    """
    pip_install_testing(
        "test_pip_install_single_package_with_flag",
        "install",
        rstring(),
        {"switch": True},
        ["--switch"],
    )


def test_pip_install_several_packages_with_flag():
    """Ensure that installing a single package with switch=True
    "pip install --upgrade <package>"
    """
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip_install_testing(
        "test_pip_install_several_packages_with_flag",
        "install",
        package_names,
        {"switch": True},
        ["--switch"],
    )


def test_pip_install_single_package_with_flag_value():
    """Ensure that installing a single package with timeout=30
    "pip install --timeout 30 <package>"
    """
    pip_install_testing(
        "test_pip_install_single_package_with_flag",
        "install",
        rstring(),
        {"switch": 30},
        ["--switch", "30"],
    )


#
# pip uninstall
#


def test_pip_uninstall_single_package():
    """Ensure that uninstalling a single package results in:
    "pip uninstall <package>"
    """
    pip_install_testing(
        "test_pip_uninstall_single_package", "uninstall", rstring()
    )


def test_pip_uninstall_several_packages():
    """Ensure that uninstalling several package results in
    "pip uninstall <packageA> <packageB>"
    """
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip_install_testing(
        "test_pip_uninstall_several_packages", "uninstall", package_names
    )


def test_pip_uninstall_single_package_with_flag():
    """Ensure that uninstalling a single package with upgrade=True
    "pip uninstall --upgrade <package>"
    """
    pip_install_testing(
        "test_pip_uninstall_single_package_with_flag",
        "uninstall",
        rstring(),
        {"switch": True},
        ["--switch"],
    )


def test_pip_uninstall_several_packages_with_flag():
    """Ensure that uninstalling a single package with switch=True
    "pip uninstall --upgrade <package>"
    """
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip_install_testing(
        "test_pip_uninstall_several_packages_with_flag",
        "uninstall",
        package_names,
        {"switch": True},
        ["--switch"],
    )


def test_pip_uninstall_single_package_with_flag_value():
    """Ensure that uninstalling a single package with timeout=30
    "pip uninstall --timeout 30 <package>"
    """
    pip_install_testing(
        "test_pip_uninstall_single_package_with_flag",
        "uninstall",
        rstring(),
        {"switch": 30},
        ["--switch", "30"],
    )


#
# freeze & list
#
def test_pip_freeze():
    """Ensure that pip.freeze calls pip freeze"""
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.freeze()
        expected_args = (
            pip_executable,
            ["freeze", "--disable-pip-version-check"],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_list():
    """Ensure that pip.list calls pip list"""
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.list()
        expected_args = (
            pip_executable,
            ["list", "--disable-pip-version-check"],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


#
# installed packages
#
def test_installed_packages():
    """Ensure that we see a list of tuples of (name, version) of packages"""
    #
    # The test shouldn't have to "know" whether the code under test is
    # using freeze or list or something else. The best we can do is to mock
    # both freeze and list with the same set of test packages and test
    # the result
    #
    Pip = mu.virtual_environment.Pip
    packages = [
        (rstring(10), rstring(6, "0123456789."), rstring(30))
        for _ in rrange(5)
    ]
    pip_list_output = os.linesep.join(
        ["*", "*"] + ["%s %s %s" % p for p in packages]
    )
    pip_freeze_output = os.linesep.join("%s==%s" % (p[:2]) for p in packages)
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking"):
        with patch.object(Pip, "freeze", return_value=pip_freeze_output):
            with patch.object(Pip, "list", return_value=pip_list_output):
                installed_packages = set(pip.installed())
                expected_packages = set(
                    (name, version) for (name, version, location) in packages
                )
                assert installed_packages == expected_packages


def test_installed_packages_no_location():
    """Ensure that we see a list of tuples of (name, version) of packages
    when one of them has no "location" entry in `pip list`
    """
    #
    # The test shouldn't have to "know" whether the code under test is
    # using freeze or list or something else. The best we can do is to mock
    # both freeze and list with the same set of test packages and test
    # the result
    #
    Pip = mu.virtual_environment.Pip
    packages = [
        (rstring(10), rstring(6, "0123456789."), rstring(30))
        for _ in rrange(5)
    ]
    pip_list_output = os.linesep.join(
        ["*", "*"] + ["%s %s" % p[:2] for p in packages]
    )
    pip_freeze_output = os.linesep.join("%s==%s" % (p[:2]) for p in packages)
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking"):
        with patch.object(Pip, "freeze") as mock_freeze:
            mock_freeze.return_value = pip_freeze_output
            with patch.object(Pip, "list") as mock_list:
                mock_list.return_value = pip_list_output

                installed_packages = set(pip.installed())
                expected_packages = set(
                    (name, version) for (name, version, location) in packages
                )
                assert installed_packages == expected_packages


def test_pip_list_returns_empty():
    """When pip list command returns empty make sure we raise
    an exception in installed_packages
    """
    pip_executable = "pip-" + rstring() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip, "list", return_value=""):
        with pytest.raises(
            mu.virtual_environment.VirtualEnvironmentError,
            match="Unable to parse",
        ):
            list(pip.installed())
