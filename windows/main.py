import shutil
import configparser
import re
import time
import winreg
import subprocess
import os

from collections import OrderedDict
from tkinter import filedialog, messagebox
from PIL import Image
from pystray import MenuItem, Menu, Icon
from contextlib import suppress

# Declarations
jmeter_recent_files_pattern = re.compile("recent_file_.*")

app_title = 'Hamster'
app_title_emoji = '🐹 Hamster'
app_caption = 'Instantly Launch JMeter Test Plans'
app_caption_emoji = 'Instantly Launch JMeter Test Plans 🚀'
app_properties_template = "hamster_app.properties"
win_app_properties = app_properties_template.replace(".properties", ".ini")
home_dir = os.path.expanduser("~")

config_parser = configparser.ConfigParser()
properties_folder_path = os.path.join(home_dir, 'Appdata', 'Local', app_title)
properties_file_path = os.path.join(home_dir, 'Appdata', 'Local', app_title, win_app_properties)

menu_items_dict = OrderedDict()


def create_app_data_dir():
    # create app data dir in user home\appdata\local
    if not os.path.exists(properties_folder_path):
        os.makedirs(properties_folder_path)
        # check for ini file inside the app data dir
    if not os.path.exists(os.path.join(properties_folder_path, win_app_properties)):
        # copy the hamster_app.properties file to the app data dir
        print(f'Copying {app_properties_template} to {properties_folder_path}')
        source_file = os.path.join(os.getcwd(), app_properties_template)
        destination_file = os.path.join(properties_folder_path, win_app_properties)
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


def get_recent_test_plans():
    recent_test_plans = []
    key_path = r'Software\JavaSoft\Prefs\org\apache\jmeter\gui\action'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            index = 0
            while True:
                try:
                    value_name, value_data, _ = winreg.EnumValue(key, index)
                    if re.match(jmeter_recent_files_pattern, value_name):
                        clean_jmeter_path = value_data.replace('///', '\\').replace('//', '\\').replace('/', '')
                        recent_test_plans.append(clean_jmeter_path)
                    index += 1
                except OSError as e:
                    with suppress(OSError):
                        winreg.CloseKey(key)
                    if e.errno == 259:  # No more data is available
                        break
                    break
    except FileNotFoundError:
        print(f"Error: Registry key '{key_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    return recent_test_plans


def launch_test_plan(plan):
    # launch jmeter with the test plan
    jmeter_plan = f"{plan}"
    config_parser.read(properties_file_path)
    jmeter_home = config_parser['JMETER']['HOME']
    jmeter_bin = os.path.join(jmeter_home, 'bin')
    jmeter_logs = os.path.join(jmeter_bin, 'jmeter.log')
    jmeter_path = os.path.join(jmeter_bin, 'jmeter.bat')
    if plan is None:
        subprocess.Popen([jmeter_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print(f'Launching JMeter with {jmeter_path} {jmeter_logs} {jmeter_plan} ')
        subprocess.Popen([jmeter_path, "-j", jmeter_logs, "-t", plan], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return


def action_launch_jmeter(icon, menu_item):
    launch_test_plan(plan=None)


def action_recent_test_plan(icon, menu_item):
    launch_test_plan(menu_item.text)
    refresh_test_plans(icon)


def action_refresh(icon, _):
    refresh_test_plans(icon, 0)


def action_view_config():
    __jmeter_home = read_properties()
    messagebox.showinfo("Hamster Config", f"JMeter Home: {__jmeter_home}")


def action_edit_config():
    _default_jmeter_home = read_properties()
    _jmeter_home = filedialog.askdirectory(initialdir=_default_jmeter_home, mustexist=True,
                                           title=f"{app_title} - Configure JMETER_HOME")
    if _jmeter_home:
        update_properties({'HOME': str(_jmeter_home).strip()})


def action_quit(icon, _):
    icon.stop()


def refresh_test_plans(icon, delay=5):
    global menu_items_dict
    time.sleep(delay)
    updated_test_plans = get_recent_test_plans()
    refreshed_test_plans_menu_items = [MenuItem(plan, action_recent_test_plan) for plan in updated_test_plans]
    menu_items_dict["Recent Test Plans"] = MenuItem('Recent Test Plans', Menu(*refreshed_test_plans_menu_items))
    icon.menu = Menu(*menu_items_dict.values())


def main():
    global menu_items_dict
    image = Image.open("hamster.png")
    recent_test_plans = get_recent_test_plans()
    recent_test_plans_menu_items = [MenuItem(plan, action_recent_test_plan) for plan in recent_test_plans]

    menu_items_dict.update({
        "Launch JMeter": MenuItem('🚀 Launch JMeter', action_launch_jmeter),
        "Recent Test Plans": MenuItem('Recent Test Plans', Menu(*recent_test_plans_menu_items)),
        "Seperator01": Menu.SEPARATOR,
        "View Config": MenuItem('View Config', action_view_config),
        "Configure JMETER_HOME": MenuItem('Configure JMETER_HOME', action_edit_config),
        "Seperator02": Menu.SEPARATOR,
        "Refresh": MenuItem('Refresh', action_refresh),
        "Quit": MenuItem('Quit', action_quit)
    })

    # Create the menu with the menu items
    menu = Menu(*menu_items_dict.values())

    # Create the icon with the menu
    icon = Icon("Hamster", image, f"{app_title} - {app_caption}", menu)
    icon.run()


if __name__ == "__main__":
    create_app_data_dir()
    main()
