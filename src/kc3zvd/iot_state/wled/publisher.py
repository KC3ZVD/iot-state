from dataclasses import dataclass
import paho.mqtt.publish as publish
import json
import os

APP_MQTT_HOST = os.getenv("APP_MQTT_HOST")
APP_MQTT_PORT = os.getenv("APP_MQTT_PORT", 1883)
APP_MQTT_PROTO = os.getenv("APP_MQTT_PROTO", "mqtt")
APP_MQTT_USER = os.getenv("APP_MQTT_USER")
APP_MQTT_PASSWORD = os.getenv("APP_MQTT_PASSWORD")

@app.task
def pub(details: str) -> None:
  platform = json.loads(details)['platform']
  topic = "%s" % (platform)
  payload = details

  MQTTPublisher().publish(
      payload = payload,
      topic = topic
  )


@dataclass
class MQTTPublisher:
    """
    Publishes messages to MQTT

    Attributes:
        host: MQTT Host
        port: MQTT Port
        proto: MQTT Protocol. Currently supports `mqtt`
        user: MQTT User
        password: MQTT Password
    """
    host: str = APP_MQTT_HOST
    port: int = APP_MQTT_PORT
    proto: str = APP_MQTT_PROTO
    user: str = APP_MQTT_USER
    password: str = APP_MQTT_PASSWORD

    def __post_init__(self):
        print('Publisher init complete.')
    
    def publish(self, payload, topic, qos=1): 
        auth = None
        if self.user:
            auth = {
                "username": self.user,
                "password": self.password 
            }
        publish.single(
            topic=topic, 
            payload=payload, 
            qos=qos,
            hostname=self.host, 
            port=self.port,
            auth=auth
            )