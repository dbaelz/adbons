import subprocess

import click

from .config import write_value
from .config import (SECTION_APP, SECTION_DEVICE, KEY_DEFAULT)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-a", "--set-app", type=click.STRING,
              help="Set a default app id")
@click.option("-d", "--set-device", type=click.STRING,
              help="Set a default device id")
def cli(ctx, set_app, set_device):
    """A wrapper for the adb tool. It's just adb on steroids."""
    if ctx.invoked_subcommand is None:
        if set_app:
            write_value(SECTION_APP, KEY_DEFAULT, set_app)
        if set_device:
            # TODO: Check if the selected device is attached
            # TODO: Only add it in this case or show prompt
            write_value(SECTION_DEVICE, KEY_DEFAULT, set_device)
    else:
        ctx.invoked_subcommand


@cli.command("devices")
def list():
    """Lists all attached devices"""
    subprocess.call(["adb", "devices"])
