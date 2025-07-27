import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclib

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(f"Speaking: {text}")  # for debug
    engine.say(text)
    engine.runAndWait()

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




def welcome():
    speak("hello welcome back master")
# Speak at startup
speak("Initializing Jarvis...")

while True:
    print("Listening for wake word...")

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = recognizer.listen(source)
            word = recognizer.recognize_google(audio)
            print("You said:", word)

        if word.lower() == "jarvis":
            engine.say("welcome master")
            

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
