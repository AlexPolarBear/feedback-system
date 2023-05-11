from dataclasses import dataclass
from context import Context 

@dataclass
class User:
    chat_id : int
    name : int
    email : str = "@"
    direction : str = "Математика" 
    context : Context

    def __post_init__(self):
        pass

    