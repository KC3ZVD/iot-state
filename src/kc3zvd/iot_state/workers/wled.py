import logging
import os

import requests
from celery import Celery
from mongoengine import DoesNotExist, MultipleObjectsReturned, connect

from iot_state.devices import Device

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")
CELERY_RESULTS_URL = os.getenv("CELERY_RESULTS_URL")
CELERY_LOG_LEVEL = os.getenv("CELERY_LOG_LEVEL", logging.INFO)
MONGODB_URL = os.getenv("MONGODB_URL")

app = Celery('iot-state')

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(level=CELERY_LOG_LEVEL)

@app.task
def discover(details: dict) -> None:

  for address in details['attributes']['addresses']:
    url = "http://%s/json/info" % address
    try:
      logger.info("Attempting to retrieve info for wled device at %s" % (address))
      r = requests.get(url)
      if r.status_code != 200:
        error_message = "Recieved status code %s from %s, expected 200" % (r.status_code, url)
        logger.error(error_message)
        logger.error("Full response: \n %s" % r.content.decode())
      else:
        process_discovered_device.delay(details, r.json())
    except Exception as e:
      error_message = "Exception while retrieving info from %s." % (url)
      logger.error(error_message, exc_info=e)
      continue

@app.task
def process_discovered_device(details: dict, state: dict) -> None:
  logger.debug("Details: %s" % (details))
  logger.debug("State: %s" % (state))
  connect(host=MONGODB_URL)
  device_id = state['mac']
  platform = details['platform']
  logger.info("Determining if device %s exists in state" % (device_id))

  try:
    device = Device.objects.get(platform_id = device_id)
    logger.info("Device %s exists" % (device.platform_id))
  except MultipleObjectsReturned:
    logger.warning("Multiple matching devices found")
  except DoesNotExist:
    logger.info("Existing device not found, proceeding to bootstrap state")
    device = Device(
      platform_id=device_id,
      platform=details['platform'],
      discovery_source=details['source'])
    device = device.save()
    logger.info("Device saved with ID %s" % (device_id))
    register_state_watcher.delay(device_id)


@app.task
def register_state_watcher(device_id):
  connect(host=MONGODB_URL)
  device = Device.objects.get(platform_id = device_id)
  logger.info("Received request to monitor state changes for %s on platform %s" % (device.platform_id, device.platform))
