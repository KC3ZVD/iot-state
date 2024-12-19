# SPDX-FileCopyrightText: 2024-present KC3ZVD <github@kc3zvd.net>
#
# SPDX-License-Identifier: MIT
import click

from kc3zvd.iot_state.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="iot-state")
def iot_state():
    click.echo("Hello world!")