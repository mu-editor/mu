#!/bin/bash
set -ev
# Ubuntu 14.04 already has Python3 install, use default sudo path version
curl -O https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
sudo python3 --version
sudo python3 get-pip.py
sudo pip3 install pyinstaller
sudo apt-get update
sudo apt-get install python3-pyqt5 -y
sudo apt-get install python3-pyqt5.qsci -y
sudo apt-get install python3-pyqt5.qtserialport -y
