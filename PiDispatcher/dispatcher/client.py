import logging
import socket
import string
import time

import docopt

from dispatcher.common import set_logging, TCP_PORT


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
    set_logging(_log, filename='dispatcher_client.log')
    args = docopt.docopt(send_to_server.__doc__, help=False)
    ip = args['--ip']
    input_ = args['MESSAGE']
    messages = input_.split(':')
    _log.debug('Got messages: %s', messages)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, TCP_PORT))

    for message in messages:
        # Split into a list of str values, trimming whitespace to allow easy parsing.
        input_numbers = [int(s) for s in message.replace(' ', '').split(',')]
        input_string = string.join([chr(b) for b in input_numbers], '')
        if len(input_string) < 160:
            missing_bytes = 160 - len(input_string)
            input_string += chr(0) * missing_bytes

        output_bytes = [ord(b) for b in input_string]
        _log.info('Sending to server %s, len=%d: %s', ip, len(output_bytes), output_bytes)
        sock.send(input_string)
        time.sleep(1)

    sock.close()
