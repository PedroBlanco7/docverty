# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para Docverty.
"""
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Recopilar datos/binarios/hidden imports ANTES de Analysis
datas_md,  binaries_md,  hidden_md  = collect_all('markitdown')
datas_ttk, binaries_ttk, hidden_ttk = collect_all('ttkbootstrap')
# tkinterdnd2 incluye los binarios tkdnd (drag & drop) que hay que empaquetar
datas_dnd, binaries_dnd, hidden_dnd = collect_all('tkinterdnd2')
# magika: detección de tipo de archivo de markitdown 0.1.x (incluye modelos ONNX)
datas_mag, binaries_mag, hidden_mag = collect_all('magika')

extra_hidden = [
    # markitdown
    'markitdown', 'markitdown._markitdown',
    # PDF
    'pdfminer', 'pdfminer.high_level', 'pdfminer.layout',
    'pdfminer.pdfinterp', 'pdfminer.pdfdevice', 'pdfminer.converter',
    'pdfminer.pdfdocument', 'pdfminer.pdfpage', 'pdfminer.pdfparser',
    # PowerPoint
    'pptx', 'pptx.util',
    # Excel
    'openpyxl', 'openpyxl.styles',
    # HTML
    'bs4', 'lxml', 'lxml.etree', 'lxml._elementpath',
    # Imágenes
    'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageDraw',
    # UI
    'ttkbootstrap', 'ttkbootstrap.themes', 'ttkbootstrap.style',
    'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox',
    'tkinterdnd2', 'tkinterdnd2.TkinterDnD',
    # Detección de tipo (markitdown 0.1.x)
    'magika', 'onnxruntime',
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries_md + binaries_ttk + binaries_dnd + binaries_mag,
    datas=[
        ('icon.ico', '.'),
        ('exiftool', 'exiftool'),               # exiftool + exiftool_files/
        ('AVISOS-DE-TERCEROS.txt', '.'),
    ] + datas_md + datas_ttk + datas_dnd + datas_mag,
    hiddenimports=extra_hidden + hidden_md + hidden_ttk + hidden_dnd + hidden_mag,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Docverty',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version=None,
)
