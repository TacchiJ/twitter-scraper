import asyncio
import logging
import datetime
import tweepy

from typing import Optional, Any, Dict

logger = logging.getLogger()


class TwitterAPI:

    def __init__(self, key, secret_key, access_token, access_token_secret):
        '''Setups a TwitterAPI object with provided credentials'''

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
        
        now = datetime.datetime.now().time()
        print(f"{now}: Twitter API created")
        self.api = api
        
        # Initialize header contents
        self.tweet_contents = ['query', 'user.name', 'text']

    def get_api(self):
        return self.api

    def get_tweet_contents(self):
        return self.tweet_contents

    async def get_tweets(self, queries, n=10, lang='en'):
        tasks = []

        for query in queries:
            tasks.append(asyncio.ensure_future(self.search_tweets(query, n, lang)))
        tweets = await asyncio.gather(*tasks)

        return tweets

    async def search_tweets(self, query, n=10, lang=''):
        '''Searches for most recent n tweets'''
        now = datetime.datetime.now().time()
        print(f"{now}: Searching for '{query}'")
        tweets = []

        for tweet in self.api.search(q=query, count=n, lang=lang):
            data = [query]

            for field in self.tweet_contents[1:]:
                data.append(self.get_attribute(tweet, field))
            tweets.append(data)

        return tweets

    def get_attribute(self, tweet, attribute: str):
        '''Recursively retrieves an attribute or child attribute of a tweet based on a string'''
        if '.' in attribute:
            attributes = attribute.split('.')
            child_attribute = get_attribute(tweet, attributes[0])
            return self.get_attribute(child_attribute, attributes[1])
        try:
            return get_attribute(tweet, attribute)
        except AttributeError:
            logger.error(f"Attribute not found: {attribute}")
            return ''
    