# SPDX-FileCopyrightText: 2024-present KC3ZVD <github@kc3zvd.net>
#
# SPDX-License-Identifier: MIT
import click
from kc3zvd.iot_state.__about__ import __version__
from kc3zvd.iot_state.publishers import mqtt
from .core.mqtt import mqtt
import logging
import sys


logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

@click.group(context_settings={"help_option_names": ["-h", "--help"], "auto_envvar_prefix": "IOT"}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="iot-state")
@click.option('--log-level', help="Log level", default="INFO", type=str)
@click.option('--redis-username', help="Redis instance username", default='', type=str)
@click.option('--redis-password', help="Redis instance password", default='', type=str)
@click.option('--redis-host', help="Redis instance host", default='localhost', type=str)
@click.option('--redis-port', help="Redis instance port", default=6379, type=int)
@click.option('--redis-db', help="Redis instance DB number", default=0, type=int)
@click.pass_context
def iot_state(ctx, log_level, redis_username, redis_password, redis_host, redis_port, redis_db):
    logger.setLevel(level=log_level)
    handler.setLevel(level=log_level)

    ctx.ensure_object(dict)
    
    if redis_username or redis_password:
        if not redis_username or not redis_password:
            logger.error("Provide both username and password for redis")
            exit()
        ctx.obj['redis_url'] = f"redis://{redis_username}:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
    else:
        ctx.obj['redis_url'] = f"redis://{redis_host}:{redis_port}/{redis_db}"

iot_state.add_command(mqtt)
