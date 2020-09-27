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

    output = pyqtSignal(str)

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
        self.output.emit("Started")

    def _readyRead(self):
        text = self.process.readAll().data().decode("utf-8").strip()
        print("Text: %r" % text)
        self.output.emit(text)

    def _finished(self):
        self.output.emit("Finished")

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.process = None
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

        self.process = Process()
        self.process.output.connect(textEdit.append)
        self.process.run(sys.executable, ["-u", "-m", "pip", "list"])
        #~ self.process.run(sys.executable, ["-u", "slowgen.py"])
        #~ self.process.run(sys.executable, ["-u", "slowgen.py"])

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()