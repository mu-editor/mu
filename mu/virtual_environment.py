import os
import sys
import datetime
from collections import namedtuple
import functools
import glob
import logging
import subprocess
import time

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

wheels_dirpath = os.path.dirname(wheels.__file__)

logger = logging.getLogger(__name__)


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
        timestamp = datetime.datetime.fromtimestamp(record.created)
        messages = record.getMessage().splitlines()
        for msg in messages:
            output = "[{level}]({timestamp}) - {message}".format(
                level=record.levelname, timestamp=timestamp, message=msg
            )
            self.emitter.emit(output)

    def handle(self, record):
        """
        Handles the log record.
        """
        self.emit(record)


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
        """Run the process with the command and args"""
        self.process = QProcess()
        environment = QProcessEnvironment(self.environment)
        for k, v in envvars.items():
            environment.insert(k, v)
        self.process.setProcessEnvironment(environment)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

    def run_blocking(self, command, args, wait_for_s=30.0, **envvars):
        self._set_up_run(**envvars)
        self.process.start(command, args)
        self.wait(wait_for_s=wait_for_s)
        output = self.data()
        return output

    def run(self, command, args, **envvars):
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
        QTimer.singleShot(
            1,
            partial,
        )

    def wait(self, wait_for_s=30.0):
        finished = self.process.waitForFinished(1000 * wait_for_s)
        #
        # If finished is False, it could be be because of an error
        # or because we've already finished before starting to wait!
        #
        if (
            not finished
            and self.process.exitStatus() == self.process.CrashExit
        ):
            raise VirtualEnvironmentError("Some error occurred")

    def data(self):
        return self.process.readAll().data().decode("utf-8")

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
        self, command, *args, wait_for_s=30.0, slots=Process.Slots(), **kwargs
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


