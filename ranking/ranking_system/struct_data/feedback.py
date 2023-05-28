from dataclasses import dataclass
from .aliases import CourseShortName, ChatBotId, LecturerStr

@dataclass
class Feedback:
    id: int # PK
    # course_id: int
    short_name: CourseShortName # FK
    author_id: ChatBotId # FK
    lecturer : LecturerStr # FK
    date: str
    text: str


    @staticmethod
    def _feedback_to_json(feedback : "Feedback"):
        return feedback.__dict__
    

