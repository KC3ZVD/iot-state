import kc3zvd.iot_state.devices as devices

def test_iot_state():
    device = devices.Device()
    device.name = "Test IOT Device"
    device.area = "Test Area"

    state = devices.State()
    state.state_class = "Humidity"

    assert device.area_name == "test_area"
    assert state.friendly_name(device.friendly_name) == "test_iot_device_humidity"

    