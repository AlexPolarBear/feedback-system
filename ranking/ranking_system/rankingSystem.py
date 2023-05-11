from tag import Tag
from context import Context
from user import User
from course import Course

from data.simpleCourses import simple_courses
from data.simpleUsers import simple_users
from data.simpleTags import simple_tags

class RankingSystem:
    # В целом, нам нужен будет только один запрос 
    # весь context от user и course  
    # Поэтому, в будущем нужно будет кешировать запрос к курсам 

    def __init__(self, users : list[User] = None,
                  courses : list[Course] = None,
                  tags : dict[int, Tag] = None) -> None:
        self.users = users
        self.courses = courses
        self.tags = tags

    # COURSES
    def _get_simple_courses(self):
        return simple_courses

    def update_courses(self):
        # обращение к базе данных
        # нужно получить list[Course]
        
        # change on request to BD
        # try except
        self.courses = self._get_simple_courses()

    def _get_courses(self) -> list[Course]:
        return self.courses
    
    def _print_courses(self):
        print("[\ course]")
        for course in self.courses:
            print(course)
        print("[course /]")

    # __COURSES

    # USERS
    def _get_simple_users(self):
        return simple_users

    def update_users(self):
        # change on request to BD
        # try except
        self.users = self._get_simple_users()

    def _get_users(self) -> list[User]:
        return self.users
    
    def _print_users(self):
        print("[\ users]")
        for users in self.users:
            print(users)
        print("[users /]")

    # __USERS

    # TAGS
    def _get_simple_tags(self):
        return simple_tags

    def update_tags(self):
        # change on request to BD
        # try except
        self.tags = self._get_simple_tags()
    
    def _get_tags(self) -> dict[int, Tag]:
        return self.tags

    def _print_tags(self):
        print("[\ tags]")
        for tag in self.tags:
            print(self.tags[tag])
        print("[tags /]")
    
    # __TAGS


    def _calc_distance_between_user_and_course(self, user : User, course : Course):
        distance = 0
        for tag_id in user.context.context:
            if tag_id in course.context.context:
                distance += 1

        return distance
    
    def get_top_match_user_and_course(self, user: User, count : int = 10):
        list_dist_and_course = []
        for course in self.courses:
            distance = self._calc_distance_between_user_and_course(user, course)
            list_dist_and_course.append((distance, course))
        
        list_dist_and_course = sorted(list_dist_and_course, key=lambda x: x[0], reverse=True)

        result_count = min(count, len(list_dist_and_course))
        result = list_dist_and_course[:result_count]

        return  [res[1] for res in result], [res[0] for res in result]

        

        
