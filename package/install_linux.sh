#!/bin/bash
set -ev
# Ubuntu 14.04 already has Python3 installed, install pip
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
rm get-pip.py
# Cannot use the PyPI Qscintilla wheel due to linked glibc
# https://www.riverbankcomputing.com/pipermail/qscintilla/2016-November/001173.html
sudo apt-get update -qq
sudo apt-get install libpython3.4-dev -y
sudo apt-get install python3-pyqt5 -y
sudo apt-get install python3-pyqt5.qsci -y
sudo apt-get install python3-pyqt5.qtserialport -y

