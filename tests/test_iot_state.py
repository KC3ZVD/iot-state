from click.testing import CliRunner
from kc3zvd.iot_state import devices
from kc3zvd.iot_state.cli import iot_state


def test_iot_state_devices():
    device = devices.Device()
    device.name = "Test IOT Device"
    device.area = "Test Area"

    state = devices.State()
    state.state_class = "Humidity"

    assert device.area_name == "test_area"
    assert state.friendly_name(device.friendly_name) == "test_iot_device_humidity"


def test_iot_state():
    runner = CliRunner()
    #result = runner.invoke(iot_state)
    #assert result.exit_code == 0
    #assert result.output == "Starting IOT state platform\n"
