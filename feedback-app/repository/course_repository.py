import logging
from typing import List, Optional
from mysql.connector import Error

from model.course import Course, Course_get
from model.connector import create_connection


logger = logging.getLogger('root')
logger.handlers


class CourseRepository:
    """
    The class executes API logic for courses.
    """

    def __init__(self):
        self.connection = create_connection()


    def get_all(self) -> Optional[Course_get]:
        """
        This method returns the list of all courses from database.
        """

        cursor = self.connection.cursor()
        result = None
        query = """
        SELECT 
            id, field_of_knowledge, short_name, full_name, 
            size, description, direction, lecturer_id, year
        FROM courses
        """
        
        courses: List[Course_get] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                courses.append(Course_get(row[0], row[1], row[2], row[3], row[4], 
                                          row[5], row[6], row[7], row[8]))
            cursor.close()
            logger.info("All courses get successfully.")
            return courses
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None


    def get_one(self, id: int) -> Optional[Course_get]:
        """
        This method gets one course by its id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT 
            id, field_of_knowledge, short_name, full_name, 
            size, description, direction, lecturer_id, year
        FROM courses WHERE id = %s
        """

        try:
            cursor.execute(query, [id])
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                logger.info("Empty result.")
                return None
            else:
                logger.info("Course get successfully.")
                return Course_get(row[0], row[1], row[2], row[3], row[4], 
                            row[5], row[6], row[7], row[8])
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None
        

    def add_courses(self, course: Course) -> Optional[str]:
        """
        Method just adds new course in the end of table.
        """

        cursor = self.connection.cursor()
        query = """
        INSERT INTO courses (
            field_of_knowledge, short_name, full_name, size, 
            description, direction, lecturer_id, year
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(query, (course.field_of_knowledge, 
                                  course.short_name, 
                                  course.full_name, 
                                  course.size, 
                                  course.description,
                                  course.direction,
                                  course.lecturer_id,
                                  course.year))
            cursor.close()
            logger.info("Course add successfully.")
            return "Course add successfully."
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None


    def delete_course(self, id: int) -> Optional[str]:
        """
        This method delete one course by its id.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM courses WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            logger.info("Course deleted successfully.")
            cursor.close()
            return "Course deleted successfully."
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None


    def update_course(self, id: int, course: Course) -> Optional[str]:
        """
        This method is updating the course information.
        """
        
        cursor = self.connection.cursor()
        query = """
        UPDATE courses
        SET field_of_knowledge = %s, short_name = %s, full_name = %s, size = %s, 
            description = %s, direction = %s, lecturer_id = %s, year = %s
        WHERE id = %s
        """

        try:
            cursor.execute(query, (course.field_of_knowledge, 
                                  course.short_name, 
                                  course.full_name, 
                                  course.size, 
                                  course.description,
                                  course.direction,
                                  course.lecturer_id,
                                  course.year, id))
            logger.info("Course update successfully.")
            cursor.close()
            return "Course update successfully."
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None
