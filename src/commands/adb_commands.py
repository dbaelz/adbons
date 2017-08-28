import click
import functools

from ..adb import Adb
from ..config import Config


def __get_id(option_id, section, key):
    if option_id is None:
        return Config.read_value(section, key)
    else:
        return option_id


def __get_device_id(ctx_params):
    # The device id to select the device
    device_id = None
    # The attached devices
    devices = Adb.get_devices_as_list()

    # No device attached, so return None
    if not devices:
        return None

    # First step: Resolve the options
    device_param = ctx_params["device"]
    index_param = ctx_params["index"]
    if device_param is not None and index_param is not None:
        raise click.UsageError("Only one of the options "
                               "--device or --index is allowed")
    elif device_param is not None:
        # Return the device param
        device_id = device_param
    elif index_param is not None:
        # Read the device id with the index
        try:
            device_id = devices[index_param][0]
        except IndexError:
            device_id = None

    # Second/Third step: When no suitable option is provided,
    # then read the local and global config
    if device_id is None:
        device_id = Config.read_value(Config.SECTION_DEVICE,
                                      Config.KEY_DEFAULT)

    if device_id is not None:
        # Check if the device with this device id is attached
        for attached_device in devices:
            # The device id is the first element
            if attached_device[0] == device_id:
                return device_id

    # Fourth step: When only one device is attached,
    # then select this device.
    if len(devices) == 1:
        # Only one device exists. So return the device id of this device
        return devices[0][0]
    else:
        # Multiple devices attached, so we can't select one
        return None


def option_device(func):
    @click.option("-d", "--device", type=click.STRING,
                  help="Use this device id.")
    @click.option("-i", "--index", type=click.INT,
                  help="Use this device index.")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def option_app(func):
    @click.option("-a", "--app", type=click.STRING, help="Use this app id.")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@click.command("adb", context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument("command", nargs=-1)
@click.pass_context
def adb_command(ctx, command):
    """Executes the adb command."""
    Adb.adb_command(command)


@click.command("devices")
def list_devices():
    """Lists all attached devices."""
    devices = Adb.get_devices_as_list()
    if not devices:
        click.echo("No devices attached")
    else:
        click.echo("Attached devices:")
        for index, item in enumerate(devices):
            entry = "index -> " + str(index) + "\tid -> " + devices[index][0]
            entry += "\t\tdescription -> " + devices[index][1]
            click.echo(entry)


@click.command()
@option_device
@option_app
@click.pass_context
def kill(ctx, device, index, app):
    """Kills (force-stop) the app."""
    device = __get_device_id(ctx.params)
    app = __get_id(app, Config.SECTION_APP, Config.KEY_DEFAULT)
    if app is None:
        raise click.NoSuchOption("app", "app id is required.")
    Adb.kill_app(device, app)


@click.command("kill-all")
@option_device
@click.pass_context
def kill_all(ctx, device, index):
    """Kills all background processes."""
    device = __get_device_id(ctx.params)
    Adb.kill_all(device)


@click.command()
@option_device
@option_app
@click.pass_context
def clear(ctx, device, index, app):
    """Clears the app data."""
    device = __get_device_id(ctx.params)
    app = __get_id(app, Config.SECTION_APP, Config.KEY_DEFAULT)
    if app is None:
        raise click.NoSuchOption("app", "app id is required.")
    Adb.clear_app_data(device, app)


@click.command("text")
@option_device
@click.option("-s", "--source",
              type=click.Choice([Adb.ADB_INPUT_SOURCE_TOUCHSCREEN,
                                 Adb.ADB_INPUT_SOURCE_KEYBOARD]),
              help="Use this input source.")
@click.argument("text")
@click.pass_context
def input_text(ctx, device, index, source, text):
    """Inputs the text."""
    device = __get_device_id(ctx.params)
    Adb.input_text(device, source, text)


@click.command("key")
@option_device
@click.argument("keyevent")
@click.pass_context
def input_keyevent(ctx, device, index, keyevent):
    """Inputs the keyevent (value or constant).
    See also
    https://developer.android.com/reference/android/view/KeyEvent.html"""
    device = __get_device_id(ctx.params)
    Adb.input_keyevent(device, keyevent)


@click.command()
@option_device
@click.argument("output")
@click.pass_context
def screencap(ctx, device, index, output):
    """Takes a screen capture and saves it into the output file."""
    device = __get_device_id(ctx.params)
    Adb.screencap(device, output)


@click.command()
@option_device
@click.option("-u", "--utc", is_flag=True,
              help="Use UTC instead of current timezone.")
@click.pass_context
def date(ctx, device, index, utc):
    """Shows the current date."""
    device = __get_device_id(ctx.params)
    Adb.show_date(device, utc)
