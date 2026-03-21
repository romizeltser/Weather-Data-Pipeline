# query functions
import sqlite3
import logging
logger = logging.getLogger(__name__)


def connect_db():
    return sqlite3.connect("weather.db")


def avg_temp(city_name):
    """returns the average temperature for a given city over the collection period """
    try:
        with connect_db() as connection:
            cursor = connection.cursor()

            sql = """
                SELECT AVG(temperature) FROM weather WHERE city=?
            """
            cursor.execute(sql, (city_name,))
            avg_result = cursor.fetchone()  # returns tuple
            if avg_result and avg_result[0] is not None:
                logger.info(
                    f"Found the avg temperature for {city_name}: {avg_result[0]}")
                return avg_result[0]
            else:
                logger.warning(f"could not find data for {city_name}")
                return None
    except sqlite3.Error as e:
        logger.error(
            f"Failed to calculate avg temperature for {city_name} - {e}")


def highest_temperature():
    """returns the city/cities with the highest recorded temperature"""
    try:
        with connect_db() as connection:
            cursor = connection.cursor()

            sql = """
                SELECT DISTINCT city FROM weather WHERE temperature = (SELECT MAX(temperature) FROM weather)
            """
            cursor.execute(sql)
            # if there are more than one city with max temp
            highest_result = cursor.fetchall()
            if highest_result:
                logger.info(
                    f"Found the city with the highest temperature: {[city[0] for city in highest_result]}")
                return highest_result
            else:
                logger.warning("could not find data")
                return None
    except sqlite3.Error as e:
        logger.error(
            f"Failed to find the city with the highest temperature - {e}")


def lowest_temperature():
    """returns the city/cities with the lowest recorded temperature"""
    try:
        with connect_db() as connection:
            cursor = connection.cursor()

            sql = """
                SELECT DISTINCT city FROM weather WHERE temperature = (SELECT MIN(temperature) FROM weather)
            """
            cursor.execute(sql)
            lowest_result = cursor.fetchall()  # if there are more than one city with min temp
            if lowest_result:
                logger.info(
                    f"Found the city with the lowest temperature: {[city[0] for city in lowest_result]}")
                return lowest_result
            else:
                logger.warning("could not find data")
                return None
    except sqlite3.Error as e:
        logger.error(
            f"Failed to find the city with the lowest temperature - {e}")


def most_humid_time():
    """returns the timestamp with the highest average humidity across all cities"""
    try:
        with connect_db() as connection:
            cursor = connection.cursor()

            sql = """
                SELECT DISTINCT timestamp, AVG(humidity) as avg_humidity FROM weather GROUP BY timestamp ORDER BY avg_humidity desc
            """
            cursor.execute(sql)
            most_humid_time_result = cursor.fetchone()

            if most_humid_time_result and most_humid_time_result[0] is not None:
                logger.info(
                    f"Found the most humid time. time:{most_humid_time_result[0]} average humidity: {most_humid_time_result[1]}")
                return {
                    "time": most_humid_time_result[0],
                    "average_humidity": most_humid_time_result[1]
                }
            else:
                logger.warning("Could not find data")
                return None
    except sqlite3.Error as e:
        logger.error(f"Failed to find the most humid time - {e}")
