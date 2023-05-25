from dataclasses import dataclass

@dataclass(init=False)
class Tags:
    id: int
    title: str
    type: str


@dataclass
class Tags_get:
    id: int
    title: str
    type: str
   