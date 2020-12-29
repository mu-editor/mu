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
import json
import random
import shutil
import subprocess
from unittest import mock
import uuid

from PyQt5.QtCore import QTimer, QProcess
import pytest

import mu.virtual_environment
import mu.wheels

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
def venv_dirpath(tmp_path, venv_name):
    """Generate a temporary venv dirpath"""
    dirpath = tmp_path / venv_name
    dirpath.mkdir()
    return str(dirpath)


@pytest.fixture
def venv(venv_dirpath):
    """Generate a temporary venv"""
    return mu.virtual_environment.VirtualEnvironment(venv_dirpath)


@pytest.fixture
def patched():
    """Creating a real venv on disk is expensive. Here we patch out
    the expensive parts and pass them into the test so we can detect
    how they've been called
    """
    with mock.patch.object(
        subprocess, "run"
    ) as subprocess_run, mock.patch.object(VE, "run_python") as run_python:
        yield subprocess_run, run_python


@pytest.fixture
def pipped():
    """Use a patched version of pip"""
    with mock.patch("mu.virtual_environment.Pip") as pip:
        yield pip


@pytest.fixture
def baseline_packages(tmp_path):
    baseline_filepath = str(tmp_path / "baseline_packages.json")
    package_name = uuid.uuid1().hex
    package_version = uuid.uuid1().hex
    packages = [[package_name, package_version]]
    with mock.patch.object(
        mu.virtual_environment.VirtualEnvironment,
        "BASELINE_PACKAGES_FILEPATH",
        baseline_filepath
    ):
        yield baseline_filepath, packages


@pytest.fixture
def test_wheels(tmp_path):
    wheels_dirpath = str(tmp_path / "wheels")
    os.mkdir(wheels_dirpath)
    shutil.copyfile(
        os.path.join(HERE, "wheels", WHEEL_FILENAME),
        os.path.join(wheels_dirpath, WHEEL_FILENAME)
    )
    with mock.patch.object(
        mu.virtual_environment, "wheels_dirpath", wheels_dirpath
    ):
        yield wheels_dirpath


def test_create_virtual_environment_on_disk(venv_dirpath, test_wheels):
    """Ensure that we're actually creating a working virtual environment
    on the disk with wheels installed
    """
    venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
    venv.create()
    venv_site_packages = venv.run_python(
            "-c", "import sysconfig; print(sysconfig.get_path('purelib'))"
        ).strip()

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
    assert venv._directory_is_venv()

    #
    # Check that we have an installed version of pip
    #
    expected_pip_filepath = os.path.join(venv_site_packages, "pip")
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
        venv.interpreter, os.path.join(venv_dirpath, bin, "python" + bin_extension)
    )

    #
    # Check that our test wheel has been installed to a single module
    #
    expected_result = os.path.join(venv_site_packages, "arrr.py")
    result = venv.run_python("-c", "import arrr; print(arrr.__file__)").strip()
    assert os.path.samefile(result, expected_result)


def test_create_virtual_environment_path(patched, venv_dirpath):
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
    assert venv.path == str(venv_dirpath)


def test_create_virtual_environment_name_obj(patched, venv_dirpath):
    """Ensure a virtual environment object has a name."""
    venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
    assert venv.name == os.path.basename(venv_dirpath)


def test_download_wheels_if_not_present(venv, test_wheels):
    """If we try to install baseline package without any wheels
    ensure we try to download them
    """
    wheels_dirpath = test_wheels
    for filepath in glob.glob(os.path.join(wheels_dirpath, "*.whl")):
        os.unlink(filepath)
    assert not glob.glob(os.path.join(wheels_dirpath, "*.whl"))

    with mock.patch.object(
        mu.virtual_environment, "wheels_dirpath", wheels_dirpath
    ), mock.patch.object(mu.wheels, "download") as mock_download:
        try:
            venv.install_baseline_packages()
        #
        # Ignore the exception which will arise from not actually
        # downloading any wheels!
        #
        except mu.virtual_environment.VirtualEnvironmentError:
            pass

    assert mock_download.called


def test_base_packages_installed(patched, venv, test_wheels):
    """Ensure that, when the venv is installed, the base packages are installed
    from wheels
    """
    #
    # Make sure the juypter kernel install doesn't interfere
    #
    with mock.patch.object(VE, "install_jupyter_kernel"):
        with mock.patch.object(VE, "register_baseline_packages"):
            with mock.patch.object(PIP, "install") as mock_pip_install:
                #
                # Check that we're calling `pip install` with all the
                # wheels in the wheelhouse
                #
                expected_args = glob.glob(
                    os.path.join(
                        mu.virtual_environment.wheels_dirpath, "*.whl"
                    )
                )
                venv.create()
                mock_pip_install.assert_called_once_with(expected_args)


def test_jupyter_kernel_installed(patched, venv):
    """Ensure when the venv is installed the Jupyter kernel is installed"""
    _, run_python = patched
    #
    # Make sure the baseline package install doesn't interfere
    #
    with mock.patch.object(VE, "install_baseline_packages"):
        with mock.patch.object(VE, "register_baseline_packages"):
            venv.create()
            #
            # Check that we're calling `ipykernel install`
            #
            expected_jupyter_args = ("-m", "ipykernel", "install")
            args, _ = run_python.call_args
            assert expected_jupyter_args == args[: len(expected_jupyter_args)]


