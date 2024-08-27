# embedded
Experiments with embedded devices

## [led-on-input](src/led-on-input.ino)

Usage:
- Connect to serial port at 115200 baud
- Send `A` to flash blue LED
- Send `B` to flash green LED
- Send `C` to flash red LED

## [ble.ino](src/ble.ino)

Usage:
- Scan for devices to find the device youre want to connect to
- Update `BLE_DEVICE_ADDRESS` variable

## References
- [Nicla Sense ME SENSOR_ID MACRO](https://docs.arduino.cc/tutorials/nicla-sense-me/cheat-sheet/#sensor-ids)
- [Arduino BLE documentation](https://www.arduino.cc/reference/en/libraries/arduinoble/)
- [Arduino BLE API](https://github.com/arduino-libraries/ArduinoBLE/blob/master/docs/api.md)
- [Arduino BHY2 UML](static/Arduino_BHY2.UML.drawio.svg)
- [Bleak documentation](https://bleak.readthedocs.io/en/latest/index.html)
- [BHI260AP Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bhi260ap-ds000.pdf)
