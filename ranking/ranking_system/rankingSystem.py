import os, sys
from pprint import pprint
import random
# add ranking directory to sys.path
sys.path.append(os.path.dirname(__file__))


from typing import Callable, Union, List, Tuple, Dict
from struct_data.aliases import TagId, TagTitle, CourseShortName, ChatBotId, \
                        TagJSON, CourseJSON

from struct_data.tag import Tag
from struct_data.user import User
from struct_data.course import Course

from simple_data.simpleCourses import simple_courses
from simple_data.simpleUsers import simple_users
from simple_data.simpleTags import simple_tags

from io_rankingSystem import IO_RankingSystem

# algorithms
import Levenshtein # distance

class RankingSystem:
    #  API FOR YOU:
    ## update_courses()
    ## update_tags()
    ## update_users()
    ## get_top_relevant_UserCourse
    ## get_top_suitable_tags_by_text
    ## get_top_suitable_tags_by_context
    ## get_top_suitable_courses_by_text

    NAMES_METRIC_DISTANCE = ["Jarow", "Levenshtain"]

    # В целом, нам нужен будет только один запрос 
    # весь context от user и course  
    # Поэтому, в будущем нужно будет кешировать запрос к курсам 

    def __init__(self, users : Dict[ChatBotId, User] = None,
                  courses : Dict[CourseShortName, Course] = None,
                  tags : Dict[TagTitle, Tag] = None) -> None:
        self.users :  Dict[ChatBotId, User] = users
        self.courses : Dict[CourseShortName, Course] = courses
        self.tags : Dict[TagTitle, Tag] = tags

        # sync data
        self.update_courses()
        self.update_tags()
        self.update_users()

        
    # COURSES
    def _get_simple_courses(self):
        return simple_courses

    def update_courses(self):
        # обращение к базе данных
        # нужно получить Dict[ShortNameCourse, Course]
        
        # change on request to BD
        # self.courses = self._get_simple_courses()
        self.courses = IO_RankingSystem.get_all_courses()
    
    # __COURSES

    # USERS
    def _get_simple_users(self):
        return simple_users

    def update_users(self):
        # change on request to BD
        # try except
        # self.users = self._get_simple_users()
        self.users = IO_RankingSystem.get_all_users()
    
    def _print_users(self):
        print("[\ users]")
        for _, user in self.users.items():
            print(user)
        print("[users /]")

    # __USERS

    # TAGS
    def _get_simple_tags(self):
        return simple_tags 

    def update_tags(self, from_file : bool = False):
        # change on request to BD
        # try except
        # self.tags = self._get_simple_tags()
        if from_file:
            self.tags = IO_RankingSystem.get_all_tags()
            return
        self.tags : Dict[TagTitle, Tag] = dict()
        for course_title, course in self.courses.items():
            for tag_title, tag in course.context.items():
                self.tags[tag_title] = tag


    # __TAGS

    # TOP_MATH
    def _calc_distance_between_user_and_course(self, user : User, course : Course):
        distance = 0
        for tag_title in user.context:
            if tag_title in course.context:
                distance += 1

        return distance
    
    def get_top_relevant_UserCourse(self, chat_id: ChatBotId, max_count : int = 10) -> List[CourseJSON]:
        if chat_id not in self.users:
            print(f"Такого юзера={chat_id} нету в базе данных!")
            self.update_users()

            if chat_id not in self.users:
                print(f"!!Такого юзера={chat_id} нету в базе данных после обновления!!!!!!")
                return None
        
        user = self.users[chat_id]

        top_courses = self._get_top_relevant_UserCourse(user=user, max_count=max_count)
        top_courses_json = [Course._course_to_json(course) for course in top_courses]
        return top_courses_json
        

    def _get_top_relevant_UserCourse(self, user: User, max_count : int = 10) -> List[Course]:

        list_dist_and_course = []
        for course_short_name, course in self.courses.items():
            
            distance = self._calc_distance_between_user_and_course(user, course)
            list_dist_and_course.append((distance, course))
        
        list_dist_and_course = sorted(list_dist_and_course, key=lambda x: x[0], reverse=True)

        result_count = min(max_count, len(list_dist_and_course))
        result = list_dist_and_course[:result_count]

        top_courses : List[Course] = [res[1] for res in result]
        return  top_courses

    # __TOP_MATH

    # TOP_TAGS_FOR_SNIPPET 
    ## DEFINE_DISTANCE
    @staticmethod
    def _levenshtain_distance(s1 : str, s2 : str) -> int:
        """
        distance: 0 - s1 and s2 is same
        distance: 100 - s1 and s2 is different
        """
        return Levenshtein.distance(s1, s2)

    @staticmethod
    def _inv_levenshtain_ratio(s1 : str, s2 : str) -> float:
        """
        Calculates a normalized indel similarity in the range [0, 1]. 1 - (1 - normalized_distance)
        ratio: 0 - s1 and s2 is same
        ratio: 1 - s1 and s2 is different
        """
        
        return 1. - Levenshtein.ratio(s1, s2)
    
    @staticmethod
    def _jarow_distance(s1 : str, s2 : str) -> float:
        """
        distance: 0 - s1 and s2 is same
        distance: 100 - s1 and s2 is different
        """
        
        return 1 - Levenshtein.jaro_winkler(s1, s2, prefix_weight=0.2)

    ## __DEFINE_DISTANCE
    
    ## TAG_TEXT_TO_TAG
    
    def get_top_suitable_tags_by_text(self, tag_req : str,
                                    #    metric_func : Callable[[str, str], Union[int, float]] = _levenshtain_distance,
                                       metric_name : str = "Jarow",
                                       max_count : int = 20) -> List[TagTitle]: 
        metric_func : Callable[[str, str], Union[int, float]] = RankingSystem._levenshtain_distance
        if metric_name == "Levenshtain":
            metric_func : Callable[[str, str], Union[int, float]] = RankingSystem._levenshtain_distance
        if metric_name == "Jarow":
            metric_func : Callable[[str, str], Union[int, float]] = RankingSystem._jarow_distance


        metric_and_tag_list : List[Tuple[float, Tag]] = []

        for tag_title in self.tags:
            metric = metric_func(tag_req, tag_title)
            metric_and_tag_list.append((metric, tag_title))

        metric_and_tag_list = sorted(metric_and_tag_list, key=lambda x: x[0], reverse=False)
        
        result_count = min(max_count, len(metric_and_tag_list))
        result = metric_and_tag_list[:result_count]

        res_tags = [res[1] for res in result]

        res_tags_title = [tag_title for tag_title in res_tags]
        return res_tags_title
    

    ## __TAG_TEXT_TO_TAG

    ## OFFER_TAGS_WITHOUT_USER_TEXT
    def _get_top_suitable_tags_by_context(self, user : User, 
                                         max_count : int = 20) -> List[Tag]:
        # добавим иеархию для основных направлений
        # TODO

        tags_names_list = [tag_title for tag_title in self.tags]

        result_tag = []
        for _ in range(max_count):
            ind = random.randrange(len(self.tags))
            result_tag.append(self.tags[tags_names_list[ind]])

        # result_tag_json = [Tag._tag_to_json(tag) for tag in result_tag]

        return result_tag

    def get_top_suitable_tags_by_context(self, chat_id : ChatBotId, max_count : int = 20) -> List[TagJSON]:

        if chat_id not in self.users:
            print(f"Такого юзера={chat_id} нету в базе данных!")
            self.update_users()

            if chat_id not in self.users:
                print(f"!!Такого юзера={chat_id} нету в базе данных после обновления!!!!!!")
                return None
        
        user = self.users[chat_id]

        result_tag = self._get_top_suitable_tags_by_context(user, max_count)
        result_tag_json = [Tag._tag_to_json(tag) for tag in result_tag]

        return result_tag_json

    ## __OFFER_TAGS_WITHOUT_USER_TEXT



    ## COURSE_TEXT_TO_COURSE
    def _get_top_suitable_courses_by_text(self, course_req : str,
                                          metric_name : str = "Jarow",
                                        #   metric_func : Callable[[str, str], Union[int, float]] = _levenshtain_distance,
                                          max_count : int = 20) -> List[Course] :
        
        metric_func : Callable[[str, str], Union[int, float]] = RankingSystem._jarow_distance
        if metric_name == "Jarow":
            metric_func : Callable[[str, str], Union[int, float]] = RankingSystem._jarow_distance
        if metric_name == "Levenshtain":
            metric_func : Callable[[str, str], Union[int, float]] = RankingSystem._levenshtain_distance

        metric_and_course_list = []

        for course_short_name, course in self.courses.items():
            metric = metric_func(course_req, course.full_name)
            metric_1 = metric_func(course_req, course_short_name)
            metric = min(metric, metric_1)

            metric_and_course_list.append((metric, course))


        metric_and_course_list = sorted(metric_and_course_list, key=lambda x: x[0], reverse=False)
        
        result_count = min(max_count, len(metric_and_course_list))
        result = metric_and_course_list[:result_count]

        result_tag = [res[1] for res in result]
        return result_tag
    
    def get_top_suitable_courses_by_text(self, course_req : str,
                                          metric_name : str = "Jarow",
                                        #   metric_func : Callable[[str, str], Union[int, float]] = _levenshtain_distance,
                                          max_count : int = 20) -> List[CourseJSON]:
        top_courses = self._get_top_suitable_courses_by_text(course_req, metric_name=metric_name)

        top_courses_json = [Course._course_to_json(course) for course in top_courses]
        return top_courses_json

    ## __COURSE_TEXT_TO_COURSE
    # __TOP_TAGS_FOR_SNIPPET

    
if __name__ == "__main__":
    rk = RankingSystem()
    # pprint(rk.users)
    # pprint(len(rk.tags))
    # pprint(rk.courses)
    # tags, _ = rk.get_top_suitable_tags_by_text("градиетный спу", max_count=5)
    # pprint(tags)

    # courses_json = rk.get_top_relevant_UserCourse(chat_id=1, max_count=5)
    # pprint(courses_json[0])

    # rk.get_top_suitable_courses_by_text("")

    # top_tags_json = rk.get_top_suitable_tags_by_context(chat_id=1, max_count=3)  
    # pprint(top_tags_json)

    rk.get_top_suitable_courses_by_text("Матанализ")
    pprint()