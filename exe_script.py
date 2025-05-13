import PyInstaller.__main__

PyInstaller.__main__.run([
    '--windowed',
    '--onefile',
    "--icon=ensaimadium.ico",
    "main.py",
])

