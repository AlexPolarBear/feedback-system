from dataclasses import dataclass
# from .context import Context 
from .tag import Tag
from .aliases import CourseShortName, TagTitle, StrPath

from typing import Dict

import json


@dataclass
class Course:
    short_name : CourseShortName = None # PK   
    description : str = None
    id : int = None
    field_of_knowledge : str = None
    full_name : str = None
    size : str = None
    lecturer_id : int = None
    year : int = None
    context : Dict[TagTitle, Tag] = None

    @staticmethod
    def _course_to_json(tag : "Course") -> dict:
        return tag.__dict__
    
    @staticmethod
    def save_to_json(course : "Course", path: StrPath):
        json.dump(Course._tag_to_json(course) , open(StrPath, "w", encoding="utf-8"), sort_keys=True, indent=4, ensure_ascii=False)
        

    @staticmethod
    def _json_to_course(course_json : Dict) -> "Course":
        course = Course()
        course.__dict__ = course_json
        return course
    
    @staticmethod
    def load_from_json(path: StrPath) -> "Course":
        course_json = json.load(open(StrPath, "w", encoding="utf-8"))
        course = Course._json_to_tag(course_json)
        return course
    