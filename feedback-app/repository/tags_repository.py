import logging
from mysql.connector import Error
from typing import List, Optional

from model.tags import Tags, Tags_get
from model.connector import create_connection


logger = logging.getLogger('root')
logger.handlers


class TagsRepository:
    """
    The class executes API logic for metrics.
    """

    def __init__(self):
        self.connection = create_connection()

    
    def get_all_tags(self) -> Optional[Tags_get]:
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
            cursor.close()
            for row in result:
                tags.append(Tags_get(row[0], row[1], row[2]))
            logger.info("Get all tags successfully.")
            return tags
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_one_tag(self, id: int) -> Optional[Tags_get]:
        """
        Return one tag by id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, title, type
        FROM tags WHERE id = %s
        """

        try:
            cursor.execute(query, [id])
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                logger.info("Empty result.")
                return None
            else:
                logger.info("Tag get successfully.")
                return Tags_get(row[0], row[1], row[2])
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def add_tag(self, tag: Tags) -> Optional[str]:
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
            cursor.close()
            logger.info("Tag added successfully.")
            return "Tag added successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None

      
    def delete_tag(self, id: int) -> Optional[str]:
        """
        Delete tag from table.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM tags WHERE id = %s
        """

        try:
            cursor.execute(query, [id])
            cursor.close()
            logger.info("Tag deleted successfully.")
            return "Tag deleted successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def update_tag_title(self, id: int, tag: Tags) -> Optional[str]:
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
            cursor.close()
            logger.info("Tag title updated successfully.")
            return "Tag title updated successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def update_tag_type(self, id: int, tag: Tags) -> Optional[str]:
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
            cursor.close()
            logger.info("Tag name updated successfully.")
            return "Tag name updated successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None
