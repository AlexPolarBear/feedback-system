from dataclasses import dataclass

@dataclass
class Scores:
    id: int
    metric_id: int
    course_id: int
    author_id: int
    date: str
    score: int
    