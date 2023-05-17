from dataclasses import dataclass
from .tag import Tag
from .aliases import TagTitle, StrPath
from typing import Dict
import json

@dataclass
class User:
    chat_id : int = None
    name : str = None
    email : str = None
    direction : str = None
    context : Dict[TagTitle, Tag] = None

    def __post_init__(self):
        pass

    
    @staticmethod
    def _user_to_json(user : "User") -> dict:
        return user.__dict__
    
    @staticmethod
    def save_to_json(user : "User", path: StrPath):
        json.dump(User._tag_to_json(user) , open(StrPath, "w", encoding="utf-8"), sort_keys=True, indent=4, ensure_ascii=False)
        

    @staticmethod
    def _json_to_user(user_json : Dict) -> "User":
        user = User()
        user.__dict__ = user_json
        return user
    
    @staticmethod
    def load_from_json(path: StrPath) -> "User":
        user_json = json.load(open(StrPath, "w", encoding="utf-8"))
        user = User._json_to_tag(user_json)
        return user
    