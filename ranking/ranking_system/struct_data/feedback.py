from dataclasses import dataclass
from .aliases import CourseShortName, ChatBotId, LecturerId

@dataclass
class Feedback:
    id: int # PK
    # course_id: int
    course_short_name: CourseShortName # FK
    author_id: ChatBotId # FK
    lecturer_id : LecturerId # FK
    date: str
    text: str


    @staticmethod
    def _feedback_to_json(feedback : "Feedback"):
        return feedback.__dict__
    

