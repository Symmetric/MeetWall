from collections import namedtuple
import logging
from math import sqrt
from random import random
import socket
from time import sleep

import docopt

from dispatcher.common import set_logging, TCP_PORT

_log = logging.getLogger(__name__)

X_DIMENSION = 19
Y_DIMENSION = 8
BYTE_ARRAY_LEN = 160
MAX_RADIUS = 20


def raindrop():
    """BodySensor Raindrop demo client

    Send a raindrop pattern to the server.

    Usage: raindrop [--ip=<IP>] [-r]

    Options:
        --ip=<IP>  The IP to connect to [default: 192.168.2.1]
        -r         Repeat the message sequence indefinitely
    """
    set_logging(_log, filename='dispatcher_client.log')
    args = docopt.docopt(send_to_server.__doc__, help=False)
    ip = args['--ip']

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, TCP_PORT))

    active = True
    raindrop = None
    output_bytes = [0] * BYTE_ARRAY_LEN
    Point = namedtuple('point', ['x', 'y', 'radius'])

    while active:
        if not raindrop:
            # First clear the screen
            for ii in xrange(BYTE_ARRAY_LEN):
                output_bytes[ii] = 0

            raindrop = Point(x=int(X_DIMENSION * random()), y=int(Y_DIMENSION * random()), radius=1)
            _log.info('Created new raindrop at %d, %d.', raindrop[0], raindrop[1])

            sock.send(output_bytes)
            sleep(0.1)
        else:
            # Already have a raindrop. Render the next step in the animation.
            for x in xrange(X_DIMENSION):
                for y in xrange(Y_DIMENSION):
                    ii = x * Y_DIMENSION + y
                    delta_x = x - raindrop.x
                    delta_y = y - raindrop.y
                    if round(sqrt(delta_x**2 + delta_y**2)) == raindrop.radius:
                        output_bytes[ii] = 90
                    else:
                        output_bytes[ii] = 0

            # Increment the radius for the next render, or delete the raindrop if it's finished.
            raindrop.radius += 1
            if raindrop.radius > MAX_RADIUS:
                raindrop = None

        # If we're not in repeat mode, terminate.
        if not args['-r']:
            active = False

    sock.close()
