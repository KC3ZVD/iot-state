from __future__ import annotations
from kc3zvd.iot_state.subscribers import redis
import paho.mqtt.client as mqtt
import asyncio
import json

# prefix/device_type/area_name/device_name/state_class
class MQTTPublisher:

    def __init__(self, host, port):
        self.host = host
        self.port = port

async def handle_messages(channel: redis.client.PubSub, publisher: str):
    publisher = json.loads(publisher)

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.connect(host=publisher['mqtt_host'], port=publisher['mqtt_port'])
    mqttc.loop_start()
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            print(f"(Reader) Message Received: {message}")
            mqttc.publish(topic="test/message", payload=message['data']).wait_for_publish()
    mqttc.disconnect()
    mqttc.loop_stop()

async def subscribe(redis_url: str, publisher: str):
    update = asyncio.create_task(redis.subscribe('device:state:update', handle_messages, redis_url, publisher))
    create = asyncio.create_task(redis.subscribe('device:state:create', handle_messages, redis_url, publisher))
    await update
    await create

def run(redis_url: str, publisher: dict):
    asyncio.run(subscribe(redis_url, json.dumps(publisher)))


