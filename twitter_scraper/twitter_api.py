import asyncio
import logging
import datetime
import tweepy

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
        now = datetime.datetime.now().time()
        print(f"{now}: Twitter API created")
        self.api = api
        
        # Initialize header contents to default values
        self.tweet_contents = ['query', 'user.name', 'text']

    def get_api(self):
        '''Returns the tweepy.API object'''
        return self.api

    def set_tweet_contents(self, contents: list):
        '''Updates tweet_contents with new values'''
        self.tweet_contents = contents
        
    def get_tweet_contents(self):
        '''Returns current tweet_contents'''
        return self.tweet_contents

    async def get_tweets(self, queries, n=10, lang='en'):
        '''Returns n most recent tweets for each query

        :param queries: a list of strings to be searched for
        :param n: the number of tweets to be returned for each query
        :param lang: the language of tweets to search for
        '''
        tasks = []

        for query in queries:
            tasks.append(asyncio.ensure_future(self._search_tweets(query, n, lang)))
        tweets = await asyncio.gather(*tasks)

        return tweets

    async def _search_tweets(self, query, n, lang):
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
            child_attribute = getattr(tweet, attributes[0])
            return self.get_attribute(child_attribute, attributes[1])
        try:
            return getattr(tweet, attribute)
        except AttributeError:
            logger.error(f"Attribute not found: {attribute}")
            return ''
    