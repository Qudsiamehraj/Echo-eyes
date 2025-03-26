import streamlit as st
import speech_recognition as sr
from google.cloud import vision
import requests
import json

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Function to recognize text from an image
def recognize_text(image):
    image = vision.Image(content=image)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else "No text found"

# Function to capture voice command
def capture_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='hi-IN')  # Hindi language
            return command
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service."

# Function to get weather information
def get_weather(city):
    api_key = "AIzaSyDDyygVu7UJsvhduse1PUVA9AOpK2Q-urU"  # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    return response.json()

# Streamlit UI
st.title("Echo Eyes - Voice-Based Assistance for Visually Impaired")

if st.button("Start Assistance"):
    command = capture_voice_command()
    st.write(f"You said: {command}")

    # Example of text recognition from an uploaded image
    uploaded_file = st.file_uploader("Upload an image for text recognition", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_content = uploaded_file.read()
        text = recognize_text(image_content)
        st.write(f"Recognized Text: {text}")

    # Weather information
    if "weather" in command.lower():
        city = st.text_input("Enter city name for weather info:")
        if st.button("Get Weather"):
            weather_info = get_weather(city)
            if weather_info.get("main"):
                st.write(f"Temperature: {weather_info['main']['temp']}°C")
                st.write(f"Weather: {weather_info['weather'][0]['description']}")
            else:
                st.write("City not found.")

# Add more features as per your requirements
