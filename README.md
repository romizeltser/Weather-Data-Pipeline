# Real-Time Weather Data Pipeline
weather data pipeline that collects data from multiple cities, processes it, and makes it queryable.

## Prerequisites
- Python 3.12+
- OpenWeatherMap API key (free tier) - at https://openweathermap.org/api

## Installation

1. Clone the repository:
git clone https://github.com/romizeltser/Weather-Data-Pipeline.git
2. Install dependencies:
pip install -r requirements.txt

## Configuration

1. Create a .env file in the project folder and write there:
weather=your_api_key_here

## How to Run

Run the pipeline (collects data every 6 minutes for 1 hour):
python main.py

After the pipeline finishes, the results of the query functions will be printed automatically, including:
- Average temperature per city
- City with highest/lowest temperature
- Most humid time
- Basic validation tests 


