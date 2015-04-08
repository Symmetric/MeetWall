"""
BodySensor Dispatcher client

    Send a message to the server.

    MESSAGE is a sequence of comma-delimeted byte values, e.g.

    1,23, 22, 14, 14 , 1, 255, 0

    Usage: demo INDEX 

"""
import docopt

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================


def setServoPulse(channel, pulse):
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)


if __name__ == '__main__':
    args = docopt.docopt(__doc__, help=False)
    # Initialise the PWM device using the default address
    pwm = PWM(0x40 + int(args['INDEX']))
    
    servoMin = 150  # Min pulse length out of 4096
    servoMax = 600  # Max pulse length out of 4096

    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    theta = 0
    increment = 1
    step = 10
    SERVOS = 16
    
    while True:
        # Change speed of continuous servo on channel O
        theta += increment*step
        if theta >= 90:
            increment = -1
        elif theta <= 0:
            increment = 1
    
        signal = servoMin + (servoMax - servoMin) * theta/180
        #print "%s = %s" % (theta, signal)
        for i in range(SERVOS):
            pwm.setPWM(i, 0, signal)
        time.sleep(0.05)

