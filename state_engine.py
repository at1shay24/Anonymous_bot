import time
import random
import os
from datetime import datetime
from bot_config import config, targets
from tweet_templates import ragebait, supportive, general

LOG_FILE = "bot_log.txt"
MEMORY_FILE = "recent_memory.txt"
MEMORY_SIZE = 50 
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,action,target,content\n")

if not os.path.exists(MEMORY_FILE):
    open(MEMORY_FILE, "w").close()
def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return [line.strip() for line in f.readlines()[-MEMORY_SIZE:]]

def save_to_memory(text):
    with open(MEMORY_FILE, "a") as f:
        f.write(text + "\n")

def pick_non_repeating(options, memory):
    random.shuffle(options)
    for opt in options:
        if opt not in memory:
            return opt
    return random.choice(options) 

def get_next_action():
    return "reply" if random.random() < config["reply_ratio"] else "tweet"

def mock_read_target_tweet(target):
    """
    Placeholder until scraping/API.
    Simulates recent tweet content.
    """
    mock_samples = [
        "Ref robbed us again",
        "We dominated possession",
        "VAR is a joke",
        "Big win today"
    ]
    return random.choice(mock_samples)

def generate_reply(pool, memory, target_tweet):
    if pool in ragebait:
        options = ragebait[pool]
    else:
        options = supportive

    return pick_non_repeating(options, memory)

def main_loop():
    last_mandate = time.time()

    while True:
        memory = load_memory()
        action = get_next_action()
        now = time.time()

        if now - last_mandate >= config["mandate_tweet_every"]:
            action = "tweet"
            last_mandate = now

        if action == "tweet":
            target = "none"
            content = pick_non_repeating(general, memory)

        else:
            pool = random.choice(list(targets.keys()))
            target = random.choice(targets[pool])

            target_tweet = mock_read_target_tweet(target)
            content = generate_reply(pool, memory, target_tweet)

        timestamp = datetime.now().isoformat()
        print(timestamp, "Action:", action, "Target:", target, "Content:", content)

        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp},{action},{target},{content}\n")

        save_to_memory(content)
        time.sleep(config["tweet_interval"])

if __name__ == "__main__":
    main_loop()