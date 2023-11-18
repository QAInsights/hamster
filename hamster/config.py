import configparser
import os
import sys
import getpass
import re

config_parser = configparser.ConfigParser()
properties_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'app.properties')
config_parser.read(properties_file_path)

icon_path=os.path.join(os.path.dirname(sys.argv[0]), 'hamster.png')
username = getpass.getuser()
pattern = re.compile("recent_file_.*")

jmeter_plist = f"/Users/{username}/Library/Preferences/org.apache.jmeter.plist"
jmeter_home = config_parser.get('JMETER', 'HOME')
jmeter_path = jmeter_home + '/bin/jmeter'