from __future__ import annotations
import redis
# prefix/device_type/area_name/device_name/state_class

def subscribe(redis_host: str, redis_port: int, redis_db: int):
  r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db,  decode_responses=True)
  p = r.pubsub()
  p.subscribe("iot-state-publish")
  for message in p.listen():
    if message["type"] == "message":
      print(f"Received: {message['data'].decode('utf-8')}")
