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
import glob
import pathlib
import random
import shutil
import subprocess
from unittest.mock import patch
import uuid

import pytest
import mu.virtual_environment

VE = mu.virtual_environment.VirtualEnvironment
PIP = mu.virtual_environment.Pip

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
    with patch.object(subprocess, "run") as subprocess_run, patch.object(
        VE, "run_python"
    ) as run_python:
        yield subprocess_run, run_python


@pytest.fixture
def pipped():
    """Use a patched version of pip"""
    with patch("mu.virtual_environment.Pip") as pip:
        yield pip


def set_up_test_wheels(temp_dirpath):
    wheels_dirpath = temp_dirpath / "wheels"
    wheels_dirpath.mkdir()
    shutil.copyfile(
        os.path.join(HERE, "wheels", WHEEL_FILENAME),
        wheels_dirpath / WHEEL_FILENAME,
    )
    return wheels_dirpath


def test_create_virtual_environment_on_disk(tmp_path):
    """Ensure that we're actually creating a working virtual environment
    on the disk with wheels installed
    """
    wheels_dirpath = set_up_test_wheels(tmp_path)
    venv_name = uuid.uuid1().hex
    venv_dirpath = tmp_path / venv_name
    with patch.object(
        mu.virtual_environment, "wheels_dirpath", wheels_dirpath
    ):
        venv = mu.virtual_environment.VirtualEnvironment(str(venv_dirpath))
        venv.create()
        venv_site_packages = pathlib.Path(
            venv.run_python(
                "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"
            ).strip()
        )

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
        pip_output = venv.pip.run("--version")
        #
        # Awkwardly the case of the filename returned as part of the version
        # string might not match the case of the expected pip filepath above
        # Although technically it might not be correct on *nix, the simplest
        # thing is to compare them both as lowecase
        #
        assert str(expected_pip_filepath).lower() in pip_output.lower()

        #
        # Check that a Python interpreter is found in the bin/scripts directory
        #
        bin = "scripts" if sys.platform == "win32" else "bin"
        bin_extension = ".exe" if sys.platform == "win32" else ""
        assert os.path.samefile(
            venv.interpreter, venv_dirpath / bin / ("python" + bin_extension)
        )

        #
        # Check that our test wheel has been installed to a single module
        #
        expected_result = str(venv_site_packages / "arrr.py")
        result = venv.run_python(
            "-c", "import arrr; print(arrr.__file__)"
        ).strip()
        assert os.path.samefile(result, expected_result)


def test_create_virtual_environment_path(patched, tmp_path, venv_name):
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    dirpath = tmp_path / venv_name
    venv = mu.virtual_environment.VirtualEnvironment(dirpath)
    assert venv.path == dirpath


def test_create_virtual_environment_name_obj(patched, venv_name):
    """Ensure a virtual environment object has a name."""
    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
    assert venv.name == venv_name


def test_base_packages_installed(tmp_path, patched, venv_name):
    """Ensure that, when the venv is installed, the base packages are installed
    from wheels
    """
    wheels_dirpath = set_up_test_wheels(tmp_path)
    #
    # Make sure the juypter kernel install doesn't interfere
    #
    with patch.object(VE, "install_jupyter_kernel"):
        with patch.object(VE, "register_baseline_packages"):
            with patch.object(PIP, "install") as mock_pip_install:
                with patch.object(
                    mu.virtual_environment, "wheels_dirpath", wheels_dirpath
                ):
                    #
                    # Check that we're calling `pip install` with all the
                    # wheels in the wheelhouse
                    #
                    expected_args = glob.glob(
                        os.path.join(
                            mu.virtual_environment.wheels_dirpath, "*.whl"
                        )
                    )
                    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
                    venv.create()
                    mock_pip_install.assert_called_once_with(expected_args)


def test_jupyter_kernel_installed(patched, venv_name):
    """Ensure when the venv is installed the Jupyter kernel is installed"""
    _, run_python = patched
    #
    # Make sure the baseline package install doesn't interfere
    #
    with patch.object(VE, "install_baseline_packages"):
        with patch.object(VE, "register_baseline_packages"):
            venv = mu.virtual_environment.VirtualEnvironment(venv_name)
            venv.create()
            #
            # Check that we're calling `ipykernel install`
            #
            expected_jupyter_args = ("-m", "ipykernel", "install")
            args, _ = run_python.call_args
            assert expected_jupyter_args == args[: len(expected_jupyter_args)]


def test_install_user_packages(patched, venv_name):
    """Ensure that, given a list of packages, we pip install them

    (Ideally we'd do this by testing the finished result, not caring
    what sequence of pip invocations got us there, but that's expensive)
    """
    packages = [uuid.uuid1().hex for _ in range(random.randint(1, 10))]
    with patch.object(PIP, "install") as mock_pip_install:
        venv = mu.virtual_environment.VirtualEnvironment(venv_name)
        venv.install_user_packages(packages)
        #
        # We call pip with the entire list of packages
        #
        args, _ = mock_pip_install.call_args
        assert args[0] == packages


