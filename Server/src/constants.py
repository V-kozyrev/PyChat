from dataclasses import dataclass
from enum import Enum
import os


@dataclass(frozen=True)
class ChatCommandsConstants:
    max_size_one_character_command_with_arg = 53
    max_size_three_character_command_with_arg = 55


class EntryType(Enum):
    REGISTRATION = 1
    AUTHORIZATION = 2
    MESSAGE_SERVER = 0


@dataclass(frozen=True)
class DbConstants:
    password = os.getenv("dbpassword") or "123"
    user = os.getenv("dbuser") or "postgres"
    host = os.getenv("dbhost") or "127.0.0.1"
    port = os.getenv("dbport") or "5432"
    database = os.getenv("database_name") or "chat"


@dataclass(frozen=True)
class LoginConstants:
    REGISTRATION = "REGISTRATION"
    AUTHORIZATION = "AUTHORIZATION"
    LOGIN = "LOGIN"
    NAME = "NAME"
    PASSWORD = "PASSWORD"
    WRONG_LOGIN_OR_PASS = "WRONG LOGIN OR PASS"
    USER_EXISTS = "USER EXISTS"


@dataclass(frozen=True)
class ConnectionConstants:
    host = os.getenv("ServerHost") or "127.0.0.1"
    port = os.getenv("ServerPort") or 7976


@dataclass(frozen=True)
class MessageConstants:
    server_encoding = "utf-8"
    size_message_bytes = 1024


@dataclass(frozen=True)
class ServerConstants:
    size_history_server = 10
    history_server = 0
