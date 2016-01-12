#!/bin/bash
set -ev
brew update
brew install python3
sudo pip install git+git://github.com/inglesp/pyinstaller.git@f75edb9ac0da15ce0bdec52ff3aaef74aab5a470
brew install pyqt5 --with-python3
brew install $(dirname "$PWD/${0#./}")/extras/qscintilla2.rb
