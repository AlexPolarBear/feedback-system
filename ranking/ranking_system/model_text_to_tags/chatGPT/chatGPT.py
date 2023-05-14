import openai
import sys
import os
# root general module in ranking_system 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Union, Dict
from struct_data.tag_id import TagId

# secrets
import project_secrets_local


# strcuct data
from struct_data.tag import Tag
from struct_data.course import Course
from struct_data.context import Context
from struct_data.user import User


class ChatGPT:
    CHATGPT_MODEL : str  = "gpt-3.5-turbo"
    PATH_TO_CONTEXT_FILE : str = os.path.join("data", "context.txt")
    PATH_TO_COURSES_DIR : str = os.path.join("data", "courses")
    PATH_TO_TAGS_TXT : str = os.path.join("data", "saved_data", "tags_txt")
    PATH_TO_TAGS_JSON : str = os.path.join("data", "saved_data", "tags_json")

    def __init__(self):
        # Я так понимаю, при нескольких ключах можно этот параметр просто менять
        openai.api_key = project_secrets_local.OPENAI_KEY
        self.max_id = 1

    @staticmethod
    def get_context(path_to_file=PATH_TO_CONTEXT_FILE):
        path_to_curdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_CONTEXT_FILE)

        file = open(path_to_curdir, "r", encoding="utf-8")
        return file.read()
    
    # @staticmethod
    # def get_list_of_simple_courses(path_to_dir=PATH_TO_COURSES_DIR) -> list[Course]:
    #     courses_list = []
    #     for filename in os.listdir(path_to_dir):
    #         path_to_file = f"{path_to_dir}/{filename}"
    #         file = open(path_to_file, "r", encoding="utf-8")

    #         courses_list.append(Course(tag=filename, description=file.read()))

    #     return courses_list
    
    # READ_WRITE_TAGS
    ## TAG_TXT
    @staticmethod
    def _get_path_to_tag_txt_by_name(short_name: str) -> str:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_TAGS_TXT, f'{short_name}_tags.txt')
        return final_path
    
    @staticmethod
    def _save_tags_txt(short_name : str, tags_txt : str,
                        PATH_TO_TAGS_TXT : str = PATH_TO_TAGS_TXT):
        path_to_tag_txt_new_file = ChatGPT._get_path_to_tag_txt_by_name(short_name)
        file = open(path_to_tag_txt_new_file, 'w', encoding="utf-8")
        file.write(tags_txt)
    
    @staticmethod
    def _read_tags_txt_from_file(short_name : str) -> Union[str, None]: 
        path_to_tag_txt_file = ChatGPT._get_path_to_tag_txt_by_name(short_name)
        try:
            file = open(path_to_tag_txt_file, 'r', encoding="utf-8")
            tags_txt = file.read()
            return tags_txt
        except:
            return None
    ## __TAG_TXT
    
    ## JSON
    @staticmethod
    def _get_path_to_tag_json_by_name(short_name: str, path_to_tags_json : str = PATH_TO_TAGS_JSON) -> str:
        final_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path_to_tags_json, f'{short_name}_tags.json')
        return final_path
    
    @staticmethod
    def _save_tags_json_to_file(short_name : str, tags_dict : Union[Dict[TagId, Tag], Context], 
                                path_to_tags_json : str = PATH_TO_TAGS_JSON, 
                                verbose : bool = False) -> None:
        result_context = tags_dict
        if type(tags_dict) != Context:
            result_context = Context(tags=tags_dict)
        absolute_path = ChatGPT._get_path_to_tag_json_by_name(short_name=short_name,
                                                            path_to_tags_json=path_to_tags_json)
        result_context._save_context_json(absolute_path=absolute_path)
        if verbose:
            print(f"[\*]{short_name} is downloaded -> {absolute_path} [*/]")

    ## __JSON

    # __READ_WRITE_TAGS

    # WORK_WITH_CHAT_GPT
    @staticmethod
    def _get_text_tags_from_course_per_api_chatGPT(course_describe : str, context : str,
                                                   verbose : bool = True) -> str:
        messages = [ {"role" : "assistant", "content": context },
                {"role": "user", "content": course_describe} ]

        if verbose:
            print("[\*] ChatGPT request starting !")
        completion = openai.ChatCompletion.create(
            model= ChatGPT.CHATGPT_MODEL,
            messages=messages
        )
        if verbose:
            print("ChatGPT request is finished! [*/]")

        return completion.choices[0].message.content
        

    def _get_and_save_tags_txt_for_course_by_descr(self, course : Course, context : str,
                                                    another_name_for_course: str = None, is_save: bool = True) -> str:
        
        
        tags_txt = ChatGPT._get_text_tags_from_course_per_api_chatGPT(course_describe=course.description,
                                                           context=context)
        if is_save:
            if another_name_for_course is not None:
                ChatGPT._save_tags_txt(short_name=another_name_for_course, tags_txt=tags_txt)
            else:
                ChatGPT._save_tags_txt(short_name=course.short_name, tags_txt=tags_txt)


        return tags_txt

    # __WORK_WITH_CHAT_GPT
    
    # GENERATE_UNIQUE_TAG_ID 
    def _get_unique_tag_id(self):
        unique_tag_id = self.max_id
        self.max_id += 1
        return unique_tag_id

    # __GENERATE_UNIQUE_TAG_ID

    # PROCESSING_TAGS
    def _tags_txt_to_tags(self, tags_txt : str) -> Dict[TagId, Tag]:
        tags_txt_list =  tags_txt.strip('.').strip().split(',')
        tags_dict = dict()
        for tag_txt in tags_txt_list:
            result_tag_txt = tag_txt.strip()
            # id and type : future - maybe need to procced after generate all tags
            # tag = Tag(id=-1, title=result_tag_txt, type=-1)
            tag = Tag(id=self._get_unique_tag_id(), title=result_tag_txt, type=-1)
            tags_dict[tag.id] = tag

        return tags_dict   
    




    # __PROCESSING_TAGS