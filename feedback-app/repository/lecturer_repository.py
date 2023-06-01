import logging
from mysql.connector import Error
from typing import List, Optional

from model.lecturer import Lecturer, Lecturer_get
from model.connector import create_connection


logger = logging.getLogger('root')
logger.handlers


class LecturerRepository:
    """
    The class executes API logic for lecturers.
    """

    def __init__(self):
        self.connection = create_connection()


    def add_lecturer(self, lecturer: Lecturer) -> Optional[str]:
        """
        Add new lecturer in table.
        """
        
        cursor = self.connection.cursor()
        query = """
        INSERT INTO lecturers (name)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE name = name
        """

        try:
            cursor.execute(query, (lecturer.name,))
            cursor.close()
            logger.info("Lecturer add successfully.")
            return "Lecturer add successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_id_by_lecturer_name(self, name):
        """
        Getting lecturers id by it's name.
        """

        cursor = self.connection.cursor(buffered=True)
        query = """
        SELECT id FROM lecturers WHERE name = %s
        """

        try:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                result = [(91,)]
            logger.info("Get lecturer id successfully.")
            return result
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None

      
    def delete_lecturer(self, id: int) -> Optional[str]:
        """
        Delete lecturer from table.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM lecturers WHERE id = %s
        """

        try:
            cursor.execute(query,[id])
            self.connection.commit()
            cursor.close()
            logger.info("Lecturer deleted successfully.")
            return "Lecturer deleted successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_all_lecturer(self) -> Optional[Lecturer_get]:
        """
        Returns the list of all lecturers in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM lecturers
        """

        lecturers: List[Lecturer_get] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            for row in result:
                lecturers.append(Lecturer_get(row[0], row[1]))
            logger.info("All lecturers get successfully.")
            return lecturers
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_one_lecturer(self, id: int) -> Optional[Lecturer_get]:
        """
        Return one lecturer by id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM lecturers WHERE id = %s
        """

        try:
            cursor.execute(query, [id])
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                logger.info("Empty result.")
                return None
            else:
                logger.info("Lecturer get successfully.")
                return Lecturer_get(row[0], row[1])
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None    


    def update_lecturer(self, id: int, lecturer: Lecturer) -> Optional[str]:
        """
        Updating the lecturer name.
        """
        
        cursor = self.connection.cursor()
        query = """
        UPDATE lecturers
        SET name = %s WHERE id = %s
        """

        try:
            cursor.execute(query, (lecturer.name, id))
            cursor.close()
            logger.info("Lecturer updated successfully.")
            return "Lecturer updated successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None
