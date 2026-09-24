import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def clean_content(html: str) -> str:
    """
    Strips scripts, styling, navbars, footers, headers, and extracts clean paragraphs.
    """
    if not html:
        return ""
    try:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 35]
        return ". ".join(sentences[:30])  # Keep top 30 most informative sentences
    except Exception:
        return ""

def scrape_page(url: str, timeout: int = 3) -> str:
    """
    Fetches raw HTML from a target URL with a strict timeout.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200 and r.text:
            return clean_content(r.text)
        return ""
    except Exception:
        return ""

def scrape_pages_parallel(urls: List[str], max_workers: int = 4, timeout: int = 3) -> Dict[str, str]:
    """
    Scrapes multiple pages concurrently in parallel, completing in ~2-3 seconds total.
    """
    results: Dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_page, url, timeout): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                content = future.result()
                if content:
                    results[url] = content
            except Exception:
                pass
    return results
