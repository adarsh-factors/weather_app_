import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Replace with your API Key for OpenWeatherMap
OPENWEATHER_API_KEY = 'c6306395de5e761ea752f47aebd03267'

# Ensure the API key is available
if not OPENWEATHER_API_KEY:
    raise EnvironmentError("OPENWEATHER_API_KEY not set in environment variables.")

# Function to fetch weather data using OpenWeatherMap API
def get_weather(location, days_ahead=0):
    """
    Fetch weather data using OpenWeatherMap API.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Unable to fetch weather data."}

    weather_data = response.json()

    # Simplify to required data based on days_ahead (forecast data)
    if "list" in weather_data:
        forecast_index = min(days_ahead * 8, len(weather_data["list"]) - 1)  # 8 data points per day
        forecast = weather_data["list"][forecast_index]
        return {
            "temperature": forecast["main"]["temp"],
            "description": forecast["weather"][0]["description"],
            "date_time": forecast["dt_txt"],
        }
    else:
        return {"error": "Weather data format error."}

# Function to generate a weather response
def generate_weather_response(query, location, weather_data):
    """
    Generates a response based on the weather data.
    """
    # Construct a simple response based on the weather data
    temperature = weather_data["temperature"]
    description = weather_data["description"]
    
    # Here, we'll construct a more dynamic response
    response = (
        f"The weather in {location} will be {description} with a temperature of {temperature}°C. "
        "It looks like a good day to be outside, but you might want to bring an umbrella if it's cloudy."
    )
    
    return response

# Handle weather query
def handle_weather_query(query, location):
    """
    Handle the weather query logic.
    """
    # Determine if the query is for future weather (days ahead)
    if "after" in query or "in" in query:
        days_ahead = 2 if "two" in query.lower() or "2" in query else 1
    else:
        days_ahead = 0

    weather_data = get_weather(location, days_ahead)

    if "error" in weather_data:
        return {"error": weather_data["error"]}

    # Generate a weather response using the weather data
    response = generate_weather_response(query, location, weather_data)
    return {"response": response}

# Test the weather query handling
location = "London"  # You can change this to any valid location
query = "What will the weather be like tomorrow?"

# Call the function to handle the query and get the response
response = handle_weather_query(query, location)

# Output the result
print(response)
