import click

from .commands.config_commands import config
from .commands.adb_commands import (adb_command, list_devices, kill, kill_all,
                                    clear, input_text, input_keyevent)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A wrapper for the adb tool. It's just adb on steroids."""
    ctx.invoked_subcommand


# Config commands
cli.add_command(config)

# ADB commands
cli.add_command(adb_command)
cli.add_command(list_devices)
cli.add_command(kill)
cli.add_command(kill_all)
cli.add_command(clear)
cli.add_command(input_text)
cli.add_command(input_keyevent)
