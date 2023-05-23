import os 
import sys

from chatGPT import ChatGPT

from simple_data.simpleCourses import simple_courses


if __name__ == "__main__":
    print("[*] ChatGPT_main is working! [*]\n")
    
    chat_gpt = ChatGPT()

    # chatGPT_context = chat_gpt.get_context()

    course = simple_courses[0]
    # chat_gpt._get_and_save_tags_txt_for_course_by_descr(course=course, context=chatGPT_context)

    tags_txt = chat_gpt._read_tags_txt_from_file(short_name=course.short_name)
    tags_list = chat_gpt._tags_txt_to_tags(tags_txt)
    print(tags_list)
