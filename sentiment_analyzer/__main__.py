import boto3
import csv
import logging
import os
import pandas as pd
import spacy

import nltk
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

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

if __name__ == "__main__":
    # run_downloads()
    tweets = list()

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

    # Tokenization
    positive_tokens = twitter_samples.tokenized('positive_tweets.json')

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    foo = lemmatize_sentence(positive_tokens[0])
    print(positive_tokens[0])
    print(foo)



    # TF-IDF
    # Sentiment Analysis
    # Result
