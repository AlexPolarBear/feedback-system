from dataclasses import dataclass


@dataclass
class Scores:
    id: int
    metric: str
    course_id: int
    author_id: int
    date: str
    score: int