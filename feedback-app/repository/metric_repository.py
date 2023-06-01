import logging
from mysql.connector import Error
from typing import List, Optional

from model.metric import Metric, Metric_get
from model.connector import create_connection


logger = logging.getLogger('root')
logger.handlers


class MetricRepository:
    """
    The class executes API logic for metrics.
    """

    def __init__(self):
        self.connection = create_connection()

    
    def get_all_metric(self) -> Optional[Metric_get]:
        """
        Returns the list of all metrics in table.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM metrics
        """

        metrics: List[Metric_get] = []
        try: 
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            for row in result:
                metrics.append(Metric_get(row[0], row[1]))
            logger.info("All metrics get successfully.")
            return metrics
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def get_one_metric(self, id: int) -> Optional[Metric_get]:
        """
        Return one metric by id.
        """

        cursor = self.connection.cursor()
        query = """
        SELECT id, name
        FROM metrics WHERE id = %s
        """

        try:
            cursor.execute(query, [id])
            row = cursor.fetchone()
            cursor.close()
            if row is None:
                logger.info("Empty result.")
                return None
            else:
                logger.info("Metric get successfully.")
                return Metric_get(row[0], row[1])
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None
        

    def add_metric(self, metric: Metric) -> Optional[str]:
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
            cursor.close()
            logger.info("Metric add successfully.")
            return "Metric add successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None

      
    def delete_metric(self, id: int) -> Optional[str]:
        """
        Delete metric from table.
        """

        cursor = self.connection.cursor()
        query = """
        DELETE FROM metrics WHERE id = %s
        """

        try:
            cursor.execute(query,[id])
            cursor.close()
            logger.info("Metric deleted successfully.")
            return "Metric deleted successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None


    def update_metric(self, id: int, metric: Metric) -> Optional[str]:
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
            cursor.close()
            logger.info("Metric updated successfully.")
            return "Metric updated successfully."
        except Error as err:
            logger.error(f"The error '{err}' occurred.")
            return None
