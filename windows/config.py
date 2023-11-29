import re

from collections import OrderedDict
from pathlib import Path
# from windows import __VERSION__


class AppConfig:
    def __init__(self):
        self.app_title = 'Hamster'
        self.app_title_emoji = f'🐹 {self.app_title}'
        self.app_caption = 'Instantly Launch JMeter Test Plans'
        self.app_caption_emoji = f'{self.app_caption} 🚀'
        self.app_properties_template = "hamster_app.properties"
        self.win_app_properties = self.app_properties_template.replace(".properties", ".ini")
        self.home_dir = Path.home()
        self.menu_items_dict = OrderedDict()

        self.jmeter_recent_files_pattern = re.compile("recent_file_.*")
        self.app_version = "0.1.0"
        self.buy_me_a_coffee_url = 'https://www.buymeacoffee.com/QAInsights'
        self.authors = ['NaveenKumar Namachivayam', 'Leela Prasad Vadla']
        self.about_website = 'https://QAInsights.com'

    @property
    def authors_str(self):
        return '\n'.join(self.authors)

    @property
    def about_text(self):
        return f'''{self.app_title_emoji} - {self.app_caption_emoji}\n\n
Authors:\n{self.authors_str}\n\n{self.about_website}
        '''

    @property
    def help_text(self):
        return '''
Hamster is a menu bar app to instantly launch JMeter test plans.\n\n
1. Configure `JMETER_HOME` by launching `Hamster > Edit JMETER_HOME`\n
2. To launch JMeter, click on `Hamster > Launch JMeter`\n
3. To launch JMeter test plans, click on `Hamster > Recent Test Plans > select the test plan`.\n
4. To view the configuration, click on `Hamster > View Config`\n
5. To restart Hamster, click on `Hamster > Refresh`\n
6. To know more about Hamster, click on `Hamster > About`\n
7. To refresh the recent test plans, click on `Hamster > Restart`\n
8. To quit Hamster, click on `Hamster > Quit`\n
        '''


app_config = AppConfig()
