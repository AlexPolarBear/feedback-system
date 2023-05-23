import openai
import sys
import os
import pprint
# root general module in ranking_system 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# secrets
import project_secrets_local


from typing import List, Union, Dict
# strcuct data
from struct_data.tag import Tag
from struct_data.course import Course
from struct_data.io_context import IO_Context
from struct_data.user import User
# alias
from struct_data.aliases import TagTitle, CourseShortName, StrPath



class ChatGPT:
    CHATGPT_MODEL : str  = "gpt-3.5-turbo"
    PATH_TO_CHATGPT_CONTEXT_FILE : StrPath = os.path.join("data", "context.txt")
    PATH_TO_COURSES_DIR : StrPath = os.path.join("data", "courses_txt")
    PATH_TO_TAGS_TXT : StrPath = os.path.join("data", "saved_data", "tags_txt")
    PATH_TO_TAGS_JSON : StrPath = os.path.join("data", "saved_data", "tags_json")
    PATH_TO_ALL_TAGS_JSON : StrPath = os.path.join("data", "saved_data", "all_tags_json")

    def __init__(self):
        # Я так понимаю, при нескольких ключах можно этот параметр просто менять
        openai.api_key = project_secrets_local.OPENAI_KEY
        self.max_id = 1

    @staticmethod
    def get_chatGPT_context(path_to_file=PATH_TO_CHATGPT_CONTEXT_FILE):
        path_to_curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_CHATGPT_CONTEXT_FILE)

        file = open(path_to_curdir, "r", encoding="utf-8")
        return file.read()

    
    # READ_WRITE_TAGS
    ## TAGS_TXT
    @staticmethod
    def _get_path_to_tag_txt_by_name(short_name: CourseShortName) -> StrPath:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_TAGS_TXT, f'{short_name}_tags.txt')
        return final_path
    
    @staticmethod
    def _save_tags_txt(short_name : CourseShortName, tags_txt : str,
                        PATH_TO_TAGS_TXT : StrPath = PATH_TO_TAGS_TXT):
        path_to_tag_txt_new_file = ChatGPT._get_path_to_tag_txt_by_name(short_name)
        file = open(path_to_tag_txt_new_file, 'w', encoding="utf-8")
        file.write(tags_txt)
    
    @staticmethod
    def _read_tags_txt_from_file(short_name : CourseShortName) -> Union[str, None]: 
        path_to_tag_txt_file = ChatGPT._get_path_to_tag_txt_by_name(short_name)
        try:
            file = open(path_to_tag_txt_file, 'r', encoding="utf-8")
            tags_txt = file.read()
            return tags_txt
        except:
            return None
        
    @staticmethod
    def _is_exists_tags_txt(short_name : CourseShortName):
        path_to_tag_txt = ChatGPT._get_path_to_tag_txt_by_name(short_name)
        is_exists = os.path.isfile(path_to_tag_txt)
        # print(f"ChatGPT._is_exists_tags_txt.path_to_tag_txt={path_to_tag_txt} is_exists={is_exists}")

        return is_exists


    ## __TAGS_TXT
    
    ## TAGS_JSON
    @staticmethod
    def _get_path_to_tag_json_by_name(short_name: CourseShortName, path_to_tags_json : StrPath = PATH_TO_TAGS_JSON) -> StrPath:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path_to_tags_json, f'{short_name}_tags.json')
        return final_path
    
    @staticmethod
    def _save_tags_to_json(short_name : CourseShortName, tags_dict : Dict[TagTitle, Tag], 
                                path_to_tags_json : StrPath = PATH_TO_TAGS_JSON, 
                                verbose : bool = False) -> None:

        absolute_path = ChatGPT._get_path_to_tag_json_by_name(short_name=short_name,
                                                            path_to_tags_json=path_to_tags_json)
        IO_Context._save_tags_to_json(absolute_path=absolute_path, tags=tags_dict)
        if verbose:
            print(f"[\*]{short_name} is downloaded -> {absolute_path} [*/]")

    @staticmethod
    def _load_tags_from_tags_json_file(short_name : CourseShortName, 
                                    path_to_tags_json : StrPath = PATH_TO_TAGS_JSON, 
                                    verbose : bool = False) -> Dict[TagTitle, Tag]:
        absolute_path = ChatGPT._get_path_to_tag_json_by_name(short_name=short_name,
                                                            path_to_tags_json=path_to_tags_json)
        
        tags = IO_Context._load_tags_from_json(absolute_path=absolute_path)

        return tags


    @staticmethod
    def _is_exists_tags_json(short_name : CourseShortName) -> bool:
        path_to_tag_json = ChatGPT._get_path_to_tag_json_by_name(short_name)
        return os.path.isfile(path_to_tag_json)
    

    @staticmethod
    def _save_all_tags_json(tags_dict: Dict[TagTitle, Tag], verbose : bool = False):
        ChatGPT._save_tags_json_to_file(short_name="all_tags", tags_dict=tags_dict,
                                        path_to_tags_json=ChatGPT.PATH_TO_ALL_TAGS_JSON,
                                        verbose=verbose)
        

    ## __TAGS_JSON

    ## COURSES
    @staticmethod
    def _get_path_to_courses_txt_dir() -> StrPath:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_COURSES_DIR)
        return final_path
    
    @staticmethod
    def _get_path_to_courses_json_dir() -> StrPath:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_TAGS_JSON)
        return final_path

    @staticmethod
    def _get_path_to_courses_txt_by_name(short_name: CourseShortName) -> StrPath:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_COURSES_DIR, f'{short_name}.txt')
        return final_path
    
    @staticmethod
    def _get_path_to_courses_json_by_name(short_name: CourseShortName) -> StrPath:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_TAGS_JSON, f'{short_name}.json')
        return final_path

    @staticmethod
    def read_all_courses_txt_to_courses() -> Dict[CourseShortName, Course]:
        """
        return : only Courses(description, short_name)
        """

        courses_dict : Dict[CourseShortName, Course] = dict()
        for course_file_name in os.listdir(ChatGPT._get_path_to_courses_txt_dir()):
            # short_name.txt
            short_name, _ = course_file_name.split('.')
            path_to_course_file = ChatGPT._get_path_to_courses_txt_by_name(short_name=short_name)

            try:
                
                with open(path_to_course_file, 'r', encoding="utf-8") as course_file:
                    course = Course(short_name=short_name,
                                    description=course_file.read())

                    courses_dict[short_name] = course
                    # courses_list.append(course)
            except IOError as e:
                print(f"ChatGPT.read_all_courses_txt_to_courses: {course_file_name} do not open! e={e}\n")

        return courses_dict
    
    @staticmethod 
    def read_all_courses_json_to_courses() -> Dict[CourseShortName, Course]:
        courses_dict = dict()
        for course_file_json_name in os.listdir(ChatGPT._get_path_to_courses_json_dir()):
            # short_name.json
            short_name_with_tags, _ = course_file_json_name.split('.')
            path_to_course_json_file = ChatGPT._get_path_to_courses_json_by_name(short_name=short_name_with_tags)
            
            short_name = short_name_with_tags.split('_')[0]
            try:
                
                course_tags = IO_Context._load_tags_from_json(absolute_path=path_to_course_json_file)
                # print(f"ChatGPT.read_all_courses_json_to_courses: course_context_json={course_context_json}")
                course = Course(short_name=short_name,
                                description="Context already ready!",
                                context=course_tags)

                courses_dict[short_name] = course
            except IOError as e:
                print(f"ChatGPT.read_all_courses_txt_to_courses: {course_file_json_name} do not open! e={e}\n")

        return courses_dict

    ## __COURSES

    # __READ_WRITE_TAGS

    # WORK_WITH_CHAT_GPT
    ## SINGLE_WORK
    @staticmethod
    def _get_text_tags_from_course_per_api_chatGPT(course_describe : str, chatGPT_context : str,
                                                   short_name : CourseShortName,
                                                   verbose : bool = True) -> str:
        messages = [ {"role" : "assistant", "content": chatGPT_context },
                {"role": "user", "content": course_describe} ]

        if verbose:
            print(f"[\*] ChatGPT request for {short_name} starting !")
        completion = openai.ChatCompletion.create(
            model= ChatGPT.CHATGPT_MODEL,
            messages=messages
        )
        if verbose:
            print(f"ChatGPT request for {short_name} is finished! [*/]")

        return completion.choices[0].message.content
    
    @staticmethod
    def _get_and_save_tags_txt_for_course_by_descr(course : Course, chatGPT_context : str,
                                                    another_name_for_course: str = None, is_save: bool = True) -> str:
        
        
        tags_txt = ChatGPT._get_text_tags_from_course_per_api_chatGPT(course_describe=course.description,
                                                           chatGPT_context=chatGPT_context,
                                                           short_name=course.short_name)
        if is_save:
            if another_name_for_course is not None:
                ChatGPT._save_tags_txt(short_name=another_name_for_course, tags_txt=tags_txt)
            else:
                ChatGPT._save_tags_txt(short_name=course.short_name, tags_txt=tags_txt)


        return tags_txt
    ## __SINGLE_WORK

    ## MULTIPLY_WORK
    def create_and_save_tags_by_courses(self, courses : Dict[CourseShortName, Course], force : bool = False,
                                        tags_txt_is_necessarily : bool = True,
                                        verbose : bool = False) -> Dict[CourseShortName, Course]:
        """
        force: False - without rewrite existed files 
        
        maybe return mask which create or not
        """
        chatGPT_context = ChatGPT.get_chatGPT_context()
        for _, course in courses.items():
            is_exists_tags_txt =  ChatGPT._is_exists_tags_txt(course.short_name)
            is_exists_tags_json = ChatGPT._is_exists_tags_json(course.short_name)

            # print(f"force={force}, is_exists_tags_txt={is_exists_tags_txt}, is_exists_tags_json={is_exists_tags_json}, tags_txt_is_necessarily={tags_txt_is_necessarily}")

            tags_txt = None
            if force or (tags_txt_is_necessarily and not is_exists_tags_txt):
                tags_txt = ChatGPT._get_and_save_tags_txt_for_course_by_descr(course=course, chatGPT_context=chatGPT_context)
            
            if tags_txt is None:
                tags_txt = ChatGPT._read_tags_txt_from_file(course.short_name)  

            tags_dict = self._tags_txt_to_tags(tags_txt=tags_txt)

            if force or not is_exists_tags_json:
                ChatGPT._save_tags_to_json(short_name=course.short_name,
                                                tags_dict=tags_dict,
                                                verbose=verbose)
            
            courses[course.short_name].context = tags_dict

        return courses


    ## __MULTIPLY_WORK
    # __WORK_WITH_CHAT_GPT
    
    # GENERATE_UNIQUE_TAG_ID 
    # def _get_unique_tag_id(self):
    #     unique_tag_id = self.max_id
    #     self.max_id += 1
    #     return unique_tag_id

    # __GENERATE_UNIQUE_TAG_ID

    # PROCESSING_TAGS
    def _tags_txt_to_tags(self, tags_txt : str) -> Dict[TagTitle, Tag]:
        tags_txt_list =  tags_txt.strip('.').strip().split(',')
        tags_dict = dict()
        for tag_txt in tags_txt_list:
            result_tag_txt = tag_txt.strip()
            # id and type : future - maybe need to procced after generate all tags
            # tag = Tag(id=-1, title=result_tag_txt, type=-1)
            # tag = Tag(id=self._get_unique_tag_id(), title=result_tag_txt, type=-1)
            tag = Tag(id=-1, title=result_tag_txt, type=-1)
            tags_dict[tag.title] = tag

        return tags_dict   

    @staticmethod
    def _load_and_union_tags_by_courses(path_to_tags_json : StrPath = PATH_TO_TAGS_JSON) -> Dict[TagTitle, Tag]:
        courses_dict = ChatGPT.read_all_courses_json_to_courses()
        # pprint.pprint(f"ChatGPT._load_and_union_tags_by_courses: courses_list={courses_list}")

        tags_dict : Dict[TagTitle, Tag] = dict()
        for course_short_name, course in courses_dict.items():

            for tag_title, tag in course.context.items():
                if tag_title in tags_dict:
                    # This is tag already existed
                    continue
                tags_dict[tag_title] = tag
        
        return tags_dict
    
    @staticmethod
    def load_union_save_all_tags(verbose : bool = True):
        tags_dict = ChatGPT._load_and_union_tags_by_courses()
        # pprint.pprint(f"ChatGPT.load_union_save_all_tags: tags_dict={tags_dict}")

        ChatGPT._save_all_tags_json(tags_dict=tags_dict, verbose=verbose)

    @staticmethod
    def load_all_tags() -> Dict[TagTitle, Tag]:
        tags = ChatGPT._load_tags_from_tags_json_file(short_name="all_tags",
                                                path_to_tags_json=ChatGPT.PATH_TO_ALL_TAGS_JSON)
        return tags

    # __PROCESSING_TAGS