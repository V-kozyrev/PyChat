from socket import socket

from constants import logger


def receive(client: socket):
    try:
        message = client.recv(1024).decode('utf-8')

        return message
    except ConnectionResetError as e:
        logger.error("disconnection from server!")
        client.close()
        return None


def listen_new_message(client: socket):
    while True:  # making valid connection
        message = receive(client)
        if message is None:
            break
        print(message)


def send_to_server(client: socket, message: str):
    client.send(message.encode('utf-8'))


def write(client: socket):  # sending a message
    while True:
        message = input('')
        send_to_server(client, message)
