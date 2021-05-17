from dataclasses import dataclass
import logging
import os

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConnectionConstants:
    host = os.getenv("ServerHost") or "127.0.0.1"
    port = os.getenv("ServerPort") or 7976


@dataclass(frozen=True)
class LoginConstants:
    LOGIN = "LOGIN"
    PASSWORD = "PASSWORD"
    NAME = "NAME"
    WRONG_LOGIN_OR_PASS = "WRONG LOGIN OR PASS"
    USER_EXISTS = "USER EXISTS"
    REGISTRATION = "REGISTRATION"
    AUTHORIZATION = "AUTHORIZATION"
    registration = os.getenv("registration") or "1"
    authorization = os.getenv("authorization") or "2"


@dataclass(frozen=True)
class MessageConstants:
    server_encoding = "utf-8"
    size_message_bytes = 1024
