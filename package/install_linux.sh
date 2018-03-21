#!/bin/bash
set -ev
# Install Python 3.6
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update -qq
sudo apt-get install python3.6 python3.6-dev -y
# Install pip
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3.6 get-pip.py
rm get-pip.py
# Change python3 link to point to python3.6 instead of python3.4 (/usr/bin/)
sudo mv /usr/bin/python3 /usr/bin/python3-old
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
