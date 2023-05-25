import requests
import difflib as dl
from datetime import datetime
from bs4 import BeautifulSoup as bs

from model.course import Course
from model.lecturer import Lecturer
from repository.course_repository import CourseRepository
from repository.lecturer_repository import LecturerRepository


def request() -> bs:
    """
    This method makes request to the site and creates soup.
    """

    year = datetime.today().strftime('%Y')
    
    url = f'https://users.math-cs.spbu.ru/~okhotin/course_process_{year}/course_announcement_{year}.html'
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        return soup
    else:
        print("Sorry, something wrong with response")


def every_field():
    """
    This method searches for field of knowledge data.
    """

    soup = request()
    if soup == None:
        print("Sorry, data is empty")

    ul = soup.find('ul')
    fields = {}
    for field in ul.find_all('a', href=True):
        name = field.text
        href = field['href']
        fields[name] = href
    return fields, soup


def every_course() -> dict:
    """
    This method is saving all field_of_knowledge tags.
    """

    fields, soup = every_field()

    table = soup.find_all('table', border="1")[3]
    
    for one in table.find_all('table', border="1"):
        for key in fields:
            s = one.find_previous_sibling('h2')
            if s.text == key:
                fields[key] = one
    return fields


def list_of_lecturers() -> list:
    """
    This method sorts the names of teachers 
    to avoid repeated and incorrect input.
    """

    fields = every_course()

    good_list = []
    sep = ['(онлайн)', ' (по факту ВК)', ' online', 
           'осень', 'весна', 'CS-центр (', ')']
    for key in fields:
        tr = fields[key].find_all('tr')
        for one in tr:
            td = one.find_all('td')
            teacher = ', '.join(td[3].text.split(' +'))
            teacher = teacher.split(', ')
            for lec in teacher:
                for s in sep:
                    lec = lec.replace(s, '')
                if lec not in good_list:
                    good_list.append(lec)
    deliter = ['Mortenson', 'E.', '?', 'будущий преподаватель', ' Белов', 
               ' Баранов', 'Дубчук Николай', 'Дмитрий Булычев', 'Романов', 
               ' D.V.Adler', 'И. С. Казменко', 'Казменко Иван']
    for one in deliter:
        good_list.remove(one)
    return good_list


def add_lecturers_in_table():
    """
    Add sorted list of teacher to database table.
    """

    good_list = list_of_lecturers()

    repository = LecturerRepository()
    entity = Lecturer()
    for one in good_list:
        entity.name = one
        repository.add_lecturer(entity)
    

def match_lecturer(teacher, good_list) -> list:
    """
    This method check match at database table 
    and return correct one.
    """

    correct_teacher = []
    for one in teacher.split(","):
        if one == "?":
            correct_teacher.append("нет преподавателя")
        elif one == "Дмитрий Булычев":
            correct_teacher.append("Булычев Дмитрий")
        elif one == "Дубчук Николай":
            correct_teacher.append("Николай Дубчук")
        elif one == "E. Mortenson + D.V.Adler":
            correct_teacher.append("E. Mortenson")
            correct_teacher.append("Д. В. Адлер")
        elif one == "осень Белов":
            correct_teacher.append("Ю. С. Белов")
        elif teacher == "Mortenson, E.":
            correct_teacher.append("E. Mortenson")
            break
        else:
            correct_one = dl.get_close_matches(one, good_list, n=1, cutoff=0.6)
            correct_teacher.append(''.join(correct_one))
    return correct_teacher


def add_courses_in_table():
    """
    Add courses to database table.
    """

    good_list = list_of_lecturers()
    fields = every_course()

    lecturer_repository = LecturerRepository()
    course_repository = CourseRepository()
    entity = Course()
    
    for field_of_knowledge in fields:
        tr = fields[field_of_knowledge].find_all('tr')
        for one in tr:
            entity.field_of_knowledge = field_of_knowledge
            td = one.find_all('td')
            entity.short_name = td[0].text
            entity.full_name = td[1].text
            entity.size = td[2].text
            teacher = td[3].text
            correct_teacher = match_lecturer(teacher, good_list)
            entity.direction = td[5].text
            description = td[4]
            if not description.text:
                entity.description = "Описание отсутсвует"
            else:
                entity.description = description.find('a', href=True)['href']
            entity.year = datetime.today().strftime('%Y')
            for lec in correct_teacher:
                entity.lecturer_id = lecturer_repository.get_id_by_lecturer_name(lec)[0][0]
                course_repository.add_course(entity)


if __name__ == "__main__":
    add_lecturers_in_table()
    add_courses_in_table()
