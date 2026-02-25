# state_engine.py

import time
import random
import os
from datetime import datetime
import importlib

from bot_config import config, targets
from tweet_templates import ragebait, supportive, general
from stupidity import is_barca_related, is_stupid
from incoming_tweets import simulated_tweet_stream
from racism_filter import is_racist  # new module

# Log file setup
LOG_FILE = "bot_log.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,action,target,content\n")

# Pools allowed for ragebait
RAGEBAIT_POOLS = set(ragebait.keys())

# Stupidity reply timing
STUPID_IGNORE_PROB = 0.9
STUPID_COOLDOWN = 40 * 60  # 40 minutes
last_stupid_reply = 0

# Reply memory
sent_replies = {}  # target_name -> set of sent templates

# Tweet generator (simulated live stream)
tweet_stream = simulated_tweet_stream(delay=5)  # delay in seconds

# Players dynamic reload
def load_players(file_path="players.txt"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

players = load_players()

# Targets dynamic reload
def reload_targets():
    import bot_config
    importlib.reload(bot_config)
    return bot_config.targets

# Pick ragebait with memory
def pick_ragebait(pool, target):
    if target not in sent_replies:
        sent_replies[target] = set()

    available = [t for t in ragebait[pool] if t not in sent_replies[target]]
    if not available:
        template = random.choice(supportive)
    else:
        template = random.choice(available)
        sent_replies[target].add(template)
    return template

# Track recent stupidity tweets for dynamic tuning
stupid_recent = []

def should_reply_to_stupidity(now: float) -> bool:
    global last_stupid_reply, STUPID_IGNORE_PROB, stupid_recent
    # Clean old entries older than 10 mins
    stupid_recent = [t for t in stupid_recent if now - t < 600]
    # Adjust ignore probability: more recent stupidity → reply more
    if len(stupid_recent) >= 3:
        prob = max(0.2, STUPID_IGNORE_PROB - 0.3)
    elif len(stupid_recent) == 0:
        prob = min(0.95, STUPID_IGNORE_PROB + 0.05)
    else:
        prob = STUPID_IGNORE_PROB
    # Track this stupidity
    stupid_recent.append(now)

    if now - last_stupid_reply < STUPID_COOLDOWN:
        return random.random() > prob
    else:
        last_stupid_reply = now
        return True

def get_next_action():
    # Dynamic reply ratio based on recent stupidity
    ratio = config["reply_ratio"]
    if len(stupid_recent) >= 3:
        ratio = min(0.95, ratio + 0.2)
    elif len(stupid_recent) == 0:
        ratio = max(0.1, ratio - 0.1)
    return "reply" if random.random() < ratio else "tweet"

def log_action(action, target, content):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()},{action},{target},{content}\n")

def main_loop():
    last_mandate = time.time()
    last_reload = time.time()

    global players
    current_targets = targets.copy()

    while True:
        now = time.time()

        # Reload players and targets every 5 minutes
        if now - last_reload > 300:
            players = load_players()
            current_targets = reload_targets()
            last_reload = now

        action = get_next_action()

        # Mandatory hourly tweet
        if now - last_mandate >= config["mandate_tweet_every"]:
            action = "tweet"
            last_mandate = now

        # Get next tweet from simulated stream
        tweet = next(tweet_stream)
        text = tweet["text"]

        # Stupidity reply with racism filter
        if is_barca_related(text) and is_stupid(text) and not is_racist(text):
            if should_reply_to_stupidity(now):
                action = "reply"
                target = tweet["author"]
                player = random.choice(players) if players else ""
                template = pick_ragebait("real_madrid", target)
                content = template.replace("{player}", player)
                print(datetime.now(), "Action:", action, "Target:", target, "Content:", content)
                log_action(action, target, content)
                time.sleep(config["tweet_interval"])
                continue

        # Regular action selection
        if action == "tweet":
            target = "none"
            content = random.choice(general)
        else:
            pool = random.choice(list(current_targets.keys()))
            target = random.choice(current_targets[pool])
            player = random.choice(players) if players else ""

            if pool in RAGEBAIT_POOLS:
                template = pick_ragebait(pool, target)
                content = template.replace("{player}", player)
            else:
                template = random.choice(supportive)
                content = template.replace("{player}", player)

        print(datetime.now(), "Action:", action, "Target:", target, "Content:", content)
        log_action(action, target, content)
        time.sleep(config["tweet_interval"])

if __name__ == "__main__":
    main_loop()