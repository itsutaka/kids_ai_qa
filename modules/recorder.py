import sounddevice as sd
import scipy.io.wavfile as wav

def record_audio(filename='input.wav', duration=5, samplerate=16000):
    print("🎙️ 開始錄音，請說話...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write(filename, samplerate, recording)
    print(f"✅ 錄音完成！音訊已儲存為：{filename}")
