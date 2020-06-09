import re
import string

from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


class TweetCleaner:

    def __init__(self, lang='english'):
        lang = lang.lower()
        self.stop_words = stopwords.words(lang)

    def tokenize(self, strings: list):
        pass

    def remove_noise(self, all_tweet_tokens: list):
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

        return all_cleaned_tokens