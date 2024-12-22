from __future__ import annotations
from kc3zvd.iot_state.subscribers import redis
import asyncio
# prefix/device_type/area_name/device_name/state_class

async def reader(channel: redis.client.PubSub):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print(f"(Reader) Message Received: {message}")
def subscribe():
    asyncio.run(redis.subscribe('publish', reader))


