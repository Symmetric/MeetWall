from SocketServer import TCPServer, BaseRequestHandler
from datetime import datetime
import logging
import socket

from dispatcher.Adafruit_PWM_Servo_Driver import PWM
from thread import start_new_thread
from dispatcher.common import set_logging, LISTEN_IP, TCP_PORT

_log = logging.getLogger(__name__)

dispatcher = None


def run_server():
    """
    Entry point for the cli start script.
    :return:
    """
    set_logging(_log)
    global dispatcher
    dispatcher = DispatcherServer()
    dispatcher.run()


class DispatcherServer():
    def __init__(self):
        self.pwms = _init_servos()
        self.server = None

    def run(self):
        self.server = ReusingTCPServer((LISTEN_IP, TCP_PORT), TcpHandler)
        _log.info("Started server on %s", self.server.server_address)
        self.server.serve_forever()


class ReusingTCPServer(TCPServer):
    def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.server_address)


class TcpHandler(BaseRequestHandler):
    @profile
    def handle(self):
        try:
            while True:
                # self.request is the TCP socket connected to the client
                data = self.request.recv(160)
                if len(data) > 0:
                    _log.debug('Received data: %s, len %d', [ord(b) for b in data], len(data))
                    t0 = datetime.now()
                    for ii, byte in enumerate(data):
                        # Only check first 9 byte values (for 9 servos).
                        if ii >= 160:
                            break
                        try:
                            setServoAngle(ii, ord(byte))
                        except Exception:
                            _log.exception('Error setting servo %s', ii)
                    delta = datetime.now() - t0
                    _log.debug('Request complete in %s microseconds.', delta.microseconds)
        except KeyboardInterrupt:
            print('Killing server...')

            def kill_me_please(server):
                server.shutdown()
            start_new_thread(kill_me_please, (dispatcher.server,))


def setServoAngle(index, angle, pulse_length_min=0.65, pulse_length_max=2.6):
    """
    Set the servo angle to {angle} degrees.
    :param int index: The channel to set the angle on (globally indexed).
    :param int angle: The new angle, in degrees.
    :param int pulse_length_min: The length of pulse for the servo's minimum angle, in ms.
    :param int pulse_length_max: The length of pulse for the servo's maximum angle, in ms.
    :return: None
    """
    # Integer division to get the index of the PWM instance (one for each 16 channels)
    pwm_index = index / 16
    # Channel is zero-indexed, 16 per PWM instance.
    channel = index % 16
    _log.debug('Got index %d. Setting servo controller %d channel %d to angle %d',
               index, pwm_index, channel, angle)
    pwm = dispatcher.pwms[pwm_index]
    MAX_ANGLE = 180.0
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
    pulseLength = 1000000.0                   # 1,000,000 us per second
    pulseLength /= 50                       # 60 Hz
    _log.debug("%d us per period", pulseLength)
    # PulseLength gives the number of uS per bit of the pulse register
    pulseLength /= 4096                     # 12 bits of resolution
    _log.debug("%d us per bit", pulseLength)
    pulse *= 1000.0   # mS to uS
    # uS / (uS/bits) => # of bits
    # of pulse that must be 'on' to achieve pulse length
    _log.debug('%d us pulse', pulse)
    pulse /= pulseLength
    _log.debug('%d bits per period', int(round(pulse)))
    pwm.setPWM(channel, 0, int(round(pulse)))


def _init_servos():
    # Initialise the PWM devices
    pwms = []
    for index in range(10):
        pwm = PWM(0x40 + index)
        pwm.setPWMFreq(50)
        pwms.append(pwm)

    return pwms

if __name__ == '__main__':
    run_server()
