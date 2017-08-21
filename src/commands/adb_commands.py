import click
import functools

from ..adb import Adb
from ..config import Config


def __get_id(option_id, section, key):
    if option_id is None:
        return Config.read_value(section, key)
    else:
        return option_id


def option_device(func):
    @click.option("-d", "--device", type=click.STRING,
                  help="Use this device id.")
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
            entry = "index: " + str(index) + "\tid: " + devices[index][0]
            entry += "\tname: " + devices[index][1]
            click.echo(entry)


@click.command()
@option_device
@option_app
@click.pass_context
def kill(ctx, device, app):
    """Kills (force-stop) the app."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    app = __get_id(app, Config.SECTION_APP, Config.KEY_DEFAULT)
    if app is None:
        raise click.NoSuchOption("app", "app id is required.")
    Adb.kill_app(device, app)


@click.command("kill-all")
@option_device
@click.pass_context
def kill_all(ctx, device):
    """Kills all background processes."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.kill_all(device)


@click.command()
@option_device
@option_app
@click.pass_context
def clear(ctx, device, app):
    """Clears the app data."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
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
def input_text(ctx, device, source, text):
    """Inputs the text."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.input_text(device, source, text)


@click.command("key")
@option_device
@click.argument("keyevent")
@click.pass_context
def input_keyevent(ctx, device, keyevent):
    """Inputs the keyevent (value or constant).
    See also
    https://developer.android.com/reference/android/view/KeyEvent.html"""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.input_keyevent(device, keyevent)


@click.command()
@option_device
@click.argument("output")
@click.pass_context
def screencap(ctx, device, output):
    """Takes a screen capture and saves it into the output file."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.screencap(device, output)


@click.command()
@option_device
@click.option("-u", "--utc", is_flag=True,
              help="Use UTC instead of current timezone.")
@click.pass_context
def date(ctx, device, utc):
    """Shows the current date."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.show_date(device, utc)
