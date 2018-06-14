# reviews.py
#
# parse text files and calculate the probabilities for
# each dictionary word given the review polarity
#
# Author: Anthony Shackell - June 8, 2018

import os, operator, random
from os.path import isfile, join

SEARCH_WORDS = ['awful', 'bad', 'boring', 'dull', 'effective', 'enjoyable', 'great', 'hilarious']

POSITIVE_REVIEW_DIRECTORY = '/Users/ashackell/git/CSC421/ass2/review_polarity/txt_sentoken/pos'
NEGATIVE_REVIEW_DIRECTORY = '/Users/ashackell/git/CSC421/ass2/review_polarity/txt_sentoken/neg'

num_pos_files = 0
num_neg_files = 0


def bernoulli_classifier(feature_vector, class_probability):
    product = 1.0
    for x in range(len(feature_vector)):
        product *= (class_probability[x]**(feature_vector[x])) * ((1-class_probability[x])**(1-feature_vector[x]))
    return product


def build_probabilities(pos_file_list = [], neg_file_list = [], probability_vector_positive = [], probability_vector_negative = []):

    global num_pos_files, num_neg_files, POSITIVE_REVIEW_DIRECTORY, NEGATIVE_REVIEW_DIRECTORY, SEARCH_WORDS

    # read positive reviews
    for filename in pos_file_list:
        local_probability_vector_positive = [0.0 for x in range(8)]
        # skip directories
        if not isfile(filename):
            continue
        file = open(filename, 'r')
        content = file.read()
        for word in content.split():
            if word.lower() in SEARCH_WORDS:
                local_probability_vector_positive[SEARCH_WORDS.index(word)] = 1
        num_pos_files += 1
        file.close()
        probability_vector_positive[:] = list(map(operator.add, probability_vector_positive, local_probability_vector_positive))


    # read negative reviews
    for filename in neg_file_list:
        local_probability_vector_negative = [0.0 for x in range(8)]
        # skip directories
        if not isfile(filename):
            continue
        file = open(filename, 'r')
        content = file.read()
        for word in content.split():
            if word.lower() in SEARCH_WORDS:
                local_probability_vector_negative[SEARCH_WORDS.index(word)] = 1
        num_neg_files += 1
        file.close()
        probability_vector_negative[:] = list(map(operator.add, probability_vector_negative, local_probability_vector_negative))


    probability_vector_positive[:] = [ x / num_pos_files for x in probability_vector_positive]
    probability_vector_negative[:] = [ x / num_neg_files for x in probability_vector_negative]


def validate(pos_file_list = [], neg_file_list = [], probability_vector_positive = [], probability_vector_negative = []):

    global POSITIVE_REVIEW_DIRECTORY, NEGATIVE_REVIEW_DIRECTORY, SEARCH_WORDS
    feature_vector = [0.0 for x in range(8)]

    positive_decisions_pos = 0
    negative_decisions_pos = 0
    positive_decisions_neg = 0
    negative_decisions_neg = 0

    for filename in pos_file_list:
        feature_vector = [0.0 for x in range(8)]
        # skip directories
        if not isfile(filename):
            continue
        file = open(filename, 'r')
        content = file.read()
        for word in content.split():
            if word.lower() in SEARCH_WORDS:
                feature_vector[SEARCH_WORDS.index(word)] = 1

        prob_neg = bernoulli_classifier(feature_vector, probability_vector_negative)
        prob_pos = bernoulli_classifier(feature_vector, probability_vector_positive)

        file.close()

        if prob_neg > prob_pos:
            negative_decisions_pos += 1
        else:
            positive_decisions_pos += 1


    for filename in neg_file_list:
        feature_vector = [0.0 for x in range(8)]
        # skip directories
        if not isfile(filename):
            continue
        file = open(filename, 'r')
        content = file.read()
        for word in content.split():
            if word.lower() in SEARCH_WORDS:
                feature_vector[SEARCH_WORDS.index(word)] = 1

        prob_neg = bernoulli_classifier(feature_vector, probability_vector_negative)
        prob_pos = bernoulli_classifier(feature_vector, probability_vector_positive)

        file.close()

        if prob_neg > prob_pos:
            negative_decisions_neg += 1
        else:
            positive_decisions_neg += 1

    return positive_decisions_pos, negative_decisions_pos, positive_decisions_neg, negative_decisions_neg