def test_remove_user_packages(patched, venv_name):
    """Ensure that, given a list of packages, we pip uninstall them

    (Ideally we'd do this by testing the finished result, not caring
    what sequence of pip invocations got us there, but that's expensive)
    """
    packages = [uuid.uuid1().hex for _ in range(random.randint(1, 10))]
    with patch.object(PIP, "uninstall") as mock_pip_uninstall:
        venv = mu.virtual_environment.VirtualEnvironment(venv_name)
        venv.remove_user_packages(packages)
        #
        # We call pip with the entire list of packages
        #
        args, _ = mock_pip_uninstall.call_args
        assert args[0] == packages


def test_installed_packages(patched, venv_name):
    """Ensure that we receive a list of package names in the venv

    NB For now we're just checking that we return whatever pip freeze
    returns only suitably stripped of versioning and other tags.

    When we've sorted out how this is going to work, we can determine
    which are pre-installed and which are user-installed
    """
    baseline_packages = [("mu-editor", 0)] + [("a", 1), ("b", 2), ("c", 3)]
    user_packages = [("d", 4), ("e", 5), ("f", 6)]
    all_packages = baseline_packages + user_packages
    random.shuffle(all_packages)

    with patch.object(VE, "baseline_packages", return_value=baseline_packages):
        with patch.object(PIP, "installed", return_value=all_packages):
            venv = mu.virtual_environment.VirtualEnvironment(venv_name)
            baseline_result, user_result = venv.installed_packages()
            assert set(baseline_result) == set(
                ["mu-editor"] + [name for name, _ in baseline_packages]
            )
            assert set(user_result) == set(name for name, _ in user_packages)


def test_venv_is_singleton(venv_name):
    """Ensure that all imported instances of `venv` are the same

    The virtual environment is created once in the `virtual_environment` module
    and then imported from each module which needs to use it, acting as a
    Singleton. But it's possible for different import styles to cause the
    module to be re-instantiated, so we check whether all instances of `venv`
    are the same instance
    """
    venv = mu.virtual_environment.venv
    from mu.modes import pygamezero, python3, web, debugger
    from mu.interface import dialogs
    from mu import app, logic

    for module in [pygamezero, python3, web, debugger, dialogs, app, logic]:
        assert module.venv is venv

def test_venv_folder_created(venv_name):
    """When the runtime venv_folder does not exist ensure we create it
    """
    with patch.object(VE, "create") as mock_create:
        #
        # Make sure we're guaranteed to find Python / pip exes
        #
        with patch.object(os.path, "isfile", return_value=True):
            venv = mu.virtual_environment.VirtualEnvironment(venv_name)
            venv.ensure()

    assert mock_create.called

def test_venv_folder_already_exists(venv_name):
    """When the venv_folder does exist as a venv ensure we do not create it
    """
    os.mkdir(venv_name)
    open(os.path.join(venv_name, "pyvenv.cfg"), "w").close()
    with patch.object(VE, "create") as mock_create:
        #
        # Make sure we're guaranteed to find Python / pip exes
        #
        with patch.object(os.path, "isfile", return_value=True):
            venv = mu.virtual_environment.VirtualEnvironment(venv_name)
            venv.ensure()

    assert not mock_create.called

def test_venv_folder_already_exists_not_venv(venv_name):
    """When the venv_folder does exist not as a venv ensure we raise an error
    """
    os.mkdir(venv_name)
    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
    with pytest.raises(mu.virtual_environment.VirtualEnvironmentError):
        venv.ensure()

def test_venv_folder_already_exists_not_directory(venv_name):
    """When the runtime venv_folder does exist but is not a directory ensure
    we raise an exception
    """
    open(venv_name, "w").close()
    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
    with pytest.raises(mu.virtual_environment.VirtualEnvironmentError):
        venv.ensure()

def test_venv_created_no_interpreter(venv_name):
    """When the venv exists but has no interpreter ensure we raise an exception
    """
    os.mkdir(venv_name)
    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
    #
    # Create the pip executable so the error is not for that
    #
    os.makedirs(venv._bin_directory)
    open(venv.pip.executable, "w").close()
    assert not os.path.isfile(venv.interpreter)

    with pytest.raises(mu.virtual_environment.VirtualEnvironmentError):
        venv.ensure()

def test_venv_created_no_pip(venv_name):
    """When the venv exists but has no pip ensure we raise an exception
    """
    os.mkdir(venv_name)
    venv = mu.virtual_environment.VirtualEnvironment(venv_name)
    #
    # Create the interpreter executable so the error is not for that
    #
    os.makedirs(venv._bin_directory)
    open(venv.interpreter, "w").close()
    assert not os.path.isfile(venv.pip.executable)
    with pytest.raises(mu.virtual_environment.VirtualEnvironmentError):
        venv.ensure()
