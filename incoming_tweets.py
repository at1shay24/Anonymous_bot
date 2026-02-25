# incoming_tweets.py

import time
import random

# Example simulated tweet pool
SIMULATED_TWEET_POOL = [
    {"author": "RealFan1", "text": "Refs working overtime again?"},
    {"author": "CityFan1", "text": "115 reasons and counting."},
    {"author": "AtletiFan1", "text": "Parking the bus isn’t football."},
    {"author": "NeutralFan", "text": "Great play by X, unstoppable!"},
    {"author": "YankeesFan1", "text": "All that money, same excuses."},
    # Add more as needed
]

def simulated_tweet_stream(delay=5):
    """
    Generator that yields tweets one by one, with an optional delay between them.
    Simulates a live incoming feed.
    """
    while True:
        tweet = random.choice(SIMULATED_TWEET_POOL)
        yield tweet
        time.sleep(delay)  # simulate time between tweets