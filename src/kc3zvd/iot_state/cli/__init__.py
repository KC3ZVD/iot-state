# SPDX-FileCopyrightText: 2024-present KC3ZVD <github@kc3zvd.net>
#
# SPDX-License-Identifier: MIT
import click
from kc3zvd.iot_state.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="iot-state")
@click.option('--redis-host', help="Redis instance host", envvar='IOT_REDIS_HOST', required=True)
@click.option('--redis-port', help="Redis instance port", envvar='IOT_REDIS_PORT', required=True, type=int)
@click.option('--redis-db', help="Redis instance DB number", envvar='IOT_REDIS_DB', required=True, type=int)
@click.pass_context
def iot_state(ctx, redis_host, redis_port, redis_db):
  ctx.ensure_object(dict)
  ctx.obj['REDIS_HOST'] = redis_host
  ctx.obj['REDIS_PORT'] = redis_port
  ctx.obj['REDIS_DB'] = redis_db

@iot_state.command()
@click.option('--platform', help="The platform to publish to", envvar='IOT_PUBLISHER_PLATFORM', required=True, 
              type=click.Choice(['mqtt'], case_sensitive=False))
@click.pass_context
def publisher(ctx, platform):
  click.echo(f"Host: {ctx.obj['redis_host']} \nPort: {ctx.obj['redis_port']}\nDB: {ctx.obj['redis_db']}")
  match platform:
    case 'mqtt':
      click.echo("mqtt platform selected")
