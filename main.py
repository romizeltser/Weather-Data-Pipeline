import os
import requests
import logging
from dotenv import load_dotenv
import schedule
from datetime import datetime, timedelta
import time
from database import init_db, save_data
from queries import avg_temp, highest_temperature, lowest_temperature, most_humid_time
import json
from validations import is_valid_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# __name__ is the name of the current file
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("weather")

if api_key:
    logger.info("api key loaded successfully")
else:
    logger.error("could not load api key")


with open("config.json") as j:
    config = json.load(j)
    logger.info("Config loaded")


init_db()  # creates db if does not exists


def url_city(lat, lon):
    """builds the OpenWeatherMap API URL for a given lat and lon"""
    return f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"


def cities():
    """fetches weather data for all configured cities and saves to database"""
    cities = config["cities"]

    timestamp = datetime.now()
    for c in cities:
        url = url_city(c["lat"], c["lon"])
        success = False

        for attempt in range(3):

            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()

                    # check required fields exist
                    if "main" not in data or "weather" not in data:
                        logger.warning(
                            f"Missing fields in response for {c['name']}")
                        break

                    city = data["name"]
                    temperature = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    weather_condition = data["weather"][0]["main"]
                    visibility = data["visibility"]

                    if is_valid_data(city, temperature, humidity, weather_condition, visibility):
                        save_data(
                            # converts to string
                            timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            city,
                            temperature,
                            humidity,
                            weather_condition,
                            visibility
                        )

                    else:
                        logger.warning(
                            "Validation failed, continues to next city")

                    success = True
                    break  # no need to attempt again

                elif response.status_code == 404:
                    logger.error(
                        f"The requested resource or endpoint does not exist. (for {c['name']})")
                    break

                elif response.status_code == 429:  # too many requests
                    retry_after = response.headers.get(
                        "Retry-After")  # returns string
                    if retry_after:
                        wait_time = int(retry_after)
                    else:
                        wait_time = 5
                    logger.warning(
                        f"Rate limit hit for {c['name']}, waiting {wait_time} sec")
                    time.sleep(wait_time)  # waits before continues
                    # tries again
                else:
                    logger.error(
                        f"Unexpected status code {response.status_code} for {c['name']}")
                    break
            except requests.exceptions.RequestException as e:  # failed before reaching the server
                logger.error(f"error while fetching {c['name']}: {e}")
        if not success:
            logger.error(f"All attempts failed for {c['name']}")


cities()
schedule.every(config["minutes"]).minutes.do(cities)
start_time = datetime.now()
finish_time = start_time+timedelta(hours=config["hours"])
while datetime.now() <= finish_time:
    schedule.run_pending()
    time.sleep(1)


# simple tests
print(avg_temp("Tel Aviv"))
print(avg_temp("Jerusalem"))
print(avg_temp("jjdjd"))  # shuld print could not find data
print(avg_temp("Metulla"))
print(avg_temp("Eilat"))
print(highest_temperature())
print(lowest_temperature())
print(most_humid_time())
print(is_valid_data("Tel Aviv", 25.0, 60, "Clear", 10000))  # should print True
# should print False - temp too high
print(is_valid_data("Tel Aviv", 500.0, 60, "Clear", 10000))
