#include "NDP.h"

const uint32_t sample_length_ms = (uint32_t)5000;
const uint16_t sample_rate = (uint16_t)16000;
const float sample_interval_ms = (float)(0.0625);
const uint16_t read_size = 512;
const uint16_t _samples = read_size * 3;
uint32_t required_samples;

void ledRedBlink() {
  while (1) {
    nicla::leds.begin();
    nicla::leds.setColor(red);
    delay(200);
    nicla::leds.setColor(off);
    delay(200);
    nicla::leds.end();
  }
}

void setup() {
  Serial.begin(1000000);
  nicla::begin();
  nicla::disableLDO();
  nicla::leds.begin();
  NDP.onError(ledRedBlink);

  Serial.println("Loading synpackages");
  NDP.begin("mcu_fw_120_v91.synpkg");
  NDP.load("dsp_firmware_v91.synpkg");
  NDP.load("ei_model.synpkg");
  Serial.println("packages loaded");
  NDP.getInfo();

  Serial.println("Configure mic");
  NDP.turnOnMicrophone();
  NDP.noInterrupts();
  Serial.println(NDP.getAudioChunkSize()); // 774

  required_samples = (uint32_t)((sample_length_ms) / (sample_interval_ms));
  if(required_samples & 1) {
    required_samples++;
  }
}

void loop() {
  // stop nn model inferencing from polluting serial port, await for 'b' char sent to serial port
  nicla::leds.setColor(magenta);
  while (1) {
    int thisChar = Serial.read();
    if (thisChar == 98) {
      break;
    }
  }
  nicla::leds.setColor(off);

  uint16_t read = 0;
  uint8_t _local_audio_buffer[_samples] = { 0 };
  uint32_t _local_current_samples = 0;
  unsigned int len = 0;
  int s = 0;

  NDP.noInterrupts();

  do {
    s = NDP.extractData(_local_audio_buffer, &len); // unload the previous buffer
  } while (s != 0);

  nicla::leds.setColor(green);

  delay(1000);

  while (_local_current_samples < required_samples) {
    NDP.extractData(&_local_audio_buffer[read], &len);

    if (len != 0) {
      read += len;
      if (read >= read_size * 2) {
        Serial.write(_local_audio_buffer, read);
        _local_current_samples += (read / 2);
        read = 0;
      }
    } else {
      delay(1);
    }
  }
}