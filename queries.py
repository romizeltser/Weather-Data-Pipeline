# query functions
import sqlite3
import logging
logger = logging.getLogger(__name__)

def connect_db():
    return sqlite3.connect("weather.db")

def avg_temp(city_name):
    with connect_db() as connection:
        cursor=connection.cursor()

        sql="""
            SELECT AVG(temperature) FROM weather WHERE city=?
        """
        cursor.execute(sql, (city_name,))
        avg_result=cursor.fetchone() #returns tuple
        if avg_result and avg_result[0] is not None:
            return avg_result[0]
        else:
            logger.warning(f"could not find data for {city_name}")
            return None 
  
def highest_temperature():
    with connect_db() as connection:
        cursor=connection.cursor()

        sql="""
            SELECT city FROM weather WHERE temperature = (SELECT MAX(temperature) FROM weather)
        """
        cursor.execute(sql)
        highest_result = cursor.fetchall() # if there are more than one city with max temp
        if highest_result:
            return highest_result
        else:
            logger.warning("could not find data")
            return None
        
def lowest_temperature():
    with connect_db() as connection:
        cursor=connection.cursor()

        sql="""
            SELECT city FROM weather WHERE temperature = (SELECT MIN(temperature) FROM weather)
        """
        cursor.execute(sql)
        lowest_result = cursor.fetchall() # if there are more than one city with min temp
        if lowest_result:
            return lowest_result
        else:
            logger.warning("could not find data")
            return None

def most_humid_time():
    with connect_db() as connection:
        cursor=connection.cursor()

        sql="""
            SELECT timestamp, AVG(humidity) as avg_humidity FROM weather GROUP BY timestamp ORDER BY avg_humidity desc
        """
        cursor.execute(sql)
        most_humid_time_result=cursor.fetchone()

        if most_humid_time_result and most_humid_time_result[0] is not None:
            return {
                "time": most_humid_time_result[0],
                "average_humidity": most_humid_time_result[1]
            }
        else:
            logger.warning("Could not find data")
            return None