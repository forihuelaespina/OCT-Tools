# -*- mode: python -*-

block_cipher = None


a = Analysis(['[all,imports,bootloader,noarchive]'],
             pathex=['E:\\Felipe\\OneDrive\\Git\\OCT-Tools\\src'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy', 'scipy._lib.messagestream', 'pywt._extensions._cwt', 'PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='[all,imports,bootloader,noarchive]',
          debug=True,
          strip=False,
          upx=True,
          console=True , icon='..\\resources\\inaoe.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='[all,imports,bootloader,noarchive]')
