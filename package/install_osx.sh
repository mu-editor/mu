#!/bin/bash
set -ev
brew update
brew install python3
sudo pip3 install --upgrade pip setuptools
pip3 install pyinstaller
brew install pyqt5 --with-python3
