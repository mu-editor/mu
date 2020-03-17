"""
UI related code for dialogs used by Mu.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import logging
import csv
import shutil
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QProcess, QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QLabel,
    QListWidgetItem,
    QDialog,
    QDialogButtonBox,
    QPlainTextEdit,
    QTabWidget,
    QWidget,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QFileDialog
)
from PyQt5.QtGui import QTextCursor
from mu.resources import load_icon
from multiprocessing import Process
from mu.logic import MODULE_DIR

logger = logging.getLogger(__name__)


class ModeItem(QListWidgetItem):
    """
    Represents an available mode listed for selection.
    """

    def __init__(self, name, description, icon, parent=None):
        super().__init__(parent)
        self.name = name
        self.description = description
        self.icon = icon
        text = "{}\n{}".format(name, description)
        self.setText(text)
        self.setIcon(load_icon(self.icon))


class ModeSelector(QDialog):
    """
    Defines a UI for selecting the mode for Mu.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, modes, current_mode):
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_("Select Mode"))
        widget_layout = QVBoxLayout()
        label = QLabel(
            _(
                'Please select the desired mode then click "OK". '
                'Otherwise, click "Cancel".'
            )
        )
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.setLayout(widget_layout)
        self.mode_list = QListWidget()
        self.mode_list.itemDoubleClicked.connect(self.select_and_accept)
        widget_layout.addWidget(self.mode_list)
        self.mode_list.setIconSize(QSize(48, 48))
        for name, item in modes.items():
            if not item.is_debugger:
                litem = ModeItem(
                    item.name, item.description, item.icon, self.mode_list
                )
                if item.icon == current_mode:
                    self.mode_list.setCurrentItem(litem)
        self.mode_list.sortItems()
        instructions = QLabel(
            _(
                "Change mode at any time by clicking "
                'the "Mode" button containing Mu\'s logo.'
            )
        )
        instructions.setWordWrap(True)
        widget_layout.addWidget(instructions)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        widget_layout.addWidget(button_box)

    def select_and_accept(self):
        """
        Handler for when an item is double-clicked.
        """
        self.accept()

    def get_mode(self):
        """
        Return details of the newly selected mode.
        """
        if self.result() == QDialog.Accepted:
            return self.mode_list.currentItem().icon
        else:
            raise RuntimeError("Mode change cancelled.")


class LogWidget(QWidget):
    """
    Used to display Mu's logs.
    """

    def setup(self, log):
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        label = QLabel(
            _(
                "When reporting a bug, copy and paste the content of "
                "the following log file."
            )
        )
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.log_text_area = QPlainTextEdit()
        self.log_text_area.setReadOnly(True)
        self.log_text_area.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.log_text_area.setPlainText(log)
        widget_layout.addWidget(self.log_text_area)


class EnvironmentVariablesWidget(QWidget):
    """
    Used for editing and displaying environment variables used with Python 3
    mode.
    """

    def setup(self, envars):
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        label = QLabel(
            _(
                "The environment variables shown below will be "
                "set each time you run a Python 3 script.\n\n"
                "Each separate enviroment variable should be on a "
                "new line and of the form:\nNAME=VALUE"
            )
        )
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.text_area = QPlainTextEdit()
        self.text_area.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.text_area.setPlainText(envars)
        widget_layout.addWidget(self.text_area)


class MicrobitSettingsWidget(QWidget):
    """
    Used for configuring how to interact with the micro:bit:

    * Minification flag.
    * Override runtime version to use.
    """

    def setup(self, minify, custom_runtime_path):
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        self.minify = QCheckBox(_("Minify Python code before flashing?"))
        self.minify.setChecked(minify)
        widget_layout.addWidget(self.minify)
        label = QLabel(
            _(
                "Override the built-in MicroPython runtime with "
                "the following hex file (empty means use the "
                "default):"
            )
        )
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.runtime_path = QLineEdit()
        self.runtime_path.setText(custom_runtime_path)
        widget_layout.addWidget(self.runtime_path)
        widget_layout.addStretch()


class PackagesWidget(QWidget):
    """
    Used for editing and displaying 3rd party packages installed via pip to be
    used with Python 3 mode.
    """

    def setup(self, packages):
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        self.text_area = QPlainTextEdit()
        self.text_area.setLineWrapMode(QPlainTextEdit.NoWrap)
        label = QLabel(
            _(
                "The packages shown below will be available to "
                "import in Python 3 mode. Delete a package from "
                "the list to remove its availability.\n\n"
                "Each separate package name should be on a new "
                "line. Packages are installed from PyPI "
                "(see: https://pypi.org/)."
            )
        )
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.text_area.setPlainText(packages)
        widget_layout.addWidget(self.text_area)


