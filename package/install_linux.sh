#!/bin/bash
set -ev
# Ubuntu 14.04 already has Python3 install, use default sudo path version
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 --version
sudo python3 get-pip.py
# Remove the get-pip.py downloaded file to exclude it from test checkers
rm get-pip.py
sudo pip3 install pyinstaller
sudo apt-get update
# sudo apt-get install python3-pyqt5 -y
# sudo apt-get install python3-pyqt5.qsci -y
# sudo apt-get install python3-pyqt5.qtserialport -y
