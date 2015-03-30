#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
theta = 0
increment = 1
step = 90
SERVOS = 9

while (True):
  # Change speed of continuous servo on channel O
  theta = theta + increment*step
  if theta >= 90:
    increment = -1
  elif theta <= 0:
    increment = 1

  signal = servoMin + (servoMax - servoMin) * theta/180
  print "%s = %s" % (theta, signal)
  for i in range(SERVOS):
    pwm.setPWM(15-i, 0, signal)
  time.sleep(1)

