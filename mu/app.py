"""
Mu - a "micro" Python editor for everyone.

Copyright (c) 2015-2016 Nicholas H.Tollervey and others (see the AUTHORS file).

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
from PyQt5.QtWidgets import QApplication, QSplashScreen
from mu.editor import Editor
from mu.resources import load_stylesheet, load_pixmap
from mu.interface import Window


def run():
    """
    Creates all the top-level assets for the application, sets things up and
    then runs the application.
    """
    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet('mu.css'))
    # Display a friendly "splash" icon.
    splash = QSplashScreen(load_pixmap('icon'))
    splash.show()
    # Create the "window" we'll be looking at.
    editor_window = Window()
    # Create the "editor" that'll control the "window".
    editor = Editor(view=editor_window)
    # Setup the window.
    editor_window.setup()
    editor.restore_session()
    # Connect the various buttons in the window to the editor.
    button_bar = editor_window.button_bar
    button_bar.connect("new", editor.new, "Ctrl+N")
    button_bar.connect("load", editor.load, "Ctrl+O")
    button_bar.connect("save", editor.save, "Ctrl+S")
    button_bar.connect("flash", editor.flash)
    button_bar.connect("repl", editor.toggle_repl)
    button_bar.connect("zoom-in", editor.zoom_in)
    button_bar.connect("zoom-out", editor.zoom_out)
    button_bar.connect("quit", editor.quit)
    # Finished starting up the application, so hide the splash icon.
    splash.finish(editor_window)
    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
