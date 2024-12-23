from __future__ import annotations
from kc3zvd.iot_state import utility
from dataclasses import dataclass
from mongoengine import Document, ReferenceField, StringField, DateTimeField
import json


class State(Document):
    """Represents an IOT Device's state

    Attributes:
      device_id (str):    The Device object this state is associated with
      state_class (str):  The state class for this state (open_close, on_off, humidity, etc.)
      value (str):        The state value
      unit (str):         The unit that the state value represents
      timestamp (str):    The timestamp representing when the state changed
    """

    device = ReferenceField("Device")
    state_class = StringField(required=True)
    value = StringField(required=True)
    unit = StringField()
    timestamp = DateTimeField(required=True)  # TODO: Find a more appropriate type

    def friendly_name(self, device_name: str) -> str:
        """Generates a machine-friendly name

        Args:
            device_name (str): The parent device's name

        Returns:
            str: Normalized, machne-friendly name
        """
        return utility.normalize(f"{device_name}_{self.state_class}")

class Device(Document):
    """Represents an IOT Device

    Attributes:
        platform (str):         The platform managing the device
        platform_id (str):      The ID if the device on it's platform
        discovery_source (str): How the device was discovered
        name (str):             The device's name
        area (str):             The area/room where the device is located
        device_type (str):      The type/category of this device
    """

    platform = StringField(required=True)
    platform_id = StringField(required=True)
    discovery_source = StringField(required=True)
    name = StringField(required=True)
    area = StringField(required=True)
    device_type = StringField(required=True)

    @property
    def friendly_name(self) -> str:
        """Generates a machine-friendly name

        Returns:
            str: Normalized, machine-friendly name
        """
        return utility.normalize(self.name)

    @property
    def area_name(self) -> str:
        """Generates a machine-friendly area name

        Returns:
            str: Normalized, machine-friendly area name
        """
        return utility.normalize(self.area)
    
    def to_dict(self) -> dict:
        d = {
            "platform": self.platform,
            "platform_id": self.platform_id,
            "disocvery_source": self.discovery_source,
            "name": self.name,
            "area": self.area,
            "device_type": self.device_type,
            "friendly_name": self.friendly_name,
            "area_name": self.area_name
        }

        return d