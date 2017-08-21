import subprocess


class Adb:
    ADB_COMMAND = "adb"
    ADB_COMMAND_DEVICES = "devices"

    # activity manager
    ADB_COMMAND_KILL = ["shell", "am", "force-stop"]
    ADB_COMMAND_KILL_ALL = ["shell", "am", "kill-all"]

    # package manager
    ADB_COMMAND_CLEAR_APP_DATA = ["shell", "pm", "clear"]

    # input
    ADB_COMMAND_INPUT_PREFIX = ["shell", "input"]
    ADB_INPUT_SOURCE_TOUCHSCREEN = "touchscreen"
    ADB_INPUT_SOURCE_KEYBOARD = "keyboard"

    ADB_COMMAND_SCREENCAP = ["exec-out", "screencap", "-p"]

    ADB_COMMAND_DATE = ["shell", "date"]

    @staticmethod
    def __command(device, app, adb_command):
        command = [Adb.ADB_COMMAND]
        if device:
            command.append("-s")
            command.append(device)
        command.extend(adb_command)
        if app:
            command.append(app)
        return command

    @staticmethod
    def adb_command(command):
        command = list(command)
        command.insert(0, Adb.ADB_COMMAND)
        subprocess.run(command)

    @staticmethod
    def get_devices_as_list():
        output = subprocess.run([Adb.ADB_COMMAND, Adb.ADB_COMMAND_DEVICES],
                                check=True,
                                stdout=subprocess.PIPE).stdout.decode(
                                    "utf-8").splitlines()
        # Delete header text and empty last line
        del output[0]
        del output[len(output) - 1]
        devices = []
        for line in output:
            devices.append(line.split("\t"))
        return devices

    @staticmethod
    def kill_app(device, app):
        subprocess.run(Adb.__command(device, app, Adb.ADB_COMMAND_KILL))

    @staticmethod
    def kill_all(device):
        subprocess.run(Adb.__command(device, None, Adb.ADB_COMMAND_KILL_ALL))

    @staticmethod
    def clear_app_data(device, app):
        subprocess.run(Adb.__command(device, app,
                                     Adb.ADB_COMMAND_CLEAR_APP_DATA))

    @staticmethod
    def input_text(device, source, text):
        command = Adb.ADB_COMMAND_INPUT_PREFIX
        if source is not None:
            command.append(source)
        command.append("text")
        command.append(text)
        subprocess.run(Adb.__command(device, None, command))

    @staticmethod
    def input_keyevent(device, keyevent):
        command = Adb.ADB_COMMAND_INPUT_PREFIX
        command.append("keyevent")
        command.append(keyevent)
        subprocess.run(Adb.__command(device, None, command))

    @staticmethod
    def screencap(device, output):
        with open(output, 'w') as output_file:
            subprocess.run(Adb.__command(device, None,
                                         Adb.ADB_COMMAND_SCREENCAP),
                           stdout=output_file)

    @staticmethod
    def show_date(device, utc):
        command = Adb.__command(device, None, Adb.ADB_COMMAND_DATE)
        if utc:
            command.append("-u")
        subprocess.run(command)
