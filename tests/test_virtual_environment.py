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
import shutil
import tempfile
from unittest.mock import Mock, MagicMock, patch
import uuid

import pytest
import mu.virtual_environment
VE = mu.virtual_environment.VirtualEnvironment

#
# Creating a virtual environment involves a certain amount of disk
# activity and is fairly expensive in testing terms; pip-installing
# things even more so, even when they're only wheels from local disk
#
#
#

@contextlib.contextmanager
@patch.object(VE, "install_baseline_packages")
@patch.object(VE, "install_jupyter_kernel")
def generate_venv(mock_pip, dirpath=None):
    with tempfile.TemporaryDirectory(prefix="mu-") as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        venv.create()
        yield venv


class MockPip(object):

    def __init__(self):
        self.called_with = []

    def __call__(*args, **kwargs):
        self.called_with.append((args, kwargs))


def test_create_virtual_environment_obj():
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    with tempfile.TemporaryDirectory(prefix="mu-") as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        assert venv.path == dirpath


def test_create_virtual_environment_name_obj():
    """Ensure a virtual environment object has a name.
    """
    with tempfile.TemporaryDirectory(prefix="mu-") as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        assert bool(venv.name)


@patch.object(VE, "pip")
def test_create_venv(mock_pip):
    """Ensure that we create a virtual environment on disk.

    The nearest thing to a canonical check seems to be the presence of
    a pyvenv.cfg file
    """
    with tempfile.TemporaryDirectory(prefix="mu-") as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        venv.create()
        assert os.path.isfile(os.path.join(dirpath, "pyvenv.cfg"))


def test_pip():
    """Ensure that the pip function calls the local pip
    """
    with generate_venv() as venv:
        expected_pip_filepath = os.path.normpath(os.path.join(venv.path, "lib/site-packages/pip"))
        pip_output = venv.pip("--version")
        assert expected_pip_filepath in pip_output


@patch.object(VE, "pip")
def test_base_packages_installed(mock_pip):
    """Ensure that, when the venv is installed, the base packages are installed
    from wheels
    """
    with generate_venv() as venv:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        venv.create()
        assert mock_pip.called