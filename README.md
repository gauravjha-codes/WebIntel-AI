# Web Intel AI — Autonomous Real-Time Research Assistant

An autonomous AI web intelligence and research platform powered by **LangChain**, **Groq LPUs**, **DuckDuckGo**, and **BeautifulSoup**. The application bridges high-speed LLMs with the live web to fetch, parse, and synthesize real-time information into structured, citation-backed intelligence reports.

---

## 🌟 Key Features

* **Dual-Mode Operations**:
  * **🌐 Live Web Search Mode**: Executes multi-source web queries via DuckDuckGo (`ddgs`), scrapes clean DOM paragraphs, and synthesizes structured reports with clickable citations.
  * **⚡ Offline AI Reasoner Mode**: Bypasses web search for high-speed direct logical reasoning and code explanations via Groq LPU inference.
* **Concurrent Web Scraping**:
  * Parallel DOM fetching with `ThreadPoolExecutor` and strict 3-second timeouts to eliminate hanging network requests.
  * Instant automatic fallback to rich DuckDuckGo search snippets if target websites block bot scraping.
* **LangChain Orchestration**:
  * Uses LangChain Expression Language (LCEL) chains with `ChatGroq` (`openai/gpt-oss-120b`).
  * Structured output extraction with clean Markdown and syntax-highlighted code blocks.
* **Verified Source Citations**:
  * Displays interactive chips linking directly to the verified external source URLs used in the synthesis.
* **Modern Matte Obsidian & Warm Amber UI**:
  * Sleek dark-mode interface with zero external icon dependencies.
  * 1-click code and text copying, suggestion prompt chips, and session restoration.
* **Persistent Session History**:
  * Automatically stores research queries, responses, timestamps, and sources in `data/chat_history.json`.

---

## 📸 Output & Interface Previews


### 1. Home Dashboard & Starter Inquiries
<img width="1919" height="937" alt="Screenshot 2026-09-24 231903" src="https://github.com/user-attachments/assets/80736fcd-4658-4852-8858-f4ac0ffdcfe5" />

*A minimalist dashboard featuring quick-start research prompts, engine telemetry, and mode toggles.*

---

### 2. Live Web Research & Map-Reduce Synthesis
<img width="1919" height="947" alt="Screenshot 2026-09-24 232214" src="https://github.com/user-attachments/assets/b4868d59-7888-4cf5-a937-df151a62d52f" />

*Real-time intelligence report generated from live web queries, complete with verified source citations.*

#### Sample Text Output:
```markdown
### Executive Summary — 2026 RAM Market Trends
* **Price Surge Projections:** Industry analysts forecast a 40%–70% increase in DRAM contract prices throughout 2026.
* **Supply Constraints:** Production lines are reallocating manufacturing capacity toward high-bandwidth memory (HBM) for AI data centers.
* **Consumer Impact:** DDR5 memory kits have seen the sharpest price hikes, prompting extended lifecycles for DDR4 platforms.

Verified Sources (4):
[1] wikipedia.org/wiki/RAM_price_spike
[2] theverge.com/news/pc-ram-shortage-pricing-spike
[3] tomshardware.com/pc-components/ram/ram-price-index-2026
[4] electroniksindia.com/pages/understanding-global-surge-ram-costs
```

---

### 3. Offline Direct AI Reasoner

<img width="1919" height="935" alt="Screenshot 2026-09-24 233245" src="https://github.com/user-attachments/assets/3b60756a-b36a-4202-994a-c8cc01177cd2" />

*High-speed conversational inference with automatic code formatting and syntax highlighting.*

---

### 4. Session History & History Restoration

<img width="289" height="317" alt="Screenshot 2026-09-24 233317" src="https://github.com/user-attachments/assets/2695083f-ab02-42bf-925d-4630f91dc81a" />

*Sidebar displaying past queries categorized by mode (`Web` vs `Offline`) with single-click session reloading.*

---

