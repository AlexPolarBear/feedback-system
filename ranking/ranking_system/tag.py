from dataclasses import dataclass

@dataclass(frozen=True)
class Tag:
    title : str
    type : int

    