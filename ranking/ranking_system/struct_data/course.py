from dataclasses import dataclass
from .context import Context 

@dataclass
class Course:
    short_name : str # PK  
    description : str
    id : int = None
    field_of_knowledge : str = None
    full_name : str = None
    size : str = None
    lecturer_id : int = None
    year : int = None
    context : Context = None

    def __post_init__(self):
        pass

    