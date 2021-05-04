from constants import StringConstants, logger
from messaging import *
from user_info import UserInfo
import threading


def receive_user_info(client):
    while True:  # making valid connection
        message = receive(client)
        if message == StringConstants.LOGIN:
            send_to_server(client, UserInfo().login)
            continue
        if message == StringConstants.NAME:
            send_to_server(client, UserInfo().nickname)
            continue
        if message == StringConstants.PASSWORD:
            send_to_server(client, UserInfo().password)
            return True
        if message == StringConstants.WRONG_LOGIN_OR_PASS:
            print("Wrong username or password")
            return False
        if message == StringConstants.USER_EXISTS:
            print("User already exists in chat, try to login")
            return False


def get_user_info() -> UserInfo:
    print('1: регистрация, 2: авторизация, напиши цифру')
    while True:
        if (user_input := input('')) in ["1", "2"]:
            break
    if user_input == '1':
        login = input("Choose your login: ")
        password = input("Choose your password: ")
        nickname = input("Choose your nickname: ")  # проверить на допустимые значения
        return UserInfo(login=login, password=password, nickname=nickname, is_new_user=True)
    if user_input == '2':
        login = input("Choose your login: ")
        password = input("Choose your password: ")
        return UserInfo(login=login, password=password, nickname=None, is_new_user=False)


def entry_process(client):
    is_authorized = False
    while not is_authorized:
        user_info = get_user_info()

        if user_info.is_new_user:
            try:
                send_to_server(client, 'REGISTRATION')  # переделать регистрацию в отправку 1 сообщения
            except ConnectionResetError as e:
                logger.error("disconnection from server!")
                client.close()
        else:
            try:
                send_to_server(client, 'AUTHORIZATION')
            except ConnectionResetError as e:
                logger.error("disconnection from server!")
                client.close()
        is_authorized = receive_user_info(client)

    read_thread = threading.Thread(target=listen_new_message, args=(client,))  # sending messages
    read_thread.start()
    write_thread = threading.Thread(target=write, args=(client,))  # sending messages
    write_thread.start()