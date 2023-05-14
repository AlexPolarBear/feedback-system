from dataclasses import dataclass, field
import json

from typing import List, Dict
from .aliases import TagTitle

from .tag import Tag

@dataclass
class Context:
    # dict[id, Tag]
    context : dict[TagTitle, Tag]
    
    def __init__(self, tags : Dict[TagTitle, Tag]):
        self.context = tags


    # READ_WRITE_CONTEXT
    @staticmethod
    def _context_to_json(context : "Context") -> dict[TagTitle, Tag]:
        context_json : dict = dict()
        # print(f"Context._context_to_json self.context={self.context}")

        for tag_title in context.context:
            context_json[tag_title] = Tag._tag_to_json(context.context[tag_title])
        
        return context_json
    
    @staticmethod
    def _json_to_context(context_json : dict[TagTitle, Tag]) -> "Context":
        context_res : Context = Context(tags=context_json)

        return context_res
    
    @staticmethod
    def _save_context_json(context : "Context", absolute_path : str, indent=4, ensure_ascii=False) -> None:
        # print(f"Context._save_context_json absolute_path={absolute_path}")

        with open(absolute_path, 'w', encoding="utf-8") as file:
            json.dump(Context._context_to_json(context), file, indent=4, ensure_ascii=False)

    @staticmethod
    def _load_context_json_from_file_json(absolute_path : str) -> dict:
        with open(absolute_path, 'r', encoding="utf-8") as file:
            context_json = json.load(file)
        return context_json
    
    @staticmethod
    def _json_to_context(context_json : Dict) -> "Context":
        tags_dict = dict()
        for tag_title in context_json:
            tags_dict[tag_title] = Tag._json_to_tag(context_json[tag_title])
        
        return Context(tags=tags_dict)


    # __READ_WRITE_CONTEXT
