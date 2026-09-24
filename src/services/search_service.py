from datetime import datetime
from typing import List, Dict, Any
from ddgs import DDGS

def enhance_query(query: str) -> str:
    """
    Cleans and optimizes the query for fresh results without forcing unindexed future dates.
    """
    current_year = datetime.now().year
    return f"{query} {current_year}"

def search_duckduckgo_detailed(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Executes a DuckDuckGo search and returns list of items with title, href, and snippet body.
    """
    items: List[Dict[str, str]] = []
    try:
        with DDGS() as ddgs:
            # First try with enhanced query, fallback to raw query
            results = list(ddgs.text(enhance_query(query), max_results=max_results))
            if not results:
                results = list(ddgs.text(query, max_results=max_results))

            for r in results:
                href = r.get("href")
                if href:
                    items.append({
                        "url": href,
                        "title": r.get("title", ""),
                        "snippet": r.get("body", "")
                    })
    except Exception as e:
        print(f"[Search Service] DuckDuckGo search error: {e}")
    return items

def search_duckduckgo(query: str, max_results: int = 5) -> List[str]:
    """
    Legacy helper returning just URLs.
    """
    items = search_duckduckgo_detailed(query, max_results=max_results)
    return [item["url"] for item in items]
