from dataclasses import dataclass
import json

from typing import Dict 
from .aliases import TagTitle, TagId, StrPath

@dataclass()
class Tag:
    id : TagId = None
    title : TagTitle = None # PK
    type : int = None

    @staticmethod
    def _tag_to_json(tag : "Tag") -> dict:
        return tag.__dict__
    
    @staticmethod
    def save_to_json(tag : "Tag", path: StrPath):
        json.dump(Tag._tag_to_json(tag) , open(StrPath, "w", encoding="utf-8"), sort_keys=True, indent=4, ensure_ascii=False)
        

    @staticmethod
    def _json_to_tag(tag_json : Dict) -> "Tag":
        tag = Tag()
        tag.__dict__ = tag_json
        return tag
    
    @staticmethod
    def load_from_json(path: StrPath) -> "Tag":
        tag_json = json.load(open(StrPath, "w", encoding="utf-8"))
        tag = Tag._json_to_tag(tag_json)
        return tag
        