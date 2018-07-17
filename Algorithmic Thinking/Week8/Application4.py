'''
ALgorithimic Thinking Application 4.
'''

"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
from collections import defaultdict

if DESKTOP:
    import matplotlib.pyplot as plt
    import alg_project4_solution as student
    import numpy as np
    import string
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

def question_1():
    '''
    Answer for Question 1.
    '''
    alignment_matrix = student.compute_alignment_matrix(HUMAN_EYELESS, FRUITFLY_EYELESS, EYELESS_SCORING_MATRIX, False)
    ans = student.compute_local_alignment(HUMAN_EYELESS, FRUITFLY_EYELESS, EYELESS_SCORING_MATRIX, alignment_matrix)
    
    print '-------------------------------------------'
    print 'Question 1'
    print 'Score:', ans[0] # 875
    print 'Human alignment:', ans[1] # HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ
    print 'Fruitfly alignment:', ans[2] # HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ
    return ans

def question_2():
    '''
    Answer for Question 2.
    '''
    human = ''
    fruitfly = ''

    human_local = QUESTION_1[1]
    fruitfly_local = QUESTION_1[2]

    for char in human_local:
        if char != '-':
            human += char

    for char in fruitfly_local:
        if char != '-':
            fruitfly += char

    human_alignment_matrix = student.compute_alignment_matrix(human, CONSENSUS_PAX, EYELESS_SCORING_MATRIX, True)
    human_ans = student.compute_global_alignment(human, CONSENSUS_PAX, EYELESS_SCORING_MATRIX, human_alignment_matrix)

    human_percentage = 0.0
    human_alignment = human_ans[1]
    human_consensus_alignment = human_ans[2]
    for index in range(len(human_alignment)):
        if human_alignment[index] == human_consensus_alignment[index]:
            human_percentage += 1
    human_percentage /= len(human_alignment)

    # print 'human'
    # print len(human_alignment)
    # print len(human_alignment) * human_percentage
    
    fruitfly_alignment_matrix = student.compute_alignment_matrix(fruitfly, CONSENSUS_PAX, EYELESS_SCORING_MATRIX, True)
    fruitfly_ans = student.compute_global_alignment(fruitfly, CONSENSUS_PAX, EYELESS_SCORING_MATRIX, fruitfly_alignment_matrix)

    fruitfly_percentage = 0.0
    fruitfly_alignment = fruitfly_ans[1]
    fruitfly_consensus_alignment = fruitfly_ans[2]
    for index in range(len(fruitfly_alignment)):
        if fruitfly_alignment[index] == fruitfly_consensus_alignment[index]:
            fruitfly_percentage += 1
    fruitfly_percentage /= len(fruitfly_alignment)
    
    # print 'fruitfly'
    # print len(fruitfly_alignment)
    # print len(fruitfly_alignment) * fruitfly_percentage

    print '-------------------------------------------'
    print 'Question 2'
    print 'Human percentage:', human_percentage # 0.729323308271
    print 'Fruitfly percentage:', fruitfly_percentage # 0.701492537313

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    '''
    Question 4.

    Takes two eyeless strings, a scoring matrix, and an integer number of trials.
    Returns a dictionary.
    '''
    scoring_distribution = defaultdict(int)

    count = 0
    for dummy in range(num_trials):
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        rand_y = ''.join(rand_y)
        alignment_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)[0]
        scoring_distribution[score] += 1
        count += 1
        print count
    return scoring_distribution

def question_4():
    '''
    Answer for Question 4.
    '''

    print '-------------------------------------------'
    print 'Question 4'
    print 'Plot as shown.'

    x_values = []
    y_values = []
    total_frequency = float(sum(NULL_DISTRIBUTION.values()))

    for score, frequency in NULL_DISTRIBUTION.items():
        x_values.append(score)
        y_values.append(frequency / total_frequency)

    plt.title('Normalized null distribution with 1000 trials')
    plt.xlabel('Score')
    plt.ylabel('Fraction of total trials')
    plt.bar(x_values, y_values,align='center')
    plt.show()

