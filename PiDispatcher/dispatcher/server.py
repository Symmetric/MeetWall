from SocketServer import TCPServer, BaseRequestHandler
from _socket import gethostname
import logging

from dispatcher.Adafruit_PWM_Servo_Driver import PWM


PI_IP = '192.168.1.14'
TCP_PORT = 9999
_log = logging.getLogger(__name__)

dispatcher = None


def run_server():
    """
    Entry point for the cli start script.
    :return:
    """
    logging.basicConfig(level=logging.DEBUG, filename='dispatcher.log')
    global dispatcher
    dispatcher = DispatcherServer()
    dispatcher.run()


class DispatcherServer():
    def __init__(self):
        self.pwm = _init_servos()
        self.server = None

    def run(self):
        self.server = TCPServer((PI_IP, TCP_PORT), TcpHandler)
        print "Started server on %s:%s" % self.server.server_address
        self.server.serve_forever()


class TcpHandler(BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        data = self.request.recv(1024).strip()
        _log.debug('Recieved data: %s', data)
        for ii, byte in enumerate(data):
            # Only check first 9 byte values (for 9 servos).
            if ii >= 15:
                break
            print "%s: %s" % (ii, ord(byte))
            setServoAngle(dispatcher.pwm, ii, ord(byte))


def setServoAngle(pwm, channel, angle, pulse_length_min=1.0, pulse_length_max=2.0):
    """
    Set the servo angle to {angle} degrees.
    :param int channel: The channel to set the angle on.
    :param int angle: The new angle, in degrees.
    :param int pulse_length_min: The length of pulse for the servo's minimum angle, in ms.
    :param int pulse_length_max: The length of pulse for the servo's maximum angle, in ms.
    :return: None
    """
    MAX_ANGLE = 180
    assert angle <= MAX_ANGLE, "Angle must be less than or equal to 180 degrees. Got " + str(angle)
    angle_fraction = angle / MAX_ANGLE
    pulse_length = pulse_length_min + (pulse_length_max - pulse_length_min) * angle_fraction
    setServoPulse(pwm, channel, pulse_length)


def setServoPulse(pwm, channel, pulse):
    """
    Set the servo pulse length to {pulse} ms.
    :param channel: The channel to set the pulse length on
    :param pulse:  The new pulse length, in ms.
    :return: None
    """
    pulseLength = 1000000                   # 1,000,000 us per second
    pulseLength /= 60                       # 60 Hz
    print("%d us per period" % pulseLength)
    # PulseLength gives the number of uS per bit of the pulse register
    pulseLength /= 4096                     # 12 bits of resolution
    print("%d us per bit" % pulseLength)
    pulse *= 1000   # mS to uS
    # uS / (uS/bits) => # of bits
    # of pulse that must be 'on' to achieve pulse length
    print('%d us pulse' % pulse)
    pulse /= pulseLength
    print('%d bits per period' % int(round(pulse)))
    pwm.setPWM(channel, 0, int(round(pulse)))


def _init_servos():
    # Initialise the PWM device using the default address
    pwm = PWM(0x40, debug=True)

    pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
    return pwm

if __name__ == '__main__':
    run_server()
