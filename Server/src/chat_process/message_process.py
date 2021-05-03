from chat_commands import ChatCommands
from constants import ChatCommandsConstants, ChatConstants, ServerRepository


def send_chat_commands(client):  # send chat commands to client
    client.send("CHAT COMMANDS".encode('utf-8'))
    for chat_command in ChatConstants.chat_commands_list:
        client.send(chat_command.encode('utf-8'))


def send_online_list(client):  # send online list to client
    client.send('ONLINE LIST'.encode('utf-8'))
    for online_list in ChatConstants.db_service.get_online_list():
        client.send('user {}: online'.format(online_list[0]).encode('utf-8'))


# send private message history to client
def send_private_message_history(client, id_sender: int, id_recipient: int, limit: int):
    client.send('MESSAGE PRIVATE HISTORY WITH {}'.format(id_recipient).encode('utf-8'))
    for array_history in ChatConstants.db_service.get_private_message_history(id_sender, id_recipient, limit):
        client.send('{}: {}'.format(array_history[0], array_history[1]).encode('utf-8'))


def send_message_history_server(client, limit: int):  # send message history server to client
    client.send('MESSAGE HISTORY'.encode('utf-8'))
    for array_history in ChatConstants.db_service.get_message_history_server(limit):
        client.send('{}: {}'.format(array_history[0], array_history[1]).encode('utf-8'))


def add_message_history(id_sender: int, id_recipient: int, message: str):  # add message history to bd
    ChatConstants.db_service.add_message_history(id_sender, id_recipient, message)


def broadcast(message):  # sending messages to users
    for key in ServerRepository.clients:
        ServerRepository.clients[key].send(message)


def private_message(id_sender: int, id_recipient: int, message: str):  # send private message sender and recipient
    ServerRepository.clients[id_sender].send(
        'Private message to {}: {}'.format(ServerRepository.nicknames[id_recipient], message).encode('utf-8'))
    ServerRepository.clients[id_recipient].send(
        'Private message from {}: {}'.format(ServerRepository.nicknames[id_sender], message).encode('utf-8'))
    add_message_history(id_sender, id_recipient, message)


def process_chat_commands(client, message: str, user_id: int) -> bool:  # handle chat commands from user
    if message[ChatCommands.private_message.start_idx_in_message: ChatCommands.private_message.end_idx_in_message] == ChatCommands.private_message.command:
        target_nickname = message[:ChatCommandsConstants.command_size_one_character].split(" ")[1]
        if ChatConstants.db_service.chek_user_online(target_nickname):
            id_recipient = ChatConstants.db_service.get_user_id_by_name(target_nickname)
            private_message(user_id, id_recipient,
                            message[len(ChatCommands.private_message.command) + len(target_nickname) + 2:])
        else:
            client.send('user {} offline'.format(target_nickname).encode('utf-8'))
        return True

    elif message[ChatCommands.history_message_server.start_idx_in_message: ChatCommands.history_message_server.end_idx_in_message] == ChatCommands.history_message_server.command:
        limit = int(message[:ChatCommandsConstants.command_size_one_character].split(" ")[1])
        send_message_history_server(client, limit)
        return True

    elif message[ChatCommands.history_private_message.start_idx_in_message: ChatCommands.history_private_message.end_idx_in_message] == ChatCommands.history_private_message.command:
        target_nickname = message[:ChatCommandsConstants.history_private_message_command_size].split(" ")[1]
        limit = int(message[:ChatCommandsConstants.history_private_message_command_size].split(" ")[2])
        id_recipient = ChatConstants.db_service.get_user_id_by_name(target_nickname)
        send_private_message_history(client, user_id, id_recipient, limit)
        return True

    elif message[ChatCommands.online_list.start_idx_in_message: ChatCommands.online_list.end_idx_in_message] == ChatCommands.online_list.command:
        send_online_list(client)
        return True

    elif message[ChatCommands.chat_commands.start_idx_in_message: ChatCommands.chat_commands.end_idx_in_message] == ChatCommands.chat_commands.command:
        send_chat_commands(client)
        return True

    return False
