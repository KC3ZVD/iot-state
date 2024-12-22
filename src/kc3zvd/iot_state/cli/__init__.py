# SPDX-FileCopyrightText: 2024-present KC3ZVD <github@kc3zvd.net>
#
# SPDX-License-Identifier: MIT
import click
from kc3zvd.iot_state.__about__ import __version__
from kc3zvd.iot_state.publishers import mqtt

@click.group(context_settings={"help_option_names": ["-h", "--help"], "auto_envvar_prefix": "IOT"}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="iot-state")
@click.option('--redis-host', help="Redis instance host", required=True)
@click.option('--redis-port', help="Redis instance port", required=True, type=int)
@click.option('--redis-db', help="Redis instance DB number", required=True, type=int)
@click.pass_context
def iot_state(ctx, redis_host, redis_port, redis_db):
  ctx.ensure_object(dict)
  ctx.obj['redis_host'] = redis_host
  ctx.obj['redis_port'] = redis_port
  ctx.obj['redis_db'] = redis_db
  click.echo("Starting IOT state platform")
@iot_state.command()
@click.option('--platform', help="The platform to publish to", required=True, 
              type=click.Choice(['mqtt'], case_sensitive=False))
@click.pass_context
def publisher(ctx, platform):
  match platform:
    case 'mqtt':
      #publishers.mqtt.subscribe(
      #  redis_host=ctx.obj['redis_host'],
      #  redis_port=ctx.obj['redis_port'],
      #  redis_db=ctx.obj['redis_db'])
      mqtt.subscribe()      
      click.echo("mqtt platform selected")
    case _:
      die()
