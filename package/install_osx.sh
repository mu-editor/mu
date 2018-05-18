#!/bin/bash
set -ev
brew update >/dev/null 2>&1  # This produces a lot of output that's not very interesting

# Install Python 3.6
brew install python
