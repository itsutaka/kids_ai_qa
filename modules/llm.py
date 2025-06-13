from duckduckgo_search import DDGS
import ollama

def simplify_for_kids(text):
    # 非常基礎的簡化語氣方式（可再優化）
    replacements = {
        "因此": "所以",
        "然而": "但是",
        "例如": "比方說",
        "這意味著": "這表示",
        "我們可以得出結論": "我們可以知道",
        "這個現象": "這件事情"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def ask_ai(question, context):
    prompt = f"""
你是一位友善的老師，正在跟 6 到 8 歲的小朋友說話。請用簡單、溫柔的語氣回答這個問題，並根據下面的資料來幫忙解釋：

問題：「{question}」
資料：「{context}」

請用簡短易懂的方式回答，讓小朋友聽得懂。
"""
    response = ollama.chat(
        model="llama2-chinese:7b-chat-q4_0",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response['message']['content']
    return simplify_for_kids(text.strip())
