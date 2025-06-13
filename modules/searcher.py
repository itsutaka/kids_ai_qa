from duckduckgo_search import DDGS

def search(query, max_results=3):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        if not results:
            return ["找不到相關資料。"]
        return [r['body'] for r in results if 'body' in r]
