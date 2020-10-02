import os
import sys
import functools
import glob
import json
import logging
import subprocess

import encodings
python36_zip = os.path.dirname(encodings.__path__[0])
del encodings

from PyQt5.QtCore import QObject, QProcess, QThread, pyqtSignal, QTimer, QProcessEnvironment

from . import wheels

wheels_dirpath = os.path.dirname(wheels.__file__)

logger = logging.getLogger(__name__)

class Process(QObject):
    """Use the QProcess mechanism to run a subprocess asynchronously

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

    def __init__(self):
        super().__init__()
        #
        # Always run unbuffered and with UTF-8 IO encoding
        #
        self.environment = QProcessEnvironment.systemEnvironment()
        self.environment.insert("PYTHONUNBUFFERED", "1")
        self.environment.insert("PYTHONIOENCODING", "utf-8")

    def _set_up_run(self, **envvars):
        """Run the process with the command and args
        """
        self.process = QProcess(self)
        environment = QProcessEnvironment(self.environment)
        for k, v in envvars.items():
            environment.insert(k, v)
        self.process.setProcessEnvironment(environment)
        self.process.setProcessChannelMode(QProcess.MergedChannels)

    def run_headless(self, command, args, **envvars):
        self._set_up_run(**envvars)
        self.process.start(command, args)
        self.wait()
        return self.data()

    def run(self, command, args, **envvars):
        self._set_up_run(**envvars)
        self.process.readyRead.connect(self._readyRead)
        self.process.started.connect(self._started)
        self.process.finished.connect(self._finished)
        QTimer.singleShot(100, functools.partial(self.process.start, command, args))

    def wait(self, wait_for_s=30.0):
        if not self.process.waitForFinished(1000 * wait_for_s):
            raise RuntimeError("Some error occurred")

    def data(self):
        return self.process.readAll().data().decode("utf-8")

    def _started(self):
        self.started.emit()

    def _readyRead(self):
        self.output.emit(self.data().strip())

    def _finished(self):
        self.finished.emit()


class Pip(object):
    """Proxy for various pip commands

    While this is a fairly useful abstraction in its own right, it's at
    least initially to assist in testing, so we can mock out various
    commands
    """
    def __init__(self, pip_executable):
        self.executable = pip_executable
        self.process = Process()

    def run(self, command, *args, started_slot=None, output_slot=None, finished_slot=None, **kwargs):
        """Run a command with args, treating kwargs as Posix switches

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

        if output_slot is None:
            return self.process.run_headless(self.executable, params)
        else:
            if started_slot: self.process.started.connect(started_slot)
            self.process.output.connect(output_slot)
            if finished_slot: self.process.finished.connect(finished_slot)
            self.process.run(self.executable, params)

    def install(self, packages, started_slot=None, output_slot=None, finished_slot=None, **kwargs):
        """Use pip to install a package or packages

        If the first parameter is a string one package is installed; otherwise
        it is assumed to be an iterable of package names.

        Any kwargs are passed as command-line switches. A value of None
        indicates a switch without a value (eg --upgrade)
        """
        if isinstance(packages, str):
            return self.run("install", packages, started_slot=started_slot, output_slot=output_slot, finished_slot=finished_slot, **kwargs)
        else:
            return self.run("install", *packages, started_slot=started_slot, output_slot=output_slot, finished_slot=finished_slot, **kwargs)

    def uninstall(self, packages, started_slot=None, output_slot=None, finished_slot=None, **kwargs):
        """Use pip to uninstall a package or packages

        If the first parameter is a string one package is uninstalled; otherwise
        it is assumed to be an iterable of package names.

        Any kwargs are passed as command-line switches. A value of None
        indicates a switch without a value (eg --upgrade)
        """
        if isinstance(packages, str):
            return self.run("uninstall", packages, started_slot=started_slot, output_slot=output_slot, finished_slot=finished_slot, yes=True, **kwargs)
        else:
            return self.run("uninstall", *packages, started_slot=started_slot, output_slot=output_slot, finished_slot=finished_slot, yes=True, **kwargs)

    def freeze(self):
        """Use pip to return a list of installed packages

        NB this is fairly trivial but is pulled out principally for
        testing purposes
        """
        return self.run("freeze")

    def list(self):
        """Use pip to return a list of installed packages

        NB this is fairly trivial but is pulled out principally for
        testing purposes
        """
        return self.run("list")

    def installed_packages(self):
        """Yield tuples of (package_name, version)

        pip list gives a more consistent view of name/version
        than pip freeze which uses different annotations for
        file-installed wheels and editable (-e) installs
        """
        lines = self.list().splitlines()
        iterlines = iter(lines)
        #
        # The first two lines are headers
        #
        next(iterlines)
        next(iterlines)
        for line in iterlines:
            #
            # Some lines have a third location element
            #
            name, version = line.split()[:2]
            yield name, version