class ESP32SettingsWidget(QWidget):
    """
    Used for configuring how to interact with the ESP32:

    * Override MicroPython.
    """

    def setup(self):
        widget_layout = QVBoxLayout()

        # Checkbox for erase, label for explain
        form_set = QHBoxLayout()
        self.erase = QCheckBox(_("Erase the entire flash before updating?"))
        self.erase.setChecked(False)
        form_set.addWidget(self.erase)
        widget_layout.addLayout(form_set)

        # Label explained the forms following
        self.setLayout(widget_layout)
        label = QLabel(
            _(
                "Override the built-in MicroPython runtime with "
                "the following file:"
            )
        )
        label.setWordWrap(True)
        widget_layout.addWidget(label)

        # Edit box for write command, Button for select firmware, Button for update
        form_set = QHBoxLayout()
        self.txtFolder = QLineEdit()
        self.btnFolder = QPushButton(_("..."))
        self.btnExec = QPushButton(_("Update"))
        self.btnExec.setEnabled(False)
        form_set.addWidget(self.txtFolder)
        form_set.addWidget(self.btnFolder)
        form_set.addWidget(self.btnExec)
        widget_layout.addLayout(form_set)

        # Text area for information
        form_set = QHBoxLayout()
        self.log_text_area = QPlainTextEdit()
        self.log_text_area.setReadOnly(True)

        init_msg = _('''
You can check the built-in MicroPython information by following command in REPL,
>>> import sys
>>> sys.implementation
''')
        self.log_text_area.setPlainText(init_msg)
        self.log_text_area.appendPlainText('''
If not install esptool yet, select "Third Party Packages" Tab and add esptool.
''')
        form_set.addWidget(self.log_text_area)
        widget_layout.addLayout(form_set)

        widget_layout.addStretch()

        # Set event
        self.btnFolder.clicked.connect(self.show_folder_dialog)
        self.btnExec.clicked.connect(self.update_firmware)
        self.btnExec.installEventFilter(self)

        self.filename = ''

    def show_folder_dialog(self):
        #default_command = 'esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 '
        default_command=''
        self.command = ''
        # open dialog and set to foldername
        filename = QFileDialog.getOpenFileName(self,
                                                'open file',
                                                os.path.expanduser('.'),
                                                "Firmware (*.bin)")
        print(filename)
        if filename:
            filename = filename[0].replace('/', os.sep)
            self.txtFolder.setText(default_command + filename)

    def update_firmware(self):
        self.err = 0
        self.commands = []
        self.log_text_area.appendPlainText('Updating...\n')

        esptool = MODULE_DIR + '/esptool.py'
        if self.erase.isChecked():
            command = [esptool, 'erase_flash']
            # self.process.start('python', command)
            self.commands.append(command)

        command = ['--chip', 'esp32', '--baud', '460800', 'write_flash', '-z', '0x1000', self.txtFolder.text()]
        command.insert(0, esptool)
        self.commands.append(command)
        self.run_esptool()

    def run_esptool(self):
        command = self.commands.pop(0)
        print(command)
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.read_process)
        self.process.finished.connect(self.finished)

        self.process.start('python', command)

    def finished(self):
        """
        Called when the subprocess that uses pip to install a package is
        finished.
        """
        if self.commands:
            self.process = None
            self.run_esptool()
        else:
            if (self.err == 1):
                self.log_text_area.appendPlainText('''
Select Third Party Packages Tab and add esptool.
''')


    def read_process(self):
        """
        Read data from the child process and append it to the text area. Try
        to keep reading until there's no more data from the process.
        """
        msg = ''
        data = self.process.readAll()
        if data:
            try:
                msg = data.data().decode("utf-8")
                self.append_data(msg)
            except UnicodeDecodeError as e:
                # print(e)
                pass
            QTimer.singleShot(2, self.read_process)

        if "[Errno 2] No such file or directory" in msg:
            self.err = 1

    def append_data(self, msg):
        """
        Add data to the end of the text area.
        """
        cursor = self.log_text_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(msg)
        cursor.movePosition(QTextCursor.End)
        self.log_text_area.setTextCursor(cursor)

    def eventFilter(self, obj, event):
        if obj == self.btnExec and event.type() == QtCore.QEvent.HoverEnter:
            self.onHovered()
        return super(ESP32SettingsWidget, self).eventFilter(obj, event)

    def onHovered(self):
        if len(self.txtFolder.text()) > 0:
            self.btnExec.setEnabled(True)
        else:
            self.btnExec.setEnabled(False)