## 🏗️ Architecture & Pipeline Flow

```text
[ User Query ]
       │
       ▼
[ Mode Router ] ─────────────────────────┐
       │ (Web Mode)                      │ (Offline Mode)
       ▼                                 ▼
[ DuckDuckGo Search (ddgs) ]     [ ChatGroq LPU Reasoning ]
       │                                 │
       ▼                                 │
[ Parallel Scraper (ThreadPool) ]        │
       │                                 │
       ▼                                 │
[ DOM Sanitizer (BeautifulSoup) ]        │
       │                                 │
       ▼                                 │
[ Text Normalizer & Fallback ]           │
       │                                 │
       ▼                                 │
[ LangChain LCEL Synthesis Chain ]       │
       │                                 │
       ▼                                 ▼
[ Structured Markdown Response + Source Citations ]
       │
       ▼
[ Saved to data/chat_history.json ]
```

---

## 📁 Project Directory Structure

```text
webscraping/
├── .env                       # Local private API keys (never commit to git)
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules for virtual environments & secrets
├── requirements.txt           # Project package dependencies
├── README.md                  # Project documentation & previews
│
├── config.py                  # Central configuration (API keys, models, file paths)
├── app.py                     # Main Flask application factory
├── server.py                  # Server runner entrypoint
│
├── src/
│   ├── services/
│   │   ├── search_service.py  # DuckDuckGo search integration
│   │   ├── scraper_service.py # Parallel DOM scraping & content cleaning
│   │   └── ai_service.py      # LangChain ChatGroq synthesis pipeline
│   ├── routes/
│   │   ├── web_routes.py      # Frontend delivery (GET /)
│   │   └── api_routes.py      # REST endpoints (/search, /history, /status)
│   └── utils/
│       ├── text_cleaner.py    # Unicode normalization & text sanitization
│       └── history_store.py   # JSON storage manager
│
├── data/
│   └── chat_history.json      # Persistent chat session records
│
└── templates/
    └── index.html             # Single-page interface (Matte Obsidian & Warm Amber)
```

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+ installed
* A free Groq Cloud API key from [console.groq.com](https://console.groq.com/keys)

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/web-intel-ai.git
cd web-intel-ai

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root (or copy from `.env.example`):
```env
GROQ_API_KEY="gsk_your_groq_api_key_here"
```

### 4. Run the Application
```bash
python server.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 📡 REST API Reference

| Endpoint | Method | Description | Payload / Response |
| :--- | :--- | :--- | :--- |
| **`/`** | `GET` | Serves the main research dashboard. | HTML template |
| **`/search`** | `POST` | Executes real-time web research or offline AI reasoning. | **Request:** `{"query": "...", "mode": "web"}`<br>**Response:** `{"answer": "...", "sources": [...], "mode": "web"}` |
| **`/history`** | `GET` | Retrieves all saved research sessions. | `[{"query": "...", "response": "...", "sources": [...], "timestamp": "..."}]` |
| **`/clear-history`** | `POST` | Wipes all session history. | `{"success": true, "message": "History cleared"}` |
| **`/status`** | `GET` | Returns system telemetry and active model. | `{"engine": "LangChain + Groq LPU", "model": "openai/gpt-oss-120b", "status": "online"}` |

---

## 🛠️ Technology Stack

* **Language:** Python 3.13
* **LLM Orchestration:** [LangChain](https://www.langchain.com/) (`langchain-groq`, `langchain-core`)
* **Inference Engine:** [Groq LPU](https://groq.com/) (`openai/gpt-oss-120b`)
* **Web Search:** `ddgs` (DuckDuckGo Search)
* **Web Scraping:** BeautifulSoup4 (`bs4`), `requests`, `concurrent.futures`
* **Backend Framework:** Flask 3.x, Flask-CORS
* **Frontend:** HTML5, CSS3 (Vanilla Glassmorphic Design), Marked.js, Highlight.js
