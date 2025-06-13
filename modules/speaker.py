# modules/speaker.py
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 140)  # 小朋友語速，數字越小越慢
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def stop_speaking():
    engine.stop()
