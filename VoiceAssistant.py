# Speech Recognition is the process of turning spoken words into text. It is a key part of any voice assistant. 
# In Python, the Speech Recognition module helps us do this by capturing audio and converting it to text.

# Run the following command in the command prompt to install all necessary libraries:
# pip install SpeechRecognition pyttsx3 wikipedia pyjokes   (Python)
# !pip install SpeechRecognition pyttsx3 wikipedia pyjokes  (Jupyter Notebook)

# To run the assistant, simply call "python [Filename].py" by using the "cmd Terminal".
# -------------------------------------------------------------------------------------------------------------------------------

"""Import all the libraries needed: (pyttsx3) for speaking out loud, (datetime) to fetch the current time, 
(wikipedia) to search and fetch content, including many more."""
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes

# For weather fetching
import python_weather
import asyncio

# Only needed on Windows
# if os.name == 'nt':
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# -------------------------------------------------------------------------------------------------------------------------------
# (Speak) function that accepts a string as input. This function prints and speaks input.
def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech output not supported in Colab.")
# -------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------
# A wish_user() function to greet the user based on the current time:
# - If it’s before 12 PM, it says “Good Morning”.
# - If it’s before 6 PM, it says “Good Afternoon”.
# - Otherwise it says “Good Evening”.

# This makes the assistant feel more natural and friendly. It also introduces itself and asks how it can help.
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")
# -------------------------------------------------------------------------------------------------------------------------------

# Improved function to fetch weather information with condition handling
async def weather(city, state):
    location = f"{city}, {state}"
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather_data = await client.get(location)
        # Debug print: inspect the weather_data object for available attributes.
        # print(weather_data)  

        temperature = weather_data.temperature
        
        # Attempt to extract the condition/description.
        # Many users have found that python-weather returns a 'condition' or 'description' attribute. 
        # (It may depend on the version you have installed.)
        condition = getattr(weather_data, "condition", None)
        if condition is None:
            # In case the attribute is named 'description'
            condition = getattr(weather_data, "description", "weather details unavailable")
        
        return temperature, condition

# -------------------------------------------------------------------------------------------------------------------------------
# Normally you would talk to the assistant using your microphone. 
# But since Google Colab doesn’t support voice input we use this by creating a list of commands in code:
# - "what is python wikipedia"
# - "open youtube"
# - "what's the time"
# - "exit"

# This list helps us test how the assistant will respond without needing a real voice input.
def take_command():
    return input("You (type your command): ").lower()
# -------------------------------------------------------------------------------------------------------------------------------

# The (run_assistant) function loops through the list of commands and checks what each command is asking for.
def run_assistant():
    wish_user()
    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
        
        elif 'weather' in query:
            try:
                speak("Please enter the city name:")
                city = input("City: ")
                speak("Please enter the state name:")
                state = input("State: ")
                temperature, condition = asyncio.run(weather(city, state))
                if temperature is not None:
                    # speak(f"The current temperature in {city} is {temperature} degrees Fahrenheit.")
                    speak(f"The current temperature in {city} is {temperature} degrees Fahrenheit, with {condition} conditions.")
                else:
                    speak("Sorry, I couldn't fetch the weather information.")
            except Exception as e:
                print(f"Error fetching weather: {e}")
                speak("Sorry, I couldn't fetch the weather information.")

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Sorry, I didn't understand that. Try again.")
# -------------------------------------------------------------------------------------------------------------------------------

# This function starts the assistant and keeps it running until the user says "exit" or "bye".
run_assistant()