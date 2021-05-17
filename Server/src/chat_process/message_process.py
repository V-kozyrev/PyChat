from socket import socket
from chat_commands import ChatCommands
from constants import ChatCommandsConstants, MessageConstants
from server_repository import ServerRepository
from db.db_service import DataBaseServices


def receive_from_client(client: socket):
    """
    Receiving a message from a client
    :param client: Client socket
    :return: Client message
    """
    try:
        message = client.recv(MessageConstants.size_message_bytes).decode(MessageConstants.server_encoding)
        return message
    except ConnectionResetError:
        client.close()
        return


def send_to_client(client: socket, message: str):
    """
    Send massage to client
    :param client: Client socket
    :param message: Client message
    :return: Nothing
    """
    try:
        client.send(message.encode(MessageConstants.server_encoding))
    except ConnectionResetError:
        client.close()
        return


def send_private_message_history(client: socket, sender_id: int, recipient_id: int, limit: int,
                                 db_service: DataBaseServices):
    """
    Send history private message to client
    :param client: Client socket
    :param sender_id: Sender id
    :param recipient_id: Recipient id
    :param limit: Number of messages taken from the db
    :param db_service: Commands from db
    :return: Nothing
    """
    send_to_client(client,
                   "MESSAGE PRIVATE HISTORY WITH {}\n".format(
                       ServerRepository.clients[recipient_id].nickname) + "\n".join(
                       '{}: {}'.format(array_history[0], array_history[1]) for array_history in
                       db_service.get_private_message_history(sender_id, recipient_id, limit)))


def send_message_history_server(client: socket, limit: int, db_service: DataBaseServices):
    """
    Send server message history to client
    :param client: Client socket
    :param limit: Number of messages taken from the db
    :param db_service: Commands from db
    :return: Nothing
    """
    send_to_client(client, "MESSAGE_HISTORY:\n" + "\n".join(
        '{}: {}'.format(array_history[0], array_history[1]) for array_history in
        db_service.get_message_history_server(limit)))
    # for array_history in db_service.get_message_history_server(limit):
    #    send_to_client(client, '{}: {}'.format(array_history[0], array_history[1]))


def broadcast(message: str):
    """
    Sending message to all users
    :param message: Client message
    :return: Nothing
    """
    for client in ServerRepository.clients:
        send_to_client(ServerRepository.clients[client].client, message)


def private_message(sender_id: int, recipient_id: int, message: str, db_service: DataBaseServices):
    """
    Sending a private message and add to db
    :param sender_id: Sender id
    :param recipient_id: Recipient id
    :param message: Client message
    :param db_service: Commands from db
    :return: Nothing
    """
    send_to_client(ServerRepository.clients[sender_id].client,
                   'Private message to {}: {}'.format(ServerRepository.clients[recipient_id].nickname, message))

    send_to_client(ServerRepository.clients[recipient_id].client,
                   'Private message from {}: {}'.format(ServerRepository.clients[sender_id].nickname, message))

    db_service.add_message_history(sender_id, recipient_id, message)


def process_chat_commands(client: socket, message: str, user_id: int,
                          db_service: DataBaseServices) -> bool:
    """
    Processing user message and command execution
    :param client: Client socket
    :param message: Client message
    :param user_id: User id from db
    :param db_service: Commands from db
    :return: True when the user message contains the command.
             False when the user message does not contains the command
    """
    if ChatCommands.private_message.is_message_contains_command(message):
        target_nickname = message[:ChatCommandsConstants.max_size_one_character_command_with_arg].split(" ")[1]
        if db_service.is_nickname_exists(target_nickname) is False:
            send_to_client(client, "this nickname does not exist")
            return True
        if db_service.chek_user_online(target_nickname):
            recipient_id = db_service.get_user_id_by_name(target_nickname)
            private_message(user_id, recipient_id,
                            message[len(ChatCommands.private_message.command) + len(target_nickname) + 2:], db_service)
        else:
            send_to_client(client, 'user {} offline'.format(target_nickname))
        return True

    if ChatCommands.history_message_server.is_message_contains_command(message):
        limit = int(message[:ChatCommandsConstants.max_size_one_character_command_with_arg].split(" ")[1])
        send_message_history_server(client, limit, db_service)
        return True

    if ChatCommands.history_private_message.is_message_contains_command(message):
        target_nickname = message[:ChatCommandsConstants.max_size_three_character_command_with_arg].split(" ")[1]
        if db_service.is_nickname_exists(target_nickname) is False:
            send_to_client(client, "this nickname does not exist")
            return True
        limit = int(message[:ChatCommandsConstants.max_size_three_character_command_with_arg].split(" ")[2])
        recipient_id = db_service.get_user_id_by_name(target_nickname)
        send_private_message_history(client, user_id, recipient_id, limit, db_service)
        return True

    if ChatCommands.online_list.is_message_contains_command(message):
        send_to_client(client, ServerRepository().get_user_online_list())
        return True

    if ChatCommands.chat_commands.is_message_contains_command(message):
        send_to_client(client, ChatCommands().get_chat_commands_with_description())
        return True

    return False
