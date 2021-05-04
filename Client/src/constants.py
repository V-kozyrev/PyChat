from dataclasses import dataclass
from enum import Enum


class EntryType(Enum):
    REGISTRATION = 1
    AUTHORIZATION = 2


@dataclass(frozen=True)
class ChatConstants:
    LOGIN = "LOGIN"
    PASSWORD = "PASSWORD"
    NAME = "NAME"
    WRONG_LOGIN_OR_PASS = "WRONG LOGIN OR PASS"
    host = '127.0.0.1'
    port = 7976
