import configparser
import os
import sys
import getpass
import re
import shutil
import uuid
from __version__ import __version__


class AppConfig:
    def __init__(self):
        self.app_title = 'Hamster'
        self.app_title_emoji = f'🐹 {self.app_title}'
        self.app_caption = 'Instantly Launch JMeter Test Plans'
        self.app_caption_emoji = f'{self.app_caption} 🚀'
        self.app_version = __version__
        self.buy_me_a_coffee_url = 'https://www.buymeacoffee.com/QAInsights'
        self.authors = ['NaveenKumar Namachivayam', 'Leela Prasad Vadla']
        self.about_website = 'https://QAInsights.com'
        self.app_uuid = str(uuid.uuid4())

    @property
    def authors_str(self):
        return '\n'.join(self.authors)

    @property
    def about_text(self):
        return f'''{self.app_title_emoji} - {self.app_caption_emoji}\n\n
    Authors:\n{self.authors_str}\n\n{self.about_website}
            '''

    @property
    def help_text(self):
        return '''
Hamster is a menu bar app to instantly launch JMeter test plans.\n\n
1. Configure `JMETER_HOME` by launching `Hamster > Edit JMETER_HOME`\n
2. To launch JMeter, click on `Hamster > Launch JMeter`\n
3. To launch JMeter test plans, click on `Hamster > Recent Test Plans > select the test plan`.\n
4. To view the configuration, click on `Hamster > View Config`\n
5. To restart Hamster, click on `Hamster > Refresh`\n
6. To know more about Hamster, click on `Hamster > About`\n
7. To quit Hamster, click on `Hamster > Quit`\n
'''


# Hamster's template properties file
app_properties_template = ".hamster_app.properties"

# Get the path to the user's home directory
home_dir = os.path.expanduser("~")

# Define the source path (current directory)
source_path = os.path.join(os.path.dirname(sys.argv[0]), app_properties_template)

# Define the destination path (user's home directory)
properties_file_path = os.path.join(home_dir, app_properties_template)

# Use shutil to copy the file if file doesn't exist
if not os.path.exists(properties_file_path):
    shutil.copy(source_path, properties_file_path)

config_parser = configparser.ConfigParser()
config_parser.read(properties_file_path)

icon_path = os.path.join(os.path.dirname(sys.argv[0]), 'img/hamster.png')
username = getpass.getuser()
pattern = re.compile("recent_file_.*")

jmeter_plist = f"/Users/{username}/Library/Preferences/org.apache.jmeter.plist"

app_config = AppConfig()
uuid = app_config.app_uuid

def jmeter_path():
    jmeter_home = config_parser.get('JMETER', 'HOME').strip()

    if jmeter_home.endswith('/'):
        jmeter_home = jmeter_home.rstrip('/')
    jmeter_bin = jmeter_home + '/bin/jmeter'
    return jmeter_home, jmeter_bin

