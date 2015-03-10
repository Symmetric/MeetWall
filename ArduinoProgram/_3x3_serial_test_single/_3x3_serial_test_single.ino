#include "Arduino.h"
#include <Servo.h>
#include <stdlib.h>
#include<Math.h>

const int FIRST_SERVO = 2;
const int NUM_BYTES = 3 * 3;

Servo servos[NUM_BYTES];
Servo test;

int ii;
byte incomingByte;
int val;
int incr;

void setup()
{
  Serial.begin(9600);

  // Loop over all servos and initialize them.
  test.attach(FIRST_SERVO);
  test.write(0);
  val = 0;
  incr = 1;
}

void loop()
{
  val += incr;
  if (val >= 180) {
    incr = -1;
  }
  else if (val <= 0) {
    incr = 1;
  }

  //Serial.println(val);
  test.write(val);
  delay(10);
}

