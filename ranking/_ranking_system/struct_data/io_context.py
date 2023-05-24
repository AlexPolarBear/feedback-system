from dataclasses import dataclass, field
import json

from typing import List, Dict
from .aliases import TagTitle

from .tag import Tag

class IO_Context:
    # context : Dict[TagTitle, Tag]
    
    @staticmethod
    def _save_tags_to_json(tags: Dict[TagTitle, Tag], absolute_path : str, indent=4, ensure_ascii=False) -> None:
        with open(absolute_path, 'w', encoding="utf-8") as file:
            json.dump(tags, file, indent=4, ensure_ascii=False)

    @staticmethod
    def _load_tags_from_json(absolute_path : str) -> Dict[TagTitle, Tag]:
        with open(absolute_path, 'r', encoding="utf-8") as file:
            tags = json.load(file)
        return tags

    # __READ_WRITE_CONTEXT
