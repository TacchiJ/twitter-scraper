import datetime
import re
import string

from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


class TweetCleaner:
    ''' Class for cleaning tweets.
    
    :param lang: sets the language (e.g. for stop words)
    '''

    def __init__(self, lang='english'):
        lang = lang.lower()
        self.stop_words = stopwords.words(lang)

    def tokenize(self, strings: list):
        '''Tokenizes provided strings

        :param strings: a list of strings to be tokenized
        :return: a list of lists of tokens
        '''
        #TODO:
        pass

    def remove_noise(self, all_tweet_tokens: list):
        '''Lemmatizes and removes stop words from a given list of tokens

        :param all_tweet_tokens: a list of lists of tokens to be cleaned
        :return: a list of lists of cleaned tokens
        '''
        all_cleaned_tokens = []

        for tweet_tokens in all_tweet_tokens:
            cleaned_tokens = []

            for token, tag in pos_tag(tweet_tokens):
                token = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|"\
                               "(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', token)
                token = re.sub("(@[A-Za-z0-9_]+)", '', token)

                if tag.startswith("NN"):
                    pos = 'n'
                elif tag.startswith('VB'):
                    pos = 'v'
                else:
                    pos = 'a'

                lemmatizer = WordNetLemmatizer()
                token = lemmatizer.lemmatize(token, pos)

                if len(token) > 0 and token not in string.punctuation and token.lower() not in self.stop_words:
                    cleaned_tokens.append(token.lower())
            all_cleaned_tokens.append(cleaned_tokens)

        now = datetime.datetime.now().time()
        print(f"{now}: Removed noise from tokens (lemm + stop words)")
        return all_cleaned_tokens

    def get_frequency_distribution(self, tokens):
        '''Returns the frequency distribution of provided tokens'''
        words = self.get_all_words(tokens)
        return FreqDist(words)

    def get_all_words(self, cleaned_tokens: list):
        '''Returns a generator for the provided tokens'''
        for tokens in cleaned_tokens:
            for token in tokens:
                yield token

    def get_dataset_from_tokens(self, cleaned_tokens: list, tag: str):
        '''Transforms a list of tokens into required format for NLTK
        
        :param cleaned_tokens: a list of lists of cleaned tokens
        :param tag: group that the token belong to
        :return: list of bag of words and tag pairs 
        '''
        dataset = []
        for tweet_tokens in cleaned_tokens:
            bag_of_tokens = {token: True for token in tweet_tokens}
            dataset.append((bag_of_tokens, tag))
        return dataset
