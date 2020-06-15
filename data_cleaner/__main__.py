import datetime
import logging
import nltk
import os
import sys

from nltk.corpus import twitter_samples

sys.path.insert(1, '')
from data_cleaner.tweet_cleaner import TweetCleaner
from import_export import ImporterExporter

logger = logging.getLogger()


def run_downloads():
    nltk.download('twitter_samples')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    print('Downloads successful')


if __name__ == "__main__":
    # run_downloads()

    ## IMPORT DATA ##
    local = True if os.getenv('ENV') == 'dev' else False
    importer_exporter = ImporterExporter()
    tweets = importer_exporter.do_import(local)

    # Test data
    # Get training data
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    # Get tokenized training data
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    # Test data

    ## CLEANING ##
    cleaner = TweetCleaner('english')

    # Tokenization
    # TODO

    # Remove noise (normalize + stop word removal)
    positive_cleaned_tokens = cleaner.remove_noise(positive_tweet_tokens)
    negative_cleaned_tokens = cleaner.remove_noise(negative_tweet_tokens)

    # Word frequency distributions
    positive_freq_dist = cleaner.get_frequency_distribution(positive_cleaned_tokens)
    negative_freq_dist = cleaner.get_frequency_distribution(negative_cleaned_tokens)
    # print(positive_freq_dist.most_common(10))
    # print(negative_freq_dist.most_common(10))

    # Convert data to NLTK-required format
    positive_dataset = cleaner.get_dataset_from_tokens(positive_cleaned_tokens, "Positive")
    negative_dataset = cleaner.get_dataset_from_tokens(negative_cleaned_tokens, "Negative")
    dataset = positive_dataset + negative_dataset

    # TF-IDF

    # TODO export dataset
    now = datetime.datetime.now().time()
    header = ['foo', 'bar']
    importer_exporter.local_export(f"cleaned_data_{now}", header=header, data=dataset)