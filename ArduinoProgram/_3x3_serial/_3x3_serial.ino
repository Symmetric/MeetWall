/***************************************************************************/	
//	Function: Measure the distance to obstacles in front and print the distance
//			  value to the serial terminal.The measured distance is from 
//			  the range 0 to 400cm(157 inches).
//	Hardware: Ultrasonic Range sensor
//	Arduino IDE: Arduino-1.0
//	Author:	 LG		
//	Date: 	 Jan 17,2013
//	Version: v1.0 modified by FrankieChu
//	by www.seeedstudio.com
//
//  This library is free software; you can redistribute it and/or
//  modify it under the terms of the GNU Lesser General Public
//  License as published by the Free Software Foundation; either
//  version 2.1 of the License, or (at your option) any later version.
//
//  This library is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//  Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public
//  License along with this library; if not, write to the Free Software
//  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
//
/*****************************************************************************/
#include "Arduino.h"
#include <Servo.h>
#include <stdlib.h>
#include<Math.h>

int FIRST_SERVO = 2;
int NUM_BYTES = 3 * 3;

Servo[] servos = Servo[9];

byte[] angleUpdates;
int bytesRead = 0;
int angleUpdate;
int ii;
byte incomingByte;

void setup()
{
  Serial.begin(9600);
  
  // Loop over all servos and initialize them.
  for (int p = 0; p < 9; p++)
  {
    servos[p].attach(p + FIRST_SERVO);
    servos[p].write(0);
  }
}

// Read NUM_BYTES from the serial port into the byte array.
// Returns number of bytes read.
int readMessage(byte[] message) {
  bytesRead = 0;
  // First, seek to the start-of-message character (0).
  do
  {
    incomingByte = Serial.read();
    bytesRead++;
  } while (incomingByte != 0)
  
  // Now read one message-length from the buffer.
  for (ii=0; i < NUM_BYTES; i++)
  {
    incomingByte = Serial.read();
    bytesRead++;
    
    // Bail out if we hit a null byte (not a valid angle).
    if (incomingByte == 0)
    {
      break;
    }
    // Otherwise, update the message array.
    message[ii] = incomingByte;
  }
}
  
void loop()
{
  // Get the next message from the serial port.
  bytesRead = readMessage(angleUpdates);
  Serial.print(bytesRead);
  
  // Don't worry about partially-filled messages;
  // if we failed to update, the old value will be valid.
  for (int i = 0; i < NUM_BYTES; i++)
  {
    angleUpdate = angleUpdates[i];
    // Assume that server polices 0 < theta <= 90
    servos[i].write(angleUpdate);
  }
  
  delay(1);
}
