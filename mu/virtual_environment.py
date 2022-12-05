import os
import sys
from collections import namedtuple
import functools
import glob
import logging
import subprocess
import tempfile
import time
import zipfile

try:
    import win32api
except ImportError:
    pass

from PyQt5.QtCore import (
    QObject,
    QProcess,
    pyqtSignal,
    QTimer,
    QProcessEnvironment,
)

from . import wheels
from . import settings
from . import config
from . import __version__ as mu_version

wheels_dirpath = os.path.dirname(wheels.__file__)

logger = logging.getLogger(__name__)

ENCODING = sys.stdout.encoding if hasattr(sys.stdout, "encoding") else "utf-8"


def safe_short_path(path):
    """On Windows it converts a path to a short path with 8.3 representation.

    This is to avoid an issue encountered on Windows were launching a virtual
    environment python/pip process results in a 101 error exit code.

    More info:
    - https://github.com/mu-editor/mu/issues/1926
    - https://bugs.python.org/issue46686
    - https://github.com/python/cpython/issues/90844
    """
    if sys.platform != "win32":
        return path
    try:
        return win32api.GetShortPathName(path)
    except Exception:
        return path


class VirtualEnvironmentError(Exception):
    def __init__(self, message):
        self.message = message


class VirtualEnvironmentEnsureError(VirtualEnvironmentError):
    pass


class VirtualEnvironmentCreateError(VirtualEnvironmentError):
    pass


def compact(text):
    """Remove double line spaces and anything else which might help"""
    compacted = "\n".join(line for line in text.splitlines() if line.strip())
    return compacted or "No output received."


class Process(QObject):
    """
    Use the QProcess mechanism to run a subprocess asynchronously

    This will interact well with Qt Gui objects, eg by connecting the
    `output` signals to an `QTextEdit.append` method and the `started`
    and `finished` signals to a `QPushButton.setEnabled`.

    eg::
        import sys
        from PyQt5.QtCore import *
        from PyQt5.QtWidgets import *

        class Example(QMainWindow):

            def __init__(self):
                super().__init__()
                textEdit = QTextEdit()

                self.setCentralWidget(textEdit)
                self.setGeometry(300, 300, 350, 250)
                self.setWindowTitle('Main window')
                self.show()

                self.process = Process()
                self.process.output.connect(textEdit.append)
                self.process.run(sys.executable, ["-u", "-m", "pip", "list"])

        def main():
            app = QApplication(sys.argv)
            ex = Example()
            sys.exit(app.exec_())
    """

    started = pyqtSignal()
    output = pyqtSignal(str)
    finished = pyqtSignal()
    Slots = namedtuple("Slots", ["started", "output", "finished"])
    Slots.__new__.__defaults__ = (None, None, None)

    def __init__(self):
        super().__init__()
        #
        # Always run unbuffered and with UTF-8 IO encoding
        #
        self.environment = QProcessEnvironment.systemEnvironment()
        self.environment.insert("PYTHONUNBUFFERED", "1")
        self.environment.insert("PYTHONIOENCODING", "utf-8")

    def _set_up_run(self, **envvars):
        """Set up common elements of a QProcess run"""
        self.process = QProcess()
        environment = QProcessEnvironment(self.environment)
        for k, v in envvars.items():
            environment.insert(k, v)
        self.process.setProcessEnvironment(environment)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

    def run_blocking(self, command, args, wait_for_s=30.0, **envvars):
        """Run `command` with `args` via QProcess, passing `envvars` as
        environment variables for the process.

        Wait `wait_for_s` seconds for completion and return any stdout/stderr
        """
        logger.info(
            "About to run blocking %s with args %s and envvars %s",
            command,
            args,
            envvars,
        )
        self._set_up_run(**envvars)
        self.process.start(command, args)
        return self.wait(wait_for_s=wait_for_s)

    def run(self, command, args, **envvars):
        """Run `command` asynchronously with `args` via QProcess, passing `envvars`
        as environment variables for the process."""
        logger.info(
            "About to run %s with args %s and envvars %s",
            command,
            args,
            envvars,
        )
        self._set_up_run(**envvars)
        self.process.readyRead.connect(self._readyRead)
        self.process.started.connect(self._started)
        self.process.finished.connect(self._finished)
        partial = functools.partial(self.process.start, command, args)
        QTimer.singleShot(1, partial)

    def wait(self, wait_for_s=30):
        """Wait for the process to complete, optionally timing out.
        Return any stdout/stderr.

        If the process fails to complete in time or returns an error, raise a
        VirtualEnvironmentError
        """
        finished = self.process.waitForFinished(int(1000 * wait_for_s))
        exit_status = self.process.exitStatus()
        exit_code = self.process.exitCode()
        output = self.data()
        #
        # if waitForFinished completes, either the process has successfully finished
        # or it crashed, was terminated or timed out. If it does finish successfully
        # we might still have an error code. In each case we might still have data
        # from stdout/stderr. Unfortunately there's no way to determine that the
        # process was timed out, as opposed to crashing in some other way
        #
        # The three elements in play are:
        #
        # finished (yes/no)
        # exitStatus (normal (0) / crashed (1)) -- we don't currently distinguish
        # exitCode (whatever the program returns; conventionally 0 => ok)
        #
        logger.debug(
            "Finished: %s; exitStatus %s; exitCode %s",
            finished,
            exit_status,
            exit_code,
        )

        #
        # Exceptions raised here will be caught by the crash-handler which will try to
        # generate a URI out of it. There's an upper limit on URI size of ~2000
        #
        if not finished:
            logger.error(compact(output))
            raise VirtualEnvironmentError(
                "Process did not terminate normally:\n" + compact(output)
            )

        if exit_code != 0:
            #
            # We finished normally but we might still have an error-code on finish
            #
            logger.error(compact(output))
            raise VirtualEnvironmentError(
                "Process finished but with error code %d:\n%s"
                % (exit_code, compact(output))
            )

        return output

    def data(self):
        """Return all the data from the running process, converted to unicode"""
        output = self.process.readAll().data()
        return output.decode(ENCODING, errors="replace")

    def _started(self):
        self.started.emit()

    def _readyRead(self):
        self.output.emit(self.data().strip())

    def _finished(self):
        self.finished.emit()


