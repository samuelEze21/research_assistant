from duckduckgo_search import DDGS
import httpx
from bs4 import BeautifulSoup

def web_search(query: str, k: int = 5):
    with DDGS() as ddg:
        results = ddg.text(query, max_results=k, safesearch="moderate")
    return [{
        "title": r.get("title", ""),
        "link": r.get("href", ""),
        "snippet": r.get("body", "")
    } for r in results or []]

async def fetch_clean_text(url: str, max_chars: int = 8000) -> str:
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            r = await client.get(url, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
        return text[:max_chars]
    except Exception:
        return ""
