#!/bin/bash
set -ev
brew update >/dev/null 2>&1  # This produces a lot of output that's not very interesting

# Install Python 3.5 creates python3, python3.5, and pip3.5 commands but no pip3
brew tap zoidbergwill/python
brew install python35
# Contrary zoidbergwill tap documentation turns out this symbolic link is not required
# sudo ln -s /usr/local/Cellar/python35/3.5.2/bin/python3.5 /usr/bin/python3

# Copy pip3.5 symlink rather than creating one, better in case installation path changes
cp -R /usr/local/bin/pip3.5 /usr/local/bin/pip3
