# import logging
from mysql.connector import Error
from typing import List

from model.tags import Tags, Tags_get
from model.connector import create_connection


class TagsRepository:
    """
    The class executes API logic for metrics.
    """

    def __init__(self):
        self.connection = create_connection()

    
    def get_all_tags(self):
        """
        Returns all tags in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, title, type
        FROM tags
        """

        tags: List[Tags_get] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                tags.append(Tags_get(row[0], row[1], row[2]))
            return tags
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_one_tag(self, id: int):
        """
        Return one tag by id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, title, type
        FROM tags WHERE id = %s
        """

        cursor.execute(query, [id])
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        else:
            return Tags_get(row[0], row[1], row[2])
        

    def add_tag(self, tag: Tags):
        """
        Add new tag in table.
        """
        
        cursor = self.connection.cursor()
        query = """
        INSERT INTO tags (title, type)
        VALUES (%s, %s)
        """

        try:
            cursor.execute(query, (tag.title, tag.type))
            print("Query executed successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()

      
    def delete_tag(self, id: int):
        """
        Delete tag from table.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM tags WHERE id = %s
        """

        try:
            cursor.execute(query, [id])
            print("Tag deleted successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def update_tag_title(self, id: int, tag: Tags):
        """
        Updating the tag title by id.
        """
        
        cursor = self.connection.cursor()
        query = """
        UPDATE tags
        SET title = %s WHERE id = %s
        """

        try:
            cursor.execute(query, (tag.title, id))
            print("Query update successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def update_tag_type(self, id: int, tag: Tags):
        """
        Updating the tag type by id.
        """
        
        cursor = self.connection.cursor()
        query = """
        UPDATE tags
        SET type = %s WHERE id = %s
        """

        try:
            cursor.execute(query, (tag.type, id))
            print("Query update successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()
