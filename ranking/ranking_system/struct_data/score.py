from dataclasses import dataclass
from struct_data.aliases import MetricStr, CourseShortName, ChatBotId, LecturerId, ScoreInt


@dataclass
class Score:
    id: int
    metric: MetricStr
    course_short_name: CourseShortName
    author_id: ChatBotId
    lecturer_id: LecturerId
    date: str
    score: ScoreInt

    @staticmethod
    def _score_to_json(score: "Score"):
        return score.__dict__