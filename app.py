import streamlit as st
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import random

load_dotenv()

# Configure Gemini 1.5 Pro
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You are a versatile AI agent that can engage in casual conversations, provide weather updates, generate content, and make music recommendations. Respond in a natural and friendly way, and make sure to keep conversations flowing and engaging."
)

def get_weather(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv('WEATHER_API_KEY')}&units=metric"
    print("In weather! - step 1")
    response = requests.get(url)
    data = response.json()
    print("In weather! - step 2")

    if data.get("cod") == 200:
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        weather_info = (
            f"Weather in {location.capitalize()}: {weather['description'].capitalize()}\n"
            f"Temperature: {main['temp']}°C\n"
            f"Humidity: {main['humidity']}%\n"
            f"Pressure: {main['pressure']} hPa\n"
            f"Wind Speed: {wind['speed']} m/s"
        )
        return weather_info
    else:
        return f"Sorry, I couldn't find the weather information for {location}. Error: {data.get('message', 'Unknown error')}"


def generate_content(prompt):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

st.title("SmartBot - AI Assistant")

user_input = st.text_input("Interact with the AI for weather updates, content generation, or any queries!")

if st.button("Send"):
    if "weather" in user_input.lower():
        location = user_input.lower().replace("weather", "").strip()
        st.write(f"Location parsed: {location}")  # Debugging line
        weather_info = get_weather(location)
        st.info(weather_info)
    else:
        response = generate_content(user_input)
        st.info(response)
