import json
import os
from typing import List, Dict, Any
from config import HISTORY_FILE  # pyright: ignore[reportMissingImports]

def load_history() -> List[Dict[str, Any]]:
    """
    Loads persistent session history from JSON storage.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(data: List[Dict[str, Any]]) -> None:
    """
    Saves session history to JSON storage.
    """
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def append_to_history(entry: Dict[str, Any]) -> None:
    """
    Appends a single research record to the history file.
    """
    history = load_history()
    history.append(entry)
    save_history(history)

def clear_all_history() -> None:
    """
    Resets history to an empty list.
    """
    save_history([])
