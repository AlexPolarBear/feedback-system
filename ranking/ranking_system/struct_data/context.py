from dataclasses import dataclass, field
import json

from typing import List, Dict
from .tag_id import TagId


from .tag import Tag

@dataclass
class Context:
    # dict[id, Tag]
    context : dict[TagId, Tag]
    
    def __init__(self, tags : Dict[TagId, Tag]):
        self.context = tags


    # READ_WRITE_CONTEXT
    @staticmethod
    def _context_to_json(context : "Context") -> dict[TagId, Tag]:
        context_json : dict = dict()
        # print(f"Context._context_to_json self.context={self.context}")

        for tag_id in context.context:
            context_json[tag_id] = context.context[tag_id]._tag_to_json()
        
        return context_json
    
    @staticmethod
    def _json_to_context(context_json : dict[TagId, Tag]) -> "Context":
        context_res : Context = Context(tags=context_json)

        return context_res
    
    def _save_context_json(self, absolute_path : str, indent=4, ensure_ascii=False) -> None:
        # print(f"Context._save_context_json absolute_path={absolute_path}")

        with open(absolute_path, 'w', encoding="utf-8") as file:
            json.dump(self._context_to_json(), file, indent=4, ensure_ascii=False)

    @staticmethod
    def _load_context_json_from_file_json(absolute_path : str) -> dict:
        with open(absolute_path, 'r', encoding="utf-8") as file:
            context_json = json.load(file)
        return context_json
    
    @staticmethod
    def _json_to_context(context_json):
        return Context(context_json)


    # __READ_WRITE_CONTEXT
