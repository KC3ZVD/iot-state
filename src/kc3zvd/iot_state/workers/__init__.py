import logging
import os

from celery import Celery

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")
CELERY_RESULTS_URL = os.getenv("CELERY_RESULTS_URL")
CELERY_LOG_LEVEL = os.getenv("CELERY_LOG_LEVEL", logging.INFO)

app = Celery('iot-state')

@app.task
def state_changed() -> None:
  pass

def mqtt_notify( topic_prefix: str) -> None:
  # {topic_prefix}/{type}/{area}/{name}/{subtype}
  #
  # {type}: One of sensor, switch, notification, meter
  #
  # TODO: Ensure inputs are sanitized
  pass

def discord_notify() -> None:
  pass

def webhook_notify() -> None:
  pass
