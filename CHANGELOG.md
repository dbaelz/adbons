# Changelog
A wrapper for the [Android adb tool](https://developer.android.com/studio/command-line/adb.html). It's just adb on steroids.

## 0.3.0 (2017-08-23)
Expand features and fix minor bugs

#### Added
- Show the current date with `adbons date`.
- Select a device from the devices list with the `--index` option

#### Changed
- Show the index and a description when `adbons devices` is executed.

#### Fixed
- Fix an evaluation bug in `adbons config --show`.


## 0.2.0 (2017-07-25)
Add more features and tests

#### Added
- Show the help, when `adbons` is invoked without a command.
- Print the current version with `adbons --version`.
- Take a screen capture and saves it into a file with `adbons screencap <filename>`.
- Show the set config values with `adbons config --show`.
- Unit tests for the commands.


## 0.1.0 (2017-07-11)
Add more features and internal restructuring.

#### Added
- Execute every adb command with `adbons adb <ADB_COMMAND>`.
- Input a text with `adbons text <text>`.
- Input a key event with `adbons key <text>`.


## 0.0.1 (2017-07-09)
Initial public release with a basic feature set. Still a beta version and work in progress. See [README](README.md) and `adbons --help` for further information.

#### Added
- Set device and app id and save it into a config file. This file could be stored locally or globally.
- List all available devices.
- Kill (force-stop) an app.
- Kill all background processes.
- Clear the app data.
