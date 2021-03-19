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
import logging
from PyQt5.QtCore import QSize, QProcess, QTimer, Qt

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
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
    QFileDialog,
    QGroupBox,
    QComboBox,
)
from PyQt5.QtGui import QTextCursor
from mu.resources import load_icon
from mu.interface.widgets import DeviceSelector
from ..virtual_environment import venv

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


class ESPFirmwareFlasherWidget(QWidget):
    """
    Used for configuring how to interact with the ESP:

    * Override MicroPython.
    """

    def setup(self, mode, device_list):
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)

        # Instructions
        grp_instructions = QGroupBox(
            _("How to flash MicroPython to your device")
        )
        grp_instructions_vbox = QVBoxLayout()
        grp_instructions.setLayout(grp_instructions_vbox)
        # Note: we have to specify the link color here, to something
        # that's suitable for both day/night/contrast themes, as the
        # link color is not configurable in the Qt Stylesheets
        instructions = _(
            "&nbsp;1. Determine the type of device (ESP8266 or ESP32)<br />"
            "&nbsp;2. Download firmware from the "
            '<a href="https://micropython.org/download" '
            'style="color:#039be5;">'
            "https://micropython.org/download</a><br/>"
            "&nbsp;3. Connect your device<br/>"
            "&nbsp;4. Load the .bin file below using the 'Browse' button<br/>"
            "&nbsp;5. Press 'Erase & write firmware'"
            # "<br /><br />Check the current MicroPython version using the "
            # "following commands:<br />"
            # ">>> import sys<br />"
            # ">>> sys.implementation"
        )
        label = QLabel(instructions)
        label.setTextFormat(Qt.RichText)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        label.setWordWrap(True)
        grp_instructions_vbox.addWidget(label)
        widget_layout.addWidget(grp_instructions)

        # Device type, firmware path, flash button
        device_selector_label = QLabel("Device:")
        self.device_selector = DeviceSelector(show_label=True, icon_first=True)
        self.device_selector.set_device_list(device_list)
        device_type_label = QLabel("Choose device type:")
        self.device_type = QComboBox(self)
        self.device_type.addItem("ESP8266")
        self.device_type.addItem("ESP32")
        firmware_label = QLabel("Firmware (.bin):")
        self.txtFolder = QLineEdit()
        self.btnFolder = QPushButton(_("Browse"))
        self.btnExec = QPushButton(_("Erase && write firmware"))
        self.btnExec.setEnabled(False)
        form_set = QGridLayout()
        form_set.addWidget(device_selector_label, 0, 0)
        form_set.addWidget(self.device_selector, 0, 1, 1, 3)
        form_set.addWidget(device_type_label, 1, 0)
        form_set.addWidget(self.device_type, 1, 1)
        form_set.addWidget(firmware_label, 2, 0)
        form_set.addWidget(self.txtFolder, 2, 1)
        form_set.addWidget(self.btnFolder, 2, 2)
        form_set.addWidget(self.btnExec, 2, 3)
        widget_layout.addLayout(form_set)

        # Output area
        self.log_text_area = QPlainTextEdit()
        self.log_text_area.setReadOnly(True)
        form_set = QHBoxLayout()
        form_set.addWidget(self.log_text_area)
        widget_layout.addLayout(form_set)

        # Connect events
        self.txtFolder.textChanged.connect(self.firmware_path_changed)
        self.btnFolder.clicked.connect(self.show_folder_dialog)
        self.btnExec.clicked.connect(self.update_firmware)
        self.device_selector.device_changed.connect(self.toggle_exec_button)

        self.mode = mode

    def esptool_is_installed(self):
        """
        Is the 'esptool' package installed?
        """
        baseline, user_packages = venv.installed_packages()
        return "esptool" in user_packages

    def show_folder_dialog(self):
        # open dialog and set to foldername
        filename = QFileDialog.getOpenFileName(
            self,
            "Select MicroPython firmware (.bin)",
            os.path.expanduser("."),
            "Firmware (*.bin)",
        )
        if filename:
            filename = filename[0].replace("/", os.sep)
            self.txtFolder.setText(filename)

    def update_firmware(self):
        baudrate = 115200

        if self.mode.repl:
            self.mode.toggle_repl(None)
        if self.mode.plotter:
            self.mode.toggle_plotter(None)
        if self.mode.fs is not None:
            self.mode.toggle_files(None)

        device = self.device_selector.selected_device()
        if device is None:
            return

        esptool = "-mesptool"
        erase_command = '"{}" "{}" --port {} erase_flash'.format(
            venv.interpreter, esptool, device.port
        )

        if self.device_type.currentText() == "ESP32":
            write_command = (
                '"{}" "{}" --chip esp32 --port {} --baud {} '
                'write_flash -z 0x1000 "{}"'
            ).format(
                venv.interpreter,
                esptool,
                device.port,
                baudrate,
                self.txtFolder.text(),
            )
        else:
            write_command = (
                '"{}" "{}" --chip esp8266 --port {} --baud {} '
                'write_flash --flash_size=detect 0 "{}"'
            ).format(
                venv.interpreter,
                esptool,
                device.port,
                baudrate,
                self.txtFolder.text(),
            )

        self.commands = [erase_command, write_command]
        self.run_esptool()

    def run_esptool(self):
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardError.connect(self.read_process)
        self.process.readyReadStandardOutput.connect(self.read_process)
        self.process.finished.connect(self.esptool_finished)
        self.process.error.connect(self.esptool_error)

        command = self.commands.pop(0)
        self.log_text_area.appendPlainText(command + "\n")
        self.process.start(command)

    def esptool_error(self, error_num):
        self.log_text_area.appendPlainText(
            "Error occurred: Error {}\n".format(error_num)
        )
        self.process = None

    def esptool_finished(self, exitCode, exitStatus):
        """
        Called when the subprocess that executes 'esptool.py is finished.
        """
        # Exit if a command fails
        if exitCode != 0 or exitStatus == QProcess.CrashExit:
            self.log_text_area.appendPlainText("Error on flashing. Aborting.")
            return
        if self.commands:
            self.process = None
            self.run_esptool()

    def read_process(self):
        """
        Read data from the child process and append it to the text area. Try
        to keep reading until there's no more data from the process.
        """
        msg = ""
        data = self.process.readAll()
        if data:
            try:
                msg = data.data().decode("utf-8")
                self.append_data(msg)
            except UnicodeDecodeError:
                pass
            QTimer.singleShot(2, self.read_process)

    def append_data(self, msg):
        """
        Add data to the end of the text area.
        """
        cursor = self.log_text_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(msg)
        cursor.movePosition(QTextCursor.End)
        self.log_text_area.setTextCursor(cursor)

    def firmware_path_changed(self):
        self.toggle_exec_button()

    def toggle_exec_button(self):
        if (
            len(self.txtFolder.text()) > 0
            and self.device_selector.selected_device() is not None
        ):
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
        self.microbit_widget = None
        self.package_widget = None
        self.envar_widget = None

    def setup(self, log, settings, packages, mode, device_list):
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
        self.log_widget = LogWidget(self)
        self.log_widget.setup(log)
        self.tabs.addTab(self.log_widget, _("Current Log"))
        if mode.short_name in ["python", "web", "pygamezero"]:
            self.envar_widget = EnvironmentVariablesWidget(self)
            self.envar_widget.setup(settings.get("envars", ""))
            self.tabs.addTab(self.envar_widget, _("Python3 Environment"))
        if mode.short_name == "microbit":
            self.microbit_widget = MicrobitSettingsWidget(self)
            self.microbit_widget.setup(
                settings.get("minify", False),
                settings.get("microbit_runtime", ""),
            )
            self.tabs.addTab(self.microbit_widget, _("BBC micro:bit Settings"))
        if mode.short_name in ["python", "web", "pygamezero"]:
            self.package_widget = PackagesWidget(self)
            self.package_widget.setup(packages)
            self.tabs.addTab(self.package_widget, _("Third Party Packages"))
        if mode.short_name == "esp":
            self.esp_widget = ESPFirmwareFlasherWidget(self)
            self.esp_widget.setup(mode, device_list)
            self.tabs.addTab(self.esp_widget, _("ESP Firmware flasher"))
        self.log_widget.log_text_area.setFocus()

    def settings(self):
        """
        Return a dictionary representation of the raw settings information
        generated by this dialog. Such settings will need to be processed /
        checked in the "logic" layer of Mu.
        """
        settings = {}
        if self.envar_widget:
            settings["envars"] = self.envar_widget.text_area.toPlainText()
        if self.microbit_widget:
            settings["minify"] = self.microbit_widget.minify.isChecked()
            settings[
                "microbit_runtime"
            ] = self.microbit_widget.runtime_path.text()
        if self.package_widget:
            settings["packages"] = self.package_widget.text_area.toPlainText()
        return settings


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
    Display the output of the pip commands needed to remove or install
    packages.

    Because the QProcess mechanism we're using is asynchronous, we have to
    manage the pip requests via `pip_queue`. When one request is signalled
    as finished we start the next.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pip_queue = []

    def setup(self, to_remove, to_add):
        """
        Create the UI for the dialog.
        """
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

        #
        # Set up the commands to be issues to pip. Since we'll be popping
        # from the list (as LIFO) we'll add the installs first so the
        # removes are the first to happen
        #
        if to_add:
            self.pip_queue.append(("install", to_add))
        if to_remove:
            self.pip_queue.append(("remove", to_remove))
        QTimer.singleShot(2, self.next_pip_command)

    def next_pip_command(self):
        """
        Run the next pip command, finishing if there is none.
        """
        if self.pip_queue:
            command, packages = self.pip_queue.pop()
            self.run_pip(command, packages)
        else:
            self.finish()

    def finish(self):
        """
        Set the UI to a valid end state.
        """
        self.text_area.appendPlainText("\nFINISHED")
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def run_pip(self, command, packages):
        """
        Run a pip command in a subprocess and pipe the output to the dialog's
        text area.
        """
        if command == "remove":
            pip_fn = venv.remove_user_packages
        elif command == "install":
            pip_fn = venv.install_user_packages
        else:
            raise RuntimeError(
                "Invalid pip command: %s %s" % (command, packages)
            )
        pip_fn(
            packages,
            slots=venv.Slots(
                output=self.text_area.appendPlainText,
                finished=self.next_pip_command,
            ),
        )
