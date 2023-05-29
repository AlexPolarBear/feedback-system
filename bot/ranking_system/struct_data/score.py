from dataclasses import dataclass
from struct_data.aliases import MetricStr, CourseShortName, \
    ChatBotId, LecturerId, ScoreInt, MetricId 


@dataclass
class Score:
    id: int
    metric_id: MetricId
    course_short_name: CourseShortName
    author_id: ChatBotId
    lecturer_id: LecturerId
    date: str
    score: ScoreInt

    @staticmethod
    def _score_to_json(score: "Score"):
        return score.__dict__