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
import random
import shutil
import subprocess
import uuid
import logging
from unittest import mock

import pytest

import mu
import mu.settings
import mu.virtual_environment
import mu.wheels

VE = mu.virtual_environment.VirtualEnvironment
VEError = mu.virtual_environment.VirtualEnvironmentError
PIP = mu.virtual_environment.Pip

HERE = os.path.dirname(__file__)
WHEEL_FILENAME = "arrr-1.0.2-py3-none-any.whl"


@pytest.fixture
def venv_name():
    """Use a random venv name each time, at least partly to expose any
    hidden assumptions about the name of the venv directory

    Force the name to have a space in it to expose possible fragilities that way
    """
    hex = uuid.uuid1().hex
    return hex[:2] + " " + hex[2:4]


@pytest.fixture
def venv_dirpath(tmp_path, venv_name):
    """Generate a temporary venv dirpath"""
    dirpath = tmp_path / venv_name
    dirpath.mkdir()
    return str(dirpath)


@pytest.fixture
def venv_settings():
    """We've introduced a check between the installed and current versions
    of mu. To ensure this doesn't trip every time we set up a faux settings
    which always matches the current version"""
    settings = mu.settings.VirtualEnvironmentSettings()
    settings["mu_version"] = mu.__version__
    yield settings


@pytest.fixture
def venv(venv_dirpath, venv_settings):
    """Generate a temporary venv"""
    logger = logging.getLogger(mu.virtual_environment.__name__)
    # Clean up the logging from an unknown previous state.
    while logger.hasHandlers() and logger.handlers:
        handler = logger.handlers[0]
        if isinstance(handler, mu.virtual_environment.SplashLogHandler):
            logger.removeHandler(handler)

    venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
    venv.settings = venv_settings
    yield venv

    # Now clean up the logging after the test.
    while logger.hasHandlers() and logger.handlers:
        handler = logger.handlers[0]
        if isinstance(handler, mu.virtual_environment.SplashLogHandler):
            logger.removeHandler(handler)


@pytest.fixture
def patched():
    """Creating a real venv on disk is expensive. Here we patch out
    the expensive parts and pass them into the test so we can detect
    how they've been called
    """
    with mock.patch.object(
        subprocess, "run"
    ) as subprocess_run, mock.patch.object(
        VE, "run_python"
    ) as run_python, mock.patch.object(
        VE, "run_subprocess", return_value=(True, "")
    ) as run_subprocess:
        yield subprocess_run, run_python, run_subprocess


@pytest.fixture
def pipped():
    """Use a patched version of pip"""
    with mock.patch("mu.virtual_environment.Pip") as pip:
        yield pip


@pytest.fixture
def workspace_dirpath(tmp_path):
    workspace_dirpath = tmp_path / uuid.uuid1().hex
    workspace_dirpath.mkdir()
    with mock.patch.object(mu.config, "DATA_DIR", workspace_dirpath):
        yield workspace_dirpath


@pytest.fixture
def test_wheels(tmp_path):
    wheels_dirpath = str(tmp_path / "wheels")
    os.mkdir(wheels_dirpath)
    shutil.copyfile(
        os.path.join(HERE, "wheels", WHEEL_FILENAME),
        os.path.join(wheels_dirpath, WHEEL_FILENAME),
    )
    with mock.patch.object(
        mu.virtual_environment, "wheels_dirpath", wheels_dirpath
    ):
        yield wheels_dirpath


def test_splash_log_handler():
    """
    Ensure a SplashLogHandler emits an appropriately formatted log entries to
    the referenced PyQT signal.
    """
    signal = mock.MagicMock()
    slh = mu.virtual_environment.SplashLogHandler(signal)
    assert slh.level == logging.DEBUG
    assert slh.emitter == signal
    log_record = mock.MagicMock()
    log_record.getMessage.return_value = "A multiline\nlog message\n"
    slh.handle(log_record)
    # One log message for each line in the record.
    assert signal.emit.call_count == 2


