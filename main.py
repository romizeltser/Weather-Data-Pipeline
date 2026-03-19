import os
import requests
from dotenv import load_dotenv
import schedule
from datetime import datetime, timedelta
import time
load_dotenv()
api_key=os.getenv("weather")

if api_key:
    print("api key loaded successfully")
else:
    print("could not load api key")



def UrlCity(lat, lon):
    return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

def Cities():
   
   cities = [
       {"name":"TelAviv" , "lat":32.09 , "lon":34.77 },
       {"name":"RishonLezyon" , "lat":31.9730 , "lon":34.7925 },
       {"name":"Eilat" , "lat":29.5577 , "lon":34.9519 },
       {"name":"Yavne" , "lat":31.8776 , "lon":34.7400 },
       {"name":"Metulla" , "lat":33.2843 , "lon":35.5801 }
   ]

   timestamp=datetime.now()
   for c in cities:
       url=UrlCity(c["lat"], c["lon"])

       try:
           response = requests.get(url, timeout=10)
           if response.status_code==200: 
               data = response.json()
               city=data["name"]
               temperature=data["main"]["temp"]
               humidity=data["main"]["humidity"]
               weather=data["weather"][0]["main"]
               visibility= data["visibility"]
               temp_min=data["main"]["temp_min"]
               temp_max=data["main"]["temp_max"]
               ##
               print(timestamp)
               print(city)
               print(temperature)
               print(humidity)
               print(weather)
               print(visibility)
               print(temp_min)
               print(temp_max)
               ##

           elif response.status_code==429: #too many requests
               continue

       except requests.exceptions.RequestException as e:
           print(f"error while fetching {c['name']}: {e}")

               

Cities()
schedule.every(6).minutes.do(Cities)
start_time=datetime.now()
finish_time=start_time+timedelta(hours=1)
while datetime.now()<=finish_time:
    schedule.run_pending()
    time.sleep(1)