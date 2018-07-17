"""
Mini-max Tic-Tac-Toe Player

Copy to codeskulptor.com and run.
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() == provided.DRAW:
        return SCORES[provided.DRAW], (-1, -1)
    elif board.check_win() != player:
        if player == provided.PLAYERX and board.check_win() != None:
            return SCORES[provided.PLAYERO], (-1, -1)
        elif player == provided.PLAYERO and board.check_win() != None:
            return SCORES[provided.PLAYERX], (-1, -1)
        else:
            empty_squares = board.get_empty_squares()
            scores = []
            moves = []
            for square in empty_squares:
                new_board = board.clone()
                new_board.move(square[0], square[1], player)
                if player == provided.PLAYERX:
                    result = mm_move(new_board, provided.PLAYERO)[0]
                    if result == SCORES[provided.PLAYERX]:
                        return SCORES[provided.PLAYERX], square
                else:
                    result = mm_move(new_board, provided.PLAYERX)[0]
                    if result == SCORES[provided.PLAYERO]:
                        return SCORES[provided.PLAYERO], square
                scores.append(result)
                moves.append(square)
            position_score = 0
            to_move = None
            if player == provided.PLAYERX:
                position_score = max(scores)
                to_move = moves[scores.index(position_score)]
            else:
                position_score = min(scores)
                to_move = moves[scores.index(position_score)]
            return position_score, to_move
#a = provided.TTTBoard(3, False, [[3, 1, 1], [1, 1, 1], [1, 1, 2]])
#print mm_move(a, provided.PLAYERX)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)



'''
Too many return statements but working version

"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if player == provided.PLAYERX:
        if board.check_win() == provided.PLAYERO:
            return -1, (-1, -1)
        elif board.check_win() == provided.DRAW:
            return 0, (-1, -1)
        else:
            empty_squares = board.get_empty_squares()
            scores = []
            moves = []
            for square in empty_squares:
                new_board = board.clone()
                new_board.move(square[0], square[1], player)
                result = mm_move(new_board, provided.PLAYERO)[0]
                if  result == 1:
                    return 1, square
                scores.append(result)
                moves.append(square)
            max_score = max(scores)
            to_move = moves[scores.index(max_score)]
            return max_score, to_move
    elif player == provided.PLAYERO:
        if board.check_win() == provided.PLAYERX:
            return 1, (-1, -1)
        elif board.check_win() == provided.DRAW:
            return 0, (-1, -1)
        else:
            empty_squares = board.get_empty_squares()
            scores = []
            moves = []
            for square in empty_squares:
                new_board = board.clone()
                new_board.move(square[0], square[1], player)
                result = mm_move(new_board, provided.PLAYERX)[0]
                if result == -1:
                    return -1, square
                scores.append(result)
                moves.append(square)
            min_score = min(scores)
            to_move = moves[scores.index(min_score)]
            return min_score, to_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
'''
