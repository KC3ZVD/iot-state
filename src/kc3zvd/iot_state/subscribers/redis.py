from __future__ import annotations
import redis.asyncio as redis
import asyncio

async def subscribe(channel: str, callback: Callable[[], None], redis_url: str, publisher: str):
    client = redis.Redis.from_url(redis_url)

    print(f"Subscribing to channel: {channel}")
    async with client.pubsub() as pubsub:
        await pubsub.subscribe(channel, publisher)
        future = asyncio.create_task(callback(pubsub, publisher))
        await future