class VirtualEnvironmentError(Exception):
    pass


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
        Construct a unique virtual environment folder

        To avoid clashing with previously-created virtual environments,
        construct one which includes the Python version and a timestamp
        """
        return "%s-%s-%s" % (
            config.VENV_DIR,
            "%s%s" % sys.version_info[:2],
            time.strftime("%Y%m%d-%H%M%S"),
        )

    def reset_pip(self):
        self.pip = Pip(self.pip_executable)

    def relocate(self, dirpath):
        """
        Relocate sets up variables for, eg, the expected location and name of
        the Python and Pip binaries, but doesn't access the file system. That's
        done by code in or called from `create`
        """
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
            return self.process.run_blocking(self.interpreter, args)

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

    def ensure_and_create(self, emitter=None):
        """
        If an emitter is provided, this will be used by a custom log handler
        to display logging events onto a splash screen.
        """
        splash_handler = None
        if emitter:
            splash_handler = SplashLogHandler(emitter)
            logger.addHandler(splash_handler)
            logger.info("Added log handler.")
        n_retries = 3
        for n in range(n_retries):
            try:
                logger.debug(
                    "Checking virtual environment; attempt #%d.", 1 + n
                )
                self.ensure()
            except VirtualEnvironmentError:
                new_dirpath = self._generate_dirpath()
                logger.debug(
                    "Creating new virtual environment at %s.", new_dirpath
                )
                self.relocate(new_dirpath)
                self.create()
            else:
                logger.info("Virtual environment already exists.")
                return
        # If we get here, there's a problem creating the virtual environment,
        # so attempt to signal this via the logger, wait for the log to be
        # displayed in the splash screen and then exit via the exception.
        logger.error("Unable to create a working virtual environment.")
        if emitter and splash_handler:
            logger.removeHandler(splash_handler)
        raise VirtualEnvironmentError(
            "Unable to create a working virtual environment."
        )

    def ensure(self):
        """
        Ensure that virtual environment exists and is in a good state.
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
            message = "%s does not exist." % self.path
            logger.error(message)
            raise VirtualEnvironmentError(message)
        elif not os.path.isdir(self.path):
            message = "%s exists but is not a directory." % self.path
            logger.error(message)
            raise VirtualEnvironmentError(message)
        elif not self._directory_is_venv():
            message = "Directory %s exists but is not a venv." % self.path
            logger.error(message)
            raise VirtualEnvironmentError(message)
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
        else:
            message = (
                "Interpreter not found where expected at: %s"
                % self.interpreter
            )
            logger.error(message)
            raise VirtualEnvironmentError(message)

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
        process = subprocess.run(
            [
                self.interpreter,
                "-c",
                'import sys; print("%s%s" % sys.version_info[:2])',
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        venv_version = process.stdout.decode("utf-8").strip()
        if current_version == venv_version:
            logger.info("Both interpreters at version %s", current_version)
        else:
            message = (
                "Mu interpreter at version %s; venv interpreter at version %s."
                % (current_version, venv_version)
            )
            logger.error(message)
            raise VirtualEnvironmentError(message)

    def ensure_key_modules(self):
        """
        Ensure that the venv interpreter is able to load key modules.
        """
        for module, *_ in wheels.mode_packages:
            logger.debug("Verifying import of: %s", module)
            try:
                subprocess.run(
                    [self.interpreter, "-c", "import %s" % module],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True,
                )
            except subprocess.CalledProcessError:
                message = "Failed to import: %s" % module
                logger.error(message)
                raise VirtualEnvironmentError(message)

    def ensure_pip(self):
        """
        Ensure that pip is available.
        """
        if os.path.isfile(self.pip_executable):
            logger.info("Pip found at: %s", self.pip_executable)
        else:
            message = (
                "Pip not found where expected at: %s" % self.pip_executable
            )
            logger.error(message)
            raise VirtualEnvironmentError(message)

    def create(self):
        """
        Create a new virtualenv at the referenced path.
        """
        logger.info("Creating virtualenv: {}".format(self.path))
        logger.info("Virtualenv name: {}".format(self.name))

        env = dict(os.environ)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "virtualenv",
                "-p",
                sys.executable,
                "-q",
                self.path,
            ],
            check=True,
            env=env,
        )
        # Set the path to the interpreter
        self.install_baseline_packages()
        self.register_baseline_packages()
        self.install_jupyter_kernel()

    def install_jupyter_kernel(self):
        """
        Install a Jupyter kernel for Mu (the name of the kernel indicates this
        is a Mu related kernel).
        """
        kernel_name = '"Python/Mu ({})"'.format(self.name)
        logger.info("Installing Jupyter Kernel: %s", kernel_name)
        return self.run_python(
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            self.name,
            "--display-name",
            kernel_name,
        )

    def install_baseline_packages(self):
        """
        Install all packages needed for non-core activity.

        Each mode needs one or more packages to be able to run: pygame zero
        mode needs pgzero and its dependencies; web mode needs Flask and so on.
        We intend to ship with all the necessary wheels for those packages so
        no network access is needed. But if the wheels aren't found, because
        we're not running from an installer, then just pip install in the
        usual way.

        --upgrade is currently used with a thought to upgrade-releases of Mu.
        """
        logger.info("Installing baseline packages.")
        logger.info(
            "%s %s",
            wheels_dirpath,
            "exists" if os.path.isdir(wheels_dirpath) else "does not exist",
        )
        #
        # This command should install the baseline packages, picking up the
        # precompiled wheels from the wheels path
        #
        # For dev purposes (where we might not have the wheels) warn where
        # the wheels are not already present and download them
        #
        wheel_filepaths = glob.glob(os.path.join(wheels_dirpath, "*.whl"))
        if not wheel_filepaths:
            logger.warn(
                "No wheels found in %s; downloading...", wheels_dirpath
            )
            wheels.download()
            wheel_filepaths = glob.glob(os.path.join(wheels_dirpath, "*.whl"))

        if not wheel_filepaths:
            raise VirtualEnvironmentError(
                "No wheels in %s; try `python -mmu.wheels`" % wheels_dirpath
            )
        self.reset_pip()
        logger.debug(self.pip.install(wheel_filepaths))

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
        self.pip.install(
            packages,
            slots=slots,
            upgrade=True,
        )

    def remove_user_packages(self, packages, slots=Process.Slots()):
        """
        Remove user defined packages.
        """
        logger.info("Removing user packages: %s", ", ".join(packages))
        self.reset_pip()
        self.pip.uninstall(
            packages,
            slots=slots,
        )

    def installed_packages(self):
        """
        List all the third party modules installed by the user in the venv
        containing the referenced Python interpreter.
        """
        logger.info("Discovering installed third party modules in venv.")

        #
        # FIXME: Basically we need a way to distinguish between installed
        # baseline packages and user-added packages. The baseline_packages
        # in this class (or, later, from modes) are just the top-level classes:
        # flask, pgzero etc. But they bring in many others further down. So:
        # we either need to keep track of what's installed as part of the
        # baseline install; or to keep track of what's installed by users.
        # And then we have to hold those in the settings file
        # The latter is probably easier.
        #

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
