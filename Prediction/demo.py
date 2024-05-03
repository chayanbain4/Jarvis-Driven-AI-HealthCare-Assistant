# Importing necessary libraries
import os
import webbrowser
import requests
import json
import wikipedia
import pyttsx3
import random
import speech_recognition as sr
import pywhatkit
from googletrans import Translator
from playsound import playsound
import time
from bs4 import BeautifulSoup
import wolframalpha
from datetime import datetime
import speedtest
from plyer import notification
from PIL import Image, ImageTk, ImageSequence
import matplotlib.pyplot as pt
from pynput.keyboard import Key, Controller as KeyboardController
import pyautogui
from tkinter import *
from pygame import mixer
import speedtest


# Initialize Pyttsx3 for text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate", 170)

# Function to speak out the given text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice command
# Function to take voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
        
        # Check if the wake-up phrase is detected
        if "wake up" in query.lower():
            print("Jarvis is awake.")
            speak("Jarvis is awake.")
            return "wake up"

    except Exception as e:
        print("Say that again")
        return "None"
    return query

# Function to search Google
def searchGoogle(query):
    query = query.replace("search google", "")
    query = query.replace("jarvis", "")
    query = query.replace("search", "")
    query = query.replace("for", "")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak("Opening Google search for " + query)

# Function to search YouTube
def searchYoutube(query):
    query = query.replace("jarvis", "")
    query = query.replace("search", "")
    query = query.replace("for", "")
    if "open youtube" in query and "play a song" in query:
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with your song URL
        speak("Playing a song on YouTube")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube")
    else:
        query = query.replace("open youtube", "")
        query = query.strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak("Opening YouTube search for " + query)

    query = query.replace("jarvis", "").strip()
    if "open youtube" in query and "play a song" in query:
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with your song URL
        speak("Playing a song on YouTube")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube")
    else:
        query = query.replace("search youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak("Opening YouTube search for " + query)

# Function to search Wikipedia
import wikipedia

def searchWikipedia(query):
    query = query.replace("search wikipedia", "")
    query = query.replace("jarvis", "")
    query = query.replace("search", "")
    query = query.replace("for", "")

    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found for {query}. Please specify your search.")
    except wikipedia.exceptions.PageError as e:
        speak(f"No Wikipedia page found for {query}.")
    except wikipedia.exceptions.WikipediaException as e:
        speak(f"An error occurred while searching Wikipedia: {e}")



# Function to pause video
def pause_video():
    pyautogui.press("k")
    speak("Video paused")

# Function to play video
def play_video():
    pyautogui.press("k")
    speak("Video played")

# Function to mute video
def mute_video():
    pyautogui.press("m")
    speak("Video muted")

# Function to increase volume
def volumeup():
    keyboard = KeyboardController()
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        time.sleep(0.1)
    speak("Volume increased")

# Function to decrease volume
def volumedown():
    keyboard = KeyboardController()
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        time.sleep(0.1)
    speak("Volume decreased")

# Function to remember a message
def remember(query):
    rememberMessage = query.replace("remember that", "")
    rememberMessage = query.replace("jarvis", "")
    speak("You told me to remember that " + rememberMessage)
    remember = open("Remember.txt", "a")
    remember.write(rememberMessage)
    remember.close()

# Function to recall a remembered message
def recall():
    remember = open("Remember.txt", "r")
    speak("You told me to remember that " + remember.read())

# Function to play favorite songs
# def play_favourite_songs(query):
#     if "play music" in query or "favorite song" in query:
#         speak("Playing your favorite songs, sir")
#         # Add your favorite songs playlist link here
#         webbrowser.open("https://www.youtube.com/watch?v=VjXQP9Jdp-E")
#     else:
#         speak("Sorry, I didn't understand what you want to play.")




# Function to fetch latest news
def latestnews():
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=#here paste your api key",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=#here paste your api key",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=#here paste your api key",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=#here paste your api key",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=#here paste your api key",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=#here paste your api key"
    }

    content = None
    url = None
    speak("Which field news do you want, [business], [health], [technology], [sports], [entertainment], [science]")
    field = input("Type field news that you want: ")
    for key, value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was found")
            break
        else:
            url = True
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")

        a = input("[press 1 to continue] and [press 2 to stop]")
        if str(a) == "1":
            pass
        elif str(a) == "2":
            break

    speak("That's all")