class AdminDialog(QDialog):
    """
    Displays administrative related information and settings (logs, environment
    variables, third party packages etc...).
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, log, settings, packages, mode):
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_("Mu Administration"))
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        self.tabs = QTabWidget()
        widget_layout.addWidget(self.tabs)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        widget_layout.addWidget(button_box)
        # Tabs
        self.log_widget = LogWidget()
        self.log_widget.setup(log)
        self.tabs.addTab(self.log_widget, _("Current Log"))
        self.envar_widget = EnvironmentVariablesWidget()
        self.envar_widget.setup(settings.get("envars", ""))
        self.tabs.addTab(self.envar_widget, _("Python3 Environment"))
        self.log_widget.log_text_area.setFocus()
        self.microbit_widget = MicrobitSettingsWidget()
        self.microbit_widget.setup(
            settings.get("minify", False), settings.get("microbit_runtime", "")
        )
        self.tabs.addTab(self.microbit_widget, _("BBC micro:bit Settings"))
        self.package_widget = PackagesWidget()
        self.package_widget.setup(packages)
        self.tabs.addTab(self.package_widget, _("Third Party Packages"))
        if mode == "esp":
            self.esp32_widget = ESP32SettingsWidget()
            self.esp32_widget.setup()
            self.tabs.addTab(self.esp32_widget, _("ESP32 Firmware Settings"))

    def settings(self):
        """
        Return a dictionary representation of the raw settings information
        generated by this dialog. Such settings will need to be processed /
        checked in the "logic" layer of Mu.
        """
        return {
            "envars": self.envar_widget.text_area.toPlainText(),
            "minify": self.microbit_widget.minify.isChecked(),
            "microbit_runtime": self.microbit_widget.runtime_path.text(),
            "packages": self.package_widget.text_area.toPlainText(),
        }


class FindReplaceDialog(QDialog):
    """
    Display a dialog for getting:

    * A term to find,
    * An optional value to replace the search term,
    * A flag to indicate if the user wishes to replace all.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, find=None, replace=None, replace_flag=False):
        self.setMinimumSize(600, 200)
        self.setWindowTitle(_("Find / Replace"))
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        # Find.
        find_label = QLabel(_("Find:"))
        self.find_term = QLineEdit()
        self.find_term.setText(find)
        self.find_term.selectAll()
        widget_layout.addWidget(find_label)
        widget_layout.addWidget(self.find_term)
        # Replace
        replace_label = QLabel(_("Replace (optional):"))
        self.replace_term = QLineEdit()
        self.replace_term.setText(replace)
        widget_layout.addWidget(replace_label)
        widget_layout.addWidget(self.replace_term)
        # Global replace.
        self.replace_all_flag = QCheckBox(_("Replace all?"))
        self.replace_all_flag.setChecked(replace_flag)
        widget_layout.addWidget(self.replace_all_flag)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        widget_layout.addWidget(button_box)

    def find(self):
        """
        Return the value the user entered to find.
        """
        return self.find_term.text()

    def replace(self):
        """
        Return the value the user entered for replace.
        """
        return self.replace_term.text()

    def replace_flag(self):
        """
        Return the value of the global replace flag.
        """
        return self.replace_all_flag.isChecked()


