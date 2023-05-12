from dataclasses import dataclass, field
from tag import Tag

@dataclass
class Context:
    # dict[id, Tag]
    context : dict[int, Tag]