def generate_random_review(probability_vector):
    words_included = []
    for feature in range(len(probability_vector)):
        included = random.uniform(0.0, 1.0)
        if included <= probability_vector[feature]:
            words_included.append(SEARCH_WORDS[feature])
    print words_included


def main():

    positive_reviews = [ join(POSITIVE_REVIEW_DIRECTORY, filename) for filename in os.listdir(POSITIVE_REVIEW_DIRECTORY) ]
    negative_reviews = [ join(NEGATIVE_REVIEW_DIRECTORY, filename) for filename in os.listdir(NEGATIVE_REVIEW_DIRECTORY) ]

    print "*** WHOLE-SET VALIDATION ***"
    print
    whole_set_probability_vector_positive = [0.0 for x in range(8)]
    whole_set_probability_vector_negative = [0.0 for x in range(8)]

    build_probabilities(positive_reviews, negative_reviews, whole_set_probability_vector_positive, whole_set_probability_vector_negative)

    print "- POSITIVE REVIEW WORD PROBABILITIES -"
    for x in range(8):
        print "Probability of word", SEARCH_WORDS[x], ":", whole_set_probability_vector_positive[x]

    print

    print "- NEGATIVE REVIEW WORD PROBABILITIES -"
    for x in range(8):
        print "Probability of word", SEARCH_WORDS[x], ":", whole_set_probability_vector_negative[x]

    print

    pos_pos, pos_neg, neg_neg, neg_pos = validate(positive_reviews, negative_reviews, whole_set_probability_vector_positive, whole_set_probability_vector_negative)

    print "positive decisions from pos reviews:",  pos_pos/1000.0*100, "%\nnegative decisions from pos reviews:", pos_neg/1000.0*100, "%\npositive decisions from neg reviews:", neg_neg/1000.0*100, "%\nnegative decisions from neg reviews:", neg_pos/1000.0*100, "%"

    print

    print "*** K-FOLD VALIDATION ***"

    fold_results_pos_pos = []
    fold_results_pos_neg = []
    fold_results_neg_neg = []
    fold_results_neg_pos = []

    for x in range(10):
        k_fold_probability_vector_positive = [0.0 for x in range(8)]
        k_fold_probability_vector_negative = [0.0 for x in range(8)]

        start_index = x*100
        classification_files_positive = positive_reviews[start_index:(start_index+100)]
        classification_files_negative = negative_reviews[start_index:(start_index+100)]

        training_files_positive = [ filename for filename in positive_reviews if filename not in classification_files_positive ]
        training_files_negative = [ filename for filename in negative_reviews if filename not in classification_files_negative ]

        build_probabilities(training_files_positive, training_files_negative, k_fold_probability_vector_positive, k_fold_probability_vector_negative)

        pos_pos, pos_neg, neg_neg, neg_pos = validate(classification_files_positive, classification_files_negative, k_fold_probability_vector_positive, k_fold_probability_vector_negative)

        fold_results_pos_pos.append(pos_pos/100.0*100)
        fold_results_pos_neg.append(pos_neg/100.0*100)
        fold_results_neg_neg.append(neg_neg/100.0*100)
        fold_results_neg_pos.append(neg_pos/100.0*100)

    # average results
    average_pos_pos = sum(fold_results_pos_pos)/10.0
    average_pos_neg = sum(fold_results_pos_neg)/10.0
    average_neg_neg = sum(fold_results_neg_neg)/10.0
    average_neg_pos = sum(fold_results_neg_pos)/10.0

    print "positive decisions from pos reviews:",  average_pos_pos, "%\nnegative decisions from pos reviews:", average_pos_neg, "%\npositive decisions from neg reviews:", average_neg_neg, "%\nnegative decisions from neg reviews:", average_neg_pos, "%"

    print "*** RANDOMLY GENERATED REVIEWS ***"
    print "- POSITIVE -"

    for x in range(5):
        generate_random_review(whole_set_probability_vector_positive)

    print "- NEGATIVE -"
    for x in range(5):
        generate_random_review(whole_set_probability_vector_negative)

if __name__ == '__main__':
    main()
