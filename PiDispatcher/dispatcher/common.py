import logging
import sys

LISTEN_IP = '0.0.0.0'
TCP_PORT = 9999


def set_logging(logger, filename='dispatcher.log'):
    logger.setLevel(logging.DEBUG)

    # File handler for debug logs
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
    logger.addHandler(file_handler)
    # Stream handler for important output to stdout
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(stdout_handler)


