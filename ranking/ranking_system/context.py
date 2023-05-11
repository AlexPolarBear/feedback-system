from dataclasses import dataclass, field
from tag import Tag

@dataclass
class Context:
    context : list[Tag] = field(default_factory=list)
