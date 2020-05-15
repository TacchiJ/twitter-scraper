import os
import logging
import tweepy

logger = logging.getLogger()

class TwitterAPI:

    def get_twitter_api(self):
        # Get credentials
        CONSUMER_KEY = os.getenv('TWITTER_KEY')
        CONSUMER_SECRET = os.getenv('TWITTER_SECRET_KEY')
        ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True, 
                wait_on_rate_limit_notify=True)

        try:
            api.verify_credentials()
        except Exception as e:
            logger.error("Error creating API", exc_info=True)
            raise e
        logger.info("API created")
        return api

