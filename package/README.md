# Packing Mu

## Windows

### Quick Installation instructions

* Install Python 3
* Install the PyQt5 binary package: https://riverbankcomputing.com/software/pyqt/download5
* Install pyinstaller (includes pypiwin32):
    ```
    pip install pyinstaller
    ```

### Package

Run:

```
pyinstaller package\pyinstaller.spec --hidden-import=PyQt5
```

The single file executable should be in the `/dist/mu.exe` location.
