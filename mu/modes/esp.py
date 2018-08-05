import os
import logging
from mu.modes.base import MicroPythonMode
from mu.modes.api import ESP_APIS, SHARED_APIS
from mu.contrib.pyboard import Pyboard, PyboardError
import mu.contrib.files as files
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer

logger = logging.getLogger(__name__)


class DeviceFlasher(QThread):
    """
    Used to flash the ESP8266/ESP32 in a non-blocking manner.
    """
    # Emitted when flashing the MicroPython-device fails for any reason.
    on_flash_fail = pyqtSignal(str)

    def __init__(self, pyboard, filename, python_script):
        """The pyboard should be an initialized Pyboard object. The
        python_script should be the text of the script to flash onto
        the device.

        """
        QThread.__init__(self)
        self.pyboard = pyboard
        self.filename = filename
        self.python_script = python_script

    def run(self):
        """
        Flash the device.
        """
        try:
            fs = files.Files(self.pyboard)
            fs.put(self.filename, self.python_script)
        except Exception as ex:
            # Catch everything so Mu can recover from all of the wide variety
            # of possible exceptions that could happen at this point.
            self.on_flash_fail.emit(str(ex))


class FileManager(QObject):
    """
    Used to manage ESP8266/ESP32 filesystem operations in a manner
    such that the UI remains responsive.

    Provides an FTP-ish API. Emits signals on success or failure of
    different operations.
    """

    # Emitted when the tuple of files on the ESP8266/ESP32 is known.
    on_list_files = pyqtSignal(tuple)
    # Emitted when a file is downloaded from the ESP8266/ESP32.
    on_get_file = pyqtSignal(str)
    # Emitted when a file with is put onto the ESP8266/ESP32.
    on_put_file = pyqtSignal(str)
    # Emitted when a file is deleted from the ESP8266/ESP32.
    on_delete_file = pyqtSignal(str)
    # Emitted when Mu is unable to list the files on the ESP8266/ESP32.
    on_list_fail = pyqtSignal()
    # Emitted when a file fails to be got from the ESP8266/ESP32.
    on_get_fail = pyqtSignal(str)
    # Emitted when a file fails to be put onto the ESP8266/ESP32.
    on_put_fail = pyqtSignal(str)
    # Emitted when a file fails to be deleted from the ESP8266/ESP32.
    on_delete_fail = pyqtSignal(str)

    def __init__(self, pyboard, fs):
        """
        The paths_to_microbits should be a list containing filesystem
        paths to attached ESP8266/ESP32s to flash. The python_script
        should be the text of the script to flash onto the device. The
        path_to_runtime should be the path of the hex file for the
        MicroPython runtime to use. If the path_to_runtime is None,
        the default MicroPython runtime is used by default.
        """
        QObject.__init__(self)
        self.pyboard = pyboard
        self.fs = fs

    def on_start(self):
        """
        Run when the thread containing this object's instance is started so
        it can emit the list of files found on the connected ESP8266/ESP32.
        """
        self.ls()

    def ls(self):
        """
        List the files on the ESP8266/ESP32. Emit the resulting tuple of
        filenames or emit a failure signal.
        """
        try:
            result = tuple(self.fs.ls(long_format=False))
            self.on_list_files.emit(result)
        except Exception as ex:
            logger.exception(ex)
            self.on_list_fail.emit()

    def get(self, microbit_filename, local_filename):
        """
        Get the referenced ESP8266/ESP32 filename and save it to the local
        filename. Emit the name of the filename when complete or emit a
        failure signal.
        """
        try:
            out = self.fs.get(microbit_filename)
            with open(local_filename, 'wb') as f:
                f.write(out)

            self.on_get_file.emit(microbit_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_get_fail.emit(microbit_filename)

    def put(self, local_filename):
        """
        Put the referenced local file onto the filesystem on the ESP8266/ESP32.
        Emit the name of the file on the ESP8266/ESP32 when complete, or emit
        a failure signal.
        """
        try:
            if not os.path.isfile(local_filename):
                raise IOError('No such file.')
            with open(local_filename, 'rb') as local:
                content = local.read()

            filename = os.path.basename(local_filename)
            self.fs.put(filename, content)
            self.on_put_file.emit(filename)
        except Exception as ex:
            logger.error(ex)
            self.on_put_fail.emit(local_filename)

    def delete(self, microbit_filename):
        """
        Delete the referenced file on the ESP8266/ESP32's filesystem. Emit
        the name of the file when complete, or emit a failure signal.
        """
        try:
            self.fs.rm(microbit_filename)
            self.on_delete_file.emit(microbit_filename)
        except Exception as ex:
            logger.error(ex)
            self.on_delete_fail.emit(microbit_filename)


class ESPMode(MicroPythonMode):
    """
    Represents the functionality required for running MicroPython on ESP8266
    """
    name = _('ESP8266/ESP32 MicroPython')
    description = _("Write MicroPython for the ESP8266/ESP32")
    icon = 'esp8266'
    fs = None
    flash_thread = None
    flash_timer = None

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        buttons = [
            {
                'name': 'flash',
                'display_name': _('Flash'),
                'description': _('Flash your code onto the ESP8266/ESP32.'),
                'handler': self.flash,
                'shortcut': 'F3',
            },
            {
                'name': 'files',
                'display_name': _('Files'),
                'description': _('Access the file system on ESP8266/ESP32.'),
                'handler': self.toggle_files,
                'shortcut': 'F4',
            },
            {
                'name': 'repl',
                'display_name': _('REPL'),
                'description': _('Use the REPL to live-code on the '
                                 'ESP8266/ESP32.'),
                'handler': self.toggle_repl,
                'shortcut': 'Ctrl+Shift+I',
            }, ]
        return buttons

    # TODO Update to reflect MicryPython APIs
    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + ESP_APIS

    def toggle_repl(self, event):
        if self.fs is None:
            if self.repl:
                # Remove REPL
                super().toggle_repl(event)
                files.Files._lock.release()
                self.set_buttons(files=True)
                self.set_buttons(flash=True)
            elif not (self.repl or self.plotter):
                # Add REPL
                files.Files._lock.acquire()
                super().toggle_repl(event)
                self.set_buttons(files=False)
                self.set_buttons(flash=False)
        else:
            message = _("REPL and file system cannot work at the same time.")
            information = _("The REPL and file system both use the same USB "
                            "serial connection. Only one can be active "
                            "at any time. Toggle the file system off and "
                            "try again.")
            self.view.show_message(message, information)

    def flash(self):
        """
        Takes the currently active tab, compiles the Python script therein into
        a hex file and flashes it all onto the connected device.
        """
        if self.repl:
            message = _("Flashing cannot be performed at the same time as the "
                        "REPL is active.")
            information = _("File transfers use the same "
                            "USB serial connection as the REPL. Toggle the "
                            "REPL off and try again.")
            self.view.show_message(message, information)
            return

        logger.info('Flashing script.')
        # Grab the Python script.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor.
            return
        filename = tab.label
        python_script = tab.text().encode('utf-8')

        # Find serial port the ESP8266/ESP32 is connected to
        device_port, serial = super().find_device()

        if not device_port:
            message = _('Could not find an attached ESP8266/ESP32.')
            information = _("Please ensure you leave enough time for the "
                            " ESP8266/ESP32 to be attached and configured"
                            " correctly by your computer. This may take"
                            " several seconds."
                            " Alternatively, try removing and re-attaching the"
                            " device or saving your work and restarting Mu if"
                            " the device remains unfound.")
            self.view.show_message(message, information)
            return

        try:
            pyboard = Pyboard(device_port, rawdelay=2)
            message = (_('Flashing "{}" onto the ESP8266/ESP32.')
                       .format(filename))
            self.editor.show_status_message(message, 10)
            self.set_buttons(flash=False, repl=False, files=False)

            # Always write to "main.py" when flashing, regardless of filename
            # (similar to micro:bit mode)
            self.flash_thread = DeviceFlasher(pyboard,
                                              "main.py",
                                              python_script)

            self.flash_thread.finished.connect(self.flash_finished)
            self.flash_thread.on_flash_fail.connect(self.flash_failed)
            self.flash_thread.start()
            # We want to err if flashing isn't finished within 15 seconds
            self.flash_timer = QTimer()
            self.flash_timer.timeout.connect(
                lambda: self.flash_failed("Timeout while flashing"))
            self.flash_timer.setSingleShot(True)
            self.flash_timer.start(15000)

        except PyboardError:
            message = _("Failed to connect to device at '" + device_port + "'")
            information = _("Found device at '" + device_port + "'"
                            "but failed to establish connection while"
                            "attempting to flash. Try again.")
            self.view.show_message(message, information)

    def flash_finished(self):
        """
        Called when the thread used to flash the ESP8266/ESP32 has finished.
        """
        self.set_buttons(flash=True, repl=True, files=True)
        self.editor.show_status_message(_("Finished flashing."))
        self.flash_thread = None
        if self.flash_timer:
            self.flash_timer.stop()
            self.flash_timer = None

    def flash_failed(self, error):
        """
        Called when the thread used to flash the ESP8266/ESP32 encounters a
        problem.
        """
        logger.error(error)
        message = _("There was a problem flashing the ESP8266/ESP32.")
        information = _("Please do not disconnect the device until flashing"
                        " has completed, and"
                        " check that no other programs are using device.")
        self.view.show_message(message, information, 'Warning')
        if self.flash_timer:
            self.flash_timer.stop()
            self.flash_timer = None
        self.set_buttons(flash=True, repl=True, files=True)

        self.flash_thread = None

    def toggle_files(self, event):
        """
        Check for the existence of the REPL or plotter before toggling the file
        system navigator for the MicroPython device on or off.
        """
        if self.repl:
            message = _("File system cannot work at the same time as the "
                        "REPL or plotter.")
            information = _("The file system and the REPL and plotter "
                            "use the same USB serial connection. Toggle the "
                            "REPL and plotter off and try again.")
            self.view.show_message(message, information)
        else:
            if self.fs is None:
                self.add_fs()
                if self.fs:
                    logger.info('Toggle filesystem on.')
                    self.set_buttons(flash=False, repl=False, plotter=False)
            else:
                self.remove_fs()
                logger.info('Toggle filesystem off.')
                self.set_buttons(flash=True, repl=True, plotter=True)

    def add_fs(self):
        """
        Add the file system navigator to the UI.
        """

        # Find serial port the ESP8266/ESP32 is connected to
        device_port, serial = super().find_device()

        # Check for MicroPython device
        if not device_port:
            message = _('Could not find an attached ESP8266/ESP32.')
            information = _("Please make sure the device is plugged "
                            "into this computer.\n\nThe device must "
                            "have MicroPython flashed onto it before "
                            "the file system will work.\n\n"
                            "Finally, press the device's reset button "
                            "and wait a few seconds before trying "
                            "again.")
            self.view.show_message(message, information)
            return

        try:
            pyboard = Pyboard(device_port, rawdelay=2)
            fs = files.Files(pyboard)

            self.file_manager_thread = QThread(self)
            self.file_manager = FileManager(pyboard, fs)
            self.file_manager.moveToThread(self.file_manager_thread)
            self.file_manager_thread.started.\
                connect(self.file_manager.on_start)
            self.fs = self.view.add_filesystem(self.workspace_dir(),
                                               self.file_manager)
            self.fs.set_message.connect(self.editor.show_status_message)
            self.fs.set_warning.connect(self.view.show_message)
            self.file_manager_thread.start()
        except PyboardError:
            message = _("Failed to connect to device at '" + device_port + "'")
            information = _("Found device at '" + device_port + "'"
                            "but failed to establish connection while"
                            "attempting to flash. Try again.")
            self.view.show_message(message, information)

    def remove_fs(self):
        """
        Remove the file system navigator from the UI.
        """
        self.view.remove_filesystem()
        self.file_manager = None
        self.file_manager_thread = None
        self.fs = None

    def on_data_flood(self):
        """
        Ensure the Files button is active before the REPL is killed off when
        a data flood of the plotter is detected.
        """
        self.set_buttons(files=True)
        super().on_data_flood()
