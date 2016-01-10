#!/bin/bash
set -ev
brew update
brew install python3
pip3 install pyinstaller
brew install pyqt5 --with-python3
brew install $(dirname "$PWD/${0#./}")/extras/qscintilla2.rb
