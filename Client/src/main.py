import socket
from auntification import entry_process
from constants import ConnectionConstants, logger


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization

    try:
        client.connect((ConnectionConstants.host, ConnectionConstants.port))  # connecting client to server
        entry_process(client)
    except ConnectionRefusedError as e:
        logger.error("the server is down!")
        client.close()


if __name__ == '__main__':
    run_client()
