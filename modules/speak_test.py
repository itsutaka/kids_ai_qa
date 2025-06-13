import pyttsx3

engine = pyttsx3.init()

# 設定慢速語速，適合小朋友（單位約 100~200 之間）
engine.setProperty('rate', 100)

# 設定音量（可選）
engine.setProperty('volume', 1.0)

# 語者可選（依系統不同）
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# 要說的話
engine.say("你好，小朋友，歡迎來到語音問答時間！")

engine.runAndWait()
