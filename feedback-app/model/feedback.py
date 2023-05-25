from dataclasses import dataclass

@dataclass
class Feedback:
    id: int
    course_id: int
    author_id: int
    date: str
    text: str
    