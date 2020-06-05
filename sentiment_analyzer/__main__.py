import boto3
import csv
import logging
import os
import pandas as pd

logger = logging.getLogger()


if __name__ == "__main__":
    tweets = []

    # Get local data
    if os.getenv('ENV') == 'dev':
        tweets = pd.read_csv(os.getenv('LOCAL_FILENAME'))
        print('Local read successful')

    # Get S3 data
    else:
        s3 = boto3.client('s3')
        bucket = os.getenv('BUCKET_NAME')
        key = os.getenv('BUCKET_KEY')
        obj = s3.get_object(Bucket=bucket, Key=key)
        tweets = pd.read_csv(obj['Body'])
        print('S3 read successful')

    # print(tweets)

    # TF-IDF
    # Sentiment Analysis
    # Result