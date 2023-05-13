from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Tag:
    id : int
    title : str
    type : int

    def _tag_to_json(self) -> dict:
        tag_json = {
            "id" : self.id,
            "tittle" : self.title,
            "type" : self.type
        }

        return tag_json