# naivebayes.py
#
# Compute the classification accuracy of Naive Bayes Bernoulli and Multinomial
# classifiers using scikit-learn.
#
# Author: Anthony Shackell - June 15, 2018

import os, numpy
from os.path import isfile, join
from sklearn.model_selection import KFold, cross_val_score
from sklearn import svm
from sklearn.naive_bayes import BernoulliNB, MultinomialNB

SEARCH_WORDS = ['awful', 'bad', 'boring', 'dull', 'effective', 'enjoyable', 'great', 'hilarious']

POSITIVE_REVIEW_DIRECTORY = '/Users/ashackell/git/CSC421/ass2/review_polarity/txt_sentoken/pos'
NEGATIVE_REVIEW_DIRECTORY = '/Users/ashackell/git/CSC421/ass2/review_polarity/txt_sentoken/neg'

NUM_FOLDS = 10

POSITIVE_DATA = []
NEGATIVE_DATA = []

def build_vectors(pos_file_list = [], neg_file_list = []):

    global SEARCH_WORDS, POSITIVE_DATA, NEGATIVE_DATA

    for filename in pos_file_list:
        feature_vector = [0.0 for x in range(len(SEARCH_WORDS))]
        # skip directories
        if not isfile(filename):
            continue
        file = open(filename, 'r')
        content = file.read()
        for word in content.split():
            if word.lower() in SEARCH_WORDS:
                feature_vector[SEARCH_WORDS.index(word)] += 1

        file.close()
        POSITIVE_DATA.append(feature_vector)

    for filename in neg_file_list:
        feature_vector = [0.0 for x in range(len(SEARCH_WORDS))]
        # skip directories
        if not isfile(filename):
            continue
        file = open(filename, 'r')
        content = file.read()
        for word in content.split():
            if word.lower() in SEARCH_WORDS:
                feature_vector[SEARCH_WORDS.index(word)] += 1

        file.close()
        NEGATIVE_DATA.append(feature_vector)


def main():
    positive_reviews = [ join(POSITIVE_REVIEW_DIRECTORY, filename) for filename in os.listdir(POSITIVE_REVIEW_DIRECTORY) ]
    negative_reviews = [ join(NEGATIVE_REVIEW_DIRECTORY, filename) for filename in os.listdir(NEGATIVE_REVIEW_DIRECTORY) ]
    bernoulli = BernoulliNB()
    multinomial = MultinomialNB()

    build_vectors(positive_reviews, negative_reviews)

    # use numpy to allow arrays to be indexed by other arrays
    multinomial_X_reviews = numpy.array(POSITIVE_DATA + NEGATIVE_DATA)

    # Binarize the feature vectors
    binary_X_reviews = []
    for review in multinomial_X_reviews:
        binary_review = []
        for feature in review:
            if feature == 0.0:
                binary_review.append(0.0)
            else:
                binary_review.append(1.0)
        binary_X_reviews.append(binary_review)

    binary_X_reviews = numpy.array(binary_X_reviews)

    y_reviews = numpy.asarray([ 1 for review in POSITIVE_DATA ] + [ 0 for review in NEGATIVE_DATA ])

    k_fold = KFold(n_splits=NUM_FOLDS)

    bernoulli_k_fold_scores = [bernoulli.fit(binary_X_reviews[train], y_reviews[train]).score(binary_X_reviews[test], y_reviews[test]) for train, test in k_fold.split(binary_X_reviews)]
    multinomial_k_fold_scores = [multinomial.fit(multinomial_X_reviews[train], y_reviews[train]).score(multinomial_X_reviews[test], y_reviews[test]) for train, test in k_fold.split(multinomial_X_reviews)]

    # alternative, less manual method
    # k_fold_scores cross_val_score(svc, X_reviews, y_reviews, cv=k_fold, n_jobs=-1)

    print "bernoulli_k_fold_scores:", bernoulli_k_fold_scores
    print "Bernoulli average accuracy:", '%.1f'%(sum(bernoulli_k_fold_scores)/NUM_FOLDS*100), "%"

    print "multinomial_k_fold_scores:", multinomial_k_fold_scores
    print "Multinomial average accuracy:", '%.1f'%(sum(multinomial_k_fold_scores)/NUM_FOLDS*100), "%"


if __name__ == '__main__':
    main()
