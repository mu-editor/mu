#!/bin/bash
set -ev
brew update >/dev/null 2>&1  # This produces a lot of output that's not very interesting

# Install Python 3.6
#brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
brew upgrade pyenv 
# The following are needed for Matplotlib
brew install freetype
