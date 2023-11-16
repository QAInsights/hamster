"""
setup.py for py2app

Usage:
    python3 setup.py py2app

"""
from setuptools import setup

APP = ['hamster.py']
APP_NAME = 'Hamster'
DATA_FILES = [('', ['app.properties', 'hamster.png', 'hamster.icns'])]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'hamster.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'configparser', 'plistlib', 'os', 're', 'sys', 'pathlib'],
}

setup(
    app=APP,
    name=APP_NAME,
    author='NaveenKumar Namachivayam',
    version='0.1',
    url='https://qainsights.com',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['rumps'],
    classifiers=[
        'Environment :: MacOS X',
        'License :: Apache 2 License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
