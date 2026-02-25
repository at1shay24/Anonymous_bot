# state_engine.py

import time
import random
import os
from datetime import datetime

def load_players(file_path="players.txt"):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

players = load_players()
from bot_config import config, targets
from tweet_templates import ragebait, supportive, general
from stupidity import is_barca_related, is_stupid
from incoming_tweets import SIMULATED_TWEETS
LOG_FILE = "bot_log.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,action,target,content\n")

STUPID_IGNORE_PROB = 0.9
STUPID_COOLDOWN = 40 * 60  
last_stupid_reply = 0

def should_reply_to_stupidity(now: float) -> bool:
    global last_stupid_reply
    if now - last_stupid_reply < STUPID_COOLDOWN:
        return random.random() > STUPID_IGNORE_PROB
    else:
        last_stupid_reply = now
        return True

def get_next_action():
    return "reply" if random.random() < config["reply_ratio"] else "tweet"

def log_action(action, target, content):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()},{action},{target},{content}\n")

def main_loop():
    last_mandate = time.time()

    while True:
        now = time.time()
        action = get_next_action()
        
        if now - last_mandate >= config["mandate_tweet_every"]:
            action = "tweet"
            last_mandate = now
        tweet = random.choice(SIMULATED_TWEETS)
        text = tweet["text"]

        if is_barca_related(text) and is_stupid(text):

            if should_reply_to_stupidity(now):
                action = "reply"
                target = tweet["author"]
                content = random.choice(ragebait["real_madrid"])
                print(datetime.now(), "Action:", action, "Target:", target, "Content:", content)
                log_action(action, target, content)
                time.sleep(config["tweet_interval"])
                continue

        if action == "tweet":
            target = "none"
            content = random.choice(general)
        else:
            pool = random.choice(list(targets.keys()))
            target = random.choice(targets[pool])
            player = random.choice(players) if players else ""
            if pool in ragebait:
                template = random.choice(ragebait[pool])
            else:
                template = random.choice(supportive)
            content = template.replace("{player}", player)

        print(datetime.now(), "Action:", action, "Target:", target, "Content:", content)
        log_action(action, target, content)
        time.sleep(config["tweet_interval"])

if __name__ == "__main__":
    main_loop()