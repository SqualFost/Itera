import requests
from ddgs import DDGS
import trafilatura

def check_network(url="https://www.google.com", timeout=3):
    """Test if the user is connected to the internet."""
    try:
        requests.get(url, timeout=timeout)
        return True
    except Exception:
        return False

def web_search_and_read(query: str, max_pages: int = 3):
    """Web search using DuckDuckGo and extract content."""
    results = DDGS().text(query, max_results=max_pages)
    output = []
    for r in results:
        url = r.get("href")
        try:
            html = requests.get(url, timeout=10).text
            text = trafilatura.extract(html)
            output.append({
                "title": r.get("title"),
                "url": url,
                "content": text[:3000] if text else None
            })
        except Exception as e:
            output.append({"url": url, "error": str(e)})
    return output
