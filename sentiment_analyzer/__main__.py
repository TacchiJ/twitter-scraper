import boto3
import csv
import logging
import os
import pandas as pd

logger = logging.getLogger()


if __name__ == "__main__":
    tweets = []
    header = []

    # Get local data
    if os.getenv('ENV') == 'dev':
        with open(os.getenv('LOCAL_FILENAME'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)
            for row in reader:
                entry = {}
                for i in range(len(header)):
                    entry[header[i]] = row[i]
                tweets.append(entry)

    # Get S3 data
    else:
        s3 = boto3.resource('s3')
        bucket = os.getenv('BUCKET_NAME')
        key = os.getenv('BUCKET_KEY')
        obj = s3.get_object(Bucket=bucket, Key=key)

    tweet_data = pd.DataFrame(tweets, columns=header)
    print(tweet_data)

    # TF-IDF
    # Sentiment Analysis
    # Result