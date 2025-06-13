from modules.transcriber import transcribe
from modules.searcher import web_search
from modules.llm import ask_ai
from modules.speaker import speak
from modules.recorder import record_audio

def main():
    print("🎙️ 開始錄音，請說話...")
    record_audio("input.wav")

    print("✅ 錄音完成！音訊已儲存為：input.wav")

    question = transcribe("input.wav")
    print(f"🧠 Whisper 辨識結果：{question}")

    if not question.strip():
        print("⚠️ 沒有辨識到語音內容")
        return

    print("🔍 查詢中...")
    search_result = web_search(question)
    print(f"🔍 查詢結果：{search_result}")

    print("🤖 生成兒童化回答中...")
    answer = ask_ai(question, search_result)
    print(f"🧒 AI回答：{answer}")

    print("🔊 語音合成中...")
    speak(answer)

if __name__ == "__main__":
    main()
