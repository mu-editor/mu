# Packing Mu

## Windows

### Quick Installation instructions

* Install Python 3
* Install the PyQt5 binary package: https://riverbankcomputing.com/software/pyqt/download
* Install pyinstaller (includes pypiwin32):
    ```
    pip install pyinstaller
    ```

### Package

Run from the project root directory:

```
pyinstaller package\pyinstaller.spec
```

The single file executable should be saved in `/dist/mu.exe`.

The spec file `package\pyinstaller.spec` can be edited to simplify packaging debugging.

### Download the Mu executable [![Build status](https://ci.appveyor.com/api/projects/status/ngt8780him9hlgch?svg=true)](https://ci.appveyor.com/project/carlosperate/mu)

You can download the latest Windows executable of Mu from: http://ardublockly-builds.s3-website-us-west-2.amazonaws.com/index.html?prefix=microbit/windows/
