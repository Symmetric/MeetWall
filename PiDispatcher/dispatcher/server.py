import logging
import socket
import asyncio

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
    server = loop.run_until_complete(loop.create_server(
        protocol_factory=DispatcherProtocol,
        port=TCP_PORT,
        family=socket.AF_INET)
    )
    loop.run_until_complete(server.wait_closed())