import os, sys
# add ranking directory to sys.path
sys.path.append(os.path.dirname(__file__))

# typing
from typing import Callable, Union, List, Tuple, Dict
from struct_data.aliases import TagId, TagTitle, CourseShortName, \
    ChatBotId, FieldOfKnowledge, StrTag, StrPath, \
    CourseJson

from struct_data.tag import Tag
from struct_data.user import User
from struct_data.course import Course

from simple_data.simpleCourses import simple_courses
from simple_data.simpleUsers import simple_users
from simple_data.simpleTags import simple_tags

import json 
import pprint

class IO_RankingSystem:
    # general
    PATH_TO_DIR_DATA = os.path.join(os.path.dirname(__file__), "relevant_data")
    # 
    PATH_TO_FILE_COURSES_JSON =  os.path.join(PATH_TO_DIR_DATA, "courses_json", "courses.json")
    PATH_TO_DIR_COURSES_TAGS = os.path.join(PATH_TO_DIR_DATA, "courses_tags")
    PATH_TO_COURSES_TXT = os.path.join(PATH_TO_DIR_DATA, "courses_txt")
    PATH_TO_DIR_ALL_TAGS = os.path.join(PATH_TO_DIR_DATA, "all_tags")
    PATH_TO_DIR_USERS_JSON = os.path.join(PATH_TO_DIR_DATA, "users")

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def _save(obj : object, path : StrPath):
        json.dump(obj, open(path, "w", encoding="utf-8"),
                          indent=4, ensure_ascii=False)
    
    @staticmethod 
    def _load(path : StrPath):
        return json.load(open(path, "r", encoding="utf-8"))

    @staticmethod
    def _collect_all_courses_tags(field_of_knowledge_list : List[FieldOfKnowledge] = None) -> Dict[CourseShortName, Dict[StrTag, Tag]]:
        if field_of_knowledge_list is None:
            field_of_knowledge_list = os.listdir(IO_RankingSystem.PATH_TO_DIR_COURSES_TAGS)
        
        courses_tags_str : Dict[CourseShortName, List[StrTag]] = dict()

        for field_of_knowledge in field_of_knowledge_list:
            path_to_dir_fok = os.path.join(IO_RankingSystem.PATH_TO_DIR_COURSES_TAGS, field_of_knowledge)

            for subdir_fok_name in sorted(os.listdir(path_to_dir_fok)):
                path_to_final_dir = os.path.join(path_to_dir_fok, subdir_fok_name)

                for file_name in os.listdir(path_to_final_dir):
                    # AlgGrS.json
                    course_short_name =  file_name.split(".")[0]
                    path_to_file = os.path.join(path_to_final_dir, file_name)
                    # print(f"_collect_all_courses_tags: {path_to_file}")

                    course_tags : List[StrTag] = json.load(open(path_to_file, "r", encoding="utf-8"))
                    tags_dict = {tag : tag for tag in course_tags}

                    courses_tags_str[course_short_name] = tags_dict

        return courses_tags_str

    @staticmethod
    def _get_courses_jsons():
        courses_jsons = json.load(open(IO_RankingSystem.PATH_TO_FILE_COURSES_JSON, "r", encoding="utf-8"))
        return courses_jsons
    
    @staticmethod
    def _all_tags(file_name : str = "all_tags.json", is_save : bool = False):
        courses_str = IO_RankingSystem._collect_all_courses_tags()
        
        tags : Dict[TagTitle : Tag] = dict()
        for course_short_name, course_tags in courses_str.items():
            for tag_str in course_tags:
                tags[tag_str] = tag_str
            
        if is_save:
            path_to_save = os.path.join(IO_RankingSystem.PATH_TO_DIR_ALL_TAGS, file_name)
            tags_list = [tag for tag in tags]
            
            IO_RankingSystem._save(tags_list, path_to_save)

        return tags 
        

    @staticmethod
    def get_all_courses() -> Dict[CourseShortName, Course]:
        courses_jsons = IO_RankingSystem._get_courses_jsons()
        courses_tags_str = IO_RankingSystem._collect_all_courses_tags()

        courses : Dict[CourseShortName, Course] = dict()
        for course in courses_jsons:
            course_short_name = course['short_name']

            courses[course_short_name] = course
            # courses[course_short_name]['description'] = None
        
        for course_short_name, tags_str_dict in courses_tags_str.items():
            courses[course_short_name]['context'] = tags_str_dict

        
        courses = {course_short_name : Course._json_to_course(course) for course_short_name, course in courses.items()}
        return courses
    
    
    
    # USER
    @staticmethod
    def save_user(chat_id : ChatBotId, name : str, direction : str = None, email : str = None, context={}):
        user = User(chat_id=chat_id, name=name, email=email, direction=direction, context=context)
        name_file = f"{chat_id}_user.json"
        path_user_file = os.path.join(IO_RankingSystem.PATH_TO_DIR_USERS_JSON, name_file)
        User.save_to_json(user, path_user_file)

    @staticmethod
    def load_user(chat_id : ChatBotId):
        name_file = f"{chat_id}_user.json"
        path_user_file = os.path.join(IO_RankingSystem.PATH_TO_DIR_USERS_JSON, name_file)

        if not os.path.isfile(path_user_file):
            return None
        user = User.load_from_json(path_user_file)
        return user
    
    @staticmethod
    def add_tag_to_user(chat_id : ChatBotId, tag : TagTitle):
        user = IO_RankingSystem.load_user(chat_id)
        if user is None:
            return False
        user.context[tag] = tag
        IO_RankingSystem.save_user(**user.__dict__)
        return True
    
    @staticmethod
    def delete_tag_from_user(chat_id : ChatBotId, tag : TagTitle):
        user = IO_RankingSystem.load_user(chat_id)
        if user is None:
            return False
        if tag in user.context:
            del user.context[tag]   
        IO_RankingSystem.save_user(**user.__dict__)
        return True
    
    @staticmethod
    def get_all_users() -> Dict[ChatBotId, User]:
        users : Dict[ChatBotId, User] = dict()
        file_name_list = os.listdir(IO_RankingSystem.PATH_TO_DIR_USERS_JSON)
        for file_name in  file_name_list:
            path_to_file = os.path.join(IO_RankingSystem.PATH_TO_DIR_USERS_JSON, file_name)
            user = User.load_from_json(path_to_file)

            users[user.chat_id] = user

        return users


    # __USER

if __name__ == "__main__":
    io_rk = IO_RankingSystem()  

    courses_str = io_rk._collect_all_courses_tags()
    # print(courses_str)

    # courses_json = io_rk._get_courses_jsons()
    # print(courses_json)

    # io_rk._all_tags(is_save=True)

    # courses = io_rk.get_all_courses()
    # pprint.pprint(courses["AlgGrS"])

    # io_rk.save_user(chat_id=2, name="Komnatskiy", direction="Науки о Данных", email="st022323@gmail.com")

    # user = io_rk.load_user(chat_id=2)

    # io_rk.save_user(chat_id=1, name="Anufree")
    # print(user)

    # io_rk.add_tag_to_user(chat_id=1, tag="Матан")

    # io_rk.add_tag_to_user(chat_id=2, tag="Алгебра")

    # io_rk.delete_tag_from_user(chat_id=2, tag="Матан")

    # user = io_rk.load_user(chat_id=1)
    
    users = io_rk.get_all_users()
    print(users)
