from __future__ import annotations
from kc3zvd.iot_state.subscribers import redis
import asyncio
# prefix/device_type/area_name/device_name/state_class

def subscribe():
     asyncio.run(redis.subscribe('publish'))

