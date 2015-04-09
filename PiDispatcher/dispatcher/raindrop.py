"""MeetWall Raindrop demo client

Send a raindrop pattern to the server.

Usage: raindrop [--ip=<IP>] [-r]

Options:
    --ip=<IP>  The IP to connect to [default: 192.168.2.1]
    -r         Repeat the message sequence indefinitely
"""
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
MAX_RADIUS = 10
DELAY = 0.1


def send_raindrop():
    _log.setLevel(logging.INFO)
    set_logging(_log, filename='raindrop.log')
    args = docopt.docopt(__doc__, help=False)
    ip = args['--ip']

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, TCP_PORT))

    active = True
    raindrop = None
    output_values = [0] * BYTE_ARRAY_LEN

    def send(output):
        # Create a byte array from the output values and send to the server.
        out = ''.join(map(chr, output))
        _log.debug('Sending %s', [ord(b) for b in out])
        sock.send(out)

    while active:
        # First clear the screen
        output_values = [0] * BYTE_ARRAY_LEN

        raindrop = Point()
        _log.info('Created new raindrop at %d, %d.', raindrop.x, raindrop.y)

        send(output_values)
        sleep(DELAY)

        # Now render the updates for the raindrop
        while raindrop:
            # Already have a raindrop. Render the next step in the animation.
            _log.debug('Rendering next step, radius=%d', raindrop.radius)
            for x in xrange(X_DIMENSION):
                for y in xrange(Y_DIMENSION):
                    ii = x * Y_DIMENSION + y
                    delta_x = x - raindrop.x
                    delta_y = y - raindrop.y
                    if round(sqrt(delta_x**2 + delta_y**2)) == raindrop.radius:
                        output_values[ii] = 90
                    else:
                        output_values[ii] = 0

            send(output_values)

            # Increment the radius for the next render, or delete the raindrop if it's finished.
            raindrop.radius += 1
            if raindrop.radius > MAX_RADIUS:
                raindrop = None
            sleep(DELAY)

        # If we're not in repeat mode, terminate.
        if not args['-r']:
            active = False

    sock.close()


class Point():
    def __init__(self):
        self.x = int(X_DIMENSION * random())
        self.y = int(Y_DIMENSION * random())
        self.radius = 1