class VirtualEnvironment(object):

    BASELINE_PACKAGES_FILEPATH = "baseline_packages.json"

    def __init__(self, dirpath):
        self.path = dirpath
        self.name = os.path.basename(self.path)
        self._is_windows = sys.platform == "win32"
        self._bin_directory = os.path.join(self.path, "scripts" if self._is_windows else "bin")
        self._bin_extension = ".exe" if self._is_windows else ""
        #
        # Pip and the interpreter will be set up when the virtualenv is ensured
        #
        self.interpreter = os.path.join(self._bin_directory, "python" + self._bin_extension)
        self.pip = Pip(os.path.join(self._bin_directory, "pip" + self._bin_extension))
        self.process = Process()
        logging.debug(
            "Starting virtual environment %s at %s", self.name, self.path
        )

    def run_python(
        self, *args,
        started_slot=None, output_slot=None, finished_slot=None
    ): ## FIXME -- do we need pythonpath?, pythonpath=python36_zip):
        """Run the referenced Python interpreter with the passed in args

        If slots are supplied for the starting, output or finished signals
        they will be used; otherwise it will be assume that this running
        headless and the process will be run synchronously and output collected
        will be returned when the process is complete
        """
        #~ logger.info(
            #~ "Starting new sub-process with: {} {} (PYTHONPATH={})".format(
                #~ self.interpreter, args, pythonpath
            #~ )
        #~ )
        if started_slot:
            self.process.started.connect(started_slot)
        if output_slot:
            self.process.output.connect(output_slot)
        if finished_slot:
            self.process.finished.connect(finished_slot)

        if output_slot:
            self.process.run(self.interpreter, args)
        else:
            return self.process.run_headless(self.interpreter, args)


    def find_interpreter(self):
        #
        # This no longer has any real purpose but we're leaving it here
        # so as not to break too many things
        #
        pass

    def ensure(self):
        """Ensure that a virtual environment exists, creating it if needed"""
        if not os.path.exists(self.path):
            logger.debug("%s does not exist; creating", self.path)
            self.create()
        elif not os.path.isdir(self.path):
            message = "%s exists but is not a directory" % self.path
            logger.error(message)
            raise RuntimeError(message)

        #
        # There doesn't seem to be a canonical way of checking whether
        # a directory is a virtual environment
        #
        elif not os.path.isfile(os.path.join(self.path, "pyvenv.cfg")):
            message = "Directory %s exists but is not a venv" % self.path
            logger.error(message)
            raise RuntimeError(message)
        else:
            logger.debug("Directory %s already exists", self.path)

        if os.path.isfile(self.interpreter):
            logger.info("Interpreter found at %s", self.interpreter)
        else:
            message = (
                "No interpreter found where expected at %s" % self.interpreter
            )
            logger.error(message)
            raise RuntimeError(message)

        if os.path.isfile(self.pip.executable):
            logger.info("Pip found at %s", self.pip.executable)
        else:
            message = (
                "Pip not found where expected at %s" % self.pip.executable
            )
            logger.error(message)
            raise RuntimeError(message)

    def create(self):
        """
        Create a new virtualenv at the referenced path.
        """
        logger.info("Creating virtualenv: {}".format(self.path))
        logger.info("Virtualenv name: {}".format(self.name))

        env = dict(os.environ)
        subprocess.run(
            [sys.executable, "-m", "venv", self.path], check=True, env=env
        )
        # Set the path to the interpreter
        self.install_baseline_packages()
        self.register_baseline_packages()
        self.install_jupyter_kernel()

    def install_jupyter_kernel(self):
        logger.info("Installing Jupyter Kernel")
        return self.run_python(
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            self.name,
            "--display-name",
            '"Python/Mu ({})"'.format(self.name),
        )

    def install_baseline_packages(self):
        """Install all packages needed for non-core activity

        Each mode needs one or more packages to be able to run: pygame zero
        mode needs pgzero and its dependencies; web mode needs Flask and so on.
        We intend to ship with all the necessary wheels for those packages so
        no network access is needed. But if the wheels aren't found, because
        we're not running from an installer, then just pip install in the
        usual way.

        --upgrade is currently used with a thought to upgrade-releases of Mu
        """
        logger.info("Installing baseline packages")
        logger.info(
            "%s %s",
            wheels_dirpath,
            "exists" if os.path.isdir(wheels_dirpath) else "does not exist",
        )
        #
        # This command should install the baseline packages, picking up the
        # precompiled wheels from the wheels path
        #
        # For dev purposes (where we might not have the wheels) bomb
        # out if there are no wheels and suggest how to get them there...
        #
        wheel_filepaths = glob.glob(os.path.join(wheels_dirpath, "*.whl"))
        if not wheel_filepaths:
            raise RuntimeError(
                "No wheels in %s; try `python -mmu.wheels`" % wheels_dirpath
            )
        self.pip.install(wheel_filepaths)

    def register_baseline_packages(self):
        """Keep track of the baseline packages installed into the empty venv
        """
        #
        # FIXME: This should go into settings. For now, though, just put it somewhere
        #
        with open(self.BASELINE_PACKAGES_FILEPATH, "w", encoding="utf-8") as f:
            json.dump(list(self.pip.installed_packages()), f)

    def baseline_packages(self):
        """Return the list of baseline packages
        """
        #
        # FIXME: This should come out of settings. For now though...
        #
        with open(self.BASELINE_PACKAGES_FILEPATH, encoding="utf-8") as f:
            return json.load(f)

    def install_user_packages(self, packages, started_slot=None, output_slot=None, finished_slot=None):
        logger.info("Installing user packages: %s", ", ".join(packages))
        self.pip.install(packages, started_slot=started_slot, output_slot=output_slot, finished_slot=finished_slot, upgrade=True)

    def remove_user_packages(self, packages, started_slot=None, output_slot=None, finished_slot=None):
        logger.info("Removing user packages: %s", ", ".join(packages))
        self.pip.uninstall(packages, started_slot=started_slot, output_slot=output_slot, finished_slot=finished_slot)

    def full_pythonpath(self):
        """
        Given an interpreter from a virtualenv, returns a PYTHONPATH containing
        both the virtualenvs paths and then the paths from Mu's own sys.path.
        """
        #
        # FIXME: not sure where this is used; maybe only Kernel creation?
        #
        result = self.run_python(
            "-c", "import sys; print('\\n'.join(sys.path))"
        )
        #
        # Using list rather than set to preserve seach order
        #
        paths = []
        for p in [line.strip() for line in result.split("\n")]:
            if p not in paths:
                paths.append(p)
        for p in sys.path:
            if p not in paths:
                paths.append(p)
        return os.pathsep.join(paths)

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

        baseline_packages = [name for name, version in self.baseline_packages()]
        user_packages = []
        p = self.pip.installed_packages()
        for package, version in p: ## self.pip.installed_packages():
            logger.info(package)
            if package not in baseline_packages:
                user_packages.append(package)

        return baseline_packages, user_packages