class Pip(object):
    """
    Proxy for various pip commands

    While this is a fairly useful abstraction in its own right, it's at
    least initially to assist in testing, so we can mock out various
    commands
    """

    def __init__(self, pip_executable):
        self.executable = pip_executable
        self.process = Process()

    def run(
        self, command, *args, wait_for_s=120.0, slots=Process.Slots(), **kwargs
    ):
        """
        Run a command with args, treating kwargs as Posix switches.

        eg run("python", version=True)
        run("python", "-c", "import sys; print(sys.executable)")
        """
        #
        # Any keyword args are treated as command-line switches
        # As a special case, a boolean value indicates that the flag
        # is a yes/no switch
        #
        params = [command, "--disable-pip-version-check"]
        for k, v in kwargs.items():
            switch = k.replace("_", "-")
            if v is False:
                switch = "no-" + switch
            params.append("--" + switch)
            if v is not True and v is not False:
                params.append(str(v))
        params.extend(args)

        if slots.output is None:
            result = self.process.run_blocking(
                self.executable, params, wait_for_s=wait_for_s
            )
            logger.debug("Process output: %s", compact(result.strip()))
            return result
        else:
            if slots.started:
                self.process.started.connect(slots.started)
            self.process.output.connect(slots.output)
            if slots.finished:
                self.process.finished.connect(slots.finished)
            self.process.run(self.executable, params)

    def install(self, packages, slots=Process.Slots(), **kwargs):
        """
        Use pip to install a package or packages.

        If the first parameter is a string one package is installed; otherwise
        it is assumed to be an iterable of package names.

        Any kwargs are passed as command-line switches. A value of None
        indicates a switch without a value (eg --upgrade)
        """
        if isinstance(packages, str):
            return self.run(
                "install", packages, wait_for_s=180.0, slots=slots, **kwargs
            )
        else:
            return self.run(
                "install", *packages, wait_for_s=180.0, slots=slots, **kwargs
            )

    def uninstall(self, packages, slots=Process.Slots(), **kwargs):
        """
        Use pip to uninstall a package or packages

        If the first parameter is a string one package is uninstalled;
        otherwise it is assumed to be an iterable of package names.

        Any kwargs are passed as command-line switches. A value of None
        indicates a switch without a value (eg --upgrade)
        """
        if isinstance(packages, str):
            return self.run(
                "uninstall",
                packages,
                wait_for_s=180.0,
                slots=slots,
                yes=True,
                **kwargs
            )
        else:
            return self.run(
                "uninstall",
                *packages,
                wait_for_s=180.0,
                slots=slots,
                yes=True,
                **kwargs
            )

    def version(self):
        """
        Get the pip version

        NB this is fairly trivial but is pulled out principally for
        testing purposes
        """
        return self.run("--version")

    def freeze(self):
        """
        Use pip to return a list of installed packages

        NB this is fairly trivial but is pulled out principally for
        testing purposes
        """
        return self.run("freeze")

    def list(self):
        """
        Use pip to return a list of installed packages

        NB this is fairly trivial but is pulled out principally for
        testing purposes
        """
        return self.run("list")

    def installed(self):
        """
        Yield tuples of (package_name, version)

        pip list gives a more consistent view of name/version
        than pip freeze which uses different annotations for
        file-installed wheels and editable (-e) installs
        """
        lines = self.list().splitlines()
        iterlines = iter(lines)
        #
        # The first two lines are headers
        #
        try:
            next(iterlines)
            next(iterlines)
        #
        # cf https://lgtm.com/rules/11000086/
        #
        except StopIteration:
            raise VirtualEnvironmentError("Unable to parse installed packages")

        for line in iterlines:
            #
            # Some lines have a third location element
            #
            name, version = line.split()[:2]
            yield name, version


