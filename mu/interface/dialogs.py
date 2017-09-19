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
import logging
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (QVBoxLayout, QListWidget, QLabel, QListWidgetItem,
                             QDialog, QDialogButtonBox, QPlainTextEdit)
from mu.resources import load_icon
from mu.interface.themes import NIGHT_STYLE, DAY_STYLE, CONTRAST_STYLE


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

    def setup(self, modes, current_mode, theme):
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_('Select Mode'))
        widget_layout = QVBoxLayout()
        label = QLabel(_('Please select the desired mode then click "OK". '
                         'Otherwise, click "Cancel".'))
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.setLayout(widget_layout)
        self.mode_list = QListWidget()
        widget_layout.addWidget(self.mode_list)
        self.mode_list.setIconSize(QSize(48, 48))
        for name, item in modes.items():
            if not item.is_debugger:
                ModeItem(item.name, item.description, item.icon,
                         self.mode_list)
        self.mode_list.sortItems()
        instructions = QLabel(_('You can change mode at any time by clicking '
                                'the name of the current mode shown in the '
                                'bottom right-hand corner of Mu.'))
        instructions.setWordWrap(True)
        widget_layout.addWidget(instructions)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok |
                                      QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        widget_layout.addWidget(button_box)

    def get_mode(self):
        """
        Return details of the newly selected mode.
        """
        if self.result() == QDialog.Accepted:
            return self.mode_list.currentItem().icon
        else:
            raise RuntimeError('Mode change cancelled.')


class LogDisplay(QDialog):
    """
    Defines the UI for displaying the logs produced by Mu.
    """

    def setup(self, log, theme):
        if theme == 'day':
            self.setStyleSheet(DAY_STYLE)
        elif theme == 'night':
            self.setStyleSheet(NIGHT_STYLE)
        else:
            self.setStyleSheet(CONTRAST_STYLE)
        self.setMinimumSize(600, 400)
        self.setWindowTitle(_('Mu Debug Log'))
        widget_layout = QVBoxLayout()
        self.setLayout(widget_layout)
        label = QLabel(_('When reporting a bug, copy and paste the content of '
                         'the following log file.'))
        label.setWordWrap(True)
        widget_layout.addWidget(label)
        self.log_text_area = QPlainTextEdit()
        self.log_text_area.setReadOnly(True)
        self.log_text_area.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.log_text_area.setPlainText(log)
        widget_layout.addWidget(self.log_text_area)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        widget_layout.addWidget(button_box)
