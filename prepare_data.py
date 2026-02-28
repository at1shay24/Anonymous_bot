# prepare_data.py

import csv
from collections import Counter

INPUT_FILE = "bot_log.txt"
OUTPUT_FILE = "train.txt"

def detect_style(text: str) -> str:
    text_lower = text.lower()

    rage_keywords = [
        "crying", "refs", "complain", "payroll", "oil money",
        "galácticos", "low block", "parking the bus"
    ]

    supportive_keywords = [
        "trust the process", "visca", "control the game",
        "football played the right way"
    ]

    for word in rage_keywords:
        if word in text_lower:
            return "<ragebait>"

    for word in supportive_keywords:
        if word in text_lower:
            return "<supportive>"

    return "<neutral>"

def main():
    texts = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            if len(row) < 4:
                continue

            content = row[3].strip()
            if not content:
                continue

            style = detect_style(content)
            texts.append(f"{style} {content}")

    # remove duplicates but preserve order
    seen = set()
    clean_texts = []
    for t in texts:
        if t not in seen:
            seen.add(t)
            clean_texts.append(t)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in clean_texts:
            f.write(line + "\n")

    print(f"Done ✅")
    print(f"Total lines written: {len(clean_texts)}")

if __name__ == "__main__":
    main()