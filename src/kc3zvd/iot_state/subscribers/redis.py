from __future__ import annotations
from typing import Callable
import redis.asyncio as redis
import asyncio
import logging
logger = logging.getLogger(__name__)

async def subscribe(channel: str, callback: Callable[[], None], redis_url: str):
    client = redis.Redis.from_url(redis_url)

    message = f"Subscribing to channel: {channel}"
    logger.info(message)
    async with client.pubsub() as pubsub:
        await pubsub.subscribe(channel)
        future = asyncio.create_task(callback(pubsub))
        await future
