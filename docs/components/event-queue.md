The event queue follows a pub/sub model. Publishers can subscribe to queue topics of interest,
parse the data, and then take action (by publishing the state to another platform, for instance)

## Payload Format
### device:state
`device:state` queue includes sub-paths for state `create` and `update` events. All messages to `device:state` and it's
subpaths are expected to follow the following format, mirroring the [Device](/reference/kc3zvd/iot_state/devices/#kc3zvd.iot_state.devices.Device) and
[State](/reference/kc3zvd/iot_state/devices/#kc3zvd.iot_state.devices.State) objects