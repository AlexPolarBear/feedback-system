from dataclasses import dataclass

@dataclass(init=False)
class Scores:
    id: int
    metric_id: int
    course_id: int
    author_id: int
    date: str
    score: int


@dataclass
class Scores_get:
    id: int
    metric_id: int
    course_id: int
    author_id: int
    date: str
    score: int
    