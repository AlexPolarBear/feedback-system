from dataclasses import dataclass
import json

from .aliases import TagTitle, TagId

@dataclass()
class Tag:
    id : TagId
    title : TagTitle # PK
    type : int

    def _tag_to_json(self) -> dict:
        tag_json = {
            "id" : self.id,
            "tittle" : self.title,
            "type" : self.type
        }

        return tag_json