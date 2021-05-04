from dataclasses import dataclass
from enum import Enum
from typing import Literal


class EntryType(Enum):
    REGISTRATION = 1
    AUTHORIZATION = 2


@dataclass(frozen=True)
class StringConstants:
    LOGIN = "LOGIN"
    PASSWORD = "PASSWORD"
    NAME = "NAME"
    WRONG_LOGIN_OR_PASS = "WRONG LOGIN OR PASS"
    USER_EXISTS = "USER EXISTS"


@dataclass(frozen=True)
class ConnectionConstants:
    host = '127.0.0.1'
    port = 7976


MessageKeys = Literal["/p", "/h", "/o", "/c", "/mph", "REGISTRATION", ""]
