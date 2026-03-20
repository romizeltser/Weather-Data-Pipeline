import sqlite3
connection=sqlite3.connect("weather.db")
cursor=connection.cursor()

sql = """
    CREATE TABLE IF NOT EXISTS weather (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, city TEXT, temperature REAL, humidity INTEGER, weather_condition TEXT, visibility INTEGER, temp_min REAL, temp_max REAL)
"""

cursor.execute(sql)
connection.commit() #save changes
connection.close()