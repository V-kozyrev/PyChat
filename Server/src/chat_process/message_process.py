from chat_commands import ChatCommands
from constants import ChatCommandsConstants, ChatConstants, ServerRepository


def send_to_client(client, message: str):
    client.send(message.encode('utf-8'))


def send_chat_commands(client):  # send chat commands to client
    send_to_client(client, "CHAT COMMANDS")
    for chat_command in ChatConstants.chat_commands_list:
        send_to_client(client, chat_command)


def send_online_list(client):  # send online list to client
    send_to_client(client, 'ONLINE LIST')
    for online_list in ChatConstants.db_service.get_online_list():
        send_to_client(client, 'user {}: online'.format(online_list[0]))


# send private message history to client
def send_private_message_history(client, id_sender: int, id_recipient: int, limit: int):
    send_to_client(client, 'MESSAGE PRIVATE HISTORY WITH {}'.format(id_recipient))
    for array_history in ChatConstants.db_service.get_private_message_history(id_sender, id_recipient, limit):
        send_to_client(client, '{}: {}'.format(array_history[0], array_history[1]))


def send_message_history_server(client, limit: int):  # send message history server to client
    send_to_client(client, 'MESSAGE HISTORY')
    for array_history in ChatConstants.db_service.get_message_history_server(limit):
        send_to_client(client, '{}: {}'.format(array_history[0], array_history[1]))


def add_message_history(id_sender: int, id_recipient: int, message: str):  # add message history to bd
    ChatConstants.db_service.add_message_history(id_sender, id_recipient, message)


def broadcast(message):  # sending messages to users
    for key in ServerRepository.clients:
        send_to_client(ServerRepository.clients[key], message)


def private_message(id_sender: int, id_recipient: int, message: str):  # send private message sender and recipient
    send_to_client(ServerRepository.clients[id_sender],
                   'Private message to {}: {}'.format(ServerRepository.nicknames[id_recipient], message))

    send_to_client(ServerRepository.clients[id_recipient],
                   'Private message from {}: {}'.format(ServerRepository.nicknames[id_sender], message))

    add_message_history(id_sender, id_recipient, message)


def process_chat_commands(client, message: str, user_id: int) -> bool:  # handle chat commands from user
    if message[ChatCommands.private_message.start_idx_in_message: ChatCommands.private_message.end_idx_in_message] == ChatCommands.private_message.command:
        target_nickname = message[:ChatCommandsConstants.command_size_one_character].split(" ")[1]
        if ChatConstants.db_service.chek_user_online(target_nickname):
            id_recipient = ChatConstants.db_service.get_user_id_by_name(target_nickname)
            private_message(user_id, id_recipient,
                            message[len(ChatCommands.private_message.command) + len(target_nickname) + 2:])
        else:
            send_to_client(client, 'user {} offline'.format(target_nickname))
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
