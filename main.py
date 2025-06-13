from modules.recorder import record_audio
from modules.transcriber import transcribe_audio
from modules.searcher import search
from modules.responder import ask_llama

# Step 1: 錄音
record_audio()

# Step 2: 語音辨識
question = transcribe_audio()
print("📝 小朋友問：", question)

# Step 3: DuckDuckGo 查詢
results = search(question)
print("🔍 查詢補充：", results)

# Step 4: 整理 Prompt 丟給 Ollama 回答
prompt = f"""小朋友問了這個問題：{question}
以下是 DuckDuckGo 的查詢摘要可以幫助你回答：
{chr(10).join(results)}

請用簡單、有趣的方式回答小朋友的問題。
"""
answer = ask_llama(prompt)
print("🤖 AI 回答：", answer)
