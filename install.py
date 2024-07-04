import PyInstaller.__main__

PyInstaller.__main__.run([
    'client\client.py',
    # '--noconsole',
    '--onefile',
])

PyInstaller.__main__.run([
    'server\server.py',
    '--onefile',
])