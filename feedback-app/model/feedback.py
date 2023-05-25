from dataclasses import dataclass

@dataclass(init=False)
class Feedback:
    id: int
    course_id: int
    author_id: int
    date: str
    text: str


@dataclass
class Feedback_get:
    id: int
    course_id: int
    author_id: int
    date: str
    text: str
