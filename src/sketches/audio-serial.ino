#undef abs
#define ARDUINO_ARDUINO_NANO33BLE

#include "NDP.h"
#include "AudioTools.h"
#include "AudioCodecs/codecWAV.h"

uint16_t sample_rate = 16000;
uint8_t channels = 1;
auto &serial = Serial;
WAVEncoder encoder;
EncodedAudioStream out_stream(&serial, &encoder);

uint8_t data[2048];

void ledBlueOn(char* label) {
  nicla::leds.begin();
  nicla::leds.setColor(blue);
  delay(200);
  nicla::leds.setColor(off);
  nicla::leds.end();
}

void ledGreenOn() {
  nicla::leds.begin();
  nicla::leds.setColor(green);
  delay(200);
  nicla::leds.setColor(off);
  nicla::leds.end();
}

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

void setup(){
  Serial.begin(115200);
  nicla::begin();
  nicla::disableLDO();
  nicla::leds.begin();

  NDP.onError(ledRedBlink);
  NDP.onMatch(ledBlueOn);
  NDP.onEvent(ledGreenOn);

  Serial.println("Loading synpackages");
  NDP.begin("mcu_fw_120_v91.synpkg");
  NDP.load("dsp_firmware_v91.synpkg");
  NDP.load("ei_model.synpkg");
  Serial.println("packages loaded");
  NDP.getInfo();

  Serial.println("Configure mic");
  NDP.turnOnMicrophone();
  Serial.println(NDP.getAudioChunkSize());

  auto cfg = encoder.defaultConfig();
  cfg.sample_rate = sample_rate;
  cfg.channels = channels;
  cfg.bits_per_sample = 16;
  out_stream.begin(cfg);
}

void loop(){
  unsigned int len = 0;
  NDP.extractData(data, &len);
  encoder.write(data, len);
}