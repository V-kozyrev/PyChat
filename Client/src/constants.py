from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)


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
