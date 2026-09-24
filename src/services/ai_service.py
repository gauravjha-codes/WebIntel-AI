from typing import Tuple, List
from config import GROQ_API_KEY, DEFAULT_MODEL  # pyright: ignore[reportMissingImports]
from src.utils.text_cleaner import clean_output
from src.services.search_service import search_duckduckgo_detailed
from src.services.scraper_service import scrape_pages_parallel

# LangChain Core & Groq Integrations
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize Groq Chat Model via LangChain
llm = ChatGroq(
    model=DEFAULT_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0.3
)

output_parser = StrOutputParser()

# 2. High-Speed Synthesis Chains
research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert AI research analyst. Synthesize information accurately, concisely, and objectively."),
    ("user", """Analyze the following research material regarding: "{query}"

Rules:
• Provide a comprehensive yet concise executive summary
• Use clear bullet points for key facts, dates, prices, and causes
• Avoid fluff and repetition
• Keep facts strictly anchored to the provided context

Research Material:
{content}""")
])
research_chain = research_prompt | llm | output_parser

# Offline Direct AI Chat
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful, knowledgeable AI assistant.

Provide clear and accurate answers.
- Explain concepts clearly
- Use bullet points where appropriate
- Keep answers structured but natural"""),
    ("user", "{query}")
])
chat_chain = chat_prompt | llm | output_parser


def chat_with_ai(query: str) -> str:
    """
    Direct reasoning using Groq LPU without external web search.
    """
    try:
        return chat_chain.invoke({"query": query})
    except Exception as e:
        return f"Offline reasoning error: {str(e)}"


def execute_web_research(query: str) -> Tuple[str, List[str]]:
    """
    High-speed autonomous web research pipeline:
    1. Search DuckDuckGo (returns URLs + instant snippets)
    2. Concurrently scrape web pages in parallel (~2 seconds total)
    3. Synthesize via LangChain in a single high-speed LPU pass
    """
    search_items = search_duckduckgo_detailed(query, max_results=5)
    if not search_items:
        return "No relevant search results found. Please try refining your query.", []

    urls = [item["url"] for item in search_items]

    # Scrape all candidate URLs concurrently with a strict 3-second timeout
    scraped_data = scrape_pages_parallel(urls, max_workers=4, timeout=3)

    # Compile structured context combining scraped pages and search snippets
    compiled_sections: List[str] = []
    verified_sources: List[str] = []

    for item in search_items:
        url = item["url"]
        title = item["title"]
        snippet = item["snippet"]

        page_content = scraped_data.get(url, "")
        # If scraped content exists and is rich, use it; otherwise fallback to the search snippet
        content_to_use = page_content if len(page_content) > 150 else snippet

        if content_to_use:
            compiled_sections.append(f"Source: {title} ({url})\nContent:\n{content_to_use}")
            verified_sources.append(url)

    if not compiled_sections:
        return "No readable content could be retrieved from search results.", []

    # Limit context size to ~8,000 characters to ensure ultra-fast 1-pass synthesis
    full_context = "\n\n---\n\n".join(compiled_sections)[:9000]

    try:
        summary = research_chain.invoke({
            "query": query,
            "content": full_context
        })
        return clean_output(summary), verified_sources
    except Exception as e:
        return f"LangChain synthesis error: {str(e)}", verified_sources
