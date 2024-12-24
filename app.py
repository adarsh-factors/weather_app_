import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Replace with your API Key for OpenWeatherMap
#OPENWEATHER_API_KEY = 'c6306395de5e761ea752f47aebd03267'

# Ensure the API key is available
if not OPENWEATHER_API_KEY:
    raise EnvironmentError("OPENWEATHER_API_KEY not set in environment variables.")

# Function to fetch weather data using OpenWeatherMap API
def get_weather(location, days_ahead=0):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Unable to fetch weather data."}

    weather_data = response.json()

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
def generate_weather_response(location, weather_data):
    temperature = weather_data["temperature"]
    description = weather_data["description"]
    
    response = (
        f"The weather in {location} will be {description} with a temperature of {temperature}°C. "
        "It looks like a good day to be outside, but you might want to bring an umbrella if it's cloudy."
    )
    
    return response

# Streamlit UI
st.title("Weather Forecast App")

# Form for user input
with st.form("weather_form"):
    location = st.text_input("Enter Location:", placeholder="e.g. London")
    query = st.text_input("Ask About the Weather:", placeholder="e.g. What will the weather be like tomorrow?")
    submit_button = st.form_submit_button("Get Weather")

# Process the form submission
if submit_button:
    if location and query:
        # Determine if the query is for future weather
        if "after" in query or "in" in query:
            days_ahead = 2 if "two" in query.lower() or "2" in query else 1
        else:
            days_ahead = 0
        
        weather_data = get_weather(location, days_ahead)

        # Display the weather information or error message
        if "error" not in weather_data:
            weather_info = generate_weather_response(location, weather_data)
            st.success(weather_info)
        else:
            st.error(weather_data["error"])
    else:
        st.warning("Please enter both a location and a query to proceed.")
