import random

from nltk import classify
from nltk import NaiveBayesClassifier


if __name__ == '__main__':

    dataset = 'foo'

    # TODO
    # Import cleaned datasets
    # Build model
    # Export model

    # In New File:
        # Import Model
        # Import recent Tweets
        # Make predicitons


    ### ANALYSIS ###
    # Split data
    split_ratio = 0.7
    split = int(len(dataset) * split_ratio)
    
    random.shuffle(dataset)
    train_data = dataset[slice(0, split)]
    test_data = dataset[slice(split, len(dataset))]

    # Build model
    classifier = NaiveBayesClassifier.train(train_data)
    print(f"Accuracy is: {classify.accuracy(classifier, test_data)}")
    print(classifier.show_most_informative_features(10))


    # Graphical Output