# embedded
Experiments with embedded devices. This repository contains Arduino sketches and accompanying Python scripts.

## [led-on-input.ino](src/sketches/led-on-input.ino)

Usage:
- Connect to serial port at 115200 baud
- Send `A` to flash blue LED
- Send `B` to flash green LED
- Send `C` to flash red LED

## [ble.ino](src/sketches/ble.ino) | [bleak.py](src/bleak.py)

Usage:
- Scan for devices to find the device you want to connect to
- Update `BLE_DEVICE_ADDRESS` variable
- Currently hardcoded to read BLE Characteristics of certain handler numbers at [src/bleak.py#L25](https://github.com/edisonchee/embedded/blob/6e45cd603507757906d9de9db6304679158a970b/src/bleak.py#L25)
- Uses an `asyncio.Queue` for collecting notifications. This is in preparation to feed data into an ML workflow for training

## [acc-serial.ino](src/sketches/acc-serial.ino) | [acc_serial.py](src/acc_serial.py)

Usage:
- Much simpler sketch for transmitting acc data over serial
- Has more bandwidth for higher sampling rate as well

## [audio-serial.ino](src/sketches/audio-serial.ino) | [mic_serial.py](src/mic_serial.py)

- Transmit 16-bit integer PCM from the Nicla Voice through serial port
- This was particarly tricky to figure out because:
  - Arduino docs suggests that [PDM library](https://docs.arduino.cc/hardware/nicla-voice/#suggested-libraries) can be used, which is not the case
  - Audio samples are only accessible through `NDP.extractData`. Moreover, `NDP` will only be initialised if all 3 synpkg are successfully loaded
  - This means that your Nicla Voice will always boot with a bunch of shit printed into the Serial port, which you need to kill
- Requires `pyserial` module

## References
- [nRF52832](https://infocenter.nordicsemi.com/pdf/nRF52832_PS_v1.4.pdf)
- [Nicla Sense ME SENSOR_ID MACRO](https://docs.arduino.cc/tutorials/nicla-sense-me/cheat-sheet/#sensor-ids)
- [Arduino BLE documentation](https://www.arduino.cc/reference/en/libraries/arduinoble/)
- [Arduino BLE API](https://github.com/arduino-libraries/ArduinoBLE/blob/master/docs/api.md)
- [Arduino BHY2 UML](static/Arduino_BHY2.UML.drawio.svg)
- [Arduino Audio Tools](https://github.com/pschatzmann/arduino-audio-tools)
- [Bleak documentation](https://bleak.readthedocs.io/en/latest/index.html)
- [BHI260AP Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bhi260ap-ds000.pdf)
