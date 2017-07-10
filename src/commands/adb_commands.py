import click

from ..adb import Adb
from ..config import Config


@click.command("adb", context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument("command", nargs=-1)
@click.pass_context
def adb_command(ctx, command):
    """Executes the adb give command."""
    Adb.adb_command(command)


@click.command("devices")
def list_devices():
    """List all attached devices."""
    Adb.list_devices()


@click.command()
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.option("-a", "--app", type=click.STRING, help="Use this app id.")
@click.pass_context
def kill(ctx, device, app):
    """Kill (force-stop) an app."""
    if device is None:
        device = Config.read_value(Config.SECTION_DEVICE,
                                   Config.KEY_DEFAULT)
    if app is None:
        app = Config.read_value(Config.SECTION_APP,
                                Config.KEY_DEFAULT)
        if app is None:
            raise click.NoSuchOption("app", "app id is required.")
    Adb.kill_app(device, app)


@click.command("kill-all")
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.pass_context
def kill_all(ctx, device):
    """Kill all background processes."""
    if device is None:
        device = Config.read_value(Config.SECTION_DEVICE,
                                   Config.KEY_DEFAULT)
    Adb.kill_all(device)


@click.command()
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.option("-a", "--app", type=click.STRING, help="Use this app id.")
@click.pass_context
def clear(ctx, device, app):
    """Clear the app data."""
    if device is None:
        device = Config.read_value(Config.SECTION_DEVICE,
                                   Config.KEY_DEFAULT)
    if app is None:
        app = Config.read_value(Config.SECTION_APP,
                                Config.KEY_DEFAULT)
        if app is None:
            raise click.NoSuchOption("app", "app id is required.")
    Adb.clear_app_data(device, app)
