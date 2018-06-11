# reviews.py
#
# parse text files and calculate the probabilities for
# each dictionary word given the review polarity
#
# Author: Anthony Shackell - June 8, 2018

import os, operator
from os.path import isfile, join

SEARCH_WORDS = ['awful', 'bad', 'boring', 'dull', 'effective', 'enjoyable', 'great', 'hilarious']

POSITIVE_REVIEW_DIRECTORY = '/Users/ashackell/git/CSC421/ass2/review_polarity/txt_sentoken/pos'
NEGATIVE_REVIEW_DIRECTORY = '/Users/ashackell/git/CSC421/ass2/review_polarity/txt_sentoken/neg'

num_pos_files = 0
num_neg_files = 0

global_probability_vector_positive = [0.0 for x in range(8)]
global_probability_vector_negative = [0.0 for x in range(8)]

# read positive reviews
for filename in os.listdir(POSITIVE_REVIEW_DIRECTORY):
    local_probability_vector_positive = [0.0 for x in range(8)]
    # skip directories
    if not isfile(join(POSITIVE_REVIEW_DIRECTORY, filename)):
        continue
    file = open(join(POSITIVE_REVIEW_DIRECTORY, filename), 'r')
    content = file.read()
    for word in content.split():
        if word.lower() in SEARCH_WORDS:
            local_probability_vector_positive[SEARCH_WORDS.index(word)] = 1
    num_pos_files += 1
    file.close()
    global_probability_vector_positive = list(map(operator.add, global_probability_vector_positive, local_probability_vector_positive))


# read negative reviews
for filename in os.listdir(NEGATIVE_REVIEW_DIRECTORY):
    local_probability_vector_negative = [0.0 for x in range(8)]
    # skip directories
    if not isfile(join(NEGATIVE_REVIEW_DIRECTORY, filename)):
        continue
    file = open(join(NEGATIVE_REVIEW_DIRECTORY, filename), 'r')
    content = file.read()
    for word in content.split():
        if word.lower() in SEARCH_WORDS:
            local_probability_vector_negative[SEARCH_WORDS.index(word)] = 1
    num_neg_files += 1
    file.close()
    global_probability_vector_negative = list(map(operator.add, global_probability_vector_negative, local_probability_vector_negative))


global_probability_vector_positive[:] = [ x / num_pos_files for x in global_probability_vector_positive]
global_probability_vector_negative[:] = [ x / num_neg_files for x in global_probability_vector_negative]

print "*** POSITIVE REVIEW WORD PROBABILITIES ***"
for x in range(8):
    print "Probability of word", SEARCH_WORDS[x], ":", global_probability_vector_positive[x]

print

print "*** NEGATIVE REVIEW WORD PROBABILITIES ***"
for x in range(8):
    print "Probability of word", SEARCH_WORDS[x], ":", global_probability_vector_negative[x]
# print global_probability_vector_positive, global_probability_vector_negative
