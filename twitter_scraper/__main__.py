import os
import logging
import asyncio

from typing import Optional, Any, Dict
from twitter_api import TwitterAPI

logger = logging.getLogger()


def unpack_tweets(tweets):
    unpacked_tweets = {}
    for entry in tweets:
        for q in entry:
            unpacked_tweets[q] = entry[q]
    return unpacked_tweets

if __name__ == "__main__":
    # Get credentials
    consumer_key = os.getenv('TWITTER_KEY')
    consumer_secret = os.getenv('TWITTER_SECRET_KEY')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    # Create API
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
    
    # Get tweets
    queries = ['pizza', 'virus', 'corona']
    loop = asyncio.get_event_loop()
    tweets = loop.run_until_complete(api.get_tweets(queries))
    loop.close()
    tweets = unpack_tweets(tweets)

    for query in tweets.values():
        for tweet in query:
            print(tweet)
