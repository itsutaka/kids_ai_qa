# modules/speaker.py
import pyttsx3
import pygame
import os

engine = pyttsx3.init()
engine.setProperty('rate', 140)  # 小朋友語速，數字越小越慢
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    return "speaking_finished"  # 添加返回值表示播放完成

def stop_speaking():
    engine.stop()

def speak_by_google_tts(text, lang="zh-TW"):
    # ... 現有代碼 ...
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(tmp_path)
    return "speaking_finished"  # 添加返回值表示播放完成
