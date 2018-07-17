"""
Monte Carlo Tic-Tac-Toe Player

Copy to codeskulptor.com and run.
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 3.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    '''
    Simulate one complete game
    Both side chooses squares randomly
    '''
    while len(board.get_empty_squares()) != 0:
        move_square = random.choice(board.get_empty_squares())
        board.move(move_square[0], move_square[1], player)
        if board.check_win() != None:
            #print board
            break
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    '''
    Analyze a completed board and update scores accordingly
    '''
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                if board.check_win() == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.check_win() == provided.DRAW:
                    pass
                else:
                    scores[row][col] -= SCORE_CURRENT
            elif board.square(row, col) == provided.EMPTY:
                continue
            else:
                if board.check_win() == player:
                    scores[row][col] -= SCORE_OTHER
                elif board.check_win() == provided.DRAW:
                    pass
                else:
                    scores[row][col] += SCORE_OTHER
    #print scores        
    
def get_best_move(board, scores):
    '''
    Find empty squares with highest scores
    Then choose one of them randomly
    '''
    empty_squares = board.get_empty_squares()
    if len(empty_squares) == 0:
        pass
    else:
        square_scores = []
        for square in empty_squares:
            square_scores.append(scores[square[0]][square[1]])
        maximum_score = max(square_scores)
        maximum_squares = [empty_squares[square] for square, score in enumerate(square_scores) \
                        if score == maximum_score]
        to_move = random.choice(maximum_squares)
        return to_move
    

def mc_move(board, player, trials):
    '''
    machine playere makes a move
    '''
    scores = [[0 for dummy_num in range(board.get_dim())] for dummy_num in range(board.get_dim())]
    for dummy_num in range(trials): 
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    #print scores
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
#print 'PLAYERX =', provided.PLAYERX
#print 'PLAYERO =', provided.PLAYERO
#print 'DRAW =', provided.DRAW
#print 'EMPTY =', provided.EMPTY

#a = provided.TTTBoard(3)
#mc_trial(a, provided.PLAYERX)
#print a 
#scores = [[0 for dummy_num in range(a.get_dim())] for dummy_num in range(a.get_dim())]
#mc_update_scores(scores, a, provided.PLAYERX)
#print scores
#print mc_trial(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), 2)

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)