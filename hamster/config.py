import configparser
import os
import sys
import getpass
import re
import shutil


# Get the path to the user's home directory
home_dir = os.path.expanduser("~")

# Define the source path (current directory)
source_path = os.path.join(os.path.dirname(sys.argv[0]), 'app.properties')

# Define the destination path (user's home directory)
destination_path = os.path.join(home_dir, 'app.properties')

# Use shutil to copy the file
shutil.copy(source_path, destination_path)

config_parser = configparser.ConfigParser()
properties_file_path = os.path.join(home_dir, 'app.properties')
config_parser.read(properties_file_path)

icon_path = os.path.join(os.path.dirname(sys.argv[0]), 'img/hamster.png')
username = getpass.getuser()
pattern = re.compile("recent_file_.*")

jmeter_plist = f"/Users/{username}/Library/Preferences/org.apache.jmeter.plist"


def jmeter_path():
    jmeter_home = config_parser.get('JMETER', 'HOME')
    jmeter_bin = jmeter_home + '/bin/jmeter'
    return jmeter_home, jmeter_bin
