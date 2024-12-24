import streamlit as st
import requests

# API Keys
OPENCAGE_GEOCODING_API_KEY = "5915b37990c44b41ab0a576f08ee66d3"  # Replace with your OpenCage API key
WEATHERAPI_API_KEY = "c07262bd071748259d8141723242412"  # Replace with your WEATHERAPI API key
BASE_URL = "https://api.weatherapi.com/v1/"  # WeatherAPI base URL

# Function to get coordinates for a place name using OpenCage Geocoding API
def get_coordinates(location):
    geocode_url = f"https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": location,
        "key": OPENCAGE_GEOCODING_API_KEY
    }
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            for result in data["results"]:
                # Ensure result confidence is above threshold
                if result["confidence"] > 0.5:  # Arbitrary threshold for confidence
                    formatted_name = result["formatted"]
                    lat = result["geometry"]["lat"]
                    lon = result["geometry"]["lng"]
                    # Check if the formatted name matches the user input exactly
                    if location.lower() in formatted_name.lower():  # Allowing case-insensitive match
                        return lat, lon
    return None, None

# Function to fetch weather using coordinates
def get_weather(lat, lon):
    url = f"{BASE_URL}current.json"
    params = {
        "key": WEATHERAPI_API_KEY,
        "q": f"{lat},{lon}",
        "aqi": "no"  # Optional: Exclude air quality data if not needed
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Could not fetch weather data for this location"}

# Function to parse query for place name
def parse_query(query):
    # Extract location from the query after the word 'in'
    words = query.lower().split()
    if "in" in words:
        location = " ".join(words[words.index("in") + 1:]).title()  # Get part after 'in'
        return location
    return None

# Streamlit UI
st.title("Weather App")

query = st.text_input("Enter your query (e.g., 'Weather in Paris')", "")

if st.button("Get Weather"):
    if query:
        location = parse_query(query)
        if location:
            lat, lon = get_coordinates(location)
            if lat and lon:
                # Fetch weather data using coordinates
                weather_data = get_weather(lat, lon)
                if "error" not in weather_data:
                    st.subheader(f"Current Weather in {weather_data['location']['name']}")
                    st.write(f"Temperature: {weather_data['current']['temp_c']}°C")
                    st.write(f"Weather: {weather_data['current']['condition']['text']}")
                    st.write(f"Humidity: {weather_data['current']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data['current']['wind_kph']} km/h")
                else:
                    st.error(weather_data["error"])
            else:
                st.error("Enter correct location")  # Error message for invalid or ambiguous location
        else:
            st.error("Could not detect a valid location. Please try again!")
    else:
        st.error("Please enter a query!")
