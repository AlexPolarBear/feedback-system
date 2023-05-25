# import logging
from mysql.connector import Error
from typing import List

from model.feedback import Feedback, Feedback_get
from model.connector import create_connection


class FeedbackRepository:
    """
    The class executes API logic for feedbacks.
    """

    def __init__(self):
        self.connection = create_connection()


    def add_feedback(self, feedback: Feedback):
        """
        This method creates and adds new feedback in table.
        """
        
        cursor = self.connection.cursor()
        query = """
        INSERT INTO feedbacks (course_id, author_id, date, text) 
        VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.execute(query, [feedback.course_id, 
                                   feedback.author_id,
                                   feedback.date,
                                   feedback.text])
            print("Query executed successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_all_feedbacks(self):
        """
        This method returns the list of all feedbacks in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT 
            id, course_id, author_id, date, text
        FROM feedbacks
        """
        courses: List[Feedback_get] = []

        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                courses.append(Feedback_get(row[0], row[1], row[2], row[3], row[4]))
            return courses
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()


    def get_one_feedback(self, id: int):
        """
        This method return one feedback by it id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT
            id, course_id, author_id, date, text
        FROM feedbacks WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            feedback = cursor.fetchone()
            return feedback
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()
    

    def delete_feedback(self, id: int):
        """
        This method deletes feedback by it's id.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM feedbacks WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            print("Query excecuted successfully")
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()


    def update_feedback(self, id:int, feedback: Feedback):
        """
        This method updates feedback by id.
        """

        cursor = self.connection.cursor()
        query = """
        UPDATE feedbacks
        SET date = %s, text = %s
        WHERE id = %s
        """

        try:
            cursor.execute(query, [feedback.date,
                                   feedback.text, id])
            print("Query excecuted successfully")
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()
