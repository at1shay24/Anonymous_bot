import time
from datetime import datetime
import random
from bot_config import config, targets
from tweet_templates import ragebait, supportive, general
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
        if action == "tweet":
            target = "none"
            content = random.choice(general)
        else:
            pool = random.choice(list(targets.keys()))
            target = random.choice(targets[pool])

            if pool in ragebait:
                content = random.choice(ragebait[pool])
            else:
                content = random.choice(supportive)
        print(datetime.now(), "Action:", action, "Target:", target, "Content:", content)
        time.sleep(config["tweet_interval"])

if __name__ == "__main__":
    main_loop()