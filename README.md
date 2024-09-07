# embedded
Experiments with embedded devices

## [led-on-input](src/sketches/led-on-input.ino)

Usage:
- Connect to serial port at 115200 baud
- Send `A` to flash blue LED
- Send `B` to flash green LED
- Send `C` to flash red LED

## [ble.ino](src/sketches/ble.ino)

Usage:
- Scan for devices to find the device you want to connect to
- Update `BLE_DEVICE_ADDRESS` variable
- Currently hardcoded to read BLE Characteristics of certain handler numbers at [src/bleak.py#L25](https://github.com/edisonchee/embedded/blob/6e45cd603507757906d9de9db6304679158a970b/src/bleak.py#L25)
- Uses an `asyncio.Queue` for collecting notifications. This is in preparation to feed data into an ML workflow for training

## [acc-serial.ino](src/sketches/acc-serial.ino)

Usage:
- Much simpler sketch for transmitting acc data over serial
- Has more bandwidth for higher sampling rate as well

## [audio-serial.ino](src/sketches/audio-serial.ino)

- If you encounter this error `error: conversion from 'int' to 'audio_tools::int24_t' is ambiguous` while compiling, check `AudioConfig.h` from the Arduino Audio Tools library and see if your platform/processor is supported
- If not supported, try defining `USE_INT24_FROM_INT` and/or other features if necessary

## References
- [Nicla Sense ME SENSOR_ID MACRO](https://docs.arduino.cc/tutorials/nicla-sense-me/cheat-sheet/#sensor-ids)
- [Arduino BLE documentation](https://www.arduino.cc/reference/en/libraries/arduinoble/)
- [Arduino BLE API](https://github.com/arduino-libraries/ArduinoBLE/blob/master/docs/api.md)
- [Arduino BHY2 UML](static/Arduino_BHY2.UML.drawio.svg)
- [Bleak documentation](https://bleak.readthedocs.io/en/latest/index.html)
- [BHI260AP Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bhi260ap-ds000.pdf)
