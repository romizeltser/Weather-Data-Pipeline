CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    city TEXT,
    temperature REAL,
    humidity INTEGER,
    weather_condition TEXT,
    visibility INTEGER
);
