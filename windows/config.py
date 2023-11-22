import os
import re

app_title = 'Hamster'
app_title_emoji = f'🐹 {app_title}'
app_caption = 'Instantly Launch JMeter Test Plans'
app_caption_emoji = f'{app_caption} 🚀'
app_properties_template = "hamster_app.properties"
win_app_properties = app_properties_template.replace(".properties", ".ini")
home_dir = os.path.expanduser("~")

jmeter_recent_files_pattern = re.compile("recent_file_.*")
