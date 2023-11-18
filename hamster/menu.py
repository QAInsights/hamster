import rumps
import subprocess
from utils import restart, update_properties, show_splash_screen
from config import jmeter_path, icon_path, properties_file_path, config_parser


class DynamicMenuApp(rumps.App):
    """
    A class representing a dynamic menu application.

    Attributes:
        title (str): The title of the application.
        menu_items (list): A list of menu items.

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
    def __init__(self, title, menu_items):
        super(DynamicMenuApp, self).__init__(title, icon=icon_path, quit_button='Quit')
        self.menu = ['Just JMeter', None] + [rumps.MenuItem(item, callback=self.menu_callback) for item in menu_items] \
                    + [None, 'View Config', 'Edit JMETER_HOME'] + [None, 'Restart', None, 'Help', 'About']
    
    @rumps.clicked("Restart")
    def restart(self, _):
        """
        Restarts the application.
        """
        restart(1)

    @rumps.clicked("Help")
    def help(self, _):
        """
        Displays the help screen.
        """
        show_splash_screen()

    @rumps.clicked("View Config")
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
    def edit_home_path(self, _):
        """
        Allows the user to edit the JMETER_HOME path.
        """
        try:
            window_builder = rumps.Window(message='Enter absolute JMETER_HOME path', cancel="Cancel", dimensions=(300, 100))
            window_builder.default_text = config_parser.get('JMETER', 'HOME')
            window_builder.icon = icon_path
            window_builder.title = "Configure JMETER_HOME"

            response = window_builder.run()
            if response.clicked:
                update_properties({'HOME': str(response.text)})
                config_parser.read(properties_file_path)
        except Exception as e:
            rumps.alert("Error", e)

    def menu_callback(self, sender):
        """
        Callback function for menu items.
        """
        try:
            subprocess.Popen([jmeter_path, '-t', sender.title], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            rumps.alert("Error", e)
    
    @rumps.clicked("Just JMeter")
    def just_jmeter(self, _):
        """
        Launches JMeter without any test plan.
        """
        try:
            subprocess.Popen([jmeter_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            rumps.alert("Error", e)
    
    @rumps.clicked("About")
    def about(self, _):
        """
        Displays information about the application.
        """
        rumps.alert("Hamster - instantly launch JMeter test plans 🚀", \
                    "Version 0.1\n\nAuthor: NaveenKumar Namachivayam\n\nhttps://qainsights.com", icon_path=icon_path)
