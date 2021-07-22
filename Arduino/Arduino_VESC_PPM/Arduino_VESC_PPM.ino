#include <Servo.h>

const uint8_t VescOutputPin = 5;

const uint8_t PotentiometerPin = A0;

Servo esc;

void setup() {

  esc.attach(VescOutputPin);

  esc.writeMicroseconds(1500);

}

 void loop() {

  esc.writeMicroseconds(map(analogRead(PotentiometerPin), 0 , 1023, 1000, 2000));

}
