import logging
import re
import socket
import string

import docopt

from dispatcher.server import TCP_PORT

_log = logging.getLogger(__name__)


def send_to_server():
    """BodySensor Dispatcher client

    Send a message to the server.

    MESSAGE is a sequence of comma-delimeted byte values, e.g.

    1,23, 22, 14, 14 , 1, 255, 0

    Usage: dispatcher_client [--ip=<IP>] MESSAGE

    Options:
        --ip=<IP>  The IP to connect to [default: 127.0.0.1]
    """
    logging.basicConfig(level=logging.DEBUG, filename='dispatcher_client.log')
    args = docopt.docopt(send_to_server.__doc__, help=False)
    ip = args['--ip']
    input_ = args['MESSAGE']
    # Split into a list of str values, trimming whitespace to allow easy parsing.
    input_numbers = [int(s) for s in input_.replace(' ', '').split(',')]
    input_string = string.join([chr(b) for b in input_list], '')

    _log.info('Sending to server %s: %s', ip, [ord(b) for b in input_string])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, TCP_PORT))
    s.send(input_string)
    s.close()