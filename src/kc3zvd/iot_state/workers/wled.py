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
HTTP_200 = 200

app = Celery("iot-state")

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(level=CELERY_LOG_LEVEL)


@app.task
def discover(details: dict) -> None:
    for address in details["attributes"]["addresses"]:
        url = f"http://{address}/json/info"
        try:
            logger.info("Attempting to retrieve info for wled device")
            r = requests.get(url, timeout=10)
            if r.status_code != HTTP_200:
                error_message = f"Recieved status code {r.status_code} from {url}, expected 200"
                logger.error(error_message)
            else:
                process_discovered_device.delay(details, r.json())
        except requests.exception.Timeout as e:
            error_message = f"Timeout while retrieving info from {url}."
            logger.exception(error_message, exc_info=e)
            continue


@app.task
def process_discovered_device(details: dict, state: dict) -> None:
    connect(host=MONGODB_URL)
    device_id = state["mac"]
    logger.info("Determining if device exists in state")

    try:
        device = Device.objects.get(platform_id=device_id)
        logger.info("Device exists")
    except MultipleObjectsReturned:
        logger.warning("Multiple matching devices found")
    except DoesNotExist:
        logger.info("Existing device not found, proceeding to bootstrap state")
        device = Device(platform_id=device_id, platform=details["platform"], discovery_source=details["source"])
        device = device.save()
        logger.info("Device saved")
        register_state_watcher.delay(device_id)


@app.task
def register_state_watcher(device_id):
    connect(host=MONGODB_URL)
    device = Device.objects.get(platform_id=device_id)
    message = f"Received request to monitor state changes for {device.platform_id} on platform {device.platform}"
    logger.info(message)
