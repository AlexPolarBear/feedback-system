from dataclasses import dataclass
import json

from typing import Dict 
from .aliases import TagTitle, TagId

@dataclass()
class Tag:
    id : TagId
    title : TagTitle # PK
    type : int

    @staticmethod
    def _tag_to_json(tag : "Tag") -> dict:
        tag_json = {
            "id" : tag.id,
            "title" : tag.title,
            "type" : tag.type
        }

        return tag_json
    
    @staticmethod
    def _json_to_tag(tag_json : Dict) -> "Tag":
        tag = Tag(
            id=tag_json["id"],
            title=tag_json["title"],
            type=tag_json["type"]
        )
        return tag