import socket
import logging
from chat_process.message_process import receive_from_client
from constants import EntryType, LoginConstants, ConnectionConstants
from chat_process.server_process import entry_process


def receive_client():
    """
    Client to server connection
    :return: Nothing
    """
    while True:
        client, address = server.accept()
        logger.info("Connected with {}".format(str(address)))
        try:
            message = receive_from_client(client)
        except ConnectionResetError:
            client.close()
            continue
        if message == LoginConstants.REGISTRATION:
            if entry_process(EntryType.REGISTRATION, client) is False:
                client.close()
                logger.info("client disconnection")
        elif message == LoginConstants.AUTHORIZATION:
            if entry_process(EntryType.AUTHORIZATION, client) is False:
                client.close()
                logger.info("client disconnection")
        # TODO в будущем сделать отдельный поток на вход каждого пользователя без разрыва соединения
        else:
            client.close()
            logger.info("client disconnection")


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    server.bind((ConnectionConstants.host, ConnectionConstants.port))  # binding host and port to socket
    server.listen()
    receive_client()
