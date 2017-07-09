# About adbons
A wrapper for the [Android adb tool](https://developer.android.com/studio/command-line/adb.html). It's just adb on steroids.

## Features
Currently only some basic features are provided. These features should simplify and shorten the required adb commands.

Example workflow to kill an app when multiple devices are connected:
* A default device and app id is set in the config. This information is saved in a `.adbons.yml` file. The file is either stored local (working dir) or global (`~/.adbons/`).
* Execute the kill command. With saved values, the app is just killed with `adbons kill` instead of `adb -s <device> shell am force-stop <app id>`.

## Install
Install adbons with `pip`/`pip3`:
```
$ pip install adbons
```

Install from source:
```
$ git clone https://github.com/dbaelz/adbons.git
$ cd adbons
$ pip install .
```

## Usage
See `adbons --help` for all currently available commands. The commands provide help pages as well (e.g. `adbons config --help`).


## Development
adbons is a Python 3.5 (and above) command line tool. It's currenlty in the beta phase and work in progress. Any suggestions, bug reports or pull requests are very much appreciated.

## License
adbons is licensed under the [BSD License](https://github.com/dbaelz/adbons/blob/master/LICENSE).