# Function to calculate using Wolfram Alpha
def calculate(query):
    query = query.replace("calculate", "")
    query = query.replace("jarvis", "")
    app_id = "42P5Q2-L597932G3P"
    client = wolframalpha.Client(app_id)
    res = client.query(query)
    answer = next(res.results).text
    print(f"Answer is {answer}")
    speak(f"The answer is {answer}")
# Function to send WhatsApp message
def sendMessage():
    speak("Who do you want to message")
    recipient = int(input("Enter recipient number: "))  # Replace with recipient's number
    speak("What's the message")
    message = str(input("Enter the message: "))
    pywhatkit.sendwhatmsg(f"+91{recipient}", message, time_hour=10, time_min=30)
    speak("Message sent")

# Function to shutdown the system
def shutdown_system():
    speak("Are You sure you want to shutdown")
    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
    if shutdown.lower() == "yes":
        os.system("shutdown /s /t 1")
    elif shutdown.lower() == "no":
        pass

# Function to change password
def change_password():
    speak("What's the new password")
    new_pw = input("Enter the new password: ")
    new_password = open("password.txt", "w")
    new_password.write(new_pw)
    new_password.close()
    speak("Done sir")
    speak(f"Your new password is {new_pw}")

# Function to schedule the day
def schedule_my_day():
    tasks = []
    speak("Do you want to clear old tasks (Plz speak YES or NO)")
    query = takeCommand().lower()
    if "yes" in query:
        file = open("tasks.txt", "w")
        file.write(f"")
        file.close()
        no_tasks = int(input("Enter the number of tasks: "))
        for i in range(no_tasks):
            tasks.append(input("Enter the task: "))
            file = open("tasks.txt", "a")
            file.write(f"{i}. {tasks[i]}\n")
            file.close()
    elif "no" in query:
        no_tasks = int(input("Enter the number of tasks: "))
        for i in range(no_tasks):
            tasks.append(input("Enter the task: "))
            file = open("tasks.txt", "a")
            file.write(f"{i}. {tasks[i]}\n")
            file.close()

# Function to show the day's schedule
def show_my_schedule():
    file = open("tasks.txt", "r")
    content = file.read()
    file.close()
    mixer.init()
    mixer.music.load("notification.mp3")
    mixer.music.play()
    notification.notify(
        title="My schedule:",
        message=content,
        timeout=15
    )

# Function to open an application or website
def open_appweb(query):
    query = query.replace("open", "")
    query = query.replace("jarvis", "")
    pyautogui.press("super")
    pyautogui.typewrite(query)
    pyautogui.sleep(2)
    pyautogui.press("enter")

# Function to close an application or website
def closeappweb(query):
    query = query.replace("close", "")
    query = query.replace("jarvis", "")
    pyautogui.hotkey('alt', 'f4')

# Function to set an alarm
def alarm(query):
    speak("What should I remind you?")
    text = takeCommand()
    speak("At what time should I remind you?")
    alarm_time = input("Enter the time in HH:MM format: ")
    alarm_time = alarm_time.split(':')
    alarm_hour = int(alarm_time[0])
    alarm_minute = int(alarm_time[1])
    while True:
        current_time = datetime.now()
        if current_time.hour == alarm_hour and current_time.minute == alarm_minute:
            speak(text)
            break

# Function to check internet speed
# import speedtest

# def internet_speed():
#     st = speedtest.Speedtest()
#     download_speed = st.download() / 1024 / 1024  # Convert to Mbps
#     upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
#     print(f"Download Speed: {download_speed:.2f} Mbps")
#     print(f"Upload Speed: {upload_speed:.2f} Mbps")

#     speak(f"Download speed is {download_speed:.2f} megabits per second")
#     speak(f"Upload speed is {upload_speed:.2f} megabits per second")

# internet_speed()


