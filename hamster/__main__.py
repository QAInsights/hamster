import config, menu, utils

def main():
    """
    Entry point of the Hamster - menu bar application.
    """
    utils.prechecks(config.jmeter_plist, config.jmeter_home, config.jmeter_path)    
    menu_items = utils.get_recent_jmeter_test_plans()
    menu.DynamicMenuApp("JMeter", menu_items).run()

if __name__ == "__main__":
    main()