def test_install_user_packages(patched, venv):
    """Ensure that, given a list of packages, we pip install them

    (Ideally we'd do this by testing the finished result, not caring
    what sequence of pip invocations got us there, but that's expensive)
    """
    packages = [uuid.uuid1().hex for _ in range(random.randint(1, 10))]
    with mock.patch.object(PIP, "install") as mock_pip_install:
        venv.install_user_packages(packages)
        #
        # We call pip with the entire list of packages
        #
        args, _ = mock_pip_install.call_args
        assert args[0] == packages


def test_remove_user_packages(patched, venv):
    """Ensure that, given a list of packages, we pip uninstall them

    (Ideally we'd do this by testing the finished result, not caring
    what sequence of pip invocations got us there, but that's expensive)
    """
    packages = [uuid.uuid1().hex for _ in range(random.randint(1, 10))]
    with mock.patch.object(PIP, "uninstall") as mock_pip_uninstall:
        venv.remove_user_packages(packages)
        #
        # We call pip with the entire list of packages
        #
        args, _ = mock_pip_uninstall.call_args
        assert args[0] == packages


def test_installed_packages(patched, venv):
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

    with mock.patch.object(
        VE, "baseline_packages", return_value=baseline_packages
    ):
        with mock.patch.object(PIP, "installed", return_value=all_packages):
            baseline_result, user_result = venv.installed_packages()
            assert set(baseline_result) == set(
                ["mu-editor"] + [name for name, _ in baseline_packages]
            )
            assert set(user_result) == set(name for name, _ in user_packages)


def test_venv_is_singleton():
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


def test_venv_folder_created(venv):
    """When the runtime venv_folder does not exist ensure we create it"""
    os.rmdir(venv.path)
    with mock.patch.object(VE, "create") as mock_create, mock.patch.object(
        VE, "ensure_pip"
    ) as mock_ensure_pip, mock.patch.object(
        VE, "ensure_interpreter"
    ) as mock_ensure_interpreter:
        venv.ensure()

    assert mock_create.called
    assert mock_ensure_pip.called
    assert mock_ensure_interpreter.called


def test_venv_folder_already_exists(venv):
    """When the venv_folder does exist as a venv ensure we do not create it"""
    open(os.path.join(venv.path, "pyvenv.cfg"), "w").close()
    with mock.patch.object(VE, "create") as mock_create, mock.patch.object(
        VE, "ensure_pip"
    ) as mock_ensure_pip, mock.patch.object(
        VE, "ensure_interpreter"
    ) as mock_ensure_interpreter:
        venv.ensure()

    assert not mock_create.called
    assert mock_ensure_pip.called
    assert mock_ensure_interpreter.called


def test_venv_folder_already_exists_not_venv(venv):
    """When venv_folder does exist not as a venv ensure we raise an error"""
    assert not os.path.isfile(os.path.join(venv.path, "pyvenv.cfg"))
    assert not os.path.isfile(venv.interpreter)
    with pytest.raises(mu.virtual_environment.VirtualEnvironmentError):
        venv.ensure()


def test_venv_folder_already_exists_not_directory(venv_dirpath):
    """When the runtime venv_folder does exist but is not a directory ensure
    we raise an exception
    """
    os.rmdir(venv_dirpath)
    open(venv_dirpath, "w").close()
    venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
    with pytest.raises(mu.virtual_environment.VirtualEnvironmentError):
        venv.ensure()


def test_ensure_interpreter(venv):
    """When venv exists but has no interpreter ensure we raise an exception"""
    assert not os.path.isfile(venv.interpreter)

    with pytest.raises(
        mu.virtual_environment.VirtualEnvironmentError, match="Interpreter"
    ):
        venv.ensure_interpreter()


def test_ensure_pip(venv):
    """When venv exists but has no interpreter ensure we raise an exception"""
    assert not os.path.isfile(venv.interpreter)

    with pytest.raises(
        mu.virtual_environment.VirtualEnvironmentError, match="Pip"
    ):
        venv.ensure_pip()


def test_read_baseline_packages_success(venv, baseline_packages):
    """Ensure that we can read back a list of baseline packages"""
    baseline_filepath, packages = baseline_packages
    with open(baseline_filepath, "w") as f:
        f.write(json.dumps(packages))

    expected_output = packages
    output = venv.baseline_packages()
    assert output == expected_output


def test_read_baseline_packages_failure(venv, baseline_packages):
    """Ensure that if we can't read a list of packages we see an error log
    and an empty list is returned
    """
    baseline_filepath, _ = baseline_packages
    with open(baseline_filepath, "w") as f:
        f.write("***")

    expected_output = []
    output = venv.baseline_packages()
    assert output == expected_output


def _QTimer_singleshot(delay, partial):
    return partial.func(*partial.args, **partial.keywords)


def test_run_python_blocking(venv):
    """Ensure that Python is run synchronously with the args passed"""
    command = venv.interpreter
    args = ("-c", "import sys; print(sys.executable)")
    with mock.patch.object(
        QTimer, "singleShot", _QTimer_singleshot
    ), mock.patch.object(QProcess, "start") as mocked_start:
        venv.run_python(*args)

    mocked_start.assert_called_with(command, args)


def test_run_python_nonblocking(venv):
    """Ensure that a QProcess is started with the relevant params"""
    command = venv.interpreter
    args = ("-c", "import sys; print(sys.executable)")
    with mock.patch.object(
        QTimer, "singleShot", _QTimer_singleshot
    ), mock.patch.object(QProcess, "start") as mocked_start:
        venv.run_python(*args, slots=venv.Slots(output=lambda x: x))

    mocked_start.assert_called_with(command, args)