def test_virtual_environment_str_contains_path(venv):
    assert venv.path in str(venv)


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
    # Check that we can still detect a venv when there's no .cfg file
    # (Then replace the .cfg for later use by the venv!)
    #
    cfg_filepath = os.path.join(venv.path, "pyvenv.cfg")
    if os.path.isfile(cfg_filepath):
        renamed_filepath = cfg_filepath + ".xyz"
        os.rename(cfg_filepath, renamed_filepath)
        assert venv._directory_is_venv()
        os.rename(renamed_filepath, cfg_filepath)

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
        venv.interpreter,
        os.path.join(venv_dirpath, bin, "python" + bin_extension),
    )

    #
    # Check that our test wheel has been installed to a single module
    #
    expected_result = os.path.join(venv_site_packages, "arrr.py")
    result = venv.run_python("-c", "import arrr; print(arrr.__file__)").strip()
    assert os.path.samefile(result, expected_result)

    #
    # Issue #1372 -- venv creation fails for paths with a space
    #
    with mock.patch.object(VE, "ensure_key_modules"):
        venv.ensure()


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


def test_create_virtual_environment_failure(venv):
    output = uuid.uuid1().hex
    with mock.patch.object(
        venv, "run_subprocess", return_value=(False, output)
    ):
        try:
            venv.create()
        except Exception as exc:
            assert isinstance(
                exc, mu.virtual_environment.VirtualEnvironmentCreateError
            )
            assert "nable to create" in exc.message
            assert output in exc.message


def test_download_wheels_if_not_present(venv, test_wheels):
    """If we try to install baseline package without any wheels
    ensure we try to download them
    """
    wheels_dirpath = test_wheels
    for filepath in glob.glob(os.path.join(wheels_dirpath, "*.zip")):
        os.unlink(filepath)
    assert not glob.glob(os.path.join(wheels_dirpath, "*.zip"))

    with mock.patch.object(
        mu.virtual_environment, "wheels_dirpath", wheels_dirpath
    ), mock.patch.object(mu.wheels, "download") as mock_download, mock.patch.object(venv, "install_from_zipped_wheels"):
        try:
            venv.install_baseline_packages()
        #
        # Ignore the exception which will arise from not actually
        # downloading any wheels!
        #
        except VEError:
            pass

    assert mock_download.called


def test_download_wheels_failure(venv, test_wheels):
    """If the wheels download fails, ensure that we raise a VirtualEnvironmentError
    with the same message"""
    message = uuid.uuid1().hex
    wheels_dirpath = test_wheels
    for filepath in glob.glob(os.path.join(wheels_dirpath, "*.zip")):
        os.unlink(filepath)
    assert not glob.glob(os.path.join(wheels_dirpath, "*.zip"))
    with mock.patch.object(
        mu.wheels,
        "download",
        side_effect=mu.wheels.WheelsDownloadError(message),
    ):
        try:
            venv.install_baseline_packages()
        except mu.wheels.WheelsDownloadError as exc:
            assert message in exc.message


def test_base_packages_installed(patched, venv, test_wheels):
    """Ensure that, when the venv is installed, the base packages are installed
    from wheels
    """
    #
    # Check that we're calling `pip install` with all the
    # wheels in the wheelhouse
    #
    expected_args = glob.glob(
        os.path.join(mu.virtual_environment.wheels_dirpath, "*.whl")
    )
    #
    # Make sure the juypter kernel install doesn't interfere
    #
    with mock.patch.object(VE, "install_jupyter_kernel"):
        with mock.patch.object(VE, "register_baseline_packages"):
            with mock.patch.object(PIP, "install") as mock_pip_install:
                venv.create()
    for mock_call_args in mock_pip_install.call_args_list:
        assert len(mock_call_args[0]) == 1
        assert mock_call_args[0][0] in expected_args
        assert mock_call_args[1] == {"deps": False, "index": False}


def test_jupyter_kernel_installed(patched, venv):
    """Ensure when the venv is installed the Jupyter kernel is installed"""
    _, _, run_subprocess = patched
    #
    # Make sure the baseline package install doesn't interfere
    #
    with mock.patch.object(VE, "install_baseline_packages"):
        with mock.patch.object(VE, "register_baseline_packages"):
            venv.create()
            #
            # Check that we're calling `ipykernel install`
            #
            expected_jupyter_args = (
                sys.executable,
                "-m",
                "ipykernel",
                "install",
            )
            print(
                "run_subprocess / call_args:",
                run_subprocess,
                run_subprocess.call_args,
            )
            args, _ = run_subprocess.call_args
            assert expected_jupyter_args == args[: len(expected_jupyter_args)]


