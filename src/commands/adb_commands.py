import click
import functools

from ..adb import Adb
from ..config import Config


def __get_id(option_id, section, key):
    if option_id is None:
        return Config.read_value(section, key)
    else:
        return option_id


def __determine_device_id(ctx_params):
    # All attached devices
    devices = Adb.get_devices_as_list()

    if not devices:
        raise click.ClickException("No devices attached")

    device_param = ctx_params["device"]
    index_param = ctx_params["index"]
    if device_param is not None and index_param is not None:
        # Only one of the two options can be passed
        raise click.BadOptionUsage(
            "Only one of the options '--device' or '--index' is allowed")

    elif device_param is not None:
        # Only return the device id when the device is attached
        if __is_device_id_attached(devices, device_param):
            return device_param
        else:
            raise click.ClickException(
                "The device '%s' isn't attached" % device_param)

    elif index_param is not None:
        # Get the device id from the index
        # Only return the device id when the device is attached
        try:
            return devices[index_param][0]
        except IndexError:
            raise click.ClickException(
                "No device with the index '%s' available" % index_param)

    # When no option is provided, then read the local and global config
    device_id = Config.read_value(Config.SECTION_DEVICE,
                                  Config.KEY_DEFAULT)

    if device_id and __is_device_id_attached(devices, device_id):
        # Only return the device id when the device is attached
        return device_id

    if len(devices) == 1:
        # Last resort: Return the only attached device
        return devices[0][0]
    else:
        raise click.ClickException("Can't determine the best matching device")


def __is_device_id_attached(devices, device_id):
    for attached_device in devices:
        # The device id is the first element
        if attached_device[0] == device_id:
            return True
    return False


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
    device = __determine_device_id(ctx.params)
    app = __get_id(app, Config.SECTION_APP, Config.KEY_DEFAULT)
    if app is None:
        raise click.NoSuchOption("app", "app id is required.")
    Adb.kill_app(device, app)


@click.command("kill-all")
@option_device
@click.pass_context
def kill_all(ctx, device, index):
    """Kills all background processes."""
    device = __determine_device_id(ctx.params)
    Adb.kill_all(device)


@click.command()
@option_device
@option_app
@click.pass_context
def clear(ctx, device, index, app):
    """Clears the app data."""
    device = __determine_device_id(ctx.params)
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
    device = __determine_device_id(ctx.params)
    Adb.input_text(device, source, text)


@click.command("key")
@option_device
@click.argument("keyevent")
@click.pass_context
def input_keyevent(ctx, device, index, keyevent):
    """Inputs the keyevent (value or constant).
    See also
    https://developer.android.com/reference/android/view/KeyEvent.html"""
    device = __determine_device_id(ctx.params)
    Adb.input_keyevent(device, keyevent)


@click.command()
@option_device
@click.argument("output")
@click.pass_context
def screencap(ctx, device, index, output):
    """Takes a screen capture and saves it into the output file."""
    device = __determine_device_id(ctx.params)
    Adb.screencap(device, output)


@click.command()
@option_device
@click.option("-u", "--utc", is_flag=True,
              help="Use UTC instead of current timezone.")
@click.pass_context
def date(ctx, device, index, utc):
    """Shows the current date."""
    device = __determine_device_id(ctx.params)
    Adb.show_date(device, utc)
