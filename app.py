import rumps
import configparser
import plistlib
import os
import re

configparser = configparser.ConfigParser()
configparser.read('app.properties')

jmeter_plist = configparser.get('JMETER', 'PLIST')
jmeter_home = configparser.get('JMETER', 'HOME')
jmeter_path = jmeter_home + '/bin/jmeter'

pattern = re.compile("recent_file_.*")

class DynamicMenuApp(rumps.App):
    def __init__(self, title, menu_items):
        super(DynamicMenuApp, self).__init__(title, icon="hamster.png", quit_button='Quit')
        self.menu = ['Just JMeter', None] + [rumps.MenuItem(item, callback=self.menu_callback) for item in menu_items] + [None, "About"] 
        
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

    with open(jmeter_plist, 'rb') as fp:
        pl = plistlib.load(fp)
        recent_files = {k: v for k, v in pl['/org/apache/jmeter/']["gui/"]["action/"].items() if pattern.match(k)}
        # enclose double quotes for file names with spaces
        recent_files = {k: v.replace(' ', '\\ ') for k, v in recent_files.items()}        
        recent_files = dict(sorted(recent_files.items()))
        recent_files = list(recent_files.values())
    return recent_files

if __name__ == "__main__":
    
    menu_items = get_recent_jmeter_test_plans()
    DynamicMenuApp("JMeter", menu_items).run()
    