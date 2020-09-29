"""
UI related code for dialogs used by Mu.

Copyright (c) 2015-2020 Nicholas H.Tollervey and others (see the AUTHORS file).

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
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
)
from mu.resources import load_pixmap


class DeviceSelector(QWidget):
    """
    Allow users to see status of connected devices (connected/disconnected),
    and select between devices, when multiple are connected.

    Emits the device_changed signal when a user selects a different device.
    """

    device_changed = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent=None, show_label=False, icon_first=False):
        """
        Initialize the DeviceSelector
        """
        super().__init__(parent)

        self.setObjectName("DeviceSelector")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.device_changed.connect(self._update_view)

        # Status indicator icon
        self.connected_icon = load_pixmap("chip-connected").scaledToHeight(24)
        self.disconnected_icon = load_pixmap(
            "chip-disconnected"
        ).scaledToHeight(24)
        self.connection_status = QLabel()
        self.connection_status.setPixmap(self.disconnected_icon)
        if icon_first:
            layout.addWidget(self.connection_status)

        # Device selection combobox
        self.selector = QComboBox()
        self.selector.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.selector.setHidden(True)
        self.selector.currentIndexChanged.connect(self._device_changed)
        layout.addWidget(self.selector)

        # Label
        self.status_label = None
        if show_label:
            self.status_label = QLabel(_("No device connected."))
            self.status_label.setHidden(True)
            layout.addWidget(self.status_label)
            layout.addStretch()
        self._update_view()

        # Status indicator icon (if last)
        if not icon_first:
            layout.addWidget(self.connection_status)

    def set_device_list(self, device_list):
        """
        Connect the selector with a DeviceList model
        """
        self.selector.setModel(device_list)
        device_list.device_connected.connect(self.device_connected)
        device_list.device_disconnected.connect(self.device_disconnected)

    def selected_device(self):
        """
        Return the currently selected device, returns None, if no device
        is selected or no devices are connected.
        """
        i = self.selector.currentIndex()
        if i < 0:
            return None
        else:
            devices = self.selector.model()
            return devices[i]

    def _device_changed(self, i):
        """
        Called when the device is changed by user or programmatically.
        Updates the current device and emits the device_changed signal.
        """
        if i < 0:
            device = None
        else:
            devices = self.selector.model()
            device = devices[i]
        self.device_changed.emit(device)

    def device_connected(self, device):
        """
        Update the view when new devices are connected.
        """
        self._update_view()

    def device_disconnected(self, device):
        """
        Update the view when devices are disconnected.
        """
        self._update_view()

    def _update_view(self):
        """
        Update icon and show/hide combobox-selector, when devices
        connects/disconnects
        """
        num_devices = self.selector.count()

        # Hide/show menu
        if num_devices <= 1:
            self.selector.setHidden(True)
        else:
            self.selector.setHidden(False)

        # Update status_label
        if self.status_label:
            if num_devices == 0:
                self.status_label.setHidden(False)
                self.status_label.setText(_("No device connected."))
            elif num_devices == 1:
                device = self.selected_device()
                self.status_label.setHidden(False)
                self.status_label.setText(
                    "{} ({})".format(device.name, device.port)
                )
            else:
                self.status_label.setHidden(True)

        # Set icon and tooltip
        if num_devices == 0:
            self.connection_status.setPixmap(self.disconnected_icon)
            self._set_tooltip(_("No device connected."))
        else:
            self.connection_status.setPixmap(self.connected_icon)
            model = self.selector.model()
            ix = model.index(self.selector.currentIndex(), 0)
            tooltip = self.selector.model().data(ix, Qt.ToolTipRole)
            self._set_tooltip(tooltip)

    def _set_tooltip(self, tooltip):
        """
        Sets the same tooltip on all widgets
        """
        self.connection_status.setToolTip(tooltip)
        self.selector.setToolTip(tooltip)
        if self.status_label:
            self.status_label.setToolTip(tooltip)
