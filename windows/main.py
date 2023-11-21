import shutil
import sys
import configparser
import re
import pystray
import winreg
import subprocess
import os

import tkinter as tk
from tkinter import simpledialog

from PIL import Image
from pystray import MenuItem as item

jmeter_recent_files_pattern = re.compile("recent_file_.*")
jmeter_home = r'C:\Tools\apache-jmeter-5.6.2\bin\jmeter.bat'
app_title = 'Hamster'
app_title_emoji = '🐹 Hamster'
app_caption = 'Instantly Launch JMeter Test Plans'
app_caption_emoji = 'Instantly Launch JMeter Test Plans 🚀'

app_properties_template = "hamster_app.ini"
home_dir = os.path.expanduser("~")

config_parser = configparser.ConfigParser()
properties_folder_path = os.path.join(home_dir, 'Appdata', 'Local', app_title)
properties_file_path = os.path.join(home_dir, 'Appdata', 'Local', app_title, app_properties_template)


def create_app_data_dir():
    # create app data dir in user home\appdata\local

    if not os.path.exists(properties_folder_path):
        os.makedirs(properties_folder_path)
        # check for ini file inside the app data dir
        if not os.path.isfile(os.path.join(properties_folder_path, app_properties_template)):
            # copy the hamster_app.ini file to the app data dir
            print(f'Copying {app_properties_template} to {properties_folder_path}')
            source_file = os.path.join(os.getcwd(), app_properties_template)
            destination_file = os.path.join(properties_folder_path, app_properties_template)
            shutil.copyfile(source_file, destination_file)


def update_properties(properties):
    config_parser.read(properties_file_path)
    for key, value in properties.items():
        print(f'Updating {key} with {value}')
        config_parser['JMETER'][key] = value

    with open(properties_file_path, 'w') as config_file:
        config_parser.write(config_file)


def read_properties():
    config_parser.read(properties_file_path)
    for key, value in config_parser['JMETER'].items():
        print(f'Reading {key} with {value}')
        return value


def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    properties = simpledialog.askstring(title=f"{app_title} - Configure JMETER_HOME", prompt=r"Please enter JMETER_HOME"
                                                                                             r" path e.g."
                                                                                             r"C:\Tools\apache-jmeter"
                                                                                             r"-5.6.2",
                                        initialvalue=read_properties())
    update_properties({'HOME': str(properties).strip()})


def get_recent_test_plans():
    recent_test_plans = []
    path = r'Software\JavaSoft\Prefs\org\apache\jmeter\gui\action'
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)
    i = 0
    while True:
        try:
            value_name, value_data, value_type = winreg.EnumValue(key, i)
            if re.match(jmeter_recent_files_pattern, value_name):
                # print(f'Name: {value_name}, Data: {value_data}, Type: {value_type}')
                clean_jmeter_path = value_data.replace('///', '\\').replace('//', '\\').replace('/', '')
                # print("Cleaned " + clean_jmeter_path)
                recent_test_plans.append(clean_jmeter_path)
            i += 1
        except OSError:
            break
    winreg.CloseKey(key)
    return recent_test_plans


def launch_test_plan(plan):
    # launch jmeter with the test plan
    jmeter_args = '-t'
    config_parser.read(properties_file_path)
    jmeter_home = config_parser['JMETER']['HOME']
    jmeter_path = os.path.join(jmeter_home, 'bin', 'jmeter.bat')
    print(f'Launching {jmeter_path}')
    if plan is None:
        subprocess.Popen([jmeter_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.Popen([jmeter_path, jmeter_args, plan], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return


def on_click(icon, menu_item):
    if str(menu_item).__contains__('Just JMeter'):
        launch_test_plan(plan=None)

    if str(menu_item).__contains__('.jmx'):
        launch_test_plan(str(menu_item))

    if str(menu_item).__contains__('Configure'):
        print('Configure JMETER_HOME')
        get_user_input()

    if str(menu_item) == 'Quit':
        icon.stop()


def main():
    image = Image.open("hamster.png")

    # Create the menu items
    menu_items = [item('🚀 Just JMeter', on_click), pystray.Menu.SEPARATOR]
    recent_test_plans = get_recent_test_plans()
    for idx, plan in enumerate(recent_test_plans, start=1):
        menu_items.append(item(plan, on_click))

    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(item('Configure JMETER_HOME', on_click))
    menu_items.append(item('Quit', on_click))

    # Create the menu with the menu items
    menu = pystray.Menu(*menu_items)

    # Create the icon with the menu
    icon = pystray.Icon("Hamster", image, f"{app_title} - {app_caption}", menu)
    icon.run()


if __name__ == "__main__":
    create_app_data_dir()
    main()