class SplashLogHandler(logging.NullHandler):
    """
    A simple log handler that does only one thing: use the referenced Qt signal
    to emit the log.
    """

    def __init__(self, emitter):
        """
        Returns an instance of the class that will use the Qt signal passed in
        as emitter.
        """
        super().__init__()
        self.setLevel(logging.DEBUG)
        self.emitter = emitter

    def emit(self, record):
        """
        Emits a record via the Qt signal.
        """
        messages = record.getMessage().splitlines()
        for msg in messages:
            output = "[{level}] - {message}".format(
                level=record.levelname, message=msg
            )
            self.emitter.emit(output)

    def handle(self, record):
        """
        Handles the log record.
        """
        self.emit(record)


class VirtualEnvironment(object):
    """
    Represents and contains methods for manipulating a virtual environment.
    """

    Slots = Process.Slots

    def __init__(self, dirpath=None):
        self.process = Process()
        self._is_windows = sys.platform == "win32"
        self._bin_extension = ".exe" if self._is_windows else ""
        self.settings = settings.VirtualEnvironmentSettings()
        self.settings.init()
        dirpath_to_use = (
            dirpath or self.settings.get("dirpath") or self._generate_dirpath()
        )
        logger.info("Using dirpath: %s", dirpath_to_use)
        self.relocate(dirpath_to_use)

    def __str__(self):
        return "<%s at %s>" % (self.__class__.__name__, self.path)

    @staticmethod
    def _generate_dirpath():
        """
        Construct a unique virtual environment folder name

        To avoid clashing with previously-created virtual environments,
        construct one which includes the Python version and a timestamp
        """
        return "%s-%s-%s" % (
            config.VENV_DIR,
            "%s%s" % sys.version_info[:2],
            time.strftime("%Y%m%d-%H%M%S"),
        )

    def run_subprocess(self, *args, **kwargs):
        """Quick wrapper to run a subprocess and log the output

        Return True if the process succeeded, False otherwise
        """
        logger.info("Running %s with kwargs %s", args, kwargs)
        process = subprocess.run(
            list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **kwargs
        )
        stdout_output = process.stdout.decode(ENCODING, errors="replace")
        stderr_output = process.stderr.decode(ENCODING, errors="replace")
        output = stdout_output
        if stderr_output:
            output += "\n\nSTDERR: " + stderr_output
        logger.debug(
            "Process returned %d; output: %s",
            process.returncode,
            compact(output),
        )
        return process.returncode == 0, output

    def reset_pip(self):
        """To avoid a problem where the same Pip process is executed by different
        threads, recreate the Pip process on demand
        """
        self.pip = Pip(self.pip_executable)

    def relocate(self, dirpath):
        """
        Relocate sets up variables for, eg, the expected location and name of
        the Python and Pip binaries, but doesn't access the file system. That's
        done by code in or called from `create`
        """
        logger.debug("Relocating to %s", dirpath)
        self.path = str(dirpath)
        self.name = os.path.basename(self.path)
        self._bin_directory = os.path.join(
            self.path, "scripts" if self._is_windows else "bin"
        )
        #
        # Pip and the interpreter will be set up when the virtualenv is created
        #
        self.interpreter = os.path.join(
            self._bin_directory, "python" + self._bin_extension
        )
        self.pip_executable = os.path.join(
            self._bin_directory, "pip" + self._bin_extension
        )
        self.reset_pip()
        logger.debug(
            "Virtual environment set up %s at %s", self.name, self.path
        )
        self.settings["dirpath"] = self.path

    def run_python(self, *args, slots=Process.Slots()):
        """
        Run the referenced Python interpreter with the passed in args

        If slots are supplied for the starting, output or finished signals
        they will be used; otherwise it will be assume that this running
        headless and the process will be run synchronously and output collected
        will be returned when the process is complete
        """
        if slots.output:
            if slots.started:
                self.process.started.connect(slots.started)
            self.process.output.connect(slots.output)
            if slots.finished:
                self.process.finished.connect(slots.finished)
            self.process.run(self.interpreter, args)
            return self.process
        else:
            output = self.process.run_blocking(self.interpreter, args)
            logger.debug("Python output: %s", output.strip())
            return output

    def _directory_is_venv(self):
        """
        Determine whether a directory appears to be an existing venv

        There appears to be no canonical way to achieve this. Often the
        presence of a pyvenv.cfg file is enough, but this isn't always there.
        Specifically, on debian it's not when created by virtualenv. So we
        fall back to finding an executable python command where we expect
        """
        if os.path.isfile(os.path.join(self.path, "pyvenv.cfg")):
            return True

        #
        # On windows os.access X_OK is close to meaningless, but it will
        # succeed for executable files (and everything else). On Posix it
        # does distinguish executable files
        #
        if os.access(self.interpreter, os.X_OK):
            return True

        return False

    def quarantine_venv(self, reason="FAILED"):
        """Rename an existing virtual environment folder out of the way to make
        it clearer which is the current one.

        NB if this fails (eg because of file locking) it won't matter: the folder
        will not be used and will simply be a little distracting
        """
        error_dirpath = self.path + "." + reason
        try:
            os.rename(self.path, error_dirpath)
        except OSError:
            logger.exception(
                "Unable to quarantine %s as %s", self.path, error_dirpath
            )
        else:
            logger.info("Quarantined %s as %s", self.path, error_dirpath)

    def recreate(self):
        """Recreate this virtual environment with updated baseline packages and the
        same user packages

        The intended use is when the Mu version changes as this can bring with it
        additional and/or updated packages. The simplest thing to do is to switch
        to a new venv and then pull in the packages the user had additionally installed
        """
        #
        # Keep track of the user packages installed into the current venv
        #
        _, user_packages = self.installed_packages()

        #
        # Now, quarantine the current venv with
        # a marker to say it's been superseded
        #
        self.quarantine_venv(reason="SUPERSEDED")

        #
        # Create a new venv which will then become the current one.
        # Install the (possibly updated) baseline packages
        #
        self.relocate(self._generate_dirpath())
        self.create()

        #
        # Now reinstall the original user packages
        #
        if user_packages:
            logger.debug("About to reinstall user packages: %s", user_packages)
            self.install_user_packages(user_packages)

    def ensure_and_create(self, emitter=None):
        """Check whether we have a valid virtual environment in place and, if not,
        create a new one. Allow a couple of tries in case we have temporary glitches
        around the network, file contention etc.
        """
        splash_handler = None
        if emitter:
            splash_handler = SplashLogHandler(emitter)
            splash_handler.setLevel(logging.INFO)
            logger.addHandler(splash_handler)
            logger.info("Added log handler.")

        n_tries = 2
        n = 1
        #
        # First time around we'll have a path with nothing in it
        # Jump straight to creation and let the ensure take over afterwards
        # For the happy path we'll get a clean creation and a clean ensure
        #
        try_to_create = not os.path.exists(self.path)
        while True:
            logger.debug("Checking virtual environment; attempt #%d.", n)
            try:
                #
                # try_to_create will be True if this is a brand new install
                # or if we've failed to ensure at least once
                #
                if try_to_create:
                    self.create()
                    try_to_create = False

                #
                # Otherwise check whether the venv settings match the version of Mu
                # If not, recreate the venv with updated baseline packages and
                # the existing user packages
                #
                else:
                    venv_mu_version = self.settings.get(
                        "mu_version", "-no-version-"
                    )
                    if venv_mu_version != mu_version:
                        logger.warning(
                            "Venv created by Mu version %s; Current Mu is version %s",
                            venv_mu_version,
                            mu_version,
                        )
                        self.recreate()

                #
                # In any situation (initial creation, recreation after Mu update,
                # regular run) ensure that the venv is still valid
                #
                self.ensure()
                logger.info("Valid virtual environment found at %s", self.path)

                #
                # If we reach this point, ensure hasn't raised an exception and
                # we're good to save settings and move on
                #
                self.settings.save()
                break

            except VirtualEnvironmentError as exc:
                #
                # If any of the ensure/create steps cause a VirtualEnvironmentError
                # retry up to a maximum number in case we've just been unlucky
                # with network, file contention etc.
                #
                logger.error(exc.message)
                self.quarantine_venv()
                if n < n_tries:
                    self.relocate(self._generate_dirpath())
                    try_to_create = True
                    n += 1
                else:
                    raise
            finally:
                if emitter and splash_handler:
                    logger.removeHandler(splash_handler)

    def ensure(self):
        """
        Ensure that virtual environment exists and is in a good state.

        If any of these fails, they should raise a (subclass of)
        VirtualEnvironmentError which will bubble up to `ensure_and_create` and be
        caught and acted on appropriately
        """
        self.ensure_path()
        self.ensure_interpreter()
        self.ensure_interpreter_version()
        self.ensure_pip()
        self.ensure_key_modules()

    def ensure_path(self):
        """
        Ensure that the virtual environment path exists and is a valid venv.
        """
        if not os.path.exists(self.path):
            raise VirtualEnvironmentEnsureError(
                "%s does not exist." % self.path
            )
        elif not os.path.isdir(self.path):
            raise VirtualEnvironmentEnsureError(
                "%s exists but is not a directory." % self.path
            )
        elif not self._directory_is_venv():
            raise VirtualEnvironmentEnsureError(
                "Directory %s exists but is not a venv." % self.path
            )
        logger.info("Virtual Environment found at: %s", self.path)

    def ensure_interpreter(self):
        """
        Ensure there is an interpreter of the expected name at the expected
        location, given the platform and naming conventions.

        NB if the interpreter is present as a symlink to a system interpreter
        (likely for a venv) but the link is broken, then os.path.isfile will
        fail as though the file wasn't there. Which is what we want in these
        circumstances.
        """
        if os.path.isfile(self.interpreter):
            logger.info("Interpreter found at: %s", self.interpreter)
        elif os.environ.get("APPDIR") and os.environ.get("APPIMAGE"):
            # When packaged as a Linux AppImage, Mu Editor is mounted
            # on a random(ish) path each time it runs. This breaks the
            # existing venv: its interpreter symlinks to a path that
            # likely no longer exists. Fix that by re-symlinking to
            # the current and now valid interpreter path.
            # PS: This is a horrible hack and it seems to work! :)
            logger.info("No interpreter found at: %s", self.interpreter)
            try:
                os.unlink(self.interpreter)
            except OSError as exc:
                logger.warning(
                    "Unlinking %s failed: %s. Moving on.",
                    self.interpreter,
                    exc,
                )
            os.symlink(sys.executable, self.interpreter)
            logger.info(
                "Symlinked %s to AppImage's %s",
                self.interpreter,
                sys.executable,
            )
        else:
            raise VirtualEnvironmentEnsureError(
                "Interpreter not found where expected at: %s"
                % self.interpreter
            )

    def ensure_interpreter_version(self):
        """
        Ensure that the venv interpreter matches the version of Python running
        Mu.

        This is necessary because otherwise we'll have mismatched wheels etc.
        """
        current_version = "%s%s" % sys.version_info[:2]
        #
        # Can't use self.run_python as we're not yet within the Qt UI loop
        #
        ok, output = self.run_subprocess(
            self.interpreter,
            "-c",
            'import sys; print("%s%s" % sys.version_info[:2])',
            shell=True if self._is_windows else False,
        )
        if not ok:
            raise VirtualEnvironmentEnsureError(
                "Failed to run venv interpreter %s\n%s"
                % (self.interpreter, compact(output))
            )

        venv_version = output.strip()
        if current_version == venv_version:
            logger.info("Both interpreters at version %s", current_version)
        else:
            raise VirtualEnvironmentEnsureError(
                "Mu interpreter at version %s; venv interpreter at version %s."
                % (current_version, venv_version)
            )

    def ensure_key_modules(self):
        """
        Ensure that the venv interpreter is able to load key modules.
        """
        for module, *_ in wheels.mode_packages:
            logger.debug("Verifying import of: %s", module)
            ok, output = self.run_subprocess(
                self.interpreter,
                "-c",
                "import %s" % module,
                shell=True if self._is_windows else False,
            )
            if not ok:
                raise VirtualEnvironmentEnsureError(
                    "Failed to import: %s\n%s" % (module, compact(output))
                )

    def ensure_pip(self):
        """
        Ensure that pip is available.
        """
        if os.path.isfile(self.pip_executable):
            logger.info("Pip found at: %s", self.pip_executable)
        else:
            raise VirtualEnvironmentEnsureError(
                "Pip not found where expected at: %s" % self.pip_executable
            )

    def create(self):
        """Create a new virtualenv and install baseline packages & kernel

        If a failure occurs, attempt to move the failed attempt out of the way
        before re-raising the error.
        """
        self.create_venv()
        self.install_baseline_packages()
        self.register_baseline_packages()
        self.install_jupyter_kernel()
        self.settings["mu_version"] = mu_version

    def create_venv(self):
        """
        Create a new virtualenv
        """
        logger.info("Creating virtualenv: {}".format(self.path))
        logger.info("Virtualenv name: {}".format(self.name))

        env = dict(os.environ)
        args = filter(
            None,
            (
                safe_short_path(sys.executable),
                "-I",
                "-m",
                "virtualenv",
                "-p",
                safe_short_path(sys.executable),
                "-q",
                "" if self._is_windows else "--symlinks",
                self.path,
            ),
        )
        ok, output = self.run_subprocess(*args, env=env)
        if ok:
            logger.info(
                "Created virtual environment using %s at %s",
                safe_short_path(sys.executable),
                self.path,
            )
        else:
            raise VirtualEnvironmentCreateError(
                "Unable to create a virtual environment using %s at %s\n%s"
                % (safe_short_path(sys.executable), self.path, compact(output))
            )

    def install_jupyter_kernel(self):
        """
        Install a Jupyter kernel for Mu (the name of the kernel indicates this
        is a Mu-related kernel).
        """
        kernel_name = self.name.replace(" ", "-")
        display_name = '"Python/Mu ({})"'.format(kernel_name)
        logger.info("Installing Jupyter Kernel: %s", kernel_name)
        ok, output = self.run_subprocess(
            safe_short_path(sys.executable),
            "-I",
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            kernel_name,
            "--display-name",
            display_name,
        )
        if ok:
            logger.info("Installed Jupyter Kernel: %s", kernel_name)
        else:
            raise VirtualEnvironmentCreateError(
                "Unable to install kernel\n%s" % compact(output)
            )

    def install_from_zipped_wheels(self, zipped_wheels_filepath):
        """Take a zip containing wheels, unzip it and install the wheels into
        the current virtualenv
        """
        with tempfile.TemporaryDirectory() as unpacked_wheels_dirpath:
            #
            # The wheel files are shipped in Mu-version-specific zip files to avoid
            # cross-contamination when a Mu version change happens and we still have
            # wheels from the previous installation.
            #
            with zipfile.ZipFile(zipped_wheels_filepath) as zip:
                zip.extractall(unpacked_wheels_dirpath)

            self.reset_pip()
            #
            # The wheels are installed one at a time as they reduces the possibility
            # of the process installing them breaching its timeout
            #
            for wheel in glob.glob(
                os.path.join(unpacked_wheels_dirpath, "*.whl")
            ):
                logger.info(
                    "About to install from wheel: {}".format(
                        os.path.basename(wheel)
                    )
                )
                self.pip.install(wheel, deps=False, index=False)

    def install_baseline_packages(self):
        """
        Install all packages needed for non-core activity.

        Each mode needs one or more packages to be able to run: pygame zero
        mode needs pgzero and its dependencies; web mode needs Flask and so on.
        We intend to ship with all the necessary wheels for those packages so
        no network access is needed. But if the wheels aren't found, because
        we're not running from an installer, then just pip install in the
        usual way.
        """
        logger.info("Installing baseline packages.")
        logger.info("pip version: %s", compact(self.pip.version()))
        #
        # TODO: Add semver check to ensure filepath is safe
        #
        zipped_wheels_filepath = os.path.join(
            wheels_dirpath, "%s.zip" % mu_version
        )
        logger.info("Expecting zipped wheels at %s", zipped_wheels_filepath)
        if not os.path.exists(zipped_wheels_filepath):
            logger.warning("No zipped wheels found; downloading...")
            wheels.download(zipped_wheels_filepath, logger)

        self.install_from_zipped_wheels(zipped_wheels_filepath)

    def register_baseline_packages(self):
        """
        Keep track of the baseline packages installed into the empty venv.
        """
        self.reset_pip()
        packages = list(self.pip.installed())
        self.settings["baseline_packages"] = packages

    def baseline_packages(self):
        """
        Return the list of baseline packages.
        """
        return self.settings.get("baseline_packages")

    def install_user_packages(self, packages, slots=Process.Slots()):
        """
        Install user defined packages.
        """
        logger.info("Installing user packages: %s", ", ".join(packages))
        self.reset_pip()
        self.pip.install(packages, slots=slots, upgrade=True)

    def remove_user_packages(self, packages, slots=Process.Slots()):
        """
        Remove user defined packages.
        """
        logger.info("Removing user packages: %s", ", ".join(packages))
        self.reset_pip()
        self.pip.uninstall(packages, slots=slots)

    def installed_packages(self):
        """
        List all the third party modules installed by the user in the venv
        containing the referenced Python interpreter.
        """
        logger.info("Discovering installed third party modules in venv.")
        baseline_packages = [
            name for name, version in self.baseline_packages()
        ]
        user_packages = []
        self.reset_pip()
        for package, version in self.pip.installed():
            if package not in baseline_packages:
                user_packages.append(package)
        logger.info(user_packages)

        return baseline_packages, user_packages


#
# Create a singleton virtual environment to be used throughout
# the application
#
venv = VirtualEnvironment()
