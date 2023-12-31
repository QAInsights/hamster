import logging
import plistlib
import time
import rumps
import os
from config import app_config
from pathlib import Path
from config import properties_file_path, config_parser, jmeter_plist, pattern, icon_path

# Create a logger
logger = logging.getLogger(__name__)

# Set the log level
logger.setLevel(logging.DEBUG)

# Create a file handler
handler = logging.FileHandler(os.path.join(app_config.log_dir, 'hamster.log'))

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)


def sleep(delay=1):
    time.sleep(delay)


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
        list: A list of recently opened JMeter test plans. If no recent test plans are found, the list will contain
        a single string indicating that no recent JMeter test plans files were found.
    """
    config_parser.read(properties_file_path)

    recent_files = []

    p = Path(jmeter_plist)
    if p.exists():
        refresh_plist(jmeter_plist)
        try:
            with open(jmeter_plist, 'rb') as fp:
                pl = plistlib.load(fp)
                recent_files = {k: v for k, v in pl['/org/apache/jmeter/']["gui/"]["action/"].items() if
                                pattern.match(k)}

                # escape file names with spaces
                recent_files = {k: v for k, v in recent_files.items()}
                recent_files = dict(sorted(recent_files.items()))
                recent_files = list(recent_files.values())

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


# Function to update properties in .hamster_app.properties
def update_properties(properties):
    for key, value in properties.items():
        config_parser['JMETER'][key] = value

    with open(properties_file_path, 'w') as config_file:
        config_parser.write(config_file)


def get_telemetry_config():
    """
    Returns the telemetry configuration.
    """

    try:
        config_parser.read(properties_file_path)
        return config_parser.getboolean('TELEMETRY', 'enabled')
    except Exception as e:
        logging.error(f"{e} Telemetry config not found. Setting telemetry to False.")
        return False

