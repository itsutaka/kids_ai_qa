import requests

# 建立一個提示詞模板，幫助模型用兒童語氣回答
prompt_template = (
    "你是一位親切的兒童老師，會用簡單、可愛、有趣的方式回答 6 到 8 歲小朋友的問題，"
    "不使用專業術語，也不說太複雜的話。請用以下格式回答：\n"
    "1. 先用親切的語氣開場白。\n"
    "2. 解釋重點，用小朋友聽得懂的話。\n"
    "3. 結尾用鼓勵孩子探索或發問的語氣。\n"
    "問題是：{question}\n\n這是一些參考資料：\n{context}"
)

def ask_ai(question, context=""):
    # 建立 prompt，將搜尋到的資料也放進去
    prompt = prompt_template.format(question=question, context=context)

    # 呼叫自定義 API
    response = requests.post(
        "http://192.168.1.187:1234/v1/chat/completions",
        json={
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
    )
    
    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        return answer.strip()
    else:
        return "抱歉，我現在無法回答這個問題。"
