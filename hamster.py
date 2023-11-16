import rumps
import configparser
import plistlib
import os
import re
import sys
from pathlib import Path

configparser = configparser.ConfigParser()
properties_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'app.properties')
configparser.read(properties_file_path)

jmeter_plist = configparser.get('JMETER', 'PLIST')
jmeter_home = configparser.get('JMETER', 'HOME')
jmeter_path = jmeter_home + '/bin/jmeter'

pattern = re.compile("recent_file_.*")


# Function to update properties in app.properties
def update_properties(properties):
    for key, value in properties.items():
        configparser['JMETER'][key] = value

    with open(properties_file_path, 'w') as config_file:
        configparser.write(config_file)


class DynamicMenuApp(rumps.App):
    def __init__(self, title, menu_items):
        super(DynamicMenuApp, self).__init__(title, icon="hamster.png", quit_button='Quit')
        self.menu = ['Just JMeter', None] + [rumps.MenuItem(item, callback=self.menu_callback) for item in menu_items] \
                    + [None, 'View Config', 'Edit JMeter HOME', 'Edit JMeter PLIST'] + [None, "About"]

    @rumps.clicked("View Config")
    def view_config(self, _):
        j_home = configparser.get('JMETER', 'HOME')
        j_plist = configparser.get('JMETER', 'PLIST')
        rumps.alert(title="JMeter Config", message=f"HOME: {j_home}\n\nPLIST: {j_plist}")

    @rumps.clicked("Edit JMeter HOME")
    def edit_home_path(self, _):
        window_builder = rumps.Window('Enter JMeter HOME path', cancel="Cancel", dimensions=(300, 100))
        window_builder.default_text = configparser.get('JMETER', 'HOME')
        response = window_builder.run()
        if response.clicked:
            update_properties({'HOME': str(response.text)})
            configparser.read(properties_file_path)

    @rumps.clicked("Edit JMeter PLIST")
    def edit_plist_path(self, _):
        window_builder = rumps.Window('Enter JMeter PLIST path', cancel="Cancel", dimensions=(300, 100))
        window_builder.default_text = configparser.get('JMETER', 'PLIST')
        response = window_builder.run()
        if response.clicked:
            update_properties({'PLIST': str(response.text)})
            configparser.read(properties_file_path)

    def menu_callback(self, sender):
        os.system(jmeter_path + ' -t ' + sender.title)
    
    @rumps.clicked("Just JMeter")
    def just_jmeter(self, _):
        os.system(jmeter_path)
    
    @rumps.clicked("About")
    def about(self, _):
        rumps.alert("Hamster - instantly launch JMeter test plans 🚀", "Version 0.1\n\nAuthor: NaveenKumar Namachivayam\n\nhttps://qainsights.com") 
    

def get_recent_jmeter_test_plans():
    """
    Returns a list of recently opened JMeter test plans.

    Reads the JMeter plist file specified in the configuration and extracts the list of recently opened test plans.
    The list is sorted in ascending order of the file names.

    Returns:
        list: A list of recently opened JMeter test plans.
    """
    jmeter_plist = configparser.get('JMETER', 'PLIST')
    recent_files = []

    p = Path(jmeter_plist)
    if p.exists():
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
    prechecks(jmeter_plist, jmeter_home, jmeter_path)
    
    menu_items = get_recent_jmeter_test_plans()
    DynamicMenuApp("JMeter", menu_items).run()
    
