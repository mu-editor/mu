#!/bin/bash
set -ev
# Install Python 3.5
sudo add-apt-repository ppa:fkrull/deadsnakes -y
sudo apt-get update -qq
sudo apt-get install python3.5 python3.5-dev -y
# Install pip
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3.5 get-pip.py
rm get-pip.py
# Change python3 link to point to python3.5 instead of python3.4 (/usr/bin/)
sudo mv /usr/bin/python3 /usr/bin/python3-old
sudo ln -s /usr/bin/python3.5 /usr/bin/python3
