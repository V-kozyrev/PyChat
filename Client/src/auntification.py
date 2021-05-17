from socket import socket
from constants import logger, LoginConstants
from messaging import send_to_server, receive, listen_new_message, write
from user_info import UserInfo
import threading


def receive_user_info(client: socket):
    """
    Getting login parameters from server
    :param client: Client socket
    :return: True when user data is correct. False when entered incorrect user data
    """
    while True:
        message = receive(client)
        if message == LoginConstants.LOGIN:
            send_to_server(client, UserInfo().login)
            continue
        if message == LoginConstants.NAME:
            send_to_server(client, UserInfo().nickname)
            continue
        if message == LoginConstants.PASSWORD:
            send_to_server(client, UserInfo().password)
            return True
        if message == LoginConstants.WRONG_LOGIN_OR_PASS:
            print("Wrong username or password")
            return False
        if message == LoginConstants.USER_EXISTS:
            print("User already exists in chat, try to login")
            return False


def get_user_info() -> UserInfo:
    """
    Get user information from input
    :return: User info
    """
    print('for registration enter: {}, for authorization enter: {}'.format
          (LoginConstants.registration, LoginConstants.authorization))
    while True:
        if (user_input := input('')) in [LoginConstants.registration, LoginConstants.authorization]:
            break
    if user_input == LoginConstants.registration:
        login = input("Choose your login: ")
        password = input("Choose your password: ")
        nickname = input("Choose your nickname: ")
        return UserInfo(login=login, password=password, nickname=nickname, is_new_user=True)
    if user_input == LoginConstants.authorization:
        login = input("Choose your login: ")
        password = input("Choose your password: ")
        return UserInfo(login=login, password=password, nickname=None, is_new_user=False)


def entry_process(client: socket):
    """
    Server login process. Opening a stream for reading and entering messages
    :param client: Client socket
    :return: Nothing
    """
    is_authorized = False
    while not is_authorized:
        user_info = get_user_info()

        if user_info.is_new_user:
            try:
                send_to_server(client, LoginConstants.REGISTRATION)
            except ConnectionResetError:
                logger.error("disconnection from server!")
                client.close()
        else:
            try:
                send_to_server(client, LoginConstants.AUTHORIZATION)
            except ConnectionResetError:
                logger.error("disconnection from server!")
                client.close()
        is_authorized = receive_user_info(client)

    read_thread = threading.Thread(target=listen_new_message, args=(client,))
    read_thread.start()
    write_thread = threading.Thread(target=write, args=(client,))
    write_thread.start()
