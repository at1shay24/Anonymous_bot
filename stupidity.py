STUPID_KEYWORDS = [
    "finished", "fraud", "overrated", "washed",
    "refs", "robbed", "var", "paid refs",
    "bottlers", "ucl joke", "europa club",
    "small club", "finished club"
]

BARCA_PLAYERS = [
    "pedri", "gavi", "lamine", "yamal", "araujo",
    "ter stegen", "frenkie", "de jong", "raphinha",
    "lewandowski", "xavi", "barca"
]

def is_barca_related(text: str) -> bool:
    t = text.lower()
    return any(p in t for p in BARCA_PLAYERS)

def is_stupid(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in STUPID_KEYWORDS)