from tag import Tag
from context import Context
from user import User
from course import Course

from data.simpleCourses import simple_courses


class RankingSystem:
    # В целом, нам нужен будет только один запрос 
    # весь context от user и course  
    # Поэтому, в будущем нужно будет кешировать запрос к курсам 

    def __init__(self, users : list[User] = None,
                  courses : list[Course] = None) -> None:
        self.users = users
        self.courses = courses

    def _get_simple_courses(self):
        return simple_courses

    def update_courses(self):
        # обращение к базе данных
        # нужно получить list[Course]
        
        # change
        # try except
        self.courses = self._get_simple_courses()

    def _print_courses(self):
        print("[\]")
        for course in self.courses:
            print(course)
        print("[/]")



    