import openai
import sys
import os

# secrets
import project_secrets_local

# root general module in ranking_system 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# strcuct data
from struct_data.tag import Tag
from struct_data.course import Course
from struct_data.context import Context
from struct_data.user import User


class ChatGPT:
    PATH_TO_CONTEXT_FILE : str = os.path.join("data", "context.txt")
    PATH_TO_COURSES_DIR : str = os.path.join("data", "courses")
    CHATGPT_MODEL : str  = "gpt-3.5-turbo"
    PATH_TO_TAGS_TXT : str = os.path.join("data", "saved_data", "tags_txt")

    def __init__(self):
        # Я так понимаю, при нескольких ключах можно этот параметр просто менять
        openai.api_key = project_secrets_local.OPENAI_KEY

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

    @staticmethod
    def _save_tags_txt(short_name : str, tags_txt : str,
                        PATH_TO_TAGS_TXT : str = PATH_TO_TAGS_TXT):
        path_to_tag_txt_new_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ChatGPT.PATH_TO_TAGS_TXT, f'{short_name}_tags.txt')
        file = open(path_to_tag_txt_new_file, 'w', encoding="utf-8")
        file.write(tags_txt)
        

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