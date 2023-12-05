import os
import webbrowser
import logging
import requests
from functools import wraps

import rumps
import subprocess
from utils import update_properties, show_splash_screen, prechecks, get_recent_jmeter_test_plans, sleep, \
    get_telemetry_config
from config import jmeter_path, icon_path, properties_file_path, config_parser, jmeter_plist
from config import app_config, uuid

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


def track(ids, menu_item):
    telemetry_enabled = get_telemetry_config()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if telemetry_enabled:
                    # Call AWS Lambda function
                    try:
                        if menu_item in app_config.valid_events:
                            requests.post(app_config.telemetry_url, json={
                            "uuid": ids,
                            "menu_item": menu_item
                            })

                            logger.info(f'Clicked {menu_item}')
                            return func(*args, **kwargs)

                    except Exception as e:
                        logger.error(e)

                else:
                    logger.info(f"Telemetry is disabled. Not tracking {menu_item}")
                    return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)

        return wrapper
    return decorator


class DynamicMenuApp(rumps.App):
    """
    A class representing a dynamic menu application.

    Attributes:
        title (str): The title of the application.

    Methods:
        __init__(self, title, menu_items): Initializes the DynamicMenuApp object.
        restart(self, _): Restarts the application.
        help(self, _): Displays the help screen.
        view_config(self, _): Displays the configuration of the application.
        edit_home_path(self, _): Allows the user to edit the JMETER_HOME path.
        menu_callback(self, sender): Callback function for menu items.
        just_jmeter(self, _): Launches JMeter without any test plan.
        about(self, _): Displays information about the application.
    """

    def __init__(self, title):
        super(DynamicMenuApp, self).__init__(title, icon=icon_path, quit_button='Quit')
        self.menu = ['Launch JMeter', 'Recent Test Plans', None, 'View Config', 'Edit JMETER_HOME', None,
                     'Refresh', 'Buy me a Coffee', 'Help', 'About']
        self.jmeter_home, self.jmeter_bin = jmeter_path()
        prechecks(jmeter_plist, self.jmeter_home, self.jmeter_bin)
        self.refresh_test_plans(delay=1)

    def refresh_test_plans(self, delay=5):
        """
        Refreshes Recent Test Plans Menu Items
        Args:
            delay: in seconds, defaults to 5

        Returns: None

        """
        sleep(delay)
        recent_test_plans_menu = self.menu["Recent Test Plans"]
        if recent_test_plans_menu:
            recent_test_plans_menu.clear()

        recent_test_plans = get_recent_jmeter_test_plans()
        if not len(recent_test_plans) > 0:
            recent_test_plans_menu.add(rumps.MenuItem("No recent JMeter test plans files found."))
            return

        for test_plan in recent_test_plans:
            recent_test_plans_menu.add(rumps.MenuItem(test_plan, callback=self.menu_callback))

    @rumps.clicked("Refresh")
    @track(uuid, "Refresh")
    def refresh(self, _):
        """
        Refreshes Test Plans
        """
        self.refresh_test_plans(1)

    @rumps.clicked("Help")
    @track(uuid, "Help")
    def help(self, _):
        """
        Displays the help screen.
        """
        show_splash_screen()

    @rumps.clicked("View Config")
    @track(uuid, "View Config")
    def view_config(self, _):
        """
        Displays the configuration of the application.
        """
        try:
            j_home = config_parser.get('JMETER', 'HOME')
            rumps.alert(title="Hamster Configuration", message=f"JMETER_HOME: {j_home}\n", icon_path=icon_path)
        except Exception as e:
            rumps.alert("Error", e)

    @rumps.clicked("Edit JMETER_HOME")
    @track(uuid, "Edit JMETER_HOME")
    def edit_home_path(self, _):
        """
        Allows the user to edit the JMETER_HOME path.
        """
        try:
            window_builder = rumps.Window(message='Enter absolute JMETER_HOME path', cancel="Cancel",
                                          dimensions=(300, 100))
            window_builder.default_text = config_parser.get('JMETER', 'HOME')
            window_builder.icon = icon_path
            window_builder.title = "Configure JMETER_HOME"
            response = window_builder.run()

            if response.clicked:
                updated_jmeter_home = response.text.strip()
                update_properties({'HOME': str(updated_jmeter_home)})
                config_parser.read(properties_file_path)
                self.jmeter_home, self.jmeter_bin = jmeter_path()
                self.refresh_test_plans(1)
        except Exception as e:
            rumps.alert("Error", e)

    @track(uuid, "Recent Test Plans")
    def menu_callback(self, sender):
        """
        Callback function for menu items.
        """
        try:
            subprocess.Popen([self.jmeter_bin, '-t', sender.title], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
            self.refresh_test_plans()
        except Exception as e:
            rumps.alert("Error", e)

    @rumps.clicked("Launch JMeter")
    @track(uuid, "Launch JMeter")
    def just_jmeter(self, _):
        """
        Launches JMeter without any test plan.
        """
        try:
            subprocess.Popen([self.jmeter_bin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            rumps.alert("Error", e)

    @rumps.clicked("Buy me a Coffee")
    @track(uuid, "Buy me a Coffee")
    def sponsor(self, _):
        """
        Displays information about the application.
        """
        webbrowser.open_new_tab(app_config.buy_me_a_coffee_url)

    @rumps.clicked("About")
    @track(uuid, "About")
    def about(self, _):
        """
        Displays information about the application.
        """
        rumps.alert("About", f"{app_config.about_text}\n\n v{app_config.app_version}", icon_path=icon_path)
