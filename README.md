# iot-state

[![PyPI - Version](https://img.shields.io/pypi/v/kc3zvd-iot-state.svg)](https://pypi.org/project/kc3zvd-iot-state)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kc3zvd-iot-state.svg)](https://pypi.org/project/kc3zvd-iot-state)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install kc3zvd-iot-state
```

## Message Formats
### device:state:{update,create}
```json
{
  "state": {},    // The State() object
  "device": {}    // The Device() object
}
```

## License

`iot-state` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
