import asyncio
import csv
import logging
import os
import sys

sys.path.insert(1, '')
from import_export import ImporterExporter
from twitter_api import TwitterAPI

from typing import Optional, Any, Dict

logger = logging.getLogger()


def get_tweets_from_api(api, queries):
    loop = asyncio.get_event_loop()
    queries = loop.run_until_complete(api.get_tweets(queries))
    loop.close()
    tweets = [tweet for query in queries for tweet in query]
    return tweets


if __name__ == "__main__":

    # Get credentials
    consumer_key = os.getenv('TWITTER_KEY')
    consumer_secret = os.getenv('TWITTER_SECRET_KEY')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    # Get tweets
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
    queries = ['pizza', 'virus', 'corona']
    tweets = get_tweets_from_api(api, queries)

    # Export data
    importer_exporter = ImporterExporter()

    # Local
    if os.getenv('ENV') == 'dev':
        filename = os.getenv('LOCAL_FILENAME')
        header = api.get_tweet_contents()
        importer_exporter.local_export(filename, header=header, data=tweets)
        
    # S3
    else:
        filename = os.getenv('S3_FILENAME')
        bucket_name = os.getenv('BUCKET_NAME')
        bucket_key = os.getenv('BUCKET_KEY')
        header = api.get_tweet_contents()
        importer_exporter.s3_export(filename, bucket_name, bucket_key, header=header, data=tweets)
