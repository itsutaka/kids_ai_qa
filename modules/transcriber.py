from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")

def transcribe_audio(audio_path='input.wav'):
    segments, _ = model.transcribe(audio_path, language="zh")
    result = " ".join([seg.text for seg in segments])
    return result
