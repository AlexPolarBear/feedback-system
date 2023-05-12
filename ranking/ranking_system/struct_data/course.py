from dataclasses import dataclass
from context import Context 

@dataclass
class Course:
    id : int
    field_of_knowledge : str
    short_name : str
    full_name : str
    size : str
    description : str
    lecturer_id : int
    year : int
    context : Context

    def __post_init__(self):
        pass

    