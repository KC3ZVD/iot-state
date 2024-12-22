from __future__ import annotations
from kc3zvd.iot_state.subscribers import redis
import asyncio
# prefix/device_type/area_name/device_name/state_class

async def reader(channel: redis.client.PubSub):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print(f"(Reader) Message Received: {message}")

def run(redis_host: str = 'localhost', redis_port: int = 6379, redis_db: int = 0):
    asyncio.run(redis.subscribe('publish', reader, redis_host, redis_port, redis_db))


