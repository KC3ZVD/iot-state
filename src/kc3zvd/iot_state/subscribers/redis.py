from __future__ import annotations
import redis.asyncio as redis
import asyncio
STOPWORD = "STOP"


async def subscribe(channel: str, callback: Callable[[], None]):
    print(f"Subscribing to channel: {channel}")
    client = redis.Redis()

    async with client.pubsub() as pubsub:
        await pubsub.subscribe(channel)
        future = asyncio.create_task(callback(pubsub))
        await future
