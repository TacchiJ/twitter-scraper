import os
import logging
import tweepy
import asyncio
import requests
import pandas as pd

from typing import Optional, Any, Dict

logger = logging.getLogger()


class TwitterAPI:

    def __init__(self, key, secret_key, access_token, access_token_secret):
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(key, secret_key)
        auth.set_access_token(access_token, access_token_secret)

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True, 
                wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except Exception as e:
            logger.error("Error creating API", exc_info=True)
            raise e
        logger.info("API created")
        self.api = api

    def get_api(self):
        return self.api

    async def get_tweets(self, queries, n=10, lang='en'):
        tasks = []
        for query in queries:
            tasks.append(asyncio.ensure_future(self.search_tweets(query, n, lang)))
        tweets = await asyncio.gather(*tasks)
        return tweets

    # Searches for most recent tweets
    async def search_tweets(self, query, n, lang):
        tweets = []
        for tweet in self.api.search(q=query, count=n, lang=lang):
            print(f"{tweet.text}")
            tweets.append([tweet.user.name, tweet.text])
        return {query: tweets}
            