from dataclasses import dataclass
from enum import Enum
from db.db import DataBase
import os
import logging


@dataclass(frozen=True)
class ChatCommandsConstants:
    command_size_one_character = 53
    history_private_message_command_size = 55


class EntryType(Enum):
    REGISTRATION = 1
    AUTHORIZATION = 2
    MESSAGE_SERVER = 0


@dataclass(frozen=True)
class DbConstants:
    password = os.getenv("dbpassword") or "38167294"
    user = os.getenv("dbuser") or "postgres"
    host = os.getenv("dbhost") or "127.0.0.1"
    port = os.getenv("dbport") or "5432"
    database = os.getenv("database_name") or "chat"


@dataclass(frozen=True)
class ChatConstants:
    REGISTRATION = 'REGISTRATION'
    AUTHORIZATION = 'AUTHORIZATION'
    db_service = DataBase().get_service()
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    chat_commands_list = ["/p: private message",
                          "/h: history message server",
                          "/o: online list",
                          "/c: commands list",
                          "/mph: private message history"]



@dataclass(frozen=True)
class ConnectionConstants:
    host = '127.0.0.1'
    port = 7976


class ServerRepository:
    clients = dict()
    nicknames = dict()
