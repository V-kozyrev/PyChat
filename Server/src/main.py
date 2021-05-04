import socket
from constants import EntryType, ChatConstants
from chat_process.server_process import entry_process


def receive_client():  # get a client and authorize
    while True:
        client, address = server.accept()
        ChatConstants.logger.info("Connected with {}".format(str(address)))
        try:
            message = client.recv(1024).decode('utf-8')
        except ConnectionResetError as e:
            client.close()
            continue
        if message == ChatConstants.REGISTRATION:
            entry_process(EntryType.REGISTRATION, client)
        elif message == ChatConstants.AUTHORIZATION:
            entry_process(EntryType.AUTHORIZATION, client)
        else:
            client.close()
            ChatConstants.logger.info("client disconnection")


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    server.bind((ChatConstants.host, ChatConstants.port))  # binding host and port to socket
    server.listen()
    receive_client()
