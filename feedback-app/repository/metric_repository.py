# import logging
from mysql.connector import Error
from typing import List

from model.metric import Metric
from model.connector import create_connection


class MetricRepository:
    """
    The class executes API logic for metrics.
    """

    def __init__(self):
        self.connection = create_connection()

    
    def get_all_metric(self):
        """
        Returns the list of all metrics in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM metrics
        """

        metrics: List[Metric] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                metrics.append(Metric(row[0], row[1]))
            return metrics
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def get_one_metric(self, id: int):
        """
        Return one metric by id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM metrics WHERE id = %s
        """

        cursor.execute(query, [id])
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        else:
            return Metric(row[0], row[1])
        

    def add_metric(self, metric: Metric):
        """
        Add new metric in table.
        """
        
        cursor = self.connection.cursor()
        query = """
        INSERT INTO metrics (name)
        VALUES (%s)
        """

        try:
            cursor.execute(query, (metric.name,))
            print("Query executed successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()

      
    def delete_metric(self, id: int):
        """
        Delete metric from table.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM metrics WHERE id = %s
        """

        try:
            cursor.execute(query,[id])
            print("Lecturer deleted successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()


    def update_metric(self, id: int, metric: Metric):
        """
        Updating the metric name.
        """
        
        cursor = self.connection.cursor()
        query = """
        UPDATE metrics
        SET name = %s WHERE id = %s
        """

        try:
            cursor.execute(query, (metric.name, id))
            print("Query update successfully")
        except Error as err:
            print(f"The error '{err}' occurred")
        cursor.close()
