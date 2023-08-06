## bleak_sigspec
### Bleak SIG Bluetooth Characteristic Specification Formatter

This package enables characteristic metadata parsing and automatic formatting (bytes unpacking) into the proper characteristic values.

To install

```
pip install bleak_sigspec
```

or to get the latest version

```
pip install https://github.com/Carglglz/bleak_sigspec.git
```

Compatibility with +200 GATT characteristics following [GATT Specifications](https://www.bluetooth.com/specifications/gatt/characteristics/)

### Usage example

`service_explorer.py` in bleak examples:

`char --> Temperature Characteristic`

```
from bleak_sigspec.utils import get_char_value
[...]
37
			bytes_value = bytes(await client.read_gatt_char(char.uuid))
			formatted_value = get_char_value(bytes_value, char)
[...]
43
			log.info(
				"Characteristic Name: {0}, Bytes Value: {1}, Formatted
				Value: {2}".format(char.description, bytes_value, formatted_value))


```

```
$ python3 service_explorer.py
[...]
Characteristic Name: Temperature, Bytes Value: b'Z\x16', Formatted Value: {'Temperature': {'Quantity': 'thermodynamic temperature',
  'Unit': 'degree celsius',
  'Symbol': '°C',
  'Value': 57.22}}
```

See more at  [bleak_sigspec documentation](https://bleak-sigspec.readthedocs.io)
