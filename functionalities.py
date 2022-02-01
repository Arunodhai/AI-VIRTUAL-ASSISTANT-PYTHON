import datetime
import pyttsx3
import time
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[7].id)
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
opera_path = 'open -a /Applications/Opera.app %s'

def speak(text):
    engine.say(text)
    engine.runAndWait()
    return

def wishMaster():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello,Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")