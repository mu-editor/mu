# -*- mode: python -*-
import os
from glob import glob

# Find PyQt5 directory
from inspect import getfile
import PyQt5
pyqt_dir = os.path.dirname(getfile(PyQt5))


# PyInstaller Cipher flag.
block_cipher = None


# Adding all css and images as part of additional resources
data_files_glob = glob(os.path.join('mu','resources', 'css', '*.css'))
data_files_glob += glob(os.path.join('mu', 'resources', 'images', '*.*'))
data_files_glob += glob(os.path.join('mu', 'resources', 'fonts', '*.*'))
data_files = []
# Paths are a bit tricky: glob works on cwd (project root), pyinstaller relative
# starts on spec file location, and packed application relative starts on
# project root directory.
for x in data_files_glob:
    data_files += [(os.path.join('..', x), os.path.dirname(x))]

print('Spec file resources selected: %s' % data_files)

# PyQt5 and dll location, specific to PyQt5 version
pyqt_dir = os.path.dirname(getfile(PyQt5))
pyqt_dlls = os.path.join(pyqt_dir, 'plugins', 'platforms')


binary_files = []


a = Analysis(['../run.py'],
             pathex=['../', pyqt_dir],
             binaries=None,
             datas=data_files,
             hiddenimports = ['sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mu',
          strip=False,
          upx=True,
          # False hides the cli window, useful ON to debug
          console=False,
          debug=False,
          icon='package/icons/win_icon.ico')

app = BUNDLE(exe,
         name='mu.app',
         icon='package/icons/mac_icon.icns',
         bundle_identifier=None,
         info_plist={
            'NSHighResolutionCapable': 'True'})

# For debugging you can uncomment COLLECT and it will package to a folder
# instead of a single executable (also comment out the "a" arguments in EXE)
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=None,
#               upx=True,
#               name='run')
