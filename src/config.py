import os
import yaml

SECTION_APP = "app"
SECTION_DEVICE = "device"
KEY_DEFAULT = "default"

__CONFIG_GLOBAL_DIR = os.path.expanduser("~") + "/.adbons/"
__CONFIG_FILE_NAME = ".adbons.yml"


def read_value(use_global, section, key):
    try:
        with open(__get_filename(use_global), 'r') as ymlfile:
            config = yaml.safe_load(ymlfile)
        return config[section][key]
    except:
        pass


def write_value(use_global, section, key, value):
    try:
        with open(__get_filename(use_global), 'r+') as ymlfile:
            config = yaml.safe_load(ymlfile)
        if section not in config:
            config[section] = {}
        config[section][key] = value
    except:
        config = {}
        config[section] = {}
        config[section][key] = value

    with open(__get_filename(use_global), 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False)


def __get_filename(use_global):
    filename = ""
    if use_global:
        filename += __CONFIG_GLOBAL_DIR
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    filename += __CONFIG_FILE_NAME
    return filename