class PackageDialog(QDialog):
    """
    Display a dialog to indicate the status of the packaging related changes
    currently run by pip.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, to_remove, to_add, module_dir):
        """
        Create the UI for the dialog.
        """
        self.to_remove = to_remove
        self.to_add = to_add
        self.module_dir = module_dir
        self.pkg_dirs = {}  # To hold locations of to-be-removed packages.
        self.process = None
        # Basic layout.
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_("Third Party Package Status"))
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        # Text area for pip output.
        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setLineWrapMode(QPlainTextEdit.NoWrap)
        widget_layout.addWidget(self.text_area)
        # Buttons.
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.button_box.accepted.connect(self.accept)
        widget_layout.addWidget(self.button_box)
        # Kick off processing of packages.
        if self.to_remove:
            self.remove_packages()
        if self.to_add:
            self.run_pip()

    def remove_packages(self):
        """
        Work out which packages need to be removed and then kick off their
        removal.
        """
        dirs = [
            os.path.join(self.module_dir, d)
            for d in os.listdir(self.module_dir)
            if d.endswith("dist-info") or d.endswith("egg-info")
        ]
        self.pkg_dirs = {}
        for pkg in self.to_remove:
            for d in dirs:
                # Assets on the filesystem use a normalised package name.
                pkg_name = pkg.replace("-", "_").lower()
                if os.path.basename(d).lower().startswith(pkg_name + "-"):
                    self.pkg_dirs[pkg] = d
        if self.pkg_dirs:
            # If there are packages to remove, schedule removal.
            QTimer.singleShot(2, self.remove_package)

    def remove_package(self):
        """
        Take a package from the pending packages to be removed, delete all its
        assets and schedule the removal of the remaining packages. If there are
        no packages to remove, move to the finished state.
        """
        if self.pkg_dirs:
            package, info = self.pkg_dirs.popitem()
            if info.endswith("dist-info"):
                # Modern
                record = os.path.join(info, "RECORD")
                with open(record) as f:
                    files = csv.reader(f)
                    for row in files:
                        to_delete = os.path.join(self.module_dir, row[0])
                        try:
                            os.remove(to_delete)
                        except Exception as ex:
                            logger.error("Unable to remove: " + to_delete)
                            logger.error(ex)
                shutil.rmtree(info, ignore_errors=True)
                # Some modules don't use the module name for the module
                # directory (they use a lower case variant thereof). E.g.
                # "Fom" vs. "fom".
                normal_module = os.path.join(self.module_dir, package)
                lower_module = os.path.join(self.module_dir, package.lower())
                shutil.rmtree(normal_module, ignore_errors=True)
                shutil.rmtree(lower_module, ignore_errors=True)
                self.append_data("Removed {}\n".format(package))
            else:
                # Egg
                try:
                    record = os.path.join(info, "installed-files.txt")
                    with open(record) as f:
                        files = f.readlines()
                        for row in files:
                            to_delete = os.path.join(info, row.strip())
                            try:
                                os.remove(to_delete)
                            except Exception as ex:
                                logger.error("Unable to remove: " + to_delete)
                                logger.error(ex)
                    shutil.rmtree(info, ignore_errors=True)
                    # Some modules don't use the module name for the module
                    # directory (they use a lower case variant thereof). E.g.
                    # "Fom" vs. "fom".
                    normal_module = os.path.join(self.module_dir, package)
                    lower_module = os.path.join(
                        self.module_dir, package.lower()
                    )
                    shutil.rmtree(normal_module, ignore_errors=True)
                    shutil.rmtree(lower_module, ignore_errors=True)
                    self.append_data("Removed {}\n".format(package))
                except Exception as ex:
                    msg = (
                        "UNABLE TO REMOVE PACKAGE: {} (check the logs for"
                        " more information.)"
                    ).format(package)
                    self.append_data(msg)
                    logger.error("Unable to remove package: " + package)
                    logger.error(ex)
            QTimer.singleShot(2, self.remove_package)
        else:
            # Clean any directories not containing files.
            dirs = [
                os.path.join(self.module_dir, d)
                for d in os.listdir(self.module_dir)
            ]
            for d in dirs:
                keep = False
                for entry in os.walk(d):
                    if entry[2]:
                        keep = True
                if not keep:
                    shutil.rmtree(d, ignore_errors=True)
            # Remove the bin directory (and anything in it) since we don't
            # use these assets.
            shutil.rmtree(
                os.path.join(self.module_dir, "bin"), ignore_errors=True
            )
            # Check for end state.
            if not (self.to_add or self.process):
                self.end_state()

    def end_state(self):
        """
        Set the UI to a valid end state.
        """
        self.append_data("\nFINISHED")
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def run_pip(self):
        """
        Run a pip command in a subprocess and pipe the output to the dialog's
        text area.
        """
        package = self.to_add.pop()
        args = ["-m", "pip", "install", package, "--target", self.module_dir]
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.read_process)
        self.process.finished.connect(self.finished)
        logger.info("{} {}".format(sys.executable, " ".join(args)))
        self.process.start(sys.executable, args)

    def finished(self):
        """
        Called when the subprocess that uses pip to install a package is
        finished.
        """
        if self.to_add:
            self.process = None
            self.run_pip()
        else:
            if not self.pkg_dirs:
                self.end_state()

    def read_process(self):
        """
        Read data from the child process and append it to the text area. Try
        to keep reading until there's no more data from the process.
        """
        data = self.process.readAll()
        if data:
            self.append_data(data.data().decode("utf-8"))
            QTimer.singleShot(2, self.read_process)

    def append_data(self, msg):
        """
        Add data to the end of the text area.
        """
        cursor = self.text_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(msg)
        cursor.movePosition(QTextCursor.End)
        self.text_area.setTextCursor(cursor)
