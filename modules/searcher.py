# modules/searcher.py
from duckduckgo_search import DDGS

def search(query: str, max_results=3) -> str:
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                if 'body' in r:
                    results.append(r['body'])
                if len(results) >= max_results:
                    break
        if not results:
            return "對不起，我找不到答案。"
        return results[0]
    except Exception as e:
        return f"查詢時發生錯誤：{e}"
