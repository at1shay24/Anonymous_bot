
import csv
import string
import os

INPUT_FILE = "bot_log.txt"          
OUTPUT_FILE = "train.txt"        

RAGE_KEYWORDS = [
    "crying", "refs", "complain", "payroll", "oil money",
    "galácticos", "low block", "parking the bus",
    "superstars", "zero chemistry", "records shadowed", "luxury roster",
    "no structure", "individual talent", "money buys stars",
    "spending big", "style before shortcuts", "payroll inflated",
    "payroll fc still crying", "same complaints"
]

SUPPORTIVE_KEYWORDS = [
    "trust the process", "visca", "control the game",
    "football played the right way", "composure",
    "confidence", "team moving", "football played with intelligence",
    "barça control the game", "team moving as one unit"
]

def normalize(text: str) -> str:
    """Lowercase and remove punctuation for keyword matching"""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def detect_style(text: str) -> str:
    """Classify text as <ragebait>, <supportive>, or <neutral>"""
    norm_text = normalize(text)
    for word in RAGE_KEYWORDS:
        if word in norm_text:
            return "<ragebait>"
    for word in SUPPORTIVE_KEYWORDS:
        if word in norm_text:
            return "<supportive>"
    return "<neutral>"

def load_existing_lines():
    """Load previous train.txt lines to prevent duplicates"""
    if not os.path.exists(OUTPUT_FILE):
        return set()
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def main():
    existing_lines = load_existing_lines()
    new_lines = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            if len(row) < 4:
                continue
            content = row[3].strip()
            if not content:
                continue
            style = detect_style(content)
            line = f"{style} {content}"
            if line not in existing_lines:
                new_lines.append(line)
                existing_lines.add(line)

    if not new_lines:
        print("No new lines to add.")
        return

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        for line in new_lines:
            f.write(line + "\n")

    print(f"Done ✅")
    print(f"Total new lines added: {len(new_lines)}")
    print(f"Total lines in train.txt: {len(existing_lines)}")

if __name__ == "__main__":
    main()