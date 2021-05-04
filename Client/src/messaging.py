from constants import logger


def receive(client):
    try:
        message = client.recv(1024).decode('utf-8')

        return message
    except ConnectionResetError as e:
        logger.error("disconnection from server!")
        client.close()
        return None


def listen_new_message(client):
    while True:  # making valid connection
        message = receive(client)
        if message is None:
            break
        print(message)


def send_to_server(client, message: str):
    client.send(message.encode('utf-8'))


def write(client):  # sending a message
    while True:
        message = input('')
        send_to_server(client, message)