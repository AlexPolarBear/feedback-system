# import logging
from mysql.connector import Error
from typing import List

from model.lecturer import Lecturer
from model.connector import create_connection


class LecturerRepository:
    """
    The class executes API logic for lecturers.
    """

    def __init__(self):
        self.connection = create_connection()


    def add_lecturer(self, lecturer: Lecturer):
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
            print("Query executed successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_id_by_lecturer_name(self, name):
        """
        Getting lecturers id by it's name.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id FROM lecturers WHERE name = %s
        """

        try:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                result = [(91,)]
                return result
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()

      
    def delete_lecturer(self, id: int):
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
            print("Lecturer deleted successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_all_lecturer(self):
        """
        Returns the list of all lecturers in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM lecturers
        """

        lecturers: List[Lecturer] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                lecturers.append(Lecturer(row[0], row[1]))
            return lecturers
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_one_lecturer(self, id: int):
        """
        Return one lecturer by id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM lecturers WHERE id = %s
        """
        cursor.execute(query, [id])

        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        else:
            return Lecturer(row[0], row[1])
    

    def update_lecturer(self, id: int, lecturer: Lecturer):
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
            print("Query update successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()
