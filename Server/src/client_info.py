from dataclasses import dataclass
from socket import socket


@dataclass
class ClientInfo:
    client: socket
    nickname: str
