import configparser
import os
import sys
import getpass
import re
import shutil

# Hamster's template properties file
app_properties_template = ".hamster_app.properties"

# Get the path to the user's home directory
home_dir = os.path.expanduser("~")

# Define the source path (current directory)
source_path = os.path.join(os.path.dirname(sys.argv[0]), app_properties_template)

# Define the destination path (user's home directory)
destination_path = os.path.join(home_dir, app_properties_template)

# Use shutil to copy the file
shutil.copy(source_path, destination_path)

config_parser = configparser.ConfigParser()
properties_file_path = os.path.join(home_dir, app_properties_template)
config_parser.read(properties_file_path)

icon_path = os.path.join(os.path.dirname(sys.argv[0]), 'img/hamster.png')
username = getpass.getuser()
pattern = re.compile("recent_file_.*")

jmeter_plist = f"/Users/{username}/Library/Preferences/org.apache.jmeter.plist"


def jmeter_path():
    jmeter_home = config_parser.get('JMETER', 'HOME').strip()

    if jmeter_home.endswith('/'):
        jmeter_home = jmeter_home.rstrip('/')
    jmeter_bin = jmeter_home + '/bin/jmeter'
    return jmeter_home, jmeter_bin
