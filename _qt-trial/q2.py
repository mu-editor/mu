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

if __name__ == '__main__':
    import sys
    process = QProcess()
    process.start(sys.executable, ["--version"])
    process.waitForFinished()
    print(process.readAll())
