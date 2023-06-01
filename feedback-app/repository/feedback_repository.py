import logging
from mysql.connector import Error
from typing import List, Optional

from model.feedback import Feedback, Feedback_get
from model.connector import create_connection


logger = logging.getLogger('root')
logger.handlers


class FeedbackRepository:
    """
    The class executes API logic for feedbacks.
    """

    def __init__(self):
        self.connection = create_connection()


    def add_feedback(self, feedback: Feedback) -> Optional[str]:
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
            cursor.close()
            logger.info("Feedback add successfully.")
            return "Feedback add successfully."
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None


    def get_all_feedbacks(self) -> Optional[Feedback_get]:
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
            cursor.close()
            logger.info("All feedback get successfully.")
            return courses
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None


    def get_one_feedback(self, id: int) -> Optional[Feedback_get]:
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
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                logger.info("Empty result.")
                return None
            else:
                logger.info("Feedback get successfully.")
                return Feedback_get(row[0], row[1], row[2], row[3], row[4])
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None
    

    def delete_feedback(self, id: int) -> Optional[str]:
        """
        This method deletes feedback by it's id.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM feedbacks WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            cursor.close()
            logger.info("Feedback deleted successfully.")
            return "Feedback deleted successfully."
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None


    def update_feedback(self, id:int, feedback: Feedback) -> Optional[str]:
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
            cursor.close()
            logger.info("Feedback updated successfully.")
            return "Feedback updated successfully."
        except Error as err:
            logger.error(f"The error '{err}' occured.")
            return None
