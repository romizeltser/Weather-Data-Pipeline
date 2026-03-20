import sqlite3

def initDB():
    connection=sqlite3.connect("weather.db")
    cursor=connection.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS weather (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, city TEXT, temperature REAL, humidity INTEGER, weather_condition TEXT, visibility INTEGER, temp_min REAL, temp_max REAL)
    """

    cursor.execute(sql)
    connection.commit() #save changes
    connection.close()

def save_data(timestamp, city, temperature, humidity, weather_condition, visibility, temp_min, temp_max):
    connection=sqlite3.connect("weather.db")
    cursor=connection.cursor()
    
    sql = """
        INSERT INTO weather (timestamp, city, temperature, humidity, weather_condition, visibility, temp_min, temp_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (timestamp, city, temperature, humidity, weather_condition, visibility, temp_min, temp_max))
    connection.commit() #save changes
    connection.close()