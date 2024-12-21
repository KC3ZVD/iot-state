from __future__ import annotations

import asyncio
import logging
import os
import sys
from typing import cast

from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import (
    AsyncServiceBrowser,
    AsyncServiceInfo,
    AsyncZeroconf,
)

from iot_state.workers import wled

_PENDING_TASKS: set[asyncio.Task] = set()
_WLED_SUPPORT = "0.15.0"
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")
CELERY_RESULTS_URL = os.getenv("CELERY_RESULTS_URL")

logger = logging.getLogger(__name__)


def async_on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    if not name.startswith('wled'):
      logger.debug("Service does not appear to be a WLED service, skipping...")
      return
    if state_change is not ServiceStateChange.Added:
      logger.debug("State change detected")
      return
    task = asyncio.ensure_future(async_publish_service_info(zeroconf, service_type, name))
    _PENDING_TASKS.add(task)
    task.add_done_callback(_PENDING_TASKS.discard)


async def async_publish_service_info(zeroconf: Zeroconf, service_type: str, name: str) -> None:
    info = AsyncServiceInfo(service_type, name)
    await info.async_request(zeroconf, 3000)
    if info:
        addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]


        details = {
          "source": 'mdns',
          "platform": 'wled',
          "attributes": {
            "addresses": addresses
          }
        }

        wled.discover.delay(details=details)

        logger.info("Adding service to MQTT")
    else:
        logger.warning("No service info available, skipping...")

class AsyncRunner:
    def __init__(self) -> None:
        self.aiobrowser: AsyncServiceBrowser|None=None
        self.aiozc: AsyncZeroconf|None=None

    async def async_run(self) -> None:
        self.aiozc = AsyncZeroconf()

        services = ["_http._tcp.local."]
        logger.debug("Watching for service(s)")
        logger.info("Monitoring mDNS...")

        self.aiobrowser = AsyncServiceBrowser(
            self.aiozc.zeroconf, services, handlers=[async_on_service_state_change]
        )
        while True:
            await asyncio.sleep(1)

    async def async_close(self) -> None:
        await self.aiobrowser.async_cancel()
        await self.aiozc.async_close()

def listen() -> None:

  # Set up logging
  logger.setLevel(level=logging.DEBUG)
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(level=logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  # set up event loop
  loop = asyncio.get_event_loop()
  runner = AsyncRunner()

  try:
    loop.run_until_complete(runner.async_run())
  except KeyboardInterrupt:
    loop.run_until_complete(runner.async_close())

if __name__ == "__main__":
   listen()
