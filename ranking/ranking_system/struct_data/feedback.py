from dataclasses import dataclass
from .aliases import CourseShortName, ChatBotId

@dataclass
class Feedback:
    id: int # PK
    # course_id: int
    short_name: CourseShortName # FK
    author_id: ChatBotId # FK
    date: str
    text: str

