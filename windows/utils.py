import configparser
import os
import re
import shutil
import subprocess
import time
import webbrowser
import winreg
import logging

from collections import OrderedDict
from contextlib import suppress
from tkinter import filedialog, messagebox
from pystray import MenuItem, Menu
from config import app_config

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.DEBUG)

# Create a file handler
handler = logging.FileHandler(os.path.join(app_config.home_dir, 'Appdata', 'Local', 'hamster.log'))

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)

menu_items_dict = OrderedDict()

config_parser = configparser.ConfigParser()
properties_folder_path = os.path.join(app_config.home_dir, 'Appdata', 'Local', app_config.app_title)
properties_file_path = os.path.join(app_config.home_dir, 'Appdata', 'Local', app_config.app_title, app_config.win_app_properties)


def create_app_data_dir():
    """
    Creates the app data directory
    Returns:

    """
    # create app data dir in user home\appdata\local
    if not os.path.exists(properties_folder_path):
        os.makedirs(properties_folder_path)
        # check for ini file inside the app data dir
    if not os.path.exists(os.path.join(properties_folder_path, app_config.win_app_properties)):
        # copy the hamster_app.properties file to the app data dir
        logger.info(f'Copying { app_config.app_properties_template} to { app_config.properties_folder_path}')

        source_file = os.path.join(os.getcwd(),  app_config.app_properties_template)
        destination_file = os.path.join(properties_folder_path,  app_config.win_app_properties)
        logger.info(f'Copying {source_file} to {destination_file}')
        shutil.copyfile(source_file, destination_file)
        logger.info(f'Copied {source_file} to {destination_file}')


def update_properties(properties):
    """
    Updates the properties file
    Args:
        properties:

    Returns:

    """
    config_parser.read(properties_file_path)
    for key, value in properties.items():
        logger.info(f'Updating {key} with {value}')
        config_parser['JMETER'][key] = value

    with open(properties_file_path, 'w') as config_file:
        config_parser.write(config_file)


def read_properties():
    """
    Reads the properties file
    Returns:

    """
    config_parser.read(properties_file_path)
    for key, value in config_parser['JMETER'].items():
        logger.info(f'Reading {key} with {value}')
        return value


def get_recent_test_plans():
    """
    Gets the recent test plans from the registry
    Returns:

    """
    recent_test_plans = []
    key_path = r'Software\JavaSoft\Prefs\org\apache\jmeter\gui\action'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            index = 0
            while True:
                try:
                    value_name, value_data, _ = winreg.EnumValue(key, index)
                    if re.match( app_config.jmeter_recent_files_pattern, value_name):
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
        logger.critical(f"Error: Registry key '{key_path}' not found.")
    except Exception as e:
        logger.critical(f"Error: {e}")

    return recent_test_plans


def launch_test_plan(test_plan=None):
    """
    Launches JMeter with the selected test plan
    Args:
        test_plan:
    """
    # launch jmeter with the test plan
    jmeter_plan = f"{test_plan}"
    config_parser.read(properties_file_path)
    jmeter_home = config_parser['JMETER']['HOME']
    jmeter_bin = os.path.join(jmeter_home, 'bin')
    jmeter_logs = os.path.join(jmeter_bin, 'jmeter.log')
    jmeter_path = os.path.join(jmeter_bin, 'jmeter.bat')
    if not test_plan:
        subprocess.Popen([jmeter_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        logger.info(f'Launching JMeter with {jmeter_path} {jmeter_logs} {jmeter_plan} ')
        subprocess.Popen([jmeter_path, "-j", jmeter_logs, "-t", test_plan], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)


def action_launch_jmeter(icon, menu_item):
    """
    Launches JMeter
    Args:
        icon:
        menu_item:

    Returns:

    """
    launch_test_plan()


def action_recent_test_plan(icon, menu_item):
    """
    Launches JMeter with the selected test plan
    Args:
        icon:
        menu_item:

    Returns:

    """
    launch_test_plan(menu_item.text)
    refresh_test_plans(icon)


def action_refresh(icon, _):
    """
    Refreshes the recent test plans menu items
    Args:
        icon:
        _:

    Returns:

    """
    refresh_test_plans(icon, 0)


def action_view_config():
    """
    Displays the JMeter home directory
    Returns:

    """
    __jmeter_home = read_properties()
    messagebox.showinfo("Hamster Config", f"JMETER_HOME: {__jmeter_home}")


def action_edit_config():
    """
    Opens a file dialog to select the JMeter home directory
    Returns:

    """
    _default_jmeter_home = read_properties()
    _jmeter_home = filedialog.askdirectory(initialdir=_default_jmeter_home, mustexist=True,
                                           title=f"{ app_config.app_title} - Configure JMETER_HOME")
    if _jmeter_home:
        update_properties({'HOME': str(_jmeter_home).strip()})


def action_quit(icon, _):
    """
    Quits the application
    Args:
        icon:
        _:

    Returns:

    """
    icon.stop()


def action_help(help_text=None):
    """
    Displays the `help` dialog
    Returns:

    """
    messagebox.showinfo(f"About {app_config.app_title_emoji}", message=app_config.help_text, icon='info')


def action_about():
    """
    Displays the `about` dialog
    Returns:

    """
    messagebox.showinfo(f"About {app_config.app_title_emoji} - v{app_config.app_version}", f"{app_config.about_text}", icon='info')


def action_sponsor():
    """
    Opens the `buy me a coffee` link
    Returns:

    """
    webbrowser.open_new_tab(app_config.buy_me_a_coffee_url)


def refresh_test_plans(icon, delay=5):
    """
    Refreshes the recent test plans menu items
    Args:
        icon:
        delay:

    Returns:

    """
    time.sleep(delay)
    updated_test_plans = get_recent_test_plans()
    refreshed_test_plans_menu = [MenuItem(plan, action_recent_test_plan) for plan in updated_test_plans]
    app_config.menu_items_dict["Recent Test Plans"] = MenuItem('Recent Test Plans', Menu(*refreshed_test_plans_menu))
    icon.menu = Menu(*app_config.menu_items_dict.values())
