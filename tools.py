from dotenv import load_dotenv
import os
import requests
import mock_data

load_dotenv()

def get_weather(city):
    
    city_weather = requests.get(f"http://api.weatherstack.com/current?access_key={os.getenv('WEATHER_API_KEY')}&query={city}")
    if city_weather.status_code != 200:
        return {"error": "Failed to fetch weather data."}
    return city_weather.json()

def search_hotels(city, budget=None):
    city_data = mock_data.TRAVEL_DATA.get(city.lower())

    if not city_data:
        return []

    hotels = city_data["hotels"]

    if budget is not None:
        hotels = [
            hotel
            for hotel in hotels
            if hotel["price_per_night_npr"] <= budget
        ]

    return hotels

def search_foods(city, budget=None):
    city_data = mock_data.TRAVEL_DATA.get(city.lower())

    if not city_data:
        return []

    foods = city_data["foods"]

    if budget is not None:
        foods = [food for food in foods if food["price"] <= budget]

    return foods

def search_attractions(city, type=None):
    city_data = mock_data.TRAVEL_DATA.get(city.lower())

    if not city_data:
        return []

    attractions = city_data["attractions"]

    if type is not None:
        attractions = [attraction for attraction in attractions if attraction["type"] == type]

    return attractions
