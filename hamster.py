from pathlib import Path
import subprocess
import configparser
import plistlib
import os
import re
import sys
import psutil
import time
import getpass

import rumps

configparser = configparser.ConfigParser()
properties_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'app.properties')
configparser.read(properties_file_path)

username = getpass.getuser()
jmeter_plist = f"/Users/{username}/Library/Preferences/org.apache.jmeter.plist"
jmeter_home = configparser.get('JMETER', 'HOME')
jmeter_path = jmeter_home + '/bin/jmeter'
icon_path=os.path.join(os.path.dirname(sys.argv[0]), 'hamster.png')

pattern = re.compile("recent_file_.*")

def show_splash_screen():
    welcome_message = '''
    ---------------------
    Hamster is a menu bar app to instantly launch JMeter test plans.
    ---------------------

    1. Configure `JMETER_HOME` by launching `Hamster > Edit JMETER_HOME`

    2. To launch JMeter, click on `Hamster > Just JMeter`

    3. To launch JMeter test plans, click on `Hamster > select the test plan`.

    4. To view the configuration, click on `Hamster > View Config`

    5. To restart Hamster, click on` Hamster > Restart`

    6. To quit Hamster, click on `Hamster > Quit`

    7. To know more about Hamster, click on `Hamster > About`

    8. To refresh the recent test plans, click on `Hamster > Restart`

    '''
    rumps.alert(title="Welcome to Hamster 🐹", message=welcome_message, icon_path=icon_path, ok="Got it!")

# Function to update properties in app.properties
def update_properties(properties):
    for key, value in properties.items():
        configparser['JMETER'][key] = value

    with open(properties_file_path, 'w') as config_file:
        configparser.write(config_file)


class DynamicMenuApp(rumps.App):
    def __init__(self, title, menu_items):
        super(DynamicMenuApp, self).__init__(title, icon=icon_path, quit_button='Quit')
        self.menu = ['Just JMeter', None] + [rumps.MenuItem(item, callback=self.menu_callback) for item in menu_items] \
                    + [None, 'View Config', 'Edit JMETER_HOME'] + [None, 'Restart', 'About']
    
    @rumps.clicked("Restart")
    def restart(self, _):
        restart(1)

    @rumps.clicked("View Config")
    def view_config(self, _):
        try:
            j_home = configparser.get('JMETER', 'HOME')
            rumps.alert(title="Hamster Configuration", message=f"JMETER_HOME: {j_home}\n", icon_path=icon_path)
            restart(1)
        except Exception as e:
            rumps.alert("Error", e)

    @rumps.clicked("Edit JMETER_HOME")
    def edit_home_path(self, _):
        try:
            window_builder = rumps.Window(message='Enter absolute JMETER_HOME path', cancel="Cancel", dimensions=(300, 100))
            window_builder.default_text = configparser.get('JMETER', 'HOME')
            window_builder.icon = icon_path
            window_builder.title = "Configure JMETER_HOME"

            response = window_builder.run()
            if response.clicked:
                update_properties({'HOME': str(response.text)})
                configparser.read(properties_file_path)
        except Exception as e:
            rumps.alert("Error", e)

    def menu_callback(self, sender):
        try:
            subprocess.Popen([jmeter_path, '-t', sender.title], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            restart(5)
        except Exception as e:
            rumps.alert("Error", e)
    
    @rumps.clicked("Just JMeter")
    def just_jmeter(self, _):
        try:
            subprocess.Popen([jmeter_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            rumps.alert("Error", e)
    
    @rumps.clicked("About")
    def about(self, _):
        rumps.alert("Hamster - instantly launch JMeter test plans 🚀", \
                    "Version 0.1\n\nAuthor: NaveenKumar Namachivayam\n\nhttps://qainsights.com", icon_path=icon_path) 

def restart(delay):
    if delay:
        time.sleep(delay)
    else:
        time.sleep(1)
    python = sys.executable
    psutil.Popen([python] + sys.argv)
    psutil.Process(os.getpid()).terminate()   

def refresh_plist(plist_path):
    with open(plist_path, 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)
    return plist_data

def get_recent_jmeter_test_plans():
    """
    Returns a list of recently opened JMeter test plans.

    Reads the JMeter plist file specified in the configuration and extracts the list of recently opened test plans.
    The list is sorted in ascending order of the file names.

    Returns:
        list: A list of recently opened JMeter test plans.
    """
    configparser.read(properties_file_path)
    
    recent_files = []

    p = Path(jmeter_plist)
    if p.exists():
        refresh_plist(jmeter_plist)
        try:
            with open(jmeter_plist, 'rb') as fp:
                pl = plistlib.load(fp)
                recent_files = {k: v for k, v in pl['/org/apache/jmeter/']["gui/"]["action/"].items() if pattern.match(k)}

                # escape file names with spaces
                recent_files = {k: v.replace(' ', '\\ ') for k, v in recent_files.items()}
                recent_files = dict(sorted(recent_files.items()))
                recent_files = list(recent_files.values())
                
                # check if recent_files is empty
                if not recent_files:
                    recent_files.append("No recent JMeter test plans files found.")
        except Exception as e:
            rumps.alert("Error", e)
        
    return recent_files

def prechecks(jmeter_plist, jmeter_home, jmeter_path):
    """
    Checks if the required configuration is set.
    """
    validation_status = False
    precheck = [jmeter_plist, jmeter_home, jmeter_path]
    for check in precheck:
        if not check:
            validation_status = True
            break
    return validation_status


    
if __name__ == "__main__":
    show_splash_screen()
    prechecks(jmeter_plist, jmeter_home, jmeter_path)    
    menu_items = get_recent_jmeter_test_plans()
    DynamicMenuApp("JMeter", menu_items).run()
    
