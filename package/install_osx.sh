#!/bin/bash
set -ev
brew update >/dev/null 2>&1  # This produces a lot of output that's not very interesting

# Install Python 3.6
brew upgrade pyenv
pyenv install 3.6.5
pyenv local 3.6.5
# The following are needed for Matplotlib
brew install freetype
brew install pkg-config
