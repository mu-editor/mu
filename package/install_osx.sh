#!/bin/bash
set -ev
brew update >/dev/null 2>&1  # This produces a lot of output that's not very interesting
brew install python3
sudo pip install git+git://github.com/inglesp/pyinstaller.git@6390b58dd2c4bb0f96642f811b6946a197b1c35a
brew install pyqt5 --with-python3
python3 -c 'import PyQt5; print(PyQt5.__file__)'
python3 -c 'import PyQt5.QtWidgets; print(PyQt5.QtWidgets.__file__)'
brew install $(dirname "$PWD/${0#./}")/extras/qscintilla2.rb
python3 -c 'import PyQt5; print(PyQt5.__file__)'
python3 -c 'import PyQt5.QtWidgets; print(PyQt5.QtWidgets.__file__)'
python3 -c 'import PyQt5.Qsci; print(PyQt5.Qsci.__file__)'
