import threading
from chat_process.message_process import *
from constants import EntryType, ChatConstants, ServerRepository


def remove_disconected_user(user_id: int, client):  # remove client
    ChatConstants.logger.info("Client was disconnect, kicking from server")
    ServerRepository.clients.pop(user_id)
    client.close()
    ChatConstants.db_service.change_offline_user_id(user_id)
    broadcast('{} left!'.format(ServerRepository.nicknames[user_id]).encode('utf-8'))
    ServerRepository.nicknames.pop(user_id)


def handle(client, user_id: int):
    while True:
        try:   # recieving valid messages from client
            message = client.recv(1024).decode('utf-8')
        except ConnectionResetError as e:  # removing clients
            remove_disconected_user(user_id, client)
            break
        if process_chat_commands(client, message, user_id):  # processing user message
            continue
        add_message_history(user_id, 0, message)
        message = '{}: {}'.format(ServerRepository.nicknames[user_id], message).encode('utf-8')
        broadcast(message)  # sending messages to users


def entry_process(entry_type: EntryType, client):  # user login process
    try:
        if entry_type == EntryType.REGISTRATION:
            client.send('LOGIN'.encode('utf-8'))
            login = client.recv(1024).decode('utf-8')
            if ChatConstants.db_service.chek_user_login(login):
                client.send('USER EXISTS'.encode('utf-8'))
                return False
            else:
                client.send('PASS'.encode('utf-8'))
                user_pass = client.recv(1024).decode('utf-8')
                client.send('NAME'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                ChatConstants.db_service.register_user(login, user_pass, nickname)
            pass
        elif entry_type == EntryType.AUTHORIZATION:
            client.send('LOGIN'.encode('utf-8'))
            login = client.recv(1024).decode('utf-8')
            client.send('PASSWORD'.encode('utf-8'))
            user_pass = client.recv(1024).decode('utf-8')
            if ChatConstants.db_service.chek_user(login, user_pass):
                user_id = ChatConstants.db_service.get_user_id_by_login(login)
                nickname = ChatConstants.db_service.get_user_name(user_id)
                ChatConstants.db_service.change_online_user_id(user_id)
                send_message_history_server(client, 10)
            else:
                client.send('WRONG LOGIN OR PASS'.encode('utf-8'))
                client.close()
                return False
            pass
    except ConnectionResetError as e:  # removing clients
        client.close()
        return False
    ServerRepository.clients[user_id] = client
    ServerRepository.nicknames[user_id] = nickname
    ChatConstants.logger.info("client logged, his nickname {}".format(nickname))
    broadcast("{} joined!".format(nickname).encode('utf-8'))
    send_chat_commands(client)
    thread = threading.Thread(target=handle, args=(client, user_id))
    thread.start()
