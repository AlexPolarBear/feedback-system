from dataclasses import dataclass
from .context import Context 

@dataclass
class User:
    chat_id : int
    name : str
    email : str
    direction : str 
    context : Context

    def __post_init__(self):
        pass

    