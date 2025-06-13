import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel
from modules.searcher import search
from modules.speaker import speak

# 錄音設定
duration = 5  # 錄音秒數
def record_audio(filename="input.wav"):
    print("🎙️ 開始錄音，請說話...")
    samplerate = 16000
    recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, samplerate, recording)
    print("✅ 錄音完成！音訊已儲存為：" + filename)

# 語音轉文字
def transcribe_audio(filename="input.wav"):
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(filename)
    return "".join([segment.text for segment in segments])

# 主流程
def main():
    record_audio()
    question = transcribe_audio().strip()
    print("🧠 Whisper 辨識結果：", question)

    if question:
        # 包裝成兒童風格 prompt
        prompt = f"請用可愛、簡單又親切的方式，告訴 6 到 8 歲小朋友：「{question}」"
        answer = search(prompt)
        print("🔍 查詢回答：", answer)
        print("🔊 語音合成中...")
        speak(answer)
    else:
        print("😅 沒聽清楚，請再試一次！")

if __name__ == "__main__":
    main()
