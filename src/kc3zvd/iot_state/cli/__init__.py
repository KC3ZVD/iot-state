# SPDX-FileCopyrightText: 2024-present KC3ZVD <github@kc3zvd.net>
#
# SPDX-License-Identifier: MIT
import click
from kc3zvd.iot_state.__about__ import __version__
from kc3zvd.iot_state.publishers import mqtt

@click.group(context_settings={"help_option_names": ["-h", "--help"], "auto_envvar_prefix": "IOT"}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="iot-state")
@click.option('--redis-username', help="Redis instance username", default='', type=str)
@click.option('--redis-password', help="Redis instance password", default='', type=str)
@click.option('--redis-host', help="Redis instance host", default='localhost', type=str)
@click.option('--redis-port', help="Redis instance port", default=6379, type=int)
@click.option('--redis-db', help="Redis instance DB number", default=0, type=int)
@click.pass_context
def iot_state(ctx, redis_username, redis_password, redis_host, redis_port, redis_db):
    ctx.ensure_object(dict)
    
    if redis_username or redis_password:
        if not redis_username or not redis_password:
            click.echo("Provide both username and password for redis")
            die()
        ctx.obj['redis_url'] = f"redis://{redis_username}:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
    else:
        ctx.obj['redis_url'] = f"redis://{redis_host}:{redis_port}/{redis_db}"
    click.echo("Starting IOT state platform")

@iot_state.command()
@click.option('--platform', help="The platform to publish to", required=True, 
              type=click.Choice(['mqtt'], case_sensitive=False))
@click.option('--mqtt-host', help="The MQTT host to connect to", default='localhost', type=str)
@click.option('--mqtt-port', help="The port to use to connect to the MQTT host", default=1883, type=int)
@click.pass_context
def publisher(ctx, platform, mqtt_host, mqtt_port):
    mqtt_url = ""
    match platform:
        case 'mqtt':
            click.echo("mqtt platform selected")
            mqtt.run(
                redis_url=ctx.obj['redis_url'],
                publisher={
                    "mqtt_host": mqtt_host,
                    "mqtt_port": mqtt_port
                }
            )
        case _:
            die()
