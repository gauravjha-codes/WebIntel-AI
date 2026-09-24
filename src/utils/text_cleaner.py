import re
import unicodedata

def clean_output(text: str) -> str:
    """
    Cleans raw LLM outputs:
    1. Normalizes non-breaking spaces and special dashes to ASCII to prevent
       Windows cp1252 encoding crashes.
    2. Removes excessive consecutive newlines.
    3. Trims whitespace.
    """
    if not text:
        return ""

    # Replace special unicode spaces and dashes that break Windows cp1252 consoles
    replacements = {
        '\u202f': ' ',
        '\u00a0': ' ',
        '\u200b': '',
        '\u2011': '-',
        '\u2012': '-',
        '\u2013': '-',
        '\u2014': '--',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)

    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text.strip()
