import subprocess

import click

from .helper import write_value_to_config


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--select-app", type=click.STRING)
@click.option("--select-device", type=click.STRING)
def cli(ctx, select_device, select_app):
    """A wrapper for the adb tool. It's just adb on steroids."""
    if ctx.invoked_subcommand is None:
        if select_app:
            write_value_to_config("app", "selected", select_app)
        if select_device:
            # TODO: Check if the selected device is attached
            # TODO: Only add it in this case or show prompt
            click.echo(write_value_to_config("device", "selected",
                                             select_device))
    else:
        ctx.invoked_subcommand


@cli.command("devices")
def list():
    """Lists all attached devices"""
    subprocess.call(["adb", "devices"])
