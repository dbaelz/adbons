import os
import yaml


class Config:
    SECTION_APP = "app"
    SECTION_DEVICE = "device"
    KEY_DEFAULT = "default"

    __CONFIG_GLOBAL_DIR = os.path.expanduser("~") + "/.adbons/"
    __CONFIG_FILE_NAME = ".adbons.yml"

    @staticmethod
    def read_value(section, key):
        if os.path.exists(Config.__filename(False)):
            # Check local file first
            value = Config.__read_value(False, section, key)
            if value is not None:
                return value
        if os.path.exists(Config.__filename(True)):
            # Check global file
            return Config.__read_value(True, section, key)

    @staticmethod
    def __read_value(use_global, section, key):
        try:
            with open(Config.__filename(use_global, False), 'r') as ymlfile:
                config = yaml.safe_load(ymlfile)
            return config[section][key]
        except:
            pass

    @staticmethod
    def write_value(use_global, section, key, value):
        try:
            with open(Config.__filename(use_global, True), 'r+') as ymlfile:
                config = yaml.safe_load(ymlfile)
            if section not in config:
                config[section] = {}
            config[section][key] = value
        except:
            config = {}
            config[section] = {}
            config[section][key] = value

        with open(Config.__filename(use_global, True), 'w') as ymlfile:
            yaml.dump(config, ymlfile, default_flow_style=False)

    @staticmethod
    def clear_value(use_global, section, key):
        if not os.path.exists(Config.__filename(use_global)):
            # File doesn't exist, so we skip the clear
            return

        try:
            with open(Config.__filename(use_global, True), 'r+') as ymlfile:
                config = yaml.safe_load(ymlfile)
                del config[section][key]
        except:
            return

        with open(Config.__filename(use_global, True), 'w') as ymlfile:
            yaml.dump(config, ymlfile, default_flow_style=False)

    @staticmethod
    def __filename(use_global, create_path=False):
        filename = ""
        if use_global:
            filename += Config.__CONFIG_GLOBAL_DIR
        else:
            filename += os.getcwd() + "/"
        filename += Config.__CONFIG_FILE_NAME

        if create_path:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        return filename