def question_5():
    '''
    Answer for Question 5.
    '''
    scores = []

    for score, frequency in NULL_DISTRIBUTION.items():
        for dummy in range(frequency):
            scores.append(score)

    scores = np.array(scores)

    mean = np.mean(scores)
    std = np.std(scores, ddof = 0)
    z_score = (875 - mean) / std

    print '-------------------------------------------'
    print 'Question 5'
    print 'Mean:', mean # 51.177
    print 'Standard deviation:', std # 6.65745229048
    print 'Z-score:', z_score # 123.744484234


def compute_edit_distance(word1, word2):
    '''
    Takes two strings.
    Returns the edit distance between the two words.
    '''
    alphabet = set(string.lowercase)
    diag_score = 2
    off_diag_score = 1
    dash_score = 0

    scoring_matrix = student.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    alignment_matrix = student.compute_alignment_matrix(word1, word2, scoring_matrix, True)
    alignment = student.compute_global_alignment(word1, word2, scoring_matrix, alignment_matrix)
    
    edit_distance = len(word1) + len(word2) - alignment[0]

    return edit_distance


def check_spelling(checked_word, dist, word_list):
    '''
    Question 8.

    Takes a word to be checked, the with-in edit distance, and a list of words.
    Returns a set of words with the input distance from the input checked word.
    '''
    word_set = set()

    for word in word_list:
        if compute_edit_distance(checked_word, word) <= dist:
            word_set.add(word)

    return word_set


def question_8():
    '''
    Answer for question 8.
    '''
    print '-------------------------------------------'
    print 'Question 8'
    print 'Humble:', check_spelling('humble', 1, WORD_LIST) # set(['bumble', 'humbled', 'tumble', 'humble', 'rumble', 'humbler', 'humbles', 'fumble', 'humbly', 'jumble', 'mumble'])
    print 'Firefly:', check_spelling('firefly', 2, WORD_LIST) # set(['firefly', 'tiredly', 'freely', 'fireclay', 'direly', 'finely', 'firstly', 'liefly', 'fixedly', 'refly', 'firmly'])

HUMAN_EYELESS = read_protein(HUMAN_EYELESS_URL)
FRUITFLY_EYELESS = read_protein(FRUITFLY_EYELESS_URL)
EYELESS_SCORING_MATRIX = read_scoring_matrix(PAM50_URL)
CONSENSUS_PAX = read_protein(CONSENSUS_PAX_URL)
WORD_LIST = read_words(WORD_LIST_URL)


# Question 1

# QUESTION_1 = question_1()

# Question 2

# question_2()

# Question 3

# # No. The numbers of elements that match for human vs consensus and fruitfly vs consensus
# follow binomial distributions, human vs consensus with n = 133, p = 0.0.0434,
# fruitfly vs consensus with n = 134, p = 0.0434. P(number of elements that match = 97)
# approximately equals 0 for human vs consensus, and P(number of elements that match = 94)
# approximately equals 0 for fruitfly vs consensus. It is extremely unlikely that
# the percentages of elements that match are due to chance.

# Question 4

NULL_DISTRIBUTION = {37: 1, 38: 1, 39: 2, 40: 7, 41: 9, 42: 23, 43: 33, 44: 53, 45: 55,
                     46: 71, 47: 74, 48: 72, 49: 73, 50: 68, 51: 67, 52: 38, 53: 45,
                     54: 49, 55: 43, 56: 33, 57: 25, 58: 31, 59: 25, 60: 11, 61: 10,
                     62: 11, 63: 8, 64: 11, 65: 9, 66: 6, 67: 10, 68: 8, 69: 2, 70: 2,
                     71: 1, 72: 5, 73: 3, 74: 1, 76: 2, 78: 1, 84: 1}

# question_4()

# Question 5

# question_5()

# Question 6

# No, not due to chance. Winning the jackpot in an extremely large lottery is more likely.
# For a normal random variable, P(Z = 123.74) approximately equals 0.

# Question 7

# diag_score = 2
# off_diag_score = 1
# dash_score = 0

# Question 8

# question_8()


