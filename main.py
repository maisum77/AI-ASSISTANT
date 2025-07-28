import speech_recognition as sr
# import pyttsx3
import webbrowser
import musiclib
import requests
import datetime
import wikipedia
import pyaudio
import os
import uuid
# import playsound
from gtts import gTTS
import pygame.mixer
pygame.mixer.init()
from api import api as api_keys

recognizer = sr.Recognizer()
# engine = pyttsx3.init()
newsapi=api_keys["API"]

def speak(text):
    print(f"Speaking: {text} (via gTTS)")
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = f"temp_speech{uuid.uuid4()}.mp3"
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove(filename) # Clean up the temporary file
    except Exception as e:
        print(f"Error speaking with gTTS: {e}")
        # Fallback to a print statement or a simpler way to notify if gTTS fails
        print(f"Could not speak: {text}")

# def speak(text):
#     print(f"Speaking: {text}")  # for debug
#     speak(text)
#     engine.runAndWait()

def process_command(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclib.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=486de460a7c64f73883f7718803fdbc1")
        if r.status_code == 200:
            data = r.json()
        articles = data.get("articles", [])
        speak("Here are the top news headlines.")
        for i, article in enumerate(articles[:5], 1):  # limit to top 5 headlines
            headline = article.get("title", "No Title")
            speak(f"Headline {i}: {headline}")
    elif "time" in c:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in c:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}")
    elif "search for" in c or "who is" in c or "what is" in c:
        query = c.replace("search for", "").replace("who is", "").replace("what is", "").strip()
        if query:
            speak(f"Searching Wikipedia for {query}")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Please be more specific. I found multiple results for {query}.")
                # print(e.options) # For debugging, uncomment to see options
            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I couldn't find anything on Wikipedia for {query}.")
            except Exception as e:
                speak(f"An unexpected error occurred during the search: {e}")
        else:
            speak("What would you like me to search for?")
    elif "exit" in c or "quit" in c or "stop" in c:
        speak("Goodbye, master!")
        exit() # Terminate the program
    else:
        speak("Sorry, I didn't understand that command. Can you please rephrase?")



# Speak at startup
speak("Initializing Jarvis...")

while True:
    

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = recognizer.listen(source)
            word = recognizer.recognize_google(audio)
            print("You said:", word)

        if word.lower() == "jarvis":
            speak("welcome master")
            

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                process_command(command)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Error: {0}".format(e))
