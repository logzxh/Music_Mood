import pyttsx3

# Initialize the engine only once
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()