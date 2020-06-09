import boto3
import csv
import logging
import nltk
import os
import pandas as pd
import re
import string

from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag

logger = logging.getLogger()


def run_downloads():
    nltk.download('twitter_samples')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    print('Downloads successful')

def remove_noise(all_tweet_tokens: list, stop_words=()):
    all_cleaned_tokens = []

    for tweet_tokens in all_tweet_tokens:
        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        all_cleaned_tokens.append(cleaned_tokens)

    return all_cleaned_tokens

if __name__ == "__main__":
    # run_downloads()
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

    # Get training data
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')

    # Get tokenized training data
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    # Remove noise (normalize + stop word removal)
    stop_words = stopwords.words('english')
    positive_cleaned_tokens = remove_noise(positive_tweet_tokens, stop_words)
    negative_cleaned_tokens = remove_noise(negative_tweet_tokens, stop_words)


    print(positive_cleaned_tokens[:2])
    print()
    print(negative_cleaned_tokens[:2])



    # TF-IDF
    # Sentiment Analysis
    # Result
