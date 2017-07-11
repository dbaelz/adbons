import click

from ..adb import Adb
from ..config import Config


def __get_id(option_id, section, key):
    if option_id is None:
        return Config.read_value(section, key)
    else:
        return option_id


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
    Adb.list_devices()


@click.command()
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.option("-a", "--app", type=click.STRING, help="Use this app id.")
@click.pass_context
def kill(ctx, device, app):
    """Kills (force-stop) the app."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    app = __get_id(app, Config.SECTION_APP, Config.KEY_DEFAULT)
    if app is None:
        raise click.NoSuchOption("app", "app id is required.")
    Adb.kill_app(device, app)


@click.command("kill-all")
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.pass_context
def kill_all(ctx, device):
    """Kills all background processes."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.kill_all(device)


@click.command()
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.option("-a", "--app", type=click.STRING, help="Use this app id.")
@click.pass_context
def clear(ctx, device, app):
    """Clears the app data."""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    app = __get_id(app, Config.SECTION_APP, Config.KEY_DEFAULT)
    if app is None:
        raise click.NoSuchOption("app", "app id is required.")
    Adb.clear_app_data(device, app)


@click.command("text")
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
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
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.argument("keyevent")
@click.pass_context
def input_keyevent(ctx, device, keyevent):
    """Inputs the keyevent (value or constant).
    See also
    https://developer.android.com/reference/android/view/KeyEvent.html"""
    device = __get_id(device, Config.SECTION_DEVICE, Config.KEY_DEFAULT)
    Adb.input_keyevent(device, keyevent)
