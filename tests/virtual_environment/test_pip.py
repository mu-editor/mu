# -*- coding: utf-8 -*-
"""
Tests for the virtual_environment module pip support
"""
import os
import random
from unittest.mock import patch

import pytest

import mu.virtual_environment

VE = mu.virtual_environment.VirtualEnvironment

HERE = os.path.dirname(__file__)


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
        expected_args = (
            pip_executable,
            [command, "--disable-pip-version-check"] + expected_parameters,
        )
        args, _ = mock_run.call_args
        assert args == expected_args


#
# pip install
#


def test_pip_install_single_package():
    """Ensure that installing a single package results in:
    "pip install <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_name = rstring()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.install(package_name)
        expected_args = (
            pip_executable,
            ["install", "--disable-pip-version-check", package_name],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_install_several_packages():
    """Ensure that installing several package results in
    "pip install <packageA> <packageB>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.install(package_names)
        expected_args = (
            pip_executable,
            ["install", "--disable-pip-version-check"] + package_names,
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_install_single_package_with_flag():
    """Ensure that installing a single package with upgrade=True
    "pip install --upgrade <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_name = rstring()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.install(package_name, switch=True)
        expected_args = (
            pip_executable,
            [
                "install",
                "--disable-pip-version-check",
                "--switch",
                package_name,
            ],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_install_several_packages_with_flag():
    """Ensure that installing a single package with switch=True
    "pip install --upgrade <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.install(package_names, switch=True)
        expected_args = (
            pip_executable,
            ["install", "--disable-pip-version-check", "--switch"]
            + package_names,
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_install_single_package_with_flag_value():
    """Ensure that installing a single package with timeout=30
    "pip install --timeout 30 <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_name = rstring()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.install(package_name, switch=30)
        expected_args = (
            pip_executable,
            [
                "install",
                "--disable-pip-version-check",
                "--switch",
                "30",
                package_name,
            ],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


#
# pip uninstall
#


def test_pip_uninstall_single_package():
    """Ensure that installing a single package results in:
    "pip uninstall <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_name = rstring()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.uninstall(package_name)
        expected_args = (
            pip_executable,
            [
                "uninstall",
                "--disable-pip-version-check",
                "--yes",
                package_name,
            ],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_uninstall_several_packages():
    """Ensure that installing several package results in
    "pip uninstall <packageA> <packageB>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.uninstall(package_names)
        expected_args = (
            pip_executable,
            ["uninstall", "--disable-pip-version-check", "--yes"]
            + package_names,
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_uninstall_single_package_with_flag():
    """Ensure that installing a single package with upgrade=True
    "pip uninstall --upgrade <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_name = rstring()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.uninstall(package_name, switch=True)
        expected_args = (
            pip_executable,
            [
                "uninstall",
                "--disable-pip-version-check",
                "--yes",
                "--switch",
                package_name,
            ],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_uninstall_several_packages_with_flag():
    """Ensure that installing a single package with switch=True
    "pip uninstall --upgrade <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_names = [rstring() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.uninstall(package_names, switch=True)
        expected_args = (
            pip_executable,
            ["uninstall", "--disable-pip-version-check", "--yes", "--switch"]
            + package_names,
        )
        args, _ = mock_run.call_args
        assert args == expected_args


def test_pip_uninstall_single_package_with_flag_value():
    """Ensure that installing a single package with timeout=30
    "pip uninstall --timeout 30 <package>"
    """
    pip_executable = "pip-" + rstring() + ".exe"
    package_name = rstring()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(pip.process, "run_blocking") as mock_run:
        pip.uninstall(package_name, switch=30)
        expected_args = (
            pip_executable,
            [
                "uninstall",
                "--disable-pip-version-check",
                "--yes",
                "--switch",
                "30",
                package_name,
            ],
        )
        args, _ = mock_run.call_args
        assert args == expected_args


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
