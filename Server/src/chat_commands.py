from dataclasses import dataclass
from typing import Literal


@dataclass
class _ChatCommand:
    start_idx_in_message: int
    end_idx_in_message: int
    command: Literal["/p", "/h", "/o", "/c", "/mph"]

    def _extract_command_from_message(self, message: str) -> str:
        """
        Extract command from message
        :param message: Client message
        :return: Сommand from message
        """
        return message[self.start_idx_in_message:self.end_idx_in_message]

    def is_message_contains_command(self, message: str) -> bool:
        """
        Check for the command in the message
        :param message: Client message
        :return: True or False
        """
        if self._extract_command_from_message(message) == self.command:
            return True
        return False


@dataclass(frozen=True)
class ChatCommands:
    private_message: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                                 end_idx_in_message=2,
                                                 command="/p")

    history_message_server: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                                        end_idx_in_message=2,
                                                        command="/h")

    history_private_message: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                                         end_idx_in_message=4,
                                                         command="/mph")

    online_list: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                             end_idx_in_message=2,
                                             command="/o")

    chat_commands: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                               end_idx_in_message=2,
                                               command="/c")
