#include <Adafruit_INA260.h>

Adafruit_INA260 ina260 = Adafruit_INA260();

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }

  // initialise ina260 module
  ina260.begin();

  }
void loop() {
  // put the power into serial
  Serial.print(ina260.readPower());

  Serial.println();
  // wait 0.5s (same as DT on python code)
  delay(500);
}
