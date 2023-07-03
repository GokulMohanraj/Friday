import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import requests
import os
from AppOpener import close, open
import pywhatkit as pwk
import geocoder
import pyautogui
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

chief = 'Gokul'
wake_word_detected = False  # Flag variable to indicate if the wake word was detected

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f'Good Morning {chief}')
    elif hour >= 12 and hour < 17:
        speak(f'Good Afternoon {chief}')
    else:
        speak(f'Good Evening {chief}')

def takecommand():
    '''
    Take microphone input from the user to convert and return as a string  
    '''
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        print('Listening....')
        r.adjust_for_ambient_noise(mic, duration=1)
        audio = r.listen(mic)
    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query} \n')
        return query
    except Exception as e:
        print(f'sorry {chief}, say that again....')

def google():
    webbrowser.open('google.com')

def youtube():
    webbrowser.open('youtube.com')

def search_google(query):
    search_keyWord = query.replace('search', '')
    print("You said: " + search_keyWord)
    url = 'https://www.google.com/search?q=' + search_keyWord
    webbrowser.open(url)

def ip():
    ip = requests.get('http://api.ipify.org').text
    print(f'Your IP address is: {ip}')
    speak(f'Your IP address is: {ip}')

def search_wikipedia():
    speak('Searching Wikipedia....')
    result = wikipedia.summary(query, sentences=2)
    speak('According to Wikipedia')
    print(result)
    speak(result)

def open_apps(inp):
    try:
        app_name = inp.lower()
        print(f'You said: {app_name}')
        speak(f'Opening {app_name}')
        open(app_name, match_closest=True)
    except Exception as e:
        speak('Application not found or some problem occurred. Please try again.')

def music(music_name):
    try:
        speak(f"Playing '{music_name}' on YouTube...")
        pwk.playonyt(music_name)
    except Exception as e:
        print("An error occurred:", str(e))
        speak("Something problem try again...")

def weather(city_name):
    if city_name == None:
        g = geocoder.ip('me')
        crd = g.latlng
        lat , lon = crd
    else:
        g = geocoder.arcgis(city_name)
        crd = g.latlng
        lat , lon = crd
    api_key = "8231a0d19aa8dd7dc2d40d3de18d98bd"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    if response.status_code == 200:
        try:
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]
            description = weather_data["weather"][0]["description"]
            city = weather_data["name"]
        except Exception as e:
            speak('something problem in the server. please try again...')

        print(f"Weather in {city}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")
        speak(f"Weather in {city}:")
        speak(f"Temperature: {temperature}°C")
        speak(f"Humidity: {humidity}%")
        speak(f"Description: {description}")
    else:
        print("Failed to retrieve weather data.")
        speak("Failed to retrieve weather data.")

def unlock_system():
    # Wait for the login screen to appear
    time.sleep(5)
    # Set the coordinates for the password input field
    password_field_x = 500
    password_field_y = 500
    # Set the coordinates for the login button
    login_button_x = 600
    login_button_y = 600
    # Enter the password
    pyautogui.click(password_field_x, password_field_y)
    speak('Say your secret word to unlock system...')
    command = takecommand()
    if command == 'killer':
        pyautogui.typewrite("your_password")  # Replace "your_password" with the actual password
    # Click the login button
        pyautogui.click(login_button_x, login_button_y)
    else:
        speak('your secret word is incorrect,please check and try again')



if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand()  # Move voice recognition outside the try-except block
        if query is None:
            continue
        query = query.lower()
        if 'hey friday' in query or 'friday' in query or 'hi friday' in query:  # Check if the wake word "Friday" is detected
            speak(f'Yes, {chief}')
            wake_word_detected = True  # Set the flag to indicate wake word detection
            continue  # Skip the rest of the loop and go to the next iteration

        if wake_word_detected:  # Check the flag before executing any commands
            try:
                if 'wikipedia' in query or 'who' in query:
                    search_wikipedia()
                elif 'search' in query:
                    search_google(query)
                elif 'my ip address' in query:
                    ip()
                elif 'open' in query:
                    inp = query.replace("open", '')
                    open_apps(inp)
                elif 'play' in query:
                    music_name = query.replace('play', '')
                    music(music_name)
                elif 'today weather' in query:
                    city_name =None
                    weather(city_name)
                elif 'tell weather report of' in query:
                    city_name = query.replace('tell weather report of', '')
                    weather(city_name)
                elif 'unlock system' in query:
                    unlock_system()
            except Exception as e:
                speak("Sorry, there was an error. Please try again.")

        if 'stop listening' in query or 'shutdown' in query:
            speak('Program shutting down.')
            speak(f'Goodbye, {chief}. Take care!')
            break
        elif 'see you later' in query:
            speak(f'Okay {chief} See you soon.')
            wake_word_detected = False  # Reset the flag
