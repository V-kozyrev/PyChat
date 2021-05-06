from dataclasses import dataclass
from socket import socket
from typing import Dict


@dataclass
class ClientInfo:
    client: socket
    nickname: str


class ServerRepository:
    clients: Dict[int, ClientInfo] = dict()
    nicknames: ClientInfo = dict()
