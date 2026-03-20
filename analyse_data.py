import csv
import random
INPUT_FILE = "bot_log.txt"
OUTPUT_FILE = "train.txt"
NEUTRAL_KEEP_PROB = 0.4
def detect_style(text: str) -> str:
    t = text.lower()
    rage_patterns = [
        "crying", "refs", "complain", "payroll", "oil money",
        "galácticos", "low block", "parking the bus",
        "no structure", "individual talent", "money buys",
        "spending big", "complaints fc", "dna of the club",
        "excuses", "charges", "allegations", "115",
        "same complaints", "zero chemistry", "noise without substance",
        "legacy still under review", "numbers don’t add up",
        "numbers dont add up", "blame", "bottlers"
    ]
    supportive_patterns = [
        "visca", "trust the process", "control the game",
        "confidence", "composure", "team moving",
        "playing the right way", "calm", "identity",
        "progress", "collective", "dominance"
    ]
    for p in rage_patterns:
        if p in t:
            return "<ragebait>"
    for p in supportive_patterns:
        if p in t:
            return "<supportive>"
    words = t.split()
    if len(words) <= 4 and any(w in t for w in ["no", "same", "just", "only"]):
        return "<ragebait>"
    return "<neutral>"
def is_valid(text: str) -> bool:
    words = text.split()
    if len(words) < 3:
        return False
    if text.endswith(("the", "a", "an", "and", "or")):
        return False
    return True
def main():
    texts = []
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader) 
        for row in reader:
            if len(row) < 4:
                continue
            content = ",".join(row[3:]).strip()
            if not content:
                continue
            if not is_valid(content):
                continue
            style = detect_style(content)
            if style == "<neutral>" and random.random() > NEUTRAL_KEEP_PROB:
                continue
            texts.append(f"{style} {content}")
    seen = set()
    clean_texts = []
    for t in texts:
        if t not in seen:
            seen.add(t)
            clean_texts.append(t)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in clean_texts:
            f.write(line + "\n")
    print("Done ✅")
    print(f"Total lines written: {len(clean_texts)}")


if __name__ == "__main__":
    main()