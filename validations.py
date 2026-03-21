import json
import logging

logger = logging.getLogger(__name__)

with open("config.json") as j:
    config = json.load(j)
    logger.info("Config loaded")


def is_valid_data(city, temperature, humidity, weather_condition, visibility):
    """Validates incoming weather data against expected ranges and types.
        returns True if all values are valid, False otherwise"""
    valid = True
    min_temp = config["validation"]["min_temperature"]
    max_temp = config["validation"]["max_temperature"]

    # checks if city is valid
    if not city:
        logger.warning("Missing city name")
        valid = False
    elif not isinstance(city, str):
        logger.warning("Invalid city name type, should be a string")
        valid = False

    # checks if temp is valid
    if temperature is None:
        logger.warning(f"Missing temperture value for {city}")
        valid = False
    elif not isinstance(temperature, (int, float)):
        logger.warning(
            f"Invalid temperature type for {city}, should be a float or integer ")
        valid = False
    elif temperature < min_temp or temperature > max_temp:
        logger.warning(f"Suspicious temperature for {city}: {temperature} ")
        valid = False

    # checks if humidity is valid
    if humidity is None:
        logger.warning(f"Missing humidity value for {city}")
        valid = False
    elif not isinstance(humidity, int):
        logger.warning(
            f"Invalid humidity type for {city}, should be an integer ")
        valid = False
    elif humidity > 100 or humidity < 0:
        logger.warning(f"Suspicious humidity for {city}: {humidity} ")
        valid = False

    # checks if weather condition is valid
    if not weather_condition:
        logger.warning(f"Missing weather condition for {city}")
        valid = False
    elif not isinstance(weather_condition, str):
        logger.warning(
            f"Invalid weather condition type for {city}, should be a string")
        valid = False

    # checks if visibility is valid
    if visibility is None:
        logger.warning(f"Missing visibility value for {city}")
        valid = False
    elif not isinstance(visibility, int):
        logger.warning(
            f"Invalid visibility type for {city}, should be an integer ")
        valid = False
    # The maximum value of the visibility is 10 km- from the openweather site
    elif visibility < 0 or visibility > 10000:
        logger.warning(f"Suspicious visibility for {city}: {visibility} ")
        valid = False

    return valid
