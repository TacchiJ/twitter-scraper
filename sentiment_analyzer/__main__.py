import boto3
import csv
import logging
import nltk
import os
import pandas as pd
import random
import re
import string

from nltk import FreqDist
from nltk import classify
from nltk import NaiveBayesClassifier
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

def get_all_words(cleaned_tokens: list):
    for tokens in cleaned_tokens:
        for token in tokens:
            yield token

def get_dataset_from_tokens(cleaned_tokens: list, tag: str):
    dataset = []
    for tweet_tokens in cleaned_tokens:
        bag_of_tokens = {token: True for token in tweet_tokens}
        dataset.append((bag_of_tokens, tag))
    return dataset


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

    # Get tokenized training data
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    # Remove noise (normalize + stop word removal)
    stop_words = stopwords.words('english')
    positive_cleaned_tokens = remove_noise(positive_tweet_tokens, stop_words)
    negative_cleaned_tokens = remove_noise(negative_tweet_tokens, stop_words)

    # Word frequency distributions
    all_positive_words = get_all_words(positive_cleaned_tokens)
    all_negative_words = get_all_words(negative_cleaned_tokens)
    positive_freq_dist = FreqDist(all_positive_words)
    negative_freq_dist = FreqDist(all_negative_words)

    # Convert data to NLTK-required format
    positive_dataset = get_dataset_from_tokens(positive_cleaned_tokens, "Positive")
    negative_dataset = get_dataset_from_tokens(negative_cleaned_tokens, "Negative")
    dataset = positive_dataset + negative_dataset

    # Split data
    split_ratio = 0.7
    split = int(len(dataset) * split_ratio)
    
    random.shuffle(dataset)
    train_data = dataset[slice(0, split)]
    test_data = dataset[slice(split, len(dataset))]

    print(len(dataset))
    print(len(train_data))
    print(len(test_data))

    # Build model
    classifier = NaiveBayesClassifier.train(train_data)
    print(f"Accuracy is: {classify.accuracy(classifier, test_data)}")
    print(classifier.show_most_informative_features(10))




    # TF-IDF
    # Sentiment Analysis
    # Result
