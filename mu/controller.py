import sys

from PyQt5.QtWidgets import QApplication

from mu.hybrid.editor import Editor
from mu.resources import load_stylesheet
from mu.views.chrome import Window


def run():
    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet('mu.css'))

    editor_window = Window()
    end_splash, splitter = editor_window.setup()

    editor = Editor(splitter)

    end_splash()

    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
