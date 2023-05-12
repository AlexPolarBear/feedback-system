from dataclasses import dataclass

@dataclass(frozen=True)
class Tag:
    id : int
    title : str
    type : int

    