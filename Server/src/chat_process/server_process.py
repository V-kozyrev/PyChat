import threading
import logging
from socket import socket

from chat_process.message_process import process_chat_commands, broadcast, send_to_client, \
    send_message_history_server, send_chat_commands, receive_from_client, add_message_history
from constants import EntryType
from client_info import ServerRepository, ClientInfo
from db.db import DataBase
from db.db_service import DataBaseServices

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def remove_disconnected_user(user_id: int, db_service: DataBaseServices):  # remove client
    """
    Remove disconnected user from db and ServerRepository
    :param user_id: User id from db
    :param db_service: Service class for db
    """

    logger.info("Client was disconnect, kicking from server")
    broadcast(user_id, '{} left!'.format(ServerRepository.clients[user_id].nickname), db_service)
    db_service.change_offline_user_id(user_id)
    ServerRepository.clients.pop(user_id)


def handle(user_id: int):
    """
    Customer message processing
    :param user_id: User id from db
    :return: Nothing
    """
    db_service = DataBase().get_service()
    client = ServerRepository.clients[user_id].client
    while True:
        message = receive_from_client(client)
        if message is None:
            remove_disconnected_user(user_id, db_service)
            break
        if process_chat_commands(client, message, user_id, db_service):  # processing user message
            continue
        add_message_history(user_id, 0, message, db_service)
        message = '{}: {}'.format(ServerRepository.clients[user_id].nickname, message)
        broadcast(user_id, message, db_service)  # sending messages to users


def post_authentication(user_id: int, client: socket, nickname: str, db_service: DataBaseServices):
    """
    Allocating a stream to a user and client connection alert
    :param user_id: User id from db
    :param client: Client socket
    :param nickname: Name of client
    :param db_service: Commands from db
    :return: Nothing
    """
    ServerRepository.clients[user_id] = ClientInfo(client=client, nickname=nickname)
    logger.info("client logged, his nickname {}".format(nickname))
    broadcast(user_id, "{} joined!".format(nickname), db_service)


def registration(client: socket, db_service: DataBaseServices):
    """
    Registration client
    :param client: Client socket
    :param db_service: Commands from db
    :return: User_id or nothing
    """
    send_to_client(client, 'LOGIN')
    login = receive_from_client(client)
    if not db_service.is_login_exists(login):
        send_to_client(client, 'USER EXISTS')
        return
    send_to_client(client, 'NAME')
    nickname = receive_from_client(client)
    send_to_client(client, 'PASSWORD')
    user_pass = receive_from_client(client)
    user_id = db_service.register_user(login, user_pass, nickname)
    post_authentication(user_id, client, nickname, db_service)
    return user_id


def authorization(client: socket, db_service: DataBaseServices):
    """
    Authorization client
    :param client: Client socket
    :param db_service: Commands from db
    :return: User_id or nothing
    """
    send_to_client(client, 'LOGIN')
    login = receive_from_client(client)
    send_to_client(client, 'PASSWORD')
    user_pass = receive_from_client(client)
    if not db_service.is_credential_valid(login, user_pass):
        send_to_client(client, 'WRONG LOGIN OR PASS')
        client.close()
        return

    user_id = db_service.get_user_id_by_login(login)
    nickname = db_service.get_user_name(user_id)
    db_service.change_online_user_id(user_id)
    send_message_history_server(client, 10, db_service)
    post_authentication(user_id, client, nickname, db_service)
    return user_id


def entry_process(entry_type: EntryType, client: socket):  # user login process
    """
    Start of client registration or authorization. Opening a stream to receive user messages
    :param entry_type: Input parameter
    :param client: Client socket
    :return: Nothing
    """
    db_service = DataBase().get_service()

    if entry_type == EntryType.REGISTRATION:
        user_id = registration(client, db_service)
    elif entry_type == EntryType.AUTHORIZATION:
        user_id = authorization(client, db_service)
    else:
        return

    send_chat_commands(client)
    thread = threading.Thread(target=handle, args=(user_id,))
    thread.start()
