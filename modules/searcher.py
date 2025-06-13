from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=max_results):
            if 'body' in r:
                results.append(r['body'])
    return "\n".join(results)
