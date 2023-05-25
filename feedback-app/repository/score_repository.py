# import logging
from mysql.connector import Error
from typing import List

from model.scores import Scores, Scores_get
from model.connector import create_connection


class ScoreRepository:
    """
    The class executes API logic for scores.
    """

    def __init__(self):
        self.connection = create_connection()


    def add_or_update_score(self, score: Scores):
        """
        Create and add a new score in table.
        If score already exist, just updates it by id.
        """
        
        cursor = self.connection.cursor()
        query = """
        INSERT INTO scores (metric_id, course_id, author_id, date, score) 
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY 
            UPDATE metric_id = metric_id,
                course_id = course_id, 
                author_id = author_id, 
                date = date, 
                score = score
        """

        try:
            cursor.execute(query, [score.metric_id, 
                                   score.course_id,
                                   score.author_id,
                                   score.date,
                                   score.score])
            print("Query executed successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_all_scores(self):
        """
        Returns the list of all scores in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT 
            id, metric_id, course_id, author_id, date, score
        FROM scores
        """
        courses: List[Scores_get] = []

        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                courses.append(Scores_get(row[0], row[1], row[2], row[3], row[4], row[5]))
            return courses
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()


    def get_one_score(self, id: int):
        """
        Return one score by it id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT
            id, metric_id, course_id, author_id, date, score
        FROM scores WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            score = cursor.fetchone()
            return score
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()
    

    def delete_score(self, id: int):
        """
        Deletes score by id.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM scores WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            print("Score was deleted successfully")
        except Error as err:
            print(f"The error '{err}' occured")
        cursor.close()


    # def update_score(self, id:int, score: Scores):
    #     """
    #     Update score by id.
    #     """

    #     cursor = self.connection.cursor()
    #     query = """
    #     UPDATE scores
    #     SET date = %s, score = %s WHERE id = %s
    #     """

    #     try:
    #         cursor.execute(query, [score.date,
    #                                score.score, id])
    #         print("Score update successfully")
    #     except Error as err:
    #         print(f"The error '{err}' occured")
    #     cursor.close()
