import os
import sys
import glob
import logging
import subprocess

from PyQt5.QtCore import QProcess, QProcessEnvironment

logger = logging.getLogger(__name__)


class VirtualEnvironment(object):

    #
    # FIXME: For now, hardcode the baseline packages here; later on, we
    # can probably have them exported by each mode
    #
    baseline_packages = [
        ("pgzero", ""),
        ("Flask", "==1.1.2"),
        ("pyserial", "==3.4"),
        ("qtconsole", "==4.7.4"),
        ("nudatus", ">=0.0.3"),
    ]

    def __init__(self, dirpath, baseline_wheels_dirpath):
        self.path = dirpath
        self.baseline_wheels_dirpath = baseline_wheels_dirpath
        self.name = os.path.basename(self.path)
        self.interpreter = None

    def run_python(self, *args, pythonpath=None):
        """
        Run the referenced Python interpreter with the passed in args and
        PYTHONPATH. This is a **BLOCKING** call to the subprocess and should
        only be used for quick Python commands needed for pip, venv and other
        related tasks to work.
        """
        logger.info(
            "Starting new sub-process with: {} {} (PYTHONPATH={})".format(
                self.interpreter, args, pythonpath
            )
        )
        process = QProcess()
        process.setProcessChannelMode(QProcess.MergedChannels)
        env = QProcessEnvironment.systemEnvironment()
        env.insert("PYTHONUNBUFFERED", "1")
        env.insert("PYTHONIOENCODING", "utf-8")
        if pythonpath:
            env.insert("PYTHONPATH", pythonpath)
        else:
            env.remove("PYTHONPATH")
        process.setProcessEnvironment(env)
        process.start(self.interpreter, args)
        if not process.waitForStarted():
            raise RuntimeError("Could not start new subprocess.")
        if not process.waitForFinished(180000):
            #
            # Allow up to three minutes for some operations (eg installing
            # all the baseline packages)
            #
            raise RuntimeError("Could not complete new subprocess.")
        result = process.readAll().data().decode("utf-8")
        logger.info("Process results:\n%s", result)
        return result

    def find_interpreter(self):
        if sys.platform == "win32":
            self.interpreter = os.path.join(self.path, "Scripts", "python.exe")
        else:
            # For Linux/OSX.
            self.interpreter = os.path.join(self.path, "bin", "python")
        if not os.path.isfile(self.interpreter):
            message = (
                "No interpreter found where expected at %s" % self.interpreter
            )
            logger.error(message)
            raise RuntimeError(message)

    def ensure(self):
        """Ensure that a virtual environment exists, creating it if needed
        """
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
        # elif not ...:
        #   message = "Directory %s exists but is not a virtual environment" % self.path
        #
        else:
            logger.debug("Directory %s already exists", self.path)

        if not self.interpreter:
            self.find_interpreter()

    def create(self):
        """
        Create a new virtualenv at the referenced path.
        """
        logger.info("Creating virtualenv: {}".format(self.path))
        logger.info("Virtualenv name: {}".format(self.name))

        #
        # The virtualenv creator expects to find a DLLs directory
        # next to the executable's directory as there is in the
        # full distribution
        #
        source_dir = os.path.dirname(os.path.abspath(sys.executable))
        DLLs_dirpath = os.path.join(source_dir, "DLLs")
        if not os.path.exists(DLLs_dirpath):
            logger.debug(
                "No DLLs directory at %s; creating it for virtualenv",
                DLLs_dirpath,
            )
            os.mkdir(DLLs_dirpath)

        #
        # Using subprocess.run rather than virtualenv.cli_run because
        # the latter appears to suppress logging for our process!
        #
        subprocess.run(
            [sys.executable, "-m", "virtualenv", self.path], check=True
        )
        # Set the path to the interpreter
        self.find_interpreter()
        # Upgrade pip
        logger.debug(self.pip("install", "--upgrade", "pip"))
        self.install_baseline_packages()
        self.install_jupyter_kernel()

    def pip(self, *args):
        return self.run_python("-m", "pip", *args)

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
        logger.info("Installing baseline packages")
        if os.path.isdir(self.baseline_wheels_dirpath):
            logger.info("Found baseline wheels at %s", self.baseline_wheels_dirpath)
            for wheel in glob.glob(
                os.path.join(self.baseline_dirpath, "*.whl")
            ):
                logger.debug("Install wheel %s", os.path.basename(wheel))
                self.pip("install", "--upgrade", wheel)
        else:
            logger.info("No baseline wheels found at %s; installing from PyPI", self.baseline_wheels_dirpath)
            #
            # Give pip all the packages at once as its dependency
            # walker should do a more efficient job of installing
            # everything needed
            #
            packages = ["%s%s" % p for p in self.baseline_packages]
            self.pip("install", "--upgrade", *packages)

    def install_user_packages(self, packages):
        logger.info("Installing user packages: %s", ", ".join(packages))
        for package in packages:
            self.pip("install", "--upgrade", package)

    def remove_user_packages(self, packages):
        logger.info("Removing user packages: %s", ", ".join(packages))
        for package in packages:
            self.pip("uninstall", package)

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
        for p in [l.strip() for l in result.split("\n")]:
            if p not in paths:
                paths.append(p)
        for p in sys.path:
            if p not in paths:
                paths.append(p)
        return os.pathsep.join(paths)

    def installed_packages(self):
        """
        List all the third party modules installed by the user in the virtualenv
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

        baseline_packages = ["mu-editor"] + [
            name for name, version in self.baseline_packages
        ]
        user_packages = []

        result = self.run_python("-m", "pip", "freeze")
        packages = result.splitlines()
        logger.info(packages)
        for package in packages:
            name, _, version = package.partition("==")
            if name not in baseline_packages:
                user_packages.append(name)

        return baseline_packages, user_packages
