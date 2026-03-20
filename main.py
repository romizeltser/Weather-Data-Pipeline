import os
import requests
import logging
from dotenv import load_dotenv
import schedule
from datetime import datetime, timedelta
import time
from database import init_db, save_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__) #__name__ is the name of the current file
                         
load_dotenv()
api_key=os.getenv("weather")

if api_key:
    logger.info("api key loaded successfully")
else:
    logger.error("could not load api key")

init_db() # creates db if do not exists 

def url_city(lat, lon):
    return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

def cities():
   
    cities = [
        {"name":"TelAviv" , "lat":32.09 , "lon":34.77 },
        {"name":"RishonLezyon" , "lat":31.9730 , "lon":34.7925 },
        {"name":"Eilat" , "lat":29.5577 , "lon":34.9519 },
        {"name":"Yavne" , "lat":31.8776 , "lon":34.7400 },
        {"name":"Metulla" , "lat":33.2843 , "lon":35.5801 }
    ]

    timestamp=datetime.now()
    for c in cities:
        url=url_city(c["lat"], c["lon"])

        try:
            response = requests.get(url, timeout=10)
            if response.status_code==200: 
                data = response.json()
                city=data["name"]
                temperature=data["main"]["temp"]
                humidity=data["main"]["humidity"]
                weather_condition=data["weather"][0]["main"]
                visibility= data["visibility"]
                temp_min=data["main"]["temp_min"]
                temp_max=data["main"]["temp_max"]
               ##
                print(timestamp)
                print(city)
                print(temperature)
                print(humidity)
                print(weather_condition)
                print(visibility)
                print(temp_min)
                print(temp_max)
               ##
                save_data(
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'), #converts to string 
                    city,
                    temperature,
                    humidity,
                    weather_condition,
                    visibility,
                    temp_min,
                    temp_max
               )

            elif response.status_code==429: #too many requests
                continue

        except requests.exceptions.RequestException as e:
            logger.error(f"error while fetching {c['name']}: {e}")

               

cities()
schedule.every(6).minutes.do(cities)
start_time=datetime.now()
finish_time=start_time+timedelta(hours=1)
while datetime.now()<=finish_time:
    schedule.run_pending()
    time.sleep(1)