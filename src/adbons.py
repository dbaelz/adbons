import click

import devices


@click.group()
def cli():
    """A wrapper for the adb tool. It's just adb on steroids."""
    pass


cli.add_command(devices.devices)
