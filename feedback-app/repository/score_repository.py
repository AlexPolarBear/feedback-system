import logging
from mysql.connector import Error
from typing import List, Optional

from model.scores import Scores, Scores_get
from model.connector import create_connection


logger = logging.getLogger('root')
logger.handlers


class ScoreRepository:
    """
    The class executes API logic for scores.
    """

    def __init__(self):
        self.connection = create_connection()


    def add_or_update_score(self, score: Scores) -> Optional[str]:
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
            cursor.close()
            logger.info("Score add/update successfully.")
            return "Score add/update successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_all_scores(self) -> Optional[Scores_get]:
        """
        Returns the list of all scores in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT 
            id, metric_id, course_id, author_id, date, score
        FROM scores
        """

        scores: List[Scores_get] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            for row in result:
                scores.append(Scores_get(row[0], row[1], row[2], row[3], row[4], row[5]))
            logger.info("Get all scores successfully.")
            return scores
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_one_score(self, id: int) -> Optional[Scores_get]:
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
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                logger.info("Empty result.")
                return None
            else:
                logger.info("Score get successfully.")
                return Scores_get(row[0], row[1], row[2], row[3], row[4], row[5])
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None
    

    def delete_score(self, id: int) -> Optional[str]:
        """
        Deletes score by id.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM scores WHERE id = %s
        """

        try:
            cursor.execute(query, (id,))
            cursor.close()
            logger.info("Score was deleted successfully.")
            return "Score was deleted successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None

    # def update_score(self, id:int, score: Scores) -> Optrinal[str]:
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
    #         cursor.close()
    #         logger.info("Score was updated successfully.")
    #         return "Score was updated successfully."
    #     except Error as err:
    #         logger.error(f"The error '{err}' occurred.")
    #         return None