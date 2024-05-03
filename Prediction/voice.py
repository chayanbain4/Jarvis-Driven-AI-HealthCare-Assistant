import speech_recognition as sr
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
import pyttsx3
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
import requests

# Load the dataset
df = pd.read_csv("C:\\Users\\CHAYAN\\Downloads\\training.csv")
# Prepare data
X = df.drop(columns=["prognosis"])
y = df["prognosis"]

# Handle missing values
imputer = SimpleImputer(strategy="most_frequent")
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)   

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Initialize pyttsx3
engine = pyttsx3.init()

def get_symptoms_from_voice():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please say the symptoms:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing symptoms...")
        symptoms = recognizer.recognize_google(audio)
        print("Symptoms detected:", symptoms)
        return symptoms
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

def get_disease_name_from_voice():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please say the disease name:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing disease name...")
        disease_name = recognizer.recognize_google(audio)
        print("Disease name detected:", disease_name)
        return disease_name
    
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "unknown"
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return "unknown"

def get_yes_or_no_response():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Yes or No?")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing response...")
        response = recognizer.recognize_google(audio).lower()
        print("Response detected:", response)
        return response
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""

def predict_disease(symptoms):
    input_symptoms = {symptom: 1 for symptom in symptoms}
    input_data = pd.DataFrame([input_symptoms], columns=X.columns)
    input_data = pd.DataFrame(imputer.transform(input_data), columns=input_data.columns)  # Impute missing values
    predicted_disease = clf.predict(input_data)[0]
    return predicted_disease

def speak(text):
    engine.say(text)
    engine.runAndWait()

def show_message_box(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Predicted Disease", message)

def disease_prediction_voice_assistant():
    speak("Welcome to the Disease Prediction Assistant.")
    while True:
        symptoms = get_symptoms_from_voice()
        if len(symptoms.split()) < 2:
            speak("Please provide at least two symptoms.")
            continue
        predicted_disease = predict_disease(symptoms.split())
        speak(f"The predicted disease is {predicted_disease}.")
        show_message_box(f"The predicted disease is {predicted_disease}.")
        
        speak("Would you like to provide the disease name verbally?")
        response = get_yes_or_no_response()
        if "yes" in response:
            disease_name = get_disease_name_from_voice()
            speak(f"The recognized disease name is {disease_name}.")
        speak("Do you want to predict another disease?")
        response = get_yes_or_no_response()
        if "no" in response:
            speak("Exiting the Disease Prediction Assistant. Goodbye!")
            break

# Start the voice assistant
disease_prediction_voice_assistant()
