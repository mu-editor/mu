"""
Mu.py - a "micro" editor and exploration of a problem space.

Copyright (c) 2015 Nicholas H.Tollervey.

Based upon work done for Puppy IDE by Dan Pope, Nicholas Tollervey and Damien
George.

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
import sys
import os
from PyQt5.QtWidgets import (QApplication, QSplashScreen, QStackedWidget,
                             QDesktopWidget)
from mu.resources import load_icon, load_pixmap, load_stylesheet
from mu.editor import Editor
from mu.repl import find_microbit, REPLPane


class Mu(QStackedWidget):
    """
    Represents the main application window.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(load_icon('icon'))
        self.update_title()
        # Ensure we have a sensible size for the application.
        self.setMinimumSize(800, 600)
        self.setup()

    def update_title(self, project=None):
        """
        Updates the title bar of the application.
        """
        title = "Mu Editor"
        if project:
            title += ' - ' + project
        self.setWindowTitle(title)

    def autosize_window(self):
        """
        Makes the editor 80% of the width*height of the screen and centres it.
        """
        screen = QDesktopWidget().screenGeometry()
        w = int(screen.width() * 0.8)
        h = int(screen.height() * 0.8)
        self.resize(w, h)
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2
        )

    def setup(self):
        """
        Sets up the application.
        """
        ed = Editor(self, None)
        mb_port = find_microbit()
        if mb_port:
            # Qt has found a device.
            if os.name == 'posix':
                # If we're on Linux or OSX reference the port like this...
                port = '/dev/{}'.format(mb_port)
            elif os.name == 'nt':
                # On Windows do something related to an appropriate port name.
                port = mb_port  # COMsomething-or-other.
            else:
                # No idea how to deal with other OS's so fail.
                raise NotImplementedError('OS not supported.')
            replpane = REPLPane(port=port, parent=ed)
            ed.add_repl(replpane)
        self.addWidget(ed)
        self.setCurrentWidget(ed)


def main():
    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet('mu.css'))

    # A splash screen is a logo that appears when you start up the application.
    # The image to be "splashed" on your screen is in the resources/images
    # directory.
    splash = QSplashScreen(load_pixmap('icon'))
    splash.show()

    # Make the editor with the Mu class defined above.
    the_editor = Mu()
    the_editor.show()
    the_editor.autosize_window()

    # Remove the splash when the_editor has finished setting itself up.
    splash.finish(the_editor)

    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
