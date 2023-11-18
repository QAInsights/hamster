import config, menu, utils


def main():
    """
    Entry point of the Hamster - menu bar application.
    """
    menu_builder = menu.DynamicMenuApp("JMeter")
    menu_builder.run()


if __name__ == "__main__":
    main()
