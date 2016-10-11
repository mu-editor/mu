Mu - a "micro" editor
=====================

**This project works with Python 3 and the Qt UI library.**

This is forked from https://github.com/mu-editor/mu and aims to add some more
features (different boards, including ESP8266) to mu. The branch at
https://github.com/eduvik/mu/tree/feature/multi-board has these features.

Currently, the latest builds for Windows, OSX and Linux x86 can be found here:

Installation
------------

At this stage you'll need to run from source.

* Clone the repo, and switch to the feature/multiboard branch
* (optionally, create a virtualenv for the project)
* install the required packages using `pip3 install -r requirements.txt`
* edit the file `mu/config.py` to match your device configuration
* run mu using `python3 run.py`

The README for the original mu project (with rationale, etc) is at
https://github.com/mu-editor/mu/blob/master/README.rst
