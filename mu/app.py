import sys

from PyQt5.QtWidgets import QApplication

from mu.models.editor import Editor
from mu.resources import load_stylesheet
from mu.views.chrome import Window


def run():
    # The app object is the application running on your computer.
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet('mu.css'))

    editor_window = Window()
    editor = Editor(view=editor_window)

    end_splash, splitter = editor_window.setup()

    button_bar = editor_window.button_bar

    button_bar.connect("new", editor.new, "Ctrl+N")
    button_bar.connect("load", editor.load, "Ctrl+O")
    button_bar.connect("save", editor.save, "Ctrl+S")

    # button_bar.connect("snippets", editor.snippets)
    # button_bar.connect("flash", editor.flash)
    # button_bar.connect("repl", editor.repl)

    button_bar.connect("zoom-in", editor.zoom_in)
    button_bar.connect("zoom-out", editor.zoom_out)

    button_bar.connect("quit", editor.quit)

    end_splash()

    # Stop the program after the application finishes executing.
    sys.exit(app.exec_())
