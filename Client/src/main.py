import socket
import threading
import logging
from constants import ChatConstants


def receive(login: str, password: str, nickname: str):
    while True:  # making valid connection
        try:
            message = client.recv(1024).decode('utf-8')
        except ConnectionResetError as e:
            logger.error("disconnection from server!")
            client.close()
            break
        if message == ChatConstants.LOGIN:
            client.send(login.encode('utf-8'))
        elif message == ChatConstants.PASSWORD:
            client.send(password.encode('utf-8'))
        elif message == ChatConstants.NAME:
            client.send(nickname.encode('utf-8'))
        elif message == ChatConstants.WRONG_LOGIN_OR_PASS:
            print(message)
            client.close()
            break
        else:
            print(message)


def write():  # sending a message
    while True:
        message = input('')
        client.send(message.encode('utf-8'))


def entry_process():
    print('1: регистрация, 2: авторизация, напиши цифру')
    user_input = input('')
    try:
        if user_input == '1':
            client.send('REGISTRATION'.encode('utf-8'))
            login = input("Choose your login: ")
            password = input("Choose your password: ")
            nickname = input("Choose your nickname: ")
            receive_thread = threading.Thread(target=receive,
                                              args=(login, password, nickname))  # receiving multiple messages
            receive_thread.start()
        elif user_input == '2':
            client.send('AUTHORIZATION'.encode('utf-8'))
            login = input("Choose your login: ")
            password = input("Choose your password: ")
            receive_thread = threading.Thread(target=receive,
                                              args=(login, password, None))  # receiving multiple messages
            receive_thread.start()
        else:
            return False
    except ConnectionResetError as e:
        logger.error("disconnection from server!")
        client.close()

    write_thread = threading.Thread(target=write)  # sending messages
    write_thread.start()


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
    logger = logging.getLogger(__name__)
    try:
        client.connect((ChatConstants.host, ChatConstants.port))  # connecting client to server
        entry_process()
    except ConnectionRefusedError as e:
        logger.error("the server is down!")
        client.close()
