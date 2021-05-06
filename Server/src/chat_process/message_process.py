from socket import socket

from chat_commands import ChatCommands
from constants import ChatCommandsConstants, ChatConstants
from client_info import ServerRepository


def receive_to_client(client):
    try:
        message = client.recv(1024).decode('utf-8')
        return message
    except ConnectionResetError as e:  # removing clients
        client.close()
        return


def send_to_client(client: socket, message: str):
    try:
        client.send(message.encode('utf-8'))
    except ConnectionResetError as e:  # removing clients
        client.close()
        return


def send_chat_commands(client: socket):  # send chat commands to client
    send_to_client(client, "CHAT COMMANDS")
    for chat_command in ChatConstants.chat_commands_list:
        send_to_client(client, chat_command)


def send_online_list(client: socket, db_service):  # send online list to client
    send_to_client(client, 'ONLINE LIST')
    for online_list in db_service.get_online_list():
        send_to_client(client, 'user {}: online'.format(online_list[0]))


# send private message history to client
def send_private_message_history(client: socket, sender_id: int, recipient_id: int, limit: int, db_service):
    send_to_client(client, 'MESSAGE PRIVATE HISTORY WITH {}'.format(recipient_id))
    for array_history in db_service.get_private_message_history(sender_id, recipient_id, limit):
        send_to_client(client, '{}: {}'.format(array_history[0], array_history[1]))


def send_message_history_server(client: socket, limit: int, db_service):  # send message history server to client
    send_to_client(client, 'MESSAGE HISTORY')
    for array_history in db_service.get_message_history_server(limit):
        send_to_client(client, '{}: {}'.format(array_history[0], array_history[1]))


def add_message_history(sender_id: int, recipient_id: int, message: str, db_service):  # add message history to bd
    db_service.add_message_history(sender_id, recipient_id, message)


def broadcast(sender_id: int, message: str, db_service):  # sending messages to users
    add_message_history(sender_id, 0, message, db_service)
    for key in ServerRepository.clients:
        send_to_client(ServerRepository.clients[key].client, message)


# send private message sender and recipient
def private_message(sender_id: int, recipient_id: int, message: str, db_service):
    send_to_client(ServerRepository.clients[sender_id].client,
                   'Private message to {}: {}'.format(ServerRepository.clients[recipient_id].nickname, message))

    send_to_client(ServerRepository.clients[recipient_id].client,
                   'Private message from {}: {}'.format(ServerRepository.clients[sender_id].nickname, message))

    add_message_history(sender_id, recipient_id, message, db_service)


def process_chat_commands(client: socket, message: str, user_id: int,
                          db_service) -> bool:  # handle chat commands from user
    if ChatCommands.private_message.is_message_contains_command(message):
        target_nickname = message[:ChatCommandsConstants.command_size_one_character].split(" ")[1]
        if db_service.chek_user_online(target_nickname):
            recipient_id = db_service.get_user_id_by_name(target_nickname)
            private_message(user_id, recipient_id,
                            message[len(ChatCommands.private_message.command) + len(target_nickname) + 2:], db_service)
        else:
            send_to_client(client, 'user {} offline'.format(target_nickname))
        return True

    if ChatCommands.history_message_server.is_message_contains_command(message):
        limit = int(message[:ChatCommandsConstants.command_size_one_character].split(" ")[1])
        send_message_history_server(client, limit, db_service)
        return True

    if ChatCommands.history_private_message.is_message_contains_command(message):
        target_nickname = message[:ChatCommandsConstants.history_private_message_command_size].split(" ")[1]
        limit = int(message[:ChatCommandsConstants.history_private_message_command_size].split(" ")[2])
        recipient_id = db_service.get_user_id_by_name(target_nickname)
        send_private_message_history(client, user_id, recipient_id, limit, db_service)
        return True

    if ChatCommands.online_list.is_message_contains_command(message):
        send_online_list(client, db_service)
        return True

    if ChatCommands.chat_commands.is_message_contains_command(message):
        send_chat_commands(client)
        return True

    return False
