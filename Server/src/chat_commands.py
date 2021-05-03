from dataclasses import dataclass
from typing import Literal


@dataclass
class _ChatCommand:
    start_idx_in_message: int
    end_idx_in_message: int
    command: Literal["/p", "/h", "/o", "/c", "/mph"]


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