from dataclasses import dataclass, field
from typing import List, Dict
import json


from .tag import Tag

@dataclass
class Context:
    # dict[id, Tag]
    context : dict[int, Tag]
    
    def __init__(self, tags : Dict[int, Tag]):
        self.context = tags


    # READ_WRITE_CONTEXT
    def _context_to_json(self) -> dict:
        context_json : dict = dict()
        # print(f"Context._context_to_json self.context={self.context}")

        for tag_id in self.context:
            context_json[tag_id] = self.context[tag_id]._tag_to_json()
        
        return context_json
    
    def _save_context_json(self, absolute_path : str, indent=4, ensure_ascii=False) -> None:
        # print(f"Context._save_context_json absolute_path={absolute_path}")

        with open(absolute_path, 'w', encoding="utf-8") as file:
            json.dump(self._context_to_json(), file, indent=4, ensure_ascii=False)

    @staticmethod
    def _load_context_from_json(absolute_path : str) -> dict:
        with open(absolute_path, 'r', encoding="utf-8") as file:
            context_json = json.load(file)

        return context_json
    
    @staticmethod
    def _json_to_context(context_json):
        return Context(context_json)


    # __READ_WRITE_CONTEXT
