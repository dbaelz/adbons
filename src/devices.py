import click

import subprocess


@click.group()
def devices():
    """Handle connected devices"""
    pass


@devices.command()
def list():
    subprocess.call(["adb", "devices"])
