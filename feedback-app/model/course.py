from dataclasses import dataclass

@dataclass
class Course:
    id: int
    field_of_knowledge: str
    short_name: str
    full_name: str
    size: str
    description: str
    direction: str
    lecturer_id: int
    year: str
    