import logging
import socket
import asyncio
import time

from dispatcher.Adafruit_PWM_Servo_Driver import PWM


TCP_PORT = 9999
_log = logging.getLogger(__name__)
logging.getLogger(asyncio.__name__).setLevel(logging.WARN)


class DispatcherProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        super().__init__()

    def connection_made(self, transport):
        # TODO: do we need self.transport?
        _log.info('Connection recieved: %s', transport)
        self.transport = transport

    def data_received(self, data):
        _log.debug('Recieved data: %s', data)
        # TODO: send out on I2C bus


def run_server():
    logging.basicConfig(level=logging.DEBUG, filename='dispatcher.log')
    loop = asyncio.get_event_loop()

    _init_servos()
    server = loop.run_until_complete(loop.create_server(
        protocol_factory=DispatcherProtocol,
        port=TCP_PORT,
        family=socket.AF_INET)
    )
    loop.run_until_complete(server.wait_closed())


def _init_servos():

    # Initialise the PWM device using the default address
    pwm = PWM(0x40, debug=True)

    servoMin = 150  # Min pulse length out of 4096
    servoMax = 600  # Max pulse length out of 4096
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

    while (True):
      # Change speed of continuous servo on channel O
      pwm.setPWM(0, 0, servoMin)
      time.sleep(1)
      pwm.setPWM(0, 0, servoMax)
      time.sleep(1)


