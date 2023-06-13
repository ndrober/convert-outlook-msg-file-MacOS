# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['convert_msg_to_eml.py'],
    pathex=[],
    binaries=[],
    datas=[ ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ConvertMsgToEml',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=os.environ.get('CODESIGNAPP'),
    entitlements_file=None,
    icon=['MSG2EML.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ConvertMsgToEml',
)
import pathlib
app = BUNDLE(
    coll,
    name='ConvertMsgToEml.app',
    icon='MSG2EML.icns',
    bundle_identifier=None,
    version=pathlib.Path("version.txt").read_text()[:-1],
    info_plist={
      'NSPrincipalClass': 'NSApplication',
      'NSAppleScriptEnabled': False,
      'CFBundleDocumentTypes': [
        {
          'CFBundleTypeName': 'CDFV2 Microsoft Outlook Message',
          'CFBundleTypeIconFile': 'MSG2EML.icns',
          'LSItemContentTypes': ['ConvertMsgToEml.msg'],
          'LSHandlerRank': 'Owner',
          'CFBundleTypeRole': 'Viewer',
          'LSIsAppleDefaultForType': True
        },
        {
          'CFBundleTypeName': 'RFC 822 Email Text',
          'CFBundleTypeIconFile': 'MSG2EML.icns',
          'LSItemContentTypes': ['ConvertMsgToEml.eml'],
          'LSHandlerRank': 'Owner',
          'CFBundleTypeRole': 'Viewer',
          'LSIsAppleDefaultForType': True
        }
      ],
      'UTExportedTypeDeclarations': [
        {
          'UTTypeIdentifier': 'ConvertMsgToEml.msg',
          'UTTypeDescription': 'CDFV2 Microsoft Outlook Message',
          'UTTypeIconFile': 'MSG2EML.icns',
          'UTTypeConformsTo': ['public.data'],
          'UTTypeTagSpecification': {
            'public.filename-extension': ['msg'],
            'public.mime-type': ['application/vnd.ms-outlook']
          }
        },
        {
          'UTTypeIdentifier': 'ConvertMsgToEml.eml',
          'UTTypeDescription': 'RFC 822 Email Text',
          'UTTypeIconFile': 'MSG2EML.icns',
          'UTTypeConformsTo': ['public.data'],
          'UTTypeTagSpecification': {
            'public.filename-extension': ['eml'],
            'public.mime-type': ['message/rfc822']
          }
        }
      ]
    },
)
