#include "Arduino.h"
#include <Arduino_BHY2.h>

SensorXYZ accelerometer(SENSOR_ID_ACC);

void setup() {
  Serial.begin(115200);
  while (!Serial);
  
  //Sensors initialization
  BHY2.begin(NICLA_STANDALONE);
  accelerometer.begin(20);
}

void loop() {
  static auto printTime = millis();
  BHY2.update();
  if (millis() - printTime >= 50) {
    printTime = millis();
    Serial.print(accelerometer.x());
    Serial.print(",");
    Serial.print(accelerometer.y());
    Serial.print(",");
    Serial.print(accelerometer.z());
    Serial.println("");
  }
}