from dataclasses import dataclass
import json

from .tag_id import TagId

@dataclass(frozen=True)
class Tag:
    id : TagId
    title : str
    type : int

    def _tag_to_json(self) -> dict:
        tag_json = {
            "id" : self.id,
            "tittle" : self.title,
            "type" : self.type
        }

        return tag_json