def test_jupyter_kernel_failure(patched, venv):
    """Ensure when the Jupyter kernel fails to install we raise an exception and
    include the output"""
    output = uuid.uuid1().hex
    with mock.patch.object(
        venv, "run_subprocess", return_value=(False, output)
    ):
        try:
            venv.install_jupyter_kernel()
        except VEError as exc:
            assert "nable to install kernel" in exc.message
            assert output in exc.message


def test_upgrade_pip_failure(venv):
    """Ensure that we raise an error with output when pip can't be upgraded"""
    output = uuid.uuid1().hex
    with mock.patch.object(
        venv, "run_subprocess", return_value=(True, output)
    ):
        venv.upgrade_pip()


def test_upgrade_pip_success(venv):
    """Ensure that we raise an error with output when pip can't be upgraded"""
    output = uuid.uuid1().hex
    with mock.patch.object(
        venv, "run_subprocess", return_value=(False, output)
    ):
        try:
            venv.upgrade_pip()
        except VEError as exc:
            assert "nable to upgrade pip" in exc.message
            assert output in exc.message


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


def _ensure_venv(results):
    def _inner_ensure_venv(self, results=results):
        result = results.pop()
        if isinstance(result, Exception):
            raise result
        else:
            return result

    return _inner_ensure_venv


def test_venv_folder_created(venv):
    """When not existing venv is ensured we create a new one"""
    os.rmdir(venv.path)
    with mock.patch.object(VE, "create") as mock_create, mock.patch.object(
        VE, "ensure", _ensure_venv([True, VEError("Failed")])
    ):
        venv.ensure_and_create()

    assert mock_create.called


def test_venv_second_try(venv):
    """If the creation of a venv fails to produce a valid venv, try again"""
    with mock.patch.object(VE, "create") as mock_create, mock.patch.object(
        VE, "ensure", _ensure_venv([True, VEError("Failed")])
    ):
        venv.ensure_and_create()

    assert mock_create.call_count == 1


def test_venv_fails_after_three_tries(venv):
    """If the venv fails to ensure after three tries we raise an exception"""
    with mock.patch.object(VE, "create"), mock.patch.object(
        VE,
        "ensure",
        _ensure_venv(
            [VEError("Failed"), VEError("Failed"), VEError("Failed")]
        ),
    ):
        with pytest.raises(VEError):
            venv.ensure_and_create()


def test_venv_ensure_and_create_splash_handler(venv):
    """Ensure the splash handler is set up when calling ensure_and_create"""
    with mock.patch.object(VE, "create"), mock.patch.object(
        VE, "ensure"
    ), mock.patch.object(mu.virtual_environment, "logger") as mock_logger:
        venv.ensure_and_create(object)

    all_args = mock_logger.addHandler.call_args
    assert all_args is not None, "logger.addHandler not called at all"
    args, _ = all_args
    (handler,) = args
    assert isinstance(handler, mu.virtual_environment.SplashLogHandler)

    all_args = mock_logger.removeHandler.call_args
    assert all_args is not None, "logger.removeHandler not called at all"
    args, _ = all_args
    (handler,) = args
    assert isinstance(handler, mu.virtual_environment.SplashLogHandler)


#
# Ensure Path
#
def test_venv_folder_already_exists(venv):
    """When all ensure tests pass, we have an existing venv so don't create it"""
    open(os.path.join(venv.path, "pyvenv.cfg"), "w").close()
    with mock.patch.object(VE, "ensure") as mock_ensure, mock.patch.object(
        VE, "create"
    ) as mock_create:
        venv.ensure_and_create()

    assert not mock_create.called
    assert mock_ensure.called


def test_venv_folder_does_not_exist(venv):
    """When venv_folder does exist not at all we raise an error"""
    os.rmdir(venv.path)
    with pytest.raises(VEError):
        venv.ensure_path()


def test_venv_folder_already_exists_not_venv(venv):
    """When venv_folder does exist not as a venv ensure we raise an error"""
    assert not os.path.isfile(os.path.join(venv.path, "pyvenv.cfg"))
    assert not os.path.isfile(venv.interpreter)
    with pytest.raises(VEError):
        venv.ensure_path()


def test_venv_folder_already_exists_not_directory(venv_dirpath):
    """When the runtime venv_folder does exist but is not a directory ensure
    we raise an exception
    """
    os.rmdir(venv_dirpath)
    open(venv_dirpath, "w").close()
    venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
    with pytest.raises(VEError):
        venv.ensure_path()


#
# Ensure Interpreter / Version
#
def test_ensure_interpreter(venv):
    """When venv exists but has no interpreter ensure we raise an exception"""
    assert not os.path.isfile(venv.interpreter)
    with pytest.raises(VEError, match="[Ii]nterpreter"):
        venv.ensure_interpreter()


def test_ensure_interpreter_failed_to_run(venv):
    """When venv interpreter can't be run raise an exception"""
    with mock.patch.object(VE, "run_subprocess", return_value=(False, "x.y")):
        with pytest.raises(VEError, match="Failed to run"):
            venv.ensure_interpreter_version()


def test_ensure_interpreter_version(venv):
    """When venv interpreter exists but for a different Py version raise an exception"""
    with mock.patch.object(VE, "run_subprocess", return_value=(True, "x.y")):
        with pytest.raises(VEError, match="[Ii]nterpreter at version"):
            venv.ensure_interpreter_version()


#
# Ensure Key Modules
#
def test_ensure_key_modules_failure(venv):
    modules = [uuid.uuid1().hex, uuid.uuid1().hex, uuid.uuid1().hex]
    output = uuid.uuid1().hex
    with mock.patch.object(
        mu.wheels, "mode_packages", modules
    ), mock.patch.object(VE, "run_subprocess", return_value=(False, output)):
        try:
            venv.ensure_key_modules()
        except VEError as exc:
            assert "Failed to import" in exc.message
            assert output in exc.message


def test_ensure_key_modules_success(venv):
    modules = [uuid.uuid1().hex, uuid.uuid1().hex, uuid.uuid1().hex]
    output = uuid.uuid1().hex
    with mock.patch.object(
        mu.wheels, "mode_packages", modules
    ), mock.patch.object(VE, "run_subprocess", return_value=(True, output)):
        venv.ensure_key_modules()


#
# Ensure Pip
#
def test_ensure_pip(venv):
    """When venv exists but has no interpreter ensure we raise an exception"""
    assert not os.path.isfile(venv.interpreter)

    with pytest.raises(VEError, match="Pip"):
        venv.ensure_pip()


def _QTimer_singleshot(delay, partial):
    return partial.func(*partial.args, **partial.keywords)


def test_run_python_blocking(venv):
    """Ensure that Python is run synchronously with the args passed

    NB all we're doing here is checking that run_python hands off to
    Process.run with the correct parameters
    """
    command = venv.interpreter
    args = (uuid.uuid1().hex, uuid.uuid1().hex)
    with mock.patch.object(
        mu.virtual_environment.Process, "run_blocking"
    ) as mocked_run:
        venv.run_python(*args)
    mocked_run.assert_called_with(command, args)


def test_run_python_nonblocking(venv):
    """Ensure that Python is started asynchronously with the relevant params

    NB all we're doing here is checking that run_python hands off to
    Process.run with the correct parameters
    """
    command = venv.interpreter
    args = (uuid.uuid1().hex, uuid.uuid1().hex)
    with mock.patch.object(
        mu.virtual_environment.Process, "run"
    ) as mocked_run:
        venv.run_python(*args, slots=venv.Slots(output=lambda x: x))
    mocked_run.assert_called_with(command, args)


def test_reset_pip(venv, pipped):
    """Ensure that we're using a new Pip object for every invocation"""
    n_tries = random.randint(1, 5)
    for i in range(n_tries):
        venv.reset_pip()
    assert pipped.call_count == n_tries


