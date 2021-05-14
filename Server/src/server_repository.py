from typing import Dict

from client_info import ClientInfo


class ServerRepository:
    clients: Dict[int, ClientInfo] = dict()

    def get_user_online_list(self) -> str:
        return "ONLINE LIST:\n" + "\n".join(
            [self.clients[client_info].nickname for client_info in self.clients])
