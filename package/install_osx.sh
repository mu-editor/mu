#!/bin/bash
set -ev
brew update >/dev/null 2>&1  # This produces a lot of output that's not very interesting

# Install Python 3.6 creates python3, python3.6, and pip3.6 commands but no pip3
brew tap zoidbergwill/python
brew install python36

# Copy pip3.6 symlink rather than creating one, better in case installation path changes
cp -R /usr/local/bin/pip3.6 /usr/local/bin/pip3
