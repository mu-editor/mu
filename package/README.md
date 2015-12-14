# Packing Mu

## Install dependencies

### Windows

* Install Python 3 from the [official website](https://www.python.org/downloads/).
* Install the PyQt5 binary package from [riverbankcomputing](https://riverbankcomputing.com/software/pyqt/download).
* Install PyiIstaller (includes pypiwin32):
    ```
    pip install pyinstaller
    ```

### Mac OS X

Assuming you have the [Homebrew](http://brew.sh/) package manager installed.

* Install Python 3
  ```
  brew update
  brew install python3
  ```
* Install the PyQt5 binary package
  ```
  brew install pyqt5 --with-python3
  ```
* Install pyinstaller:
  ```
  pip3 install pyinstaller
  ```

### Linux

Assuming you are running a Linux distribution with apt.

* Install Python 3
  ```
  sudo apt-get update
  sudo apt-get install python3
  ```
* Install PyQt5:
  ```
  sudo apt-get install python3-pyqt5
  ```
* Install pyinstalle:
  ```
  pip3 install pyinstaller
  ```


## Package MU

Run from the project root directory:

```
pyinstaller package\pyinstaller.spec
```

The single file executable should be saved in `/dist/mu` or `/dist/mu`.

The spec file `package/pyinstaller.spec` can be edited to simplify packaging debugging.

## Download the Mu executable [![Windows Build status](https://ci.appveyor.com/api/projects/status/ngt8780him9hlgch?svg=true)](https://ci.appveyor.com/project/carlosperate/mu) [![Linux and OS X Build status](https://travis-ci.org/carlosperate/mu.svg)](https://travis-ci.org/carlosperate/mu)

You can download the latest executable of Mu for your operating system:

* [Windows](http://ardublockly-builds.s3-website-us-west-2.amazonaws.com/index.html?prefix=microbit/windows/)
* [Mac OS X](http://ardublockly-builds.s3-website-us-west-2.amazonaws.com/index.html?prefix=microbit/osx/)
* [Linux](http://ardublockly-builds.s3-website-us-west-2.amazonaws.com/index.html?prefix=microbit/linux/)
