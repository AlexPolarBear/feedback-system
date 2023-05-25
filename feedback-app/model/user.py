from dataclasses import dataclass

@dataclass(init=False)
class User:
    chat_id: int
    name: str
    email: str
    direction: str


@dataclass
class User_get:
    chat_id: int
    name: str
    email: str
    direction: str
