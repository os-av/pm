import os
import platform
import configparser

class Settings:
    def __init__(self):
        directory = {
            "Linux": os.path.expanduser("~/.local/share/pm/"),
            "Windows": os.path.expanduser("~\\AppData\\pm\\"),
        }
        self.dir = directory.get(platform.system())
        self.settings_path = os.path.join(self.dir, "settings.ini")

    def create_settings(self):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        
        config = configparser.ConfigParser()
        config["pw_gen"] = {
            "len": "32",
            "upper": "true",
            "other": "true"
        }
        config["ui"] = {
            "use_images": "true"
        }

        with open(self.settings_path, "w") as f:
            config.write(f)

    def read_setting(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.settings_path)
        return config[section][key]

    def read_boolean_setting(self, section, key):
        config = configparser.ConfigParser()
        config.read(self.settings_path)
        return config.getboolean(section, key)

    def update_setting(self, section, key, value):
        config = configparser.ConfigParser()
        config.read(self.settings_path)
        config[section][key] = value 

        with open(self.settings_path, "w") as f:
            config.write(f)

    def settings_setup_required(self):
        if not os.path.exists(self.settings_path):
            return True
        return False
