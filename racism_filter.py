# racism_filter.py

import re

# Simple keyword-based filter (expand list as needed)
RACIST_KEYWORDS = [
    "slur1", "slur2", "offensivephrase", "hateword"
]

def is_racist(text: str) -> bool:
    """
    Returns True if the text contains any racist/offensive keywords.
    Case-insensitive match.
    """
    text_lower = text.lower()
    for keyword in RACIST_KEYWORDS:
        if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", text_lower):
            return True
    return False