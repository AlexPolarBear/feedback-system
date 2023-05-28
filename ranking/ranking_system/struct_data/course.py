from dataclasses import dataclass, field
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
    context : Dict[TagTitle, Tag] = field(default_factory=lambda: dict())

    @staticmethod
    def _course_to_json(course : "Course") -> dict:
        res_course = course.__dict__
        res_course['context'] = Tag.dict_tags_to_json(course.context)

        return res_course
    
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
    
    @staticmethod
    def _course_to_list_tags(course: "Course"):
        list_tags = [tag_title for tag_title in course.context]

        return list_tags