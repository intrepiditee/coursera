"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game

Copy to codeskulptor.com and run.
"""

import random
import codeskulptor
codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10000

def evaluate_position(num_items):
    '''
    Monte Carlo evalation method for Nim
    '''
    win_fraction = []
    for initial_move in range(1, MAX_REMOVE + 1):
        win = 0
        for dummy_trial in range(TRIALS):
            total = 0
            total += initial_move
            is_win = 1
            while num_items > total:
                total += random.randint(1, 3)
                is_win += 1
                #print 'Total =', total
            if is_win % 2 != 0:
                win += 1
        #print 'Wins =', win
        win_fraction.append(float(win) / TRIALS)
    print win_fraction
    return win_fraction.index(max(win_fraction)) + 1


def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """
    
    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

play_game(10)
#print evaluate_position(10)
       
    
                 
    