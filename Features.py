import wikipedia
import Features
import weather
import webbrowser
import News
import json
import time
import YT_AUDIO
import selenium_web
import pywhatkit
import wolframalpha
from twilio.rest import Client
from datetime import date
from serpapi import GoogleSearch
import urllib.request
import smtplib
import getpass
import functionalities
from playsound import playsound

bot_name="ALFRED"

def sendMail():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    print("Type your username and press enter : ")
    functionalities.speak("Type your username and press enter.")
    sender_email_id = input()
    print("Type your password and press enter: ")
    functionalities.speak("Type your password and press enter.")
    sender_password = getpass.getpass()
    print("Type receiver's username and press enter: ")
    functionalities.speak("Type receiver's username and press enter.")
    receiver_email_id = input()
    s.login(sender_email_id, sender_password)
    print("Type the message you need to send : ")
    functionalities.speak("Type the message you need to send.")
    message = input()
    try:
        s.sendmail(sender_email_id, receiver_email_id, message)
        print("Mail has been sent successfully.")
        functionalities.speak("Mail has been sent successfully.")
    except:
        print("An exception occurred. Could'nt send the mail. Sorry....")
        functionalities.speak("An exception occurred. Could'nt send the mail. Sorry....")
    s.quit()




def features(_query,response):
    if "bye" in _query or "Bye" in _query:
        print(f"{bot_name}: {response}")
        functionalities.speak(response)
        playsound("assistant_off.wav")
        exit()

    if "what is your name?" in _query:
        print(f"{bot_name}: My name is {bot_name}. ")
        functionalities.speak(f"My name is {bot_name}.")



    elif 'open youtube' in _query:
        functionalities.speak("Here you go to Youtube.\n")
        print(f"{bot_name}: Here you go to Youtube. ")
        webbrowser.get(functionalities.chrome_path).open("http://youtube.com")


    elif 'open gmail' in _query:
        webbrowser.get(functionalities.chrome_path).open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
        functionalities.speak("Opening GMail.")
        print(f"{bot_name}: Opening GMail..")

    elif 'make mail' in _query:
        sendMail()


    elif 'open netflix' in _query:
        webbrowser.get(functionalities.chrome_path).open("https://www.netflix.com/in/")
        functionalities.speak("Opening Netflix")
        print(f"{bot_name}: Opening Netflix")

    elif 'open prime video' in _query:
        webbrowser.get(functionalities.chrome_path).open("https://www.primevideo.com/")
        functionalities.speak("Amazon Prime Video open now")


    elif "news" in _query:
        print(f"{bot_name}: {'Sure sir, Now I will read news for you.'}")
        functionalities.speak("Sure sir, Now I will read news for you.")
        arr = News.news()
        for i in range(len(arr)):
            print(arr[i])
            functionalities.speak(arr[i])

    elif 'time' in _query:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(f"{bot_name}: Current time is {current_time}")
        functionalities.speak(f"Current time is {current_time}")

    elif 'date' in _query:
        print(f"{bot_name}:Today is {date.today().strftime('%B %d, %Y')}")
        functionalities.speak(f"Today is {date.today().strftime('%B %d, %Y')}")


    elif "calculate" in _query:
        temp = _query
        app_id = "your app id from wolfram alpha site"
        client = wolframalpha.Client(app_id)
        ind = _query.lower().split().index("calculate")
        _query = _query.split()[ind + 1:]
        try:
            res = client.query(" ".join(_query))
            answer = next(res.results).text
            print(f"{bot_name}: The answer is {answer}")
            functionalities.speak(f"The answer is {answer}")
        except:
            print(
                f"{bot_name}: Sorry, but I was unable to process the response to this query.\n I'll look up the answer on Google for you.")
            functionalities.speak(
                "Sorry, but I was unable to process the response to this query. I'll look up the answer on Google for you.")
            temp = temp.replace('alfred', '')
            pywhatkit.search(temp)

    elif "what is" in _query or "who is" in _query or "when is" in _query or "alfred" in _query:
        temp = _query
        app_id = "your app id from wolfram alpha site"
        client = wolframalpha.Client(app_id)
        if 'alfred' in _query:
            ind = _query.lower().split().index("alfred")
        else:
            ind = _query.lower().split().index("is")
        _query = _query.split()[ind + 1:]
        try:
            res = client.query(" ".join(_query))
            answer = next(res.results).text
            print(f"{bot_name}: The answer is {answer}")
            functionalities.speak(f"The answer is {answer}")
        except:
            temp = temp.replace('alfred', '')
            params = {
                "api_key": "your api key from serpapi",
                "engine": "google",
                "q": temp,
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            print(f"{bot_name}: The answer is {results['answer_box']['answer']}")
            functionalities.speak(f"The answer is {results['answer_box']['answer']}")



    elif 'open google chrome' in _query:
        webbrowser.get(functionalities.chrome_path).open("https://www.google.com")
        functionalities.speak("Google chrome is open now.")
        print(f"{bot_name}: Google chrome is open now.")

    elif 'google' in _query:
        functionalities.speak("Googling...")
        _query = _query.replace('google', '')
        pywhatkit.search(_query)


    elif "send message" in _query or "send a message" in _query:
        account_sid = "Your sid from twilio"
        auth_token = "Your auth_token from twilio"
        client = Client(account_sid, auth_token)
        print(f"{bot_name}: What should I send : ")
        functionalities.speak('What should I send')
        message = client.messages.create(body=input(), from_="Your temp number from twilio", to="receiver's number") #you should add and verify the receiver's number in twilio website before using it.
        print(f"{bot_name}:Message sent successfully.")

    elif ('corona' or 'covid') and 'status' in _query:
        webbrowser.get(functionalities.chrome_path).open("https://www.worldometers.info/coronavirus/")
        functionalities.speak('Here are the latest covid-19 numbers')



    elif ("search" and "wikipedia") and ("open" and "wikipedia") in _query:
        functionalities.speak("you need information related to which topic? ")
        topic = input("You need information related to which topic? : ")
        print(f"Searching {topic} in wikipedia")
        functionalities.speak(f"Searching {topic} in wikipedia")
        assist = selenium_web.infow()
        assist.get_info(topic)

    elif 'wiki' in _query:
        _query = _query.replace("wiki", "")
        print(f"{bot_name}: Searching Wikipedia...")
        functionalities.speak('Searching Wikipedia...')
        _query = _query.replace("wikipedia", "")
        results = wikipedia.summary(_query, sentences=3)
        print(f"{bot_name}: {results}")
        functionalities.speak("According to Wikipedia," + results)


    elif "where is" in _query:
        _query = _query.replace("where is", "")
        location = _query
        functionalities.speak("Locating " + location)
        webbrowser.get(functionalities.chrome_path).open("https://www.google.com/maps/place/" + location + "")

    elif "play" and "video" in _query:
        functionalities.speak("you want me to play which video?")
        res = input("you want me to play which video? : ")
        print(f"Playing {res} on youtube")
        functionalities.speak(f"Playing {res} on youtube")
        assist = YT_AUDIO.music()
        assist.play(res)


    elif "weather" in _query:
        functionalities.speak("Sure sir.")
        functionalities.speak("Enter your city name : ")
        city = input("Enter your city name : ")
        weather.setCity(city)
        print(f"{bot_name}: Temperature in {city} is " + str(weather.temp()) + " degree celcius and with " + str(
            weather.des()))
        functionalities.speak(
            f" Temperature in {city} is " + str(weather.temp()) + " degree celcius and with " + str(weather.des()))


    elif "play" and "song" in _query:
        functionalities.speak("you want me to play which song?")
        res = input("you want me to play which song? : ")
        print(f"Playing {res} on youtube")
        functionalities.speak(f"Playing {res} on youtube")
        assist = YT_AUDIO.music()
        assist.play(res)

    elif '--help' in _query:
        help.manual()

    else:
        return 0