# query functions
import sqlite3
import logging
logger = logging.getLogger(__name__)

def avg_temp(city_name):
    connection=sqlite3.connect("weather.db")
    cursor=connection.cursor()

    sql="""
        SELECT AVG(temperature) FROM weather WHERE city=?
    """
    cursor.execute(sql, (city_name,))

    avg_result=cursor.fetchone() #returns tuple
    connection.close()
    if avg_result[0] is not None:
        return avg_result[0]
    else:
        logger.warning(f"could not find data for {city_name}")
        return None 
  
