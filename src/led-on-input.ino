void ledBlueOn() {
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

void ledRedOn() {
  nicla::leds.begin();
  nicla::leds.setColor(red);
  delay(200);
  nicla::leds.setColor(off);
  nicla::leds.end();
}

void setup() {
  // Begin the board
  nicla::begin();
  nicla::disableLDO();
  nicla::leds.begin();

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("A: Blue, B: Green, C: Red");
  Serial.println();
}

void loop() {
  if (Serial.available() > 0) {
    int thisChar = Serial.read();
    Serial.print("Received: ");
    Serial.println(thisChar);

    if (thisChar == 65) {
      ledBlueOn();
    } else if (thisChar == 66) {
      ledGreenOn();
    } else if (thisChar == 67) {
      ledRedOn();
    } else {
      Serial.println("A: Blue, B: Green, C: Red");
    }
  }
}
