from dataclasses import dataclass
from typing import Literal


@dataclass
class _ChatCommand:
    """
    Chat command
    """
    start_idx_in_message: int
    end_idx_in_message: int
    command: Literal["/p", "/h", "/o", "/c", "/mph"]
    description: str

    def _extract_command_from_message(self, message: str) -> str:
        """
        Extract command from message
        :param message: Client message
        :return: Command from message
        """
        return message[self.start_idx_in_message:self.end_idx_in_message]

    def is_message_contains_command(self, message: str) -> bool:
        """
        Check for the command in the message
        :param message: Client message
        :return: True when there is a command in the users message. False when there is no command in the users message
        """
        if self._extract_command_from_message(message) == self.command:
            return True
        return False


@dataclass(frozen=True)
class ChatCommands:
    """
    All chat command
    """
    private_message: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                                 end_idx_in_message=2,
                                                 command="/p",
                                                 description="private message")

    history_message_server: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                                        end_idx_in_message=2,
                                                        command="/h",
                                                        description="history message server")

    history_private_message: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                                         end_idx_in_message=4,
                                                         command="/mph",
                                                         description="private message history")

    online_list: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                             end_idx_in_message=2,
                                             command="/o",
                                             description="online list")

    chat_commands: _ChatCommand = _ChatCommand(start_idx_in_message=0,
                                               end_idx_in_message=2,
                                               command="/c",
                                               description="commands list")

    def get_chat_commands_with_description(self) -> str:
        return "CHAT COMMANDS:\n" + "\n".join(
            [self.__getattribute__(field_name).command + ": " + self.__getattribute__(field_name).description for
             field_name in self.__annotations__.keys()])
