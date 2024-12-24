import streamlit as st
from weather import handle_weather_query

# Streamlit UI
st.title("Weather Forecast App")

# Form for user input
with st.form("weather_form"):
    query = st.text_input("Ask About the Weather:", placeholder="e.g. What will the weather be like in London tomorrow at 3 PM?")
    submit_button = st.form_submit_button("Get Weather")

# Process the form submission
if submit_button:
    if query:
        response = handle_weather_query(query)

        if "error" in response:
            st.error(response["error"])
        else:
            st.success(response["response"])
    else:
        st.warning("Please enter a weather query to proceed.")