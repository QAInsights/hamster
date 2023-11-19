import menu
import os


def main():
    """
    Entry point of the Hamster - menu bar application.
    """
    # Get the path to the user's home directory
    home_dir = os.path.expanduser("~")

    # Create a new directory within the home directory
    app_dir = os.path.join(home_dir, "HamsterApp")
    os.makedirs(app_dir, exist_ok=True)

    # Specify the path to the properties file within the new directory
    properties_file = os.path.join(app_dir, "app.properties")

    menu_builder = menu.DynamicMenuApp("JMeter")
    menu_builder.run()


if __name__ == "__main__":
    main()
