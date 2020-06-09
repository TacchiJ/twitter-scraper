import asyncio
import boto3
import csv
import logging
import os

from twitter_api import TwitterAPI
from typing import Optional, Any, Dict

logger = logging.getLogger()


def get_tweets_from_api(api, queries):
    loop = asyncio.get_event_loop()
    tweets = loop.run_until_complete(api.get_tweets(queries))
    loop.close()
    return tweets
    

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
    tweets = get_tweets_from_api(api, queries)

    # Local output
    if os.getenv('ENV') == 'dev':
        with open (os.getenv('LOCAL_FILENAME'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            tweet_contents = api.get_tweet_contents()
            writer.writerow(tweet_contents)

            for query_tweets in tweets:
                for tweet in query_tweets:
                    writer.writerow(tweet)
        
        print('Local upload successful')

    # S3 output
    else:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.getenv('BUCKET_NAME'))

        with open ('s3_output.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            tweet_contents = api.get_tweet_contents()
            writer.writerow(tweet_contents)

            for query_tweets in tweets:
                for tweet in query_tweets:
                    writer.writerow(tweet)

        bucket.upload_file('s3_output.csv', os.getenv('BUCKET_KEY'))
        print('S3 upload successful')

