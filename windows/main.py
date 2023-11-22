from collections import OrderedDict

from PIL import Image
from pystray import MenuItem, Menu, Icon

from config import app_title, app_caption
from utils import get_recent_test_plans, create_app_data_dir, action_launch_jmeter, action_recent_test_plan, \
    action_view_config, action_edit_config, action_refresh, action_quit

menu_items_dict = OrderedDict()


def main():
    """
    The main function of the application. It creates a system tray icon with a context menu.
    The context menu includes options to launch JMeter, view recent test plans, view and edit configuration, refresh, and quit the application.
    Returns:

    """
    global menu_items_dict
    image = Image.open("img/hamster.png")
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
