import yaml

SECTION_APP = "app"
SECTION_DEVICE = "device"
KEY_DEFAULT = "default"


def read_value(section, key):
    try:
        with open(".adbons.yml", 'r') as ymlfile:
            config = yaml.safe_load(ymlfile)
        return config[section][key]
    except:
        pass


def write_value(section, key, value):
    try:
        with open(".adbons.yml", 'r+') as ymlfile:
            config = yaml.safe_load(ymlfile)
        if section not in config:
            config[section] = {}
        config[section][key] = value
    except:
        config = {}
        config[section] = {}
        config[section][key] = value

    with open(".adbons.yml", 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False)
