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
WHEEL_FILENAME = "arrr-1.0.2-py3-none-any.whl"

@pytest.fixture
def venv_name():
    """Use a random venv name each time, at least partly to expose any
    hidden assumptions about the name of the venv directory
    """
    return uuid.uuid1().hex


@pytest.fixture
def patched():
    """Creating a real venv on disk is expensive. Here we patch out
    the expensive parts and pass them into the test so we can detect
    how they've been called
    """
    with patch.object(subprocess, "run") as subprocess_run, \
      patch.object(VE, "run_python") as run_python, \
      patch.object(VE, "find_interpreter"):
        yield subprocess_run, run_python


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
        venv_site_packages = venv_dirpath / "lib" / "site-packages"

        #
        # Having a series of unrelated asserts is generally frowned upon
        # But creating and populating an actual venv on disk is relatively
        # expensive so we'll do it the once and test everything about it
        # that we need to.
        #
        # The remaining tests will mock things out and then just check that
        # the appropriate things were called
        #

        #
        # Check that we've created a virtual environment on disk
        #
        assert (venv_dirpath / "pyvenv.cfg").is_file()

        #
        # Check that we have an installed version of pip
        #
        expected_pip_filepath = venv_site_packages / "pip"
        pip_output = venv.pip("--version")
        assert str(expected_pip_filepath) in pip_output

        #
        # Check that a Python interpreter is found in the bin/scripts directory
        #
        venv.find_interpreter()
        bin = "scripts" if sys.platform == "win32" else "bin"
        assert pathlib.Path(venv.interpreter) == venv_dirpath / bin / "python.exe"

        #
        # Check that our test wheel has been installed to a single module
        #
        expected_result = str(venv_site_packages / "arrr.py")
        result = venv.run_python("-c", "import arrr; print(arrr.__file__)").strip()
        assert result == expected_result


def test_create_virtual_environment_path(patched, tmp_path, venv_name):
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    dirpath = tmp_path / venv_name
    venv = mu.virtual_environment.VirtualEnvironment(dirpath)
    assert venv.path == dirpath


def test_create_virtual_environment_name_obj(patched, venv_name):
    """Ensure a virtual environment object has a name.
    """
    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
    assert venv.name == venv_name


def test_base_packages_installed(patched, venv_name):
    """Ensure that, when the venv is installed, the base packages are installed
    from wheels
    """
    _, run_python = patched
    #
    # Make sure the juypter kernel install doesn't interfere
    #
    with patch.object(VE, "install_jupyter_kernel"):
        venv = mu.virtual_environment.VirtualEnvironment(venv_name)
        venv.create()
        #
        # Check that we're calling `pip install` with all the wheels in our wheelhouse
        #
        expected_python_args = ("-m", "pip", "install") + tuple(glob.glob(os.path.join(mu.virtual_environment.wheels_dirpath, "*.whl")))
        assert expected_python_args == run_python.call_args.args


def test_jupyter_kernel_installed(patched, venv_name):
    """Ensure that, when the venv is installed, the Jupyter kernel is installed
    """
    _, run_python = patched
    #
    # Make sure the baseline package install doesn't interfere
    #
    with patch.object(VE, "install_baseline_packages"):
        venv = mu.virtual_environment.VirtualEnvironment(venv_name)
        venv.create()
        #
        # Check that we're calling `ipykernel install`
        #
        expected_jupyter_args = ("-m", "ipykernel", "install")
        assert expected_jupyter_args == run_python.call_args.args[:len(expected_jupyter_args)]


def test_install_user_packages(patched, venv_name):
    """Ensure that, given a list of packages, we pip install them

    (Ideally we'd do this by testing the finished result, not caring
    what sequence of pip invocations got us there, but that's expensive)
    """
    packages = [uuid.uuid1().hex for _ in range(random.randint(1, 10))]
    with patch.object(VE, "pip") as run_pip:
        venv = mu.virtual_environment.VirtualEnvironment(venv_name)
        venv.install_user_packages(packages)
        #
        # For each package we should have called our pip runner with
        # install as the first parameter and the package name as the
        # last. There may be switches (eg --upgrade) but we don't want
        # to be sensitive to those
        #
        assert run_pip.call_count == len(packages)
        for (call_args, package) in zip(run_pip.call_args_list, packages):
            assert call_args.args[0] == "install"
            assert call_args.args[-1] == package


def test_remove_user_packages(patched, venv_name):
    """Ensure that, given a list of packages, we pip uninstall them

    (Ideally we'd do this by testing the finished result, not caring
    what sequence of pip invocations got us there, but that's expensive)
    """
    packages = [uuid.uuid1().hex for _ in range(random.randint(1, 10))]
    with patch.object(VE, "pip") as run_pip:
        venv = mu.virtual_environment.VirtualEnvironment(venv_name)
        venv.remove_user_packages(packages)
        #
        # For each package we should have called our pip runner with
        # install as the first parameter and the package name as the
        # last. There may be switches but we don't want to be sensitive
        # to those
        #
        assert run_pip.call_count == len(packages)
        for (call_args, package) in zip(run_pip.call_args_list, packages):
            assert call_args.args[0] == "uninstall"
            assert call_args.args[-1] == package


def test_installed_packages(patched, venv_name):
    """Ensure that we receive a list of package names in the venv

    NB For now we're just checking that we return whatever pip freeze
    returns only suitably stripped of versioning and other tags.

    When we've sorted out how this is going to work, we can determine
    which are pre-installed and which are user-installed
    """
    baseline_packages = ['a', 'b', 'c']
    user_packages = ['d', 'e', 'f']
    all_packages = baseline_packages + user_packages
    random.shuffle(all_packages)

    with patch.object(VE, "baseline_packages", baseline_packages):
        with patch.object(VE, "pip") as run_pip:
            run_pip.return_value = all_packages
            venv = mu.virtual_environment.VirtualEnvironment(venv_name)
            baseline_result, user_result = venv.installed_packages()
            assert set(baseline_result) == set(baseline_packages)
            assert set(user_result) == set(user_packages)
