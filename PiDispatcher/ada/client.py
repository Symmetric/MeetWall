import logging
import socket

import docopt

from dispatcher.server import TCP_PORT

_log = logging.getLogger(__name__)


def send_to_server():
    """BodySensor Dispatcher client

    Send a message to the server.

    Usage: dispatcher_client [--ip=<IP>] MESSAGE

    Options:
        --ip=<IP>  The IP to connect to [default: 127.0.0.1]
    """
    logging.basicConfig(level=logging.DEBUG, filename='dispatcher_client.log')
    args = docopt.docopt(send_to_server.__doc__, help=False)
    ip = args['--ip']
    msg = args['MESSAGE']
    _log.info('Sending to server %s: %s', ip, msg)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, TCP_PORT))
    s.send(bytes(msg, 'UTF-8'))
    s.close()