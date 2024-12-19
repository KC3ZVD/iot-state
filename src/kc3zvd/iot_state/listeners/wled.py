from zeroconf import ServiceStateChange, Zeroconf
from typing import Optional, cast
from iot_state.workers import wled
import logging
import asyncio
import sys
import os

from zeroconf.asyncio import (
    AsyncServiceBrowser,
    AsyncServiceInfo,
    AsyncZeroconf,
)

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
      logger.debug(f"Service {name} does not appear to be a WLED service, skipping...")
      return
    if state_change is not ServiceStateChange.Added:
      logger.debug(f"State Change: {state_change}")
      return
    task = asyncio.ensure_future(async_publish_service_info(zeroconf, service_type, name))
    _PENDING_TASKS.add(task)
    task.add_done_callback(_PENDING_TASKS.discard)


async def async_publish_service_info(zeroconf: Zeroconf, service_type: str, name: str) -> None:
    info = AsyncServiceInfo(service_type, name)
    await info.async_request(zeroconf, 3000)
    logger.debug("Info from zeroconf.get_service_info: %r" % (info))
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

        logger.info(f"Adding service {name} to MQTT")
    else:
        logger.warning("No service info available for %s, skipping..." % (name))

class AsyncRunner:
    def __init__(self) -> None:
        self.aiobrowser: Optional[AsyncServiceBrowser] = None
        self.aiozc: Optional[AsyncZeroconf] = None

    async def async_run(self) -> None:
        self.aiozc = AsyncZeroconf()

        services = ["_http._tcp.local."]
        logger.debug("Watching for %s service(s)" % services)
        logger.info("Monitoring mDNS...")
        
        self.aiobrowser = AsyncServiceBrowser(
            self.aiozc.zeroconf, services, handlers=[async_on_service_state_change]
        )
        while True:
            await asyncio.sleep(1)

    async def async_close(self) -> None:
        assert self.aiozc is not None
        assert self.aiobrowser is not None
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
