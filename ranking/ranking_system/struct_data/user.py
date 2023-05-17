from dataclasses import dataclass
from .tag import Tag
from .aliases import TagTitle
from typing import Dict

@dataclass
class User:
    chat_id : int
    name : str
    email : str
    direction : str 
    context : Dict[TagTitle, Tag]

    def __post_init__(self):
        pass

    