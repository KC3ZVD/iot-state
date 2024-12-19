from mongoengine import Document, StringField, EmbeddedDocument, EmbeddedDocumentListField, ReferenceField
from kc3zvd.iot_state import utility

class State(EmbeddedDocument):
  """Represents an IOT Device's state

  Attributes:
    device_id (str):    The Device object this state is associated with
    state_class (str):  The state class for this state (open_close, on_off, humidity, etc.)
    value (str):        The state value
    unit (str):         The unit that the state value represents
    timestamp (str):    The timestamp representing when the state changed
     

  """
  device_id = ReferenceField('Device') 
  state_class = StringField(required=True)
  value = StringField(required=True)
  unit = StringField()
  timestamp = StringField(required=True) # TODO: Find a more appropriate type

  def friendly_name(self, device_name: str) -> str:
    """Generates a machine-friendly name

    Args:
        device_name (str): The parent device's name

    Returns:
        str: Normalized, machne-friendly name
    """
    return utility.normalize("%s_%s" % (device_name, self.state_class))

class Device(Document):
  """Represents an IOT Device

  Attributes:
      platform (str):         The platform managing the device
      platform_id (str):      The ID if the device on it's platform
      discovery_source (str): How the device was discovered
      name (str):             The device's name
      area (str):             The area/room where the device is located
      states [List(State)]:   Embedded State documents for state history with this device

  """
  platform = StringField(required=True)
  platform_id = StringField(required=True)
  discovery_source = StringField(required=True)
  name = StringField(required=True)
  area = StringField(required=True)


  states = EmbeddedDocumentListField(State)

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
