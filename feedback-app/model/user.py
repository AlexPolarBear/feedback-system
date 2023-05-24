from dataclasses import dataclass

@dataclass
class User:
    chat_id: int
    name: str
    email: str
    direction: str
