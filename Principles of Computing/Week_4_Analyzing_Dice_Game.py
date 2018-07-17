"""
Analyzing a simple dice game
"""


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

# example for digits


def max_repeats(seq):
    """
    Compute the maxium number of times that an outcome is repeated
    in a sequence
    """
    times = [seq.count(outcome) for index, outcome in enumerate(seq)]
    return max(times)


def compute_expected_value(outcomes):
    """
    Function to compute expected value of simple dice game
    """
    two_repeat = 0
    three_repeat = 0
    seqs = gen_all_sequences(outcomes, 3)
    for seq in seqs:
        max_repeat = max_repeats(seq)
        if max_repeat == 2:
            two_repeat += 1
        elif max_repeat == 3:
            three_repeat += 1
    expected_val = (two_repeat * 10 + three_repeat * 200) / float(216)
    return expected_val


def run_test():
    """
    Testing code, note that the initial cost of playing the game
    has been subtracted
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
    print "All possible sequences of three dice are"
    print gen_all_sequences(outcomes, 3)
    print
    print "Test for max repeats"
    print "Max repeat for (3, 1, 2) is", max_repeats((3, 1, 2))
    print "Max repeat for (3, 3, 2) is", max_repeats((3, 3, 2))
    print "Max repeat for (3, 3, 3) is", max_repeats((3, 3, 3))
    print
    print "Ignoring the initial $10, the expected value was $", compute_expected_value(outcomes)
    
run_test()
