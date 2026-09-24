"""
CLI & quick runner utility for Web Intel AI.
Allows running terminal searches directly or starting the server via `python main.py --server`.
"""
import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.services.search_service import search_duckduckgo_detailed

def run_cli_search():
    print("\nDuckDuckGo Search Tool (Web Intel AI)")
    print("-" * 40)
    query = input("Enter your search query: ").strip()
    if not query:
        print("Search query cannot be empty.")
        return

    try:
        max_results = int(input("Number of results (default 5): ") or 5)
    except ValueError:
        max_results = 5

    print("\nSearching...\n")
    results = search_duckduckgo_detailed(query, max_results=max_results)

    if not results:
        print("No results found.")
    else:
        for i, item in enumerate(results, 1):
            print(f"\n{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   Snippet: {item['snippet']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--server", "-s"]:
        from server import app
        from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, FLASK_USE_RELOADER
        app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG, use_reloader=FLASK_USE_RELOADER)
    else:
        run_cli_search()
