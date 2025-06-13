import os
import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

# 音訊參數
SAMPLE_RATE = 16000
DURATION = 5  # 秒數
FILENAME = "input.wav"

# 初始化模型（medium 模型適合在 CPU 上運行）
model = WhisperModel("medium", device="cpu", compute_type="int8")

def record_audio(filename=FILENAME, duration=DURATION):
    print("🎙️ 開始錄音，請說話...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, SAMPLE_RATE, recording)
    print(f"✅ 錄音完成！音訊已儲存為：{filename}")

def transcribe(filename=FILENAME):
    print("🧠 開始使用 Whisper 辨識語音內容...")
    segments, _ = model.transcribe(filename, beam_size=5, vad_filter=True, vad_parameters={"threshold": 0.6})

    results = []
    for segment in segments:
        start = round(segment.start, 2)
        end = round(segment.end, 2)
        text = segment.text.strip()
        print(f"  📄 時間 {start}s - {end}s：{text}")
        results.append(text)

    full_text = " ".join(results).strip()
    print("🧠 Whisper 辨識結果：" + full_text)
    return full_text

if __name__ == "__main__":
    record_audio()
    transcribe()
