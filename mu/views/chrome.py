from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QToolBar,
    QAction,
    QStackedWidget,
    QSplashScreen,
    QDesktopWidget,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QTabWidget,
)

from mu.resources import load_icon, load_pixmap


class ButtonBar(QToolBar):
    """
    Represents the bar of buttons across the top of the editor and defines
    their behaviour.
    """

    slots = None
    
    def addAction(self, name, tool_text):
        action = QAction(
            load_icon(name),
            name.capitalize(), self,
            statusTip=tool_text
        )
        super().addAction(action)
        self.slots[name] = action

    def connect(self, name, slot):
        self.slots[name].pyqtConfigure(triggered=slot)
    
    def __init__(self, parent):
        super().__init__(parent)

        self.slots = {}
        
        self.setMovable(False)
        self.setIconSize(QSize(64, 64))
        self.setToolButtonStyle(3)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setObjectName("StandardToolBar")

        self.addAction(name="new", tool_text="Create a new MicroPython script.")
        self.addAction(name="load", tool_text="Load a MicroPython script.")
        self.addAction(
            name="save",
            tool_text="Save the current MicroPython script.",
        )
        self.addSeparator()
        self.addAction(
            name="snippets",
            tool_text="Use code snippets to help you program.",
        )
        self.addAction(
            name="flash",
            tool_text="Flash your MicroPython script onto the micro:bit.",
        )
        self.addAction(
            name="repl",
            tool_text=
            "Connect to the MicroPython REPL for live coding of the micro:bit.",
        )
        self.addSeparator()
        self.addAction(
            name="zoom-in",
            tool_text="Zoom in (to make the text bigger).",
        )
        self.addAction(
            name="zoom-out",
            tool_text="Zoom out (to make the text smaller).",
        )
        self.addSeparator()
        self.addAction(name="quit", tool_text="Quit the application.")


class Window(QStackedWidget):

    title = "Mu Editor"
    icon = "icon"

    def update_title(self, project=None):
        """
        Updates the title bar of the application.
        """
        title = self.title

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

        self.setWindowIcon(load_icon(self.icon))
        self.update_title()
        self.setMinimumSize(800, 600)

        splash = QSplashScreen(load_pixmap(self.icon))
        splash.show()

        widget = QWidget()
        splitter = QSplitter(Qt.Vertical)

        widget_layout = QVBoxLayout()
        widget.setLayout(widget_layout)

        self.button_bar = ButtonBar(widget)
        self.tabs = QTabWidget(widget)

        widget_layout.addWidget(self.button_bar)
        widget_layout.addWidget(splitter)
        splitter.addWidget(self.tabs)

        self.addWidget(widget)
        self.setCurrentWidget(widget)

        self.show()
        self.autosize_window()

        return (lambda: splash.finish(self)), splitter
