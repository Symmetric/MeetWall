#include "Arduino.h"
#include <Servo.h>
#include <stdlib.h>
#include<Math.h>

const int FIRST_SERVO = 2;
const int NUM_SERVOS= 4;

Servo servos[NUM_SERVOS];
Servo test;

int ii;
byte incomingByte;
int val;
int incr;
int servo;

void setup()
{
  Serial.begin(9600);

  // Loop over all servos and initialize them.
  for (ii = 0; ii < NUM_SERVOS; ii++)
  {
    servos[ii].attach(ii + FIRST_SERVO);
    servos[ii].write(0);
  }
  //test.attach(FIRST_SERVO);
  //test.write(0);
  val = 0;
  incr = 1;
  servo = 0;
}

void loop()
{
  val += incr;
  if (val >= 90) {
    incr = -1;
  }
  else if (val <= 0) {
    incr = 1;
    servo += 1;
    servo %=NUM_SERVOS;
  }
  

//  for (int ii = 0; ii < NUM_SERVOS; ii++)
//  {
    //angleUpdate = angleUpdates[ii];
    // Assume that server polices 0 < theta <= 90
    servos[servo].write(val);

    Serial.print(servo);
    Serial.println(" updated");
//  }
  //Serial.println(val);
//  test.write(val);
  delay(10);
}

