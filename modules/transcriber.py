import os
import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

def record_audio(filename="input.wav", duration=5, fs=16000):
    print("🎙️ 開始錄音，請說話...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        wav.write(filename, fs, recording)
        print(f"✅ 錄音完成！音訊已儲存為：{filename}")
    except Exception as e:
        print("❌ 錄音失敗：", e)

def transcribe(filename="input.wav"):
    print("🧠 開始使用 Whisper 辨識語音內容...")
    
    if not os.path.exists(filename):
        print("❌ 找不到音訊檔案：", filename)
        return ""

    try:
        model = WhisperModel("small", device="cpu", compute_type="int8")  # 使用小模型較穩定
        segments, info = model.transcribe(filename, beam_size=5)

        texts = []
        for segment in segments:
            print(f"  📄 時間 {segment.start:.2f}s - {segment.end:.2f}s：{segment.text}")
            if segment.text.strip():
                texts.append(segment.text.strip())

        result = " ".join(texts)
        if result:
            print("🧠 Whisper 辨識結果：", result)
        else:
            print("⚠️ Whisper 沒有辨識出任何語音內容")

        return result

    except Exception as e:
        print("❌ Whisper 辨識失敗：", e)
        return ""
