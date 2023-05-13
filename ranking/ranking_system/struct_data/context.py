from dataclasses import dataclass, field
import json

from .tag import Tag

@dataclass
class Context:
    # dict[id, Tag]
    context : dict[int, Tag]

    # READ_WRITE_CONTEXT
    def _context_to_json(self) -> dict:
        context_json : dict = dict()
        for id in self.context:
            context_json[id] = self.context[id]._tag_to_json()
        
        return context_json
    
    def _save_context_json(self, absolute_path : str, indent=4, ensure_ascii=False) -> None:
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
