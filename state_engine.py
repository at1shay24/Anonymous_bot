import time
import random
import os
import importlib
from datetime import datetime
from bot_config import config, targets
from tweet_templates import ragebait, supportive, general
from stupidity import is_barca_related, is_stupid
from incoming_tweets import simulated_tweet_stream
from racism_filter import is_racist

LOG_FILE = "bot_log.txt"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("timestamp,action,target,content\n")

def log_action(action, target, content):
    """Append actions to the fixed log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()},{action},{target},{content}\n")

REPLY_MIN_DELAY = 5 * 60
REPLY_MAX_DELAY = 8 * 60
last_reply_time = 0

def can_reply(now: float) -> bool:
    global last_reply_time
    delay = random.randint(REPLY_MIN_DELAY, REPLY_MAX_DELAY)
    if now - last_reply_time >= delay:
        last_reply_time = now
        return True
    return False

STUPID_IGNORE_PROB = 0.9
STUPID_COOLDOWN = 40 * 60
last_stupid_reply = 0
stupid_recent = []

def should_reply_to_stupidity(now: float) -> bool:
    global last_stupid_reply, stupid_recent
    stupid_recent = [t for t in stupid_recent if now - t < 600]
    stupid_recent.append(now)

    if len(stupid_recent) >= 3:
        prob = max(0.2, STUPID_IGNORE_PROB - 0.3)
    elif len(stupid_recent) == 0:
        prob = min(0.95, STUPID_IGNORE_PROB + 0.05)
    else:
        prob = STUPID_IGNORE_PROB

    if now - last_stupid_reply < STUPID_COOLDOWN:
        return random.random() > prob

    last_stupid_reply = now
    return True

sent_replies = {}

def pick_ragebait(pool, target):
    if target not in sent_replies:
        sent_replies[target] = set()

    available = [t for t in ragebait[pool] if t not in sent_replies[target]]
    if not available:
        return random.choice(supportive)

    template = random.choice(available)
    sent_replies[target].add(template)
    return template

def load_players(file_path="players.txt"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def reload_targets():
    import bot_config
    importlib.reload(bot_config)
    return bot_config.targets

players = load_players()
RAGEBAIT_POOLS = set(ragebait.keys())

def get_next_action():
    ratio = config["reply_ratio"]
    if len(stupid_recent) >= 3:
        ratio = min(0.95, ratio + 0.2)
    elif len(stupid_recent) == 0:
        ratio = max(0.1, ratio - 0.1)
    return "reply" if random.random() < ratio else "tweet"

def main_loop():
    last_mandate = time.time()
    last_reload = time.time()
    current_targets = targets.copy()

    tweet_stream = simulated_tweet_stream(delay=5)
    global players

    while True:  # run indefinitely
        now = time.time()

        if now - last_reload > 300:
            players = load_players()
            current_targets = reload_targets()
            last_reload = now

        action = get_next_action()

        if now - last_mandate >= config["mandate_tweet_every"]:
            action = "tweet"
            last_mandate = now

        tweet = next(tweet_stream)
        text = tweet["text"]
        author = tweet["author"]

        if is_barca_related(text) and is_stupid(text) and not is_racist(text):
            if can_reply(now) and should_reply_to_stupidity(now):
                player = random.choice(players) if players else ""
                template = pick_ragebait("real_madrid", author)
                content = template.replace("{player}", player)

                print(datetime.now(), "reply →", author, content)
                log_action("reply", author, content)
                time.sleep(30)
                continue

        if action == "tweet":
            content = random.choice(general)
            print(datetime.now(), "tweet →", content)
            log_action("tweet", "none", content)
        else:
            if not can_reply(now):
                time.sleep(30)
                continue

            pool = random.choice(list(current_targets.keys()))
            target = random.choice(current_targets[pool])
            player = random.choice(players) if players else ""

            template = pick_ragebait(pool, target) if pool in RAGEBAIT_POOLS else random.choice(supportive)
            content = template.replace("{player}", player)

            print(datetime.now(), "reply →", target, content)
            log_action("reply", target, content)

        time.sleep(30)

if __name__ == "__main__":
    main_loop()