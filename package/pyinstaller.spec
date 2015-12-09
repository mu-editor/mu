# -*- mode: python -*-

block_cipher = None


a = Analysis(['../run.py'],
             pathex=['../'],
             binaries=None,
             datas=None,
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
          debug=True,
          strip=False,
          upx=True,
          console=True,
          icon='mu/resources/icons/win_icon.ico')
