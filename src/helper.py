import subprocess
import yaml


def get_device_ids():
    output = subprocess.check_output(["adb", "devices"]).splitlines()
    # Delete header text and empty last line
    del output[0]
    del output[len(output) - 1]
    lines = []
    for line in output:
        lines.append(line.split("\t")[0].strip())
    return lines


def read_value_from_config(section, key):
    with open(".adbons.yml", 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)
    try:
        return config[section][key]
    except:
        return ""


def write_value_to_config(section, key, value):
    try:
        with open(".adbons.yml", 'r+') as ymlfile:
            config = yaml.safe_load(ymlfile)
        if section not in config:
            config[section] = {}
        config[section][key] = value
    except:
        print("except")
        config = {}
        config[section] = {}
        config[section][key] = value

    with open(".adbons.yml", 'w') as ymlfile:
        yaml.dump(config, ymlfile, default_flow_style=False)
