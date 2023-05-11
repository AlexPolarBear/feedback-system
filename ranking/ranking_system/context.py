from dataclasses import dataclass, field
from tag import Tag

@dataclass
class Context:
    context : dict[int, Tag]

    