def test_reset_pip_used(venv_dirpath):
    with mock.patch("mu.virtual_environment.Pip") as mock_pip:
        mock_pip.installed.return_value = []
        venv = mu.virtual_environment.VirtualEnvironment(venv_dirpath)
        with mock.patch.object(venv, "reset_pip") as mocked_reset:
            venv.relocate(".")
            venv.register_baseline_packages()
            venv.install_user_packages([])
            venv.remove_user_packages([])
            venv.installed_packages()

    assert mocked_reset.call_count == 5


#
# Quarantine
#
def test_quarantine_success(venv):
    """Check that when a venv is quarantined, an attempt is made to rename it"""
    with mock.patch.object(os, "rename") as mocked_rename:
        venv.quarantine_venv()

    assert mocked_rename.called
    args, kwargs = mocked_rename.call_args
    assert args[0] == venv.path


def test_quarantine_os_failure(venv):
    """Check that when a venv quarantine fails for OS reasons we carry on"""
    with mock.patch.object(os, "rename", side_effect=OSError()):
        venv.quarantine_venv()


def test_quarantine_other_failure(venv):
    """Check that when a venv quarantine fails for other reasons we
    let the exception raise"""

    class Error(Exception):
        pass

    with mock.patch.object(os, "rename", side_effect=Error):
        try:
            venv.quarantine_venv()
        except Exception as exc:
            assert isinstance(exc, Error)


#
# Recreate on version change
#
def test_recreate_on_version_change(venv):
    """Test that recreate is called when there is a mu version change"""
    mu_version = uuid.uuid1().hex
    settings = mu.settings.VirtualEnvironmentSettings()
    settings["mu_version"] = mu_version
    with mock.patch.object(venv, "settings", settings), mock.patch.object(
        venv, "recreate"
    ) as mocked_recreate, mock.patch.object(venv, "ensure"):
        venv.ensure_and_create()

    assert mocked_recreate.called


def test_no_recreate_on_same_version(venv):
    """Test that recreate is not called when there is no mu version change"""
    mu_version = mu.__version__
    settings = mu.settings.VirtualEnvironmentSettings()
    settings["mu_version"] = mu_version
    with mock.patch.object(venv, "settings", settings), mock.patch.object(
        venv, "recreate"
    ) as mocked_recreate, mock.patch.object(venv, "ensure"):
        venv.ensure_and_create()

    assert not mocked_recreate.called


def test_recreate_steps(venv):
    """Test that, if a recreate is invoked, it carries out the expected steps:

    * Track installed user packages
    * Quarantine existing venv
    * Relocate to new paths
    * Create a new path
    * Reinstall user packages
    """
    user_packages = [uuid.uuid1().hex, uuid.uuid1().hex]
    mu_version = uuid.uuid1().hex
    settings = mu.settings.VirtualEnvironmentSettings()
    settings["mu_version"] = mu_version

    with mock.patch.object(venv, "settings", settings), mock.patch.object(
        venv, "quarantine_venv"
    ) as mocked_quarantine_venv, mock.patch.object(
        venv, "installed_packages", return_value=(None, user_packages)
    ) as mocked_installed_packages, mock.patch.object(
        venv, "relocate"
    ) as mocked_relocate, mock.patch.object(
        venv, "create"
    ) as mocked_create, mock.patch.object(
        venv, "install_user_packages"
    ) as mocked_install_user_packages, mock.patch.object(
        venv, "ensure"
    ):
        venv.ensure_and_create()

    assert mocked_installed_packages.called
    assert mocked_quarantine_venv.called
    assert mocked_relocate.called
    assert mocked_create.called
    mocked_install_user_packages.assert_called_with(user_packages)


#
# There are two places we return the outputs from subprocesses
# decoded to utf-8 with errors replaced by the unicode "unknown" character:
# The result of Process.wait (which can be invoked via .run_blocking); and
# the result of VirtualEnvironment.run_subprocess
#
def test_subprocess_run_invalid_utf8(venv):
    """Ensure that if the output of a run_subprocess call is not valid UTF-8 we
    carry on as best we can"""
    corrupted_utf8 = b"\xc2\x00\xa3"
    expected_output = "\ufffd\x00\ufffd"
    mocked_run_return = mock.Mock(stdout=corrupted_utf8, stderr=b"")
    with mock.patch.object(subprocess, "run", return_value=mocked_run_return):
        _, output = venv.run_subprocess("")

    assert output == expected_output
