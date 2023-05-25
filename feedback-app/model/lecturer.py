from dataclasses import dataclass

@dataclass(init=False)
class Lecturer:
    id: int
    name: str


@dataclass
class Lecturer_get:
    id: int
    name: str
