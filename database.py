# for creating table and saving data
import sqlite3
import logging
logger = logging.getLogger(__name__)


def init_db():
    try:
        with sqlite3.connect("weather.db") as connection:
            cursor = connection.cursor()

            sql = """
                CREATE TABLE IF NOT EXISTS weather (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, city TEXT, temperature REAL, humidity INTEGER, weather_condition TEXT, visibility INTEGER)
            """

            cursor.execute(sql)
            connection.commit()  # save changes
            logger.info("Database initialized!")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database - {e}")


def save_data(timestamp, city, temperature, humidity, weather_condition, visibility):
    try:
        with sqlite3.connect("weather.db") as connection:
            cursor = connection.cursor()

            sql = """
                INSERT INTO weather (timestamp, city, temperature, humidity, weather_condition, visibility)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (timestamp, city, temperature,
                           humidity, weather_condition, visibility))
            connection.commit()  # save changes
            logger.info(f"Data saved for {city}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save data for {city} - {e}")
