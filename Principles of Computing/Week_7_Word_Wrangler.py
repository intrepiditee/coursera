"""
Student code for Word Wrangler game

Copy to codeskulptor.com and run.
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    ans = []
    for elem in list1:
        if elem not in ans:
            ans.append(elem)
    return ans

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    ans = [elem for elem in list1 if elem in list2]
    return ans

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    ans = []
    length1 = len(list1)
    length2 = len(list2)
    index1 = 0
    index2 = 0
    while length1 != 0:
        if list1[index1] >= list2[index2]:
            ans.append(list2[index2])
            length2 -= 1
            index2 += 1
            if length2 == 0:
                break
        else:
            ans.append(list1[index1])
            length1 -= 1
            index1 += 1
    if length1 == 0:
        ans += list2[index2:]
    elif length2 == 0:
        ans += list1[index1:]
    return ans

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        first_half = merge_sort(list1[:len(list1) // 2])
        second_half = merge_sort(list1[len(list1) // 2:])
        return merge(first_half, second_half)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return ['']
    else:
        first = word[:1]
        ans = []
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        for string in rest_strings:
            for index in range(len(string) + 1):
                ans.append(string[:index] + first + string[index:])
        ans += rest_strings
        return ans

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_dict = urllib2.urlopen('http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt')
    return word_dict.read()

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()