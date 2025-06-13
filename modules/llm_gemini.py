import google.generativeai as genai
from google.cloud import texttospeech
import tempfile
import os
import pygame

# 設定 Gemini API 金鑰
genai.configure(api_key="你的_GEMINI_API_KEY")

def ask_gemini(question, context=""):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([question, context])
    return response.text

def speak_by_google_tts(text, lang="zh-TW"):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
        out.write(response.audio_content)
        tmp_path = out.name
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(tmp_path)