# -*- coding: utf-8 -*-
"""
Tests for the virtual_environment module supporting Mu's runtime venv

Creating a virtual environment involves a certain amount of disk
activity and is fairly expensive in testing terms; pip-installing
things even more so, even when they're only wheels from local disk

The trick is not to test that *venv* itself works, or pip, both of which
we assume. Rather we have to test whether our use of those tools give
the effect we want.

So a lot of the time we're going to be mocking things like subprocess.run
and checking that appropriate things are called. We need to be careful
not to over-describe the parameters as we might, for example, want later
to add or remove certain flags, or to use different wheels.
"""
import sys
import os
import contextlib
import pathlib
import shutil
import subprocess
import tempfile
from unittest.mock import Mock, MagicMock, patch
import uuid

import pytest
import mu.virtual_environment
VE = mu.virtual_environment.VirtualEnvironment

HERE = os.path.dirname(__file__)
WHEEL_FILENAME = "arrr-1.0.2-py3-none-any.whl"

@pytest.fixture
def venv_name():
    return uuid.uuid1().hex

def test_create_virtual_environment_on_disk(tmp_path):
    """Ensure that we're actually creating a working virtual environment
    on the disk with wheels installed
    """
    wheels_dirpath = tmp_path / "wheels"
    wheels_dirpath.mkdir()
    shutil.copyfile(os.path.join(HERE, "wheels", WHEEL_FILENAME), wheels_dirpath / WHEEL_FILENAME)
    venv_name = uuid.uuid1().hex
    venv_dirpath = tmp_path / venv_name
    with patch.object(mu.virtual_environment, "wheels_dirpath", wheels_dirpath):
        venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
        venv.create()

        #
        # Having a series of unrelated asserts is generally frowned upon
        # But creating and populating an actual venv on disk is relatively
        # expensive so we'll do it the once and test everything about it
        # that we need to.
        #
        # The remaining tests will mock things out and then just check that
        # the appropriate things were called
        #
        assert (venv_dirpath / "pyvenv.cfg").is_file()
        expected_pip_filepath = venv_dirpath / "lib" / "site-packages" / "pip"
        pip_output = venv.pip("--version")
        assert str(expected_pip_filepath) in pip_output
        venv.find_interpreter()
        #
        # FIXME: need to use platform-independent location
        #
        assert pathlib.Path(venv.interpreter) == venv_dirpath / "scripts" / "python.exe"

@patch.object(subprocess, "run")
@patch.object(VE, "run_python")
def test_create_virtual_environment_path(mock_run, mock_run_python, venv_name, tmp_path):
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    dirpath = tmp_path / venv_name
    venv = mu.virtual_environment.VirtualEnvironment(dirpath)
    assert venv.path == dirpath


@patch.object(subprocess, "run")
@patch.object(VE, "run_python")
def test_create_virtual_environment_name_obj(mock_run, mock_run_python, tmp_path, venv_name):
    """Ensure a virtual environment object has a name.
    """
    dirpath = tmp_path / venv_name
    venv = mu.virtual_environment.VirtualEnvironment(dirpath)
    assert venv.name == venv_name


@patch.object(subprocess, "run")
@patch.object(VE, "run_python")
@patch.object(VE, "find_interpreter")
#
# FIXME: need to find some way of combining several patches into one fixture
#
def test_base_packages_installed(mock_run, mock_run_python, mock_find_interpreter, tmp_path, venv_name):
    """Ensure that, when the venv is installed, the base packages are installed
    from wheels
    """
    dirpath = tmp_path / venv_name
    venv = mu.virtual_environment.VirtualEnvironment(dirpath)
    venv.create()
    assert mock_run_python.called_with("pip")
