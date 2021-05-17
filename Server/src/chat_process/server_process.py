import threading
import logging
from socket import socket

from chat_commands import ChatCommands
from chat_process.message_process import process_chat_commands, broadcast, send_to_client, \
    send_message_history_server, receive_from_client
from constants import EntryType, LoginConstants, ServerConstants
from client_info import ClientInfo
from server_repository import ServerRepository
from db.db import DataBase
from db.db_service import DataBaseServices

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def remove_disconnected_user(user_id: int, db_service: DataBaseServices):
    """
    Remove disconnected user from db and ServerRepository
    :param user_id: User id from db
    :param db_service: Service class for db
    """
    logger.info("Client was disconnect, kicking from server")
    db_service.change_offline_user_id(user_id)
    ServerRepository.clients.pop(user_id)
    if len(ServerRepository.clients.keys()) != 0:
        broadcast('{} left!'.format(ServerRepository.clients[user_id].nickname))


def handle(user_id: int):
    """
    Client message processing
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
        try:
            if process_chat_commands(client, message, user_id, db_service):
                continue
        except IndexError:
            send_to_client(client, "The server couldn't process the chat command")
            continue
        db_service.add_message_history(user_id, ServerConstants.history_server, message)
        message = '{}: {}'.format(ServerRepository.clients[user_id].nickname, message)
        broadcast(message)


def post_authentication(user_id: int, client: socket, nickname: str):
    """
    Post authentication process, adding a user to server repository, and broadcast notification to all users.
    :param user_id: User id from db
    :param client: Client socket
    :param nickname: Name of client
    :return: Nothing
    """
    ServerRepository.clients[user_id] = ClientInfo(client=client, nickname=nickname)
    logger.info("client logged, his nickname {}".format(nickname))
    broadcast("{} joined!".format(nickname))


def registration(client: socket, db_service: DataBaseServices):
    """
    Client registration
    :param client: Client socket
    :param db_service: Commands from db
    :return: User_id when registration is successful or False when registration was unsuccessful
    """
    send_to_client(client, LoginConstants.LOGIN)
    login = receive_from_client(client)
    if db_service.is_login_exists(login):
        send_to_client(client, LoginConstants.USER_EXISTS)
        return False
    send_to_client(client, LoginConstants.NAME)
    nickname = receive_from_client(client)
    send_to_client(client, LoginConstants.PASSWORD)
    user_pass = receive_from_client(client)
    user_id = db_service.register_user(login, user_pass, nickname)
    post_authentication(user_id, client, nickname)
    return user_id


def authorization(client: socket, db_service: DataBaseServices):
    """
    Authorization client
    :param client: Client socket
    :param db_service: Commands from db
    :return: User_id when authorization is successful or False when authorization was unsuccessful
    """
    send_to_client(client, LoginConstants.LOGIN)
    login = receive_from_client(client)
    send_to_client(client, LoginConstants.PASSWORD)
    user_pass = receive_from_client(client)
    if not db_service.is_credential_valid(login, user_pass):
        send_to_client(client, LoginConstants.WRONG_LOGIN_OR_PASS)
        client.close()
        return False
    user_id = db_service.get_user_id_by_login(login)
    nickname = db_service.get_user_name(user_id)
    db_service.change_online_user_id(user_id)
    send_message_history_server(client, ServerConstants.size_history_server, db_service)
    post_authentication(user_id, client, nickname)
    return user_id


def entry_process(entry_type: EntryType, client: socket):
    """
    Start of client registration or authorization. Opening a stream to receive user messages
    :param entry_type: Input parameter
    :param client: Client socket
    :return: False when login failed
    """
    db_service = DataBase().get_service()
    if entry_type == EntryType.REGISTRATION:
        user_id = registration(client, db_service)
    elif entry_type == EntryType.AUTHORIZATION:
        user_id = authorization(client, db_service)
    else:
        return
    if user_id is False:
        return False
    send_to_client(client, ChatCommands().get_chat_commands_with_description())
    thread = threading.Thread(target=handle, args=(user_id,))
    thread.start()
