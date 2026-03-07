# analyse_data.py

import csv

INPUT_FILE = "bot_log_20260228.txt"
OUTPUT_FILE = "train.txt"

# Keywords to classify tweets
RAGE_KEYWORDS = [
    "crying", "refs", "complain", "payroll", "oil money",
    "galácticos", "low block", "parking the bus", "superstars", "zero chemistry"
]

SUPPORTIVE_KEYWORDS = [
    "trust the process", "visca", "control the game",
    "football played the right way", "composure", "confidence", "team moving"
]

def detect_style(text: str) -> str:
    """Return <ragebait>, <supportive>, or <neutral> based on keywords."""
    text_lower = text.lower()
    for word in RAGE_KEYWORDS:
        if word in text_lower:
            return "<ragebait>"
    for word in SUPPORTIVE_KEYWORDS:
        if word in text_lower:
            return "<supportive>"
    return "<neutral>"

def main():
    texts = []

    # Open CSV with proper quoting to handle commas in tweet content
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if len(row) < 4:
                continue
            timestamp, action, target, content = row[0], row[1], row[2], row[3].strip()
            if not content:
                continue
            style = detect_style(content)
            texts.append(f"{style} {content}")

    # Remove duplicates but preserve order
    seen = set()
    clean_texts = []
    for t in texts:
        if t not in seen:
            seen.add(t)
            clean_texts.append(t)

    # Write to output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in clean_texts:
            f.write(line + "\n")

    print(f"Done ✅")
    print(f"Total lines written: {len(clean_texts)}")

if __name__ == "__main__":
    main()