
import time
from datetime import datetime
import random
from bot_config import config

def get_next_action():
    return "reply" if random.random() < config["reply_ratio"] else "tweet"

def main_loop():
    last_mandate = time.time()
    while True:
        action = get_next_action()
        now = time.time()

        if now - last_mandate >= config["mandate_tweet_every"]:
            action = "tweet"
            last_mandate = now

        print(datetime.now(), "Action:", action)
        time.sleep(config["tweet_interval"])

if __name__ == "__main__":
    main_loop()