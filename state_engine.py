# state_engine.py

import time
from datetime import datetime
import random
from bot_config import config
from tweet_templates import ragebait, supportive, general

def get_next_action():
    return "reply" if random.random() < config["reply_ratio"] else "tweet"

def main_loop():
    last_mandate = time.time()
    while True:
        action = get_next_action()
        now = time.time()

        # Hourly mandatory tweet
        if now - last_mandate >= config["mandate_tweet_every"]:
            action = "tweet"
            last_mandate = now

        # Pick content based on action
        if action == "tweet":
            content = random.choice(general)
        else:  # reply
            content = random.choice(ragebait + supportive)

        print(datetime.now(), "Action:", action, "Content:", content)
        time.sleep(config["tweet_interval"])

if __name__ == "__main__":
    main_loop()