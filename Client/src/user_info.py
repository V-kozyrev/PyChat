from dataclasses import dataclass
from typing import Optional
from patterns import Singleton


@dataclass()
class UserInfo(metaclass=Singleton):
    """
    User info
    """
    login: Optional[str] = None
    password: Optional[str] = None
    nickname: Optional[str] = None
    is_new_user: bool = False
