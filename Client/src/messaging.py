from socket import socket
from constants import logger, MessageConstants


def receive(client: socket):
    """
    Receiving messages from the server
    :param client: Client socket
    :return: Message
    """
    try:
        message = client.recv(MessageConstants.size_message_bytes).decode(MessageConstants.server_encoding)
        return message
    except ConnectionResetError:
        logger.error("disconnection from server!")
        client.close()
        return


def listen_new_message(client: socket):
    """
    Displaying a message to the user
    :param client: Client socket
    :return: Nothing
    """
    while True:
        message = receive(client)
        if message is None:
            break
        print(message)


def send_to_server(client: socket, message: str):
    """
    Send message to server
    :param client: Client socket
    :param message:
    :return: Nothing
    """
    client.send(message.encode(MessageConstants.server_encoding))


def write(client: socket):
    """
    User input new message
    :param client: Client socket
    :return: Nothing
    """
    while True:
        message = input('')
        send_to_server(client, message)
