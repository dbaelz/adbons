# About adbons
A wrapper for the [Android adb tool](https://developer.android.com/studio/command-line/adb.html). It's just adb on steroids.

## Features
adbons simplifies and shortens common Android `adb` commands by adding sensible defaults and easy device/app selection. It's meant for everyday workflows where you
would otherwise type long `adb` invocations over and over.

Example workflow to kill an app when multiple devices are connected:
- A default device and app id is set in the config. This information is saved in a `.adbons.yml` file. The file is either stored local (working dir) or global (`~/.adbons/`).
- Execute the kill command. With saved values, the app is just killed with `adbons kill` instead of `adb -s <device> shell am force-stop <app id>`.

## Install
Install the released package from PyPI:
```bash
pip3 install adbons
```

Requires Python 3.10 or newer.

Install from source (developer mode):
```bash
git clone https://github.com/dbaelz/adbons.git
cd adbons
pip install -e .
```

Build a release artifact locally (creates `dist/`):
```bash
python -m pip install --upgrade build
python -m build
```

Upload to TestPyPI or PyPI using `twine`:
```bash
python -m pip install --upgrade twine
# test upload
python -m twine upload --repository testpypi dist/*
# publish
python -m twine upload dist/*
```

Note: this project includes a `pyproject.toml` so it is compatible with modern Python build tools.

## Usage
Once installed, the `adbons` console script is available. Run `adbons --help` for all currently available commands. Individual commands provide help pages as well (e.g. `adbons config --help`).

### Commands

| Command | Description |
| --- | --- |
| `adb <args>` | Forward any arguments directly to `adb`. |
| `devices` | List all attached devices with their index, id and description. |
| `kill [-a/--app]` | Force-stop an app (defaults to the configured app if `-a` is omitted). |
| `kill-all` | Kill all background processes on the device. |
| `clear [-a/--app]` | Clear the app data. |
| `text <text>` | Send text input to the device. |
| `key <keyevent>` | Send a key event (value or constant). |
| `screencap <output>` | Take a screen capture and save it to a file. |
| `date` | Show the current date from the device. |
| `device-info` | Show selected device properties (use `--all` for every property). |
| `reboot` | Reboot the device (optionally with `-t/--target`). |

Commands that operate on a device accept `-d/--device <id>` or `-i/--index <n>` to select it. When neither is given, the configured default is used; if none is configured, a single attached device is selected automatically.

## Development - Getting started
- (Optional) Create/activate a virtual environment.
- Fork and clone the repository.
- Switch to a feature branch.
- Read the [Click documentation](https://click.palletsprojects.com/) for guidance on writing CLI commands.
- Add your feature/bugfix and run tests.
- Create a pull request.

### Testing
Unit tests are executed with Python's `unittest`:
```bash
python -m unittest discover -v
```

You can also run the project locally by installing it in editable mode (`pip install -e .`) and exercising the `adbons` command.

## License
adbons is licensed under the [BSD License](https://github.com/dbaelz/adbons/blob/master/LICENSE).
