import os 
import sys

from chatGPT import ChatGPT

from simple_data.simpleCourses import simple_courses


if __name__ == "__main__":
    print("[*] ChatGPT_main is working! [*]\n")
    
    chat_gpt = ChatGPT()

    chatGPT_context = chat_gpt.get_context()

    course = simple_courses[0]
    chat_gpt._get_and_save_tags_txt_for_course_by_descr(course=course, context=chatGPT_context)

