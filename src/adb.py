import subprocess

ADB_COMMAND = "adb"
ADB_COMMAND_DEVICES = "devices"
ADB_COMMAND_KILL = ["shell", "am", "force-stop"]


def __command(device, app, adb_command):
    command = [ADB_COMMAND]
    if device:
        command.append("-s")
        command.append(device)
    command.extend(adb_command)
    command.append(app)
    return command


def list_devices():
    subprocess.run([ADB_COMMAND, ADB_COMMAND_DEVICES])


def get_device_ids():
    output = subprocess.run([ADB_COMMAND, ADB_COMMAND_DEVICES],
                            check=True, stdout=subprocess.PIPE).stdout.decode(
                                "utf-8").splitlines()
    # Delete header text and empty last line
    del output[0]
    del output[len(output) - 1]
    lines = []
    for line in output:
        lines.append(line.split("\t")[0].strip())
    return lines


def kill_app(device, app):
    subprocess.run(__command(device, app, ADB_COMMAND_KILL))
