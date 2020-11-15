#!/usr/bin/python

"""
ZetCode PyQt5 tutorial

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar, and a central widget.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
import functools

from PyQt5.QtCore import QObject, QProcess, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication

class Process(QObject):
    """

    eg::
        class Example(QMainWindow):

            def __init__(self):
                super().__init__()
                textEdit = QTextEdit()

                self.setCentralWidget(textEdit)
                self.setGeometry(300, 300, 350, 250)
                self.setWindowTitle('Main window')
                self.show()

                self.process = Process()
                self.process.output.connect(textEdit.append)
                self.process.run(sys.executable, ["-u", "-m", "pip", "list"])

        def main():
            app = QApplication(sys.argv)
            ex = Example()
            sys.exit(app.exec_())
    """

    started = pyqtSignal()
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self, command, args):
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self._readyRead)
        self.process.started.connect(self._started)
        self.process.finished.connect(self._finished)
        QTimer.singleShot(100, functools.partial(self.process.start, command, args))

    def _started(self):
        self.started.emit()

    def _readyRead(self):
        text = self.process.readAll().data().decode("utf-8").strip()
        print("Text: %r" % text)
        self.output.emit(text)

    def _finished(self):
        self.finished.emit()

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.abc = 1
        self.process = None
        self.textEdit = QTextEdit(self)
        self.textEdit.textChanged.connect(self.text_changed )
        self.setCentralWidget(self.textEdit)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

        #~ self.process = Process()
        #~ self.process.output.connect(textEdit.append)
        #~ self.process.run(sys.executable, ["-u", "-m", "pip", "list"])
        #~ self.process.run(sys.executable, ["-u", "slowgen.py"])
        #~ self.process.run(sys.executable, ["-u", "slowgen.py"])

    def text_changed(self):
        print(repr(self.textEdit.parent()))
        print(self.textEdit.parent().abc)
        print(self.textEdit.toPlainText())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()