# Function to get IPL score
def ipl_score():
    url = "https://www.cricbuzz.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    team1 = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
    team2 = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
    team1_score = soup.find_all(class_="cb-ovr-flo")[8].get_text()
    team2_score = soup.find_all(class_="cb-ovr-flo")[10].get_text()

    a = print(f"{team1} : {team1_score}")
    b = print(f"{team2} : {team2_score}")

    notification.notify(
        title="IPL SCORE:",
        message=f"{team1} : {team1_score}\n {team2} : {team2_score}",
        timeout=15
    )

# Function to play rock-paper-scissors game
def game_play():
    speak("Let's Play ROCK PAPER SCISSORS !!")
    print("LET'S PLAY")
    i = 0
    Me_score = 0
    Com_score = 0
    while(i < 5):
        choose = ("rock", "paper", "scissors")
        com_choose = random.choice(choose)
        query = takeCommand().lower()
        if (query == "rock"):
            if (com_choose == "rock"):
                speak("ROCK")
            elif (com_choose == "paper"):
                speak("paper")
                Com_score += 1
            else:
                speak("Scissors")
                Me_score += 1

        elif (query == "paper"):
            if (com_choose == "rock"):
                speak("ROCK")
                Me_score += 1
            elif (com_choose == "paper"):
                speak("paper")
            else:
                speak("Scissors")
                Com_score += 1

        elif (query == "scissors" or query == "scissor"):
            if (com_choose == "rock"):
                speak("ROCK")
                Com_score += 1
            elif (com_choose == "paper"):
                speak("paper")
                Me_score += 1
            else:
                speak("Scissors")
        i += 1

    speak(f"FINAL SCORE: ME: {Me_score}, COM: {Com_score}")

# Function to take screenshot
def screenshot():
    im = pyautogui.screenshot()
    im.save("screenshot.jpg")
    speak("Screenshot taken")

# Function to take a photo
def click_photo():
    pyautogui.press("super")
    pyautogui.typewrite("camera")
    pyautogui.press("enter")
    pyautogui.sleep(2)
    speak("SMILE")
    pyautogui.press("enter")

# Function to enter focus mode
def focus_mode():
    a = int(input("Are you sure that you want to enter focus mode: [1 for YES / 2 for NO] "))
    if a == 1:
        speak("Entering the focus mode....")
        os.startfile("D:\\Coding\\Youtube\\Jarvis\\FocusMode.py")  # Replace with your focus mode script path
        exit()
    else:
        pass

# Main function to handle voice commands
while True:
    wakeup_command = takeCommand().lower()
    if "wake up" in wakeup_command:
        # Respond to wake up command
        print("Jarvis is awake.")
        # Add any specific actions you want to perform after waking up
        
        # Now listen for other commands
        while True:
            query = takeCommand().lower()
            if "sleep" in query:
                speak("Jarvis is going to sleep.")
                break 

            if "search google" in query:
                searchGoogle(query)
            elif "search youtube" in query:
                searchYoutube(query)
            elif "search wikipedia" in query:
                searchWikipedia(query)
            elif "pause" in query:
                pause_video()
            elif "play" in query:
                play_video()
            elif "mute" in query:
                mute_video()
            elif "volume up" in query:
                volumeup()
            elif "volume down" in query:
                volumedown()
            elif "remember that" in query:
                remember(query)
            elif "recall" in query:
                recall()
            elif "play music" in query:
                play_favourite_songs()
            elif "latest news" in query:
                latestnews()
            elif "calculate" in query:
                calculate(query)
            elif "send message" in query:
                sendMessage()
            elif "shutdown" in query:
                shutdown_system()
            elif "change password" in query:
                change_password()
            elif "schedule my day" in query:
                schedule_my_day()
            elif "show my schedule" in query:
                show_my_schedule()
            elif "open" in query:
                open_appweb(query)
            elif "close" in query:
                closeappweb(query)
            elif "alarm" in query:
                alarm(query)
            elif "internet speed" in query:
                internet_speed()
            elif "ipl score" in query:
                ipl_score()
            elif "play a game" in query:
                game_play()
            elif "screenshot" in query:
                screenshot()
            elif "click my photo" in query:
                click_photo()
            elif "focus mode" in query:
                focus_mode()
