# About adbons
A wrapper for the [Android adb tool](https://developer.android.com/studio/command-line/adb.html). It's just adb on steroids.

## Features
Currently only some basic features are provided. These features should simplify and shorten the required adb commands.

Example workflow to kill an app when multiple devices are connected:
* A default device and app id is set in the config. This information is saved in a `.adbons.yml` file. The file is either stored local (working dir) or global (`~/.adbons/`).
* Execute the kill command. With saved values, the app is just killed with `adbons kill` instead of `adb -s <device> shell am force-stop <app id>`.

## Install
Install adbons with [pip](https://pypi.python.org/pypi/pip) for Python 3 (usually `pip` or `pip3`):
```
$ pip3 install adbons
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
adbons is a Python 3.5 (and above) command line tool. It's still work in progress. Any suggestions, feature requests, bug reports or pull requests are very much appreciated.

### Getting started
A short introduction how to develop for adbons. If you have any questions feel free to contact me.
- Optional: Create/activate a [virtual environment](https://docs.python.org/3.5/library/venv.html)
- Fork and clone adbons
- Switch to a feature branch (usually branched from develop)
- Read the [Click documentation](http://click.pocoo.org/6/)
- Add your cool feature/bugfix/whatever
- Create a [pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)

### Testing
There are some tests for the adbons commands. These tests are executed with `python -m unittest`. For information who to write unit tests see the Click documentation.

## License
adbons is licensed under the [BSD License](https://github.com/dbaelz/adbons/blob/master/LICENSE).
