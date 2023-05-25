import os, sys
sys.path.append(os.path.dirname(__file__))


from struct_data.tag import Tag
from struct_data.user import User
from struct_data.course import Course
from struct_data.feedback import Feedback

from struct_data.aliases import TagId, TagTitle, CourseShortName, \
    ChatBotId, FieldOfKnowledge, StrPath, \
    CourseJSON, UserJSON, FeedbackJSON

from typing import Callable, Union, List, Tuple, Dict


from nltk.stem import SnowballStemmer
import pymorphy2

class TagsHandler:
    MorphAnalyzer = pymorphy2.MorphAnalyzer()

    @staticmethod
    def _info_tag_cnt(courses : Dict[CourseShortName, Course]) \
        -> Tuple[int, Dict[TagTitle, int]]:
        tags_cnt : Dict[TagTitle, int] = dict()
        for course_title, course in courses.items():
            for tag_title, tag in course.context.items():
                if tag_title not in tags_cnt:
                    tags_cnt[tag_title] = 1
                else:
                    tags_cnt[tag_title] += 1
        all_count = 0
        for tag_title, cnt in tags_cnt.items():
            all_count += cnt
        
        return all_count, tags_cnt
    
    @staticmethod
    def _all_tags(courses : Dict[CourseShortName, Course]) -> Dict[TagTitle, Tag]:
        all_count, tags_cnt = TagsHandler._info_tag_cnt(courses)
        tags : Dict[TagTitle, Tag] = {tag: tag for tag in tags_cnt}
        return tags

    # FUNC_PROCESS
    @staticmethod
    def _to_lower(tag_title : TagTitle) -> TagTitle:
        tag_title = tag_title.strip()

        tag_title = list(tag_title)
        tag_title[0] = tag_title[0].lower()
        tag_title = ''.join(tag_title)
        return tag_title, True

    @staticmethod
    def _ban(tag_title : TagTitle)  -> Tuple[TagTitle, bool]:
        for c in tag_title:
            if c.isdigit():
                return "", False
            if c == ".":
                return "", False
        
        return tag_title, True
    

    @staticmethod
    def _lemmating(tag_title : TagTitle)  -> Tuple[TagTitle, bool]:
        words = tag_title.split(" ")
        if len(words) > 1:
            return tag_title, True

        res_tag_title =  TagsHandler.MorphAnalyzer.parse(tag_title)[0].normal_form
        # if tag_title[:3] == "гру":
        #     print(f"_lemmating: |{tag_title}| |{res_tag_title}|  |{len(words)}|")



        return res_tag_title, True

    @staticmethod
    def _small(tag_title : TagTitle)  -> Tuple[TagTitle, bool]:
        if len(tag_title) <= 3:
            return "", False
        
        return tag_title, True
    # __FUNC_PROCESS
    
    @staticmethod
    def _to_apply_all(courses : Dict[CourseShortName, Course],\
                       func_process : Callable[[TagTitle], Tuple[TagTitle, bool]]) -> Dict[CourseShortName, Course]:
        new_courses : Dict[CourseShortName, Course] = dict()

        for course_title, course in courses.items():
            new_context : Dict[TagTitle, Tag] = dict()

            for tag_title, tag in course.context.items():
                new_tag_title, ok = func_process(tag_title)
                if ok:
                    new_context[new_tag_title] = new_tag_title

            course.context = new_context
            new_courses[course_title] = course

        return new_courses

    # @staticmethod
    # def _apply(courses : Dict[CourseShortName, Course], old_cnt : int) -> Tuple[Dict[CourseShortName, Course], int]:
    #     courses_new = TagsHandler._to_apply_all(courses_new, func_process=TagsHandler._to_lower)
    #     new_cnt, _ = TagsHandler._info_tag_cnt(courses_new)
    #     print(f"processing_tags: _to_lower_all: {old_cnt} -> {new_cnt}")
    #     return courses, new_cnt

    @staticmethod
    def processing_tags(courses : Dict[CourseShortName, Course]) -> Dict[CourseShortName, Course]:
        old_cnt, _ =  TagsHandler._info_tag_cnt(courses)
        courses_new = courses

        courses_new = TagsHandler._to_apply_all(courses_new, func_process=TagsHandler._to_lower)
        new_cnt, _ = TagsHandler._info_tag_cnt(courses_new)
        print(f"processing_tags: _to_lower_all: {old_cnt} -> {new_cnt}")
        old_cnt = new_cnt

        courses_new = TagsHandler._to_apply_all(courses_new, func_process=TagsHandler._ban)
        new_cnt, _ = TagsHandler._info_tag_cnt(courses_new)
        print(f"processing_tags: _ban: {old_cnt} -> {new_cnt}")
        old_cnt = new_cnt

        courses_new = TagsHandler._to_apply_all(courses_new, func_process=TagsHandler._lemmating)
        new_cnt, _ = TagsHandler._info_tag_cnt(courses_new)
        print(f"processing_tags: _lemmating: {old_cnt} -> {new_cnt}")
        old_cnt = new_cnt

        courses_new = TagsHandler._to_apply_all(courses_new, func_process=TagsHandler._small)
        new_cnt, _ = TagsHandler._info_tag_cnt(courses_new)
        print(f"processing_tags: _small: {old_cnt} -> {new_cnt}")
        old_cnt = new_cnt
        
        return courses_new