# -*- coding: utf-8 -*-
"""
Tests for the virtual_environment module pip support
"""
import sys
import os
import contextlib
import glob
import pathlib
import random
import shutil
import subprocess
import tempfile
from unittest.mock import Mock, MagicMock, patch
import uuid

import pytest
import mu.virtual_environment
VE = mu.virtual_environment.VirtualEnvironment

HERE = os.path.dirname(__file__)

def random_string():
    return uuid.uuid1().hex

def test_pip_creation():
    """Ensure we can create a pip object which retains the pip executable
    """
    pip_executable = "pip-" + random_string() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    assert pip.pip_executable == pip_executable

def test_pip_run():
    """Ensure we are calling out to pip with whatever parameters
    """
    params = [random_string() for _ in range(random.randint(1, 5))]
    pip_executable = "pip-" + random_string() + ".exe"
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.run(*params)
        expected_args = tuple([pip_executable] + params)
        assert mock_run.call_args.args == expected_args

#
# pip install
#

def test_pip_install_single_package():
    """Ensure that installing a single package results in:
    "pip install <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_name = random_string()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.install(package_name)
        expected_args = (pip_executable, "install", package_name)
        assert mock_run.call_args.args == expected_args

def test_pip_install_several_packages():
    """Ensure that installing several package results in
    "pip install <packageA> <packageB>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_names = [random_string() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.install(package_names)
        expected_args = (pip_executable, "install") + tuple(package_names)
        assert mock_run.call_args.args == expected_args

def test_pip_install_single_package_with_flag():
    """Ensure that installing a single package with upgrade=True
    "pip install --upgrade <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_name = random_string()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.install(package_name, switch=None)
        expected_args = (pip_executable, "install", "--switch", package_name)
        assert mock_run.call_args.args == expected_args

def test_pip_install_several_packages_with_flag():
    """Ensure that installing a single package with switch=None
    "pip install --upgrade <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_names = [random_string() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.install(package_names, switch=None)
        expected_args = (pip_executable, "install", "--switch") + tuple(package_names)
        assert mock_run.call_args.args == expected_args

def test_pip_install_single_package_with_flag_value():
    """Ensure that installing a single package with timeout=30
    "pip install --timeout 30 <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_name = random_string()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.install(package_name, switch=30)
        expected_args = (pip_executable, "install", "--switch", "30", package_name)
        assert mock_run.call_args.args == expected_args

#
# pip uninstall
#

def test_pip_uninstall_single_package():
    """Ensure that uninstalling a single package results in:
    "pip uninstall <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_name = random_string()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.uninstall(package_name)
        expected_args = (pip_executable, "uninstall", package_name)
        assert mock_run.call_args.args == expected_args

def test_pip_uninstall_several_packages():
    """Ensure that uninstalling several package results in
    "pip uninstall <packageA> <packageB>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_names = [random_string() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.uninstall(package_names)
        expected_args = (pip_executable, "uninstall") + tuple(package_names)
        assert mock_run.call_args.args == expected_args

def test_pip_uninstall_single_package_with_flag():
    """Ensure that uninstalling a single package with upgrade=True
    "pip uninstall --upgrade <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_name = random_string()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.uninstall(package_name, switch=None)
        expected_args = (pip_executable, "uninstall", "--switch", package_name)
        assert mock_run.call_args.args == expected_args

def test_pip_uninstall_several_packages_with_flag():
    """Ensure that uninstalling a single package with switch=None
    "pip uninstall --upgrade <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_names = [random_string() for _ in range(random.randint(1, 5))]
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.uninstall(package_names, switch=None)
        expected_args = (pip_executable, "uninstall", "--switch") + tuple(package_names)
        assert mock_run.call_args.args == expected_args

def test_pip_uninstall_single_package_with_flag_value():
    """Ensure that uninstalling a single package with timeout=30
    "pip uninstall --timeout 30 <package>"
    """
    pip_executable = "pip-" + random_string() + ".exe"
    package_name = random_string()
    pip = mu.virtual_environment.Pip(pip_executable)
    with patch.object(subprocess, "run") as mock_run:
        pip.uninstall(package_name, switch=30)
        expected_args = (pip_executable, "uninstall", "--switch", "30", package_name)
        assert mock_run.call_args.args == expected_args

