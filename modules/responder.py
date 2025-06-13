import subprocess

def ask_llama(prompt):
    print("🤖 叫用 Ollama 處理中...")

    process = subprocess.Popen(
        ["ollama", "run", "llama2-chinese:7b-chat-q4_0"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, _ = process.communicate(prompt)
    return output.strip()
