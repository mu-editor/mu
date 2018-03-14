#!/bin/bash
set -ev
# Check python3 installation
python3 --version
python3 -c "import sys; print(sys.executable)"
# Install pip
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
rm get-pip.py
