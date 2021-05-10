from socket import socket

from constants import logger


def receive(client: socket):
    """
    Receiving messages from the server
    :param client: Client socket
    :return: Message
    """
    try:
        message = client.recv(1024).decode('utf-8')

        return message
    except ConnectionResetError as e:
        logger.error("disconnection from server!")
        client.close()
        return None


def listen_new_message(client: socket):
    """
    Displaying a message to the user
    :param client: Client socket
    :return: Nothing
    """
    while True:  # making valid connection
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
    client.send(message.encode('utf-8'))


def write(client: socket):  # sending a message
    """
    User input new message
    :param client: Client socket
    :return: Nothing
    """
    while True:
        message = input('')
        send_to_server(client, message)
