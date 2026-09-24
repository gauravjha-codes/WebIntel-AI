from datetime import datetime
from flask import Blueprint, request, jsonify
from config import DEFAULT_MODEL  # pyright: ignore[reportMissingImports]
from src.services.ai_service import execute_web_research, chat_with_ai
from src.utils.history_store import load_history, append_to_history, clear_all_history

api_bp = Blueprint("api", __name__)

@api_bp.route("/search", methods=["POST"])
def search():
    """
    Main research endpoint:
    - mode="web": triggers DuckDuckGo search + parallel scraping + LangChain synthesis.
    - mode="offline": direct Groq LPU chat completion.
    """
    data = request.json or {}
    query = data.get("query", "").strip()
    mode = data.get("mode", "web")

    if not query:
        return jsonify({"answer": "Query cannot be empty.", "sources": [], "mode": mode}), 400

    try:
        if mode == "offline":
            answer = chat_with_ai(query)
            sources = []
        else:
            answer, sources = execute_web_research(query)

        append_to_history({
            "query": query,
            "response": answer,
            "mode": mode,
            "sources": sources,
            "timestamp": datetime.now().strftime("%b %d, %I:%M %p")
        })

        return jsonify({
            "answer": answer,
            "sources": sources,
            "mode": mode
        })
    except Exception as e:
        print(f"[API Error] /search: {e}")
        return jsonify({
            "answer": f"**Research Pipeline Error:** {str(e)}",
            "sources": [],
            "mode": mode
        }), 200


@api_bp.route("/history", methods=["GET"])
def get_history():
    """Returns stored session history."""
    try:
        return jsonify(load_history())
    except Exception as e:
        return jsonify([])


@api_bp.route("/clear-history", methods=["POST"])
def clear_history():
    """Clears all session history."""
    try:
        clear_all_history()
        return jsonify({"success": True, "message": "History cleared successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api_bp.route("/status", methods=["GET"])
def status():
    """Returns system status, active model, and engine configuration."""
    return jsonify({
        "status": "online",
        "model": DEFAULT_MODEL,
        "engine": "LangChain + Groq LPU",
        "pipeline": "Parallel Scraping + Synthesis"
    })
