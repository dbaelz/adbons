import click

from .adb import Adb
from .config import read_value, write_value, clear_value
from .config import (SECTION_APP, SECTION_DEVICE, KEY_DEFAULT)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A wrapper for the adb tool. It's just adb on steroids."""
    ctx.invoked_subcommand


@cli.command()
@click.option("use_global", "-g", "--global", is_flag=True,
              help="Use the global config (~/.adbons/.adbons.yml).")
@click.option("-d", "--set-device", type=click.STRING,
              help="Set a default device id.")
@click.option("-a", "--set-app", type=click.STRING,
              help="Set a default app id.")
@click.option("-c", "--clear",
              type=click.Choice([SECTION_DEVICE, SECTION_APP]),
              help="Clear the default value.")
@click.pass_context
def config(ctx, use_global, set_device, set_app, clear):
    """"Configurate adbons."""
    if set_device:
        write_value(use_global, SECTION_DEVICE, KEY_DEFAULT, set_device)
    if set_app:
        write_value(use_global, SECTION_APP, KEY_DEFAULT, set_app)
    if clear:
        clear_value(use_global, clear, KEY_DEFAULT)


@cli.command("devices")
def list():
    """List all attached devices."""
    Adb.list_devices()


@cli.command()
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.option("-a", "--app", type=click.STRING, help="Use this app id.")
@click.pass_context
def kill(ctx, device, app):
    """Kill (force-stop) an app."""
    if device is None:
        device = read_value(SECTION_DEVICE, KEY_DEFAULT)
    if app is None:
        app = read_value(SECTION_APP, KEY_DEFAULT)
        if app is None:
            raise click.NoSuchOption("app", "app id is required.")

    Adb.kill_app(device, app)


@cli.command("kill-all")
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.pass_context
def kill_all(ctx, device):
    """Kill all background processes."""
    if device is None:
        device = read_value(SECTION_DEVICE, KEY_DEFAULT)
    Adb.kill_all(device)


@cli.command()
@click.option("-d", "--device", type=click.STRING, help="Use this device id.")
@click.option("-a", "--app", type=click.STRING, help="Use this app id.")
@click.pass_context
def clear(ctx, device, app):
    """Clear the app data."""
    if device is None:
        device = read_value(SECTION_DEVICE, KEY_DEFAULT)
    if app is None:
        app = read_value(SECTION_APP, KEY_DEFAULT)
        if app is None:
            raise click.NoSuchOption("app", "app id is required.")

    Adb.clear_app_data(device, app)
