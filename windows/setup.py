import PyInstaller.__main__

import sys
import os

if getattr(sys, 'frozen', False):
    # Running in a bundle
    base_path = sys._MEIPASS
else:
    # Running in normal Python environment
    base_path = os.path.abspath(".")

image_path = os.path.join(base_path, "hamster.png")
print(image_path)

# Get the directory of this script file
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to hamster.png relative to the script directory
hamster_path = os.path.join(script_dir, r'hamster.png')
# Convert the path to a raw string
hamster_path = r'{}'.format(hamster_path)

# Print the path and the current working directory
print("Path to hamster.png: ", hamster_path)
print("Current working directory: ", os.getcwd())

PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--add-data={}:.'.format(hamster_path),
    'main.py'
])