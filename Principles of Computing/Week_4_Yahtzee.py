"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level

Copy to codeskulptor.com and run.
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def check_occurance(hold, hand):
    '''
    Helper function
    Check if occurances of each number match
    '''
    success = 0
    for num in hold:
        if hold.count(num) <= hand.count(num):
            success += 1
    if success == len(hold):
        return True
    
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    if len(hand) == 0:
        return 0
    num_scores = []
    for num in hand:
        temp = [outcome for dummy_index, outcome in enumerate(hand) if outcome == num]
        num_scores.append(sum(temp))
    return max(num_scores)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.
,
    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    rolls = gen_all_sequences([side + 1 for side in range(num_die_sides)], num_free_dice)
    expected = 0
    for roll in rolls:
        roll_score = score(held_dice + roll)
        expected += roll_score / (float(num_die_sides) ** num_free_dice)
    return expected

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = []
    for length in range(len(hand) + 1):
        all_holds += gen_all_sequences(hand, length)
    ans = []
    for hold in all_holds:
        if check_occurance(hold, hand):
            hold = list(hold)
            hold.sort()
            hold = tuple(hold)
            if hold not in ans:
                ans.append(hold)
    return set(ans)

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    expected = []
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        expected.append(expected_value(hold, num_die_sides, num_free_dice))
    expected_score = float(max(expected))
    to_hold = list(all_holds)[expected.index(expected_score)]
    return (expected_score, to_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



