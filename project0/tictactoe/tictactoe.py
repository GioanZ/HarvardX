"""
Tic Tac Toe Player
"""

from email.errors import ObsoleteHeaderDefect
import math
import my_extra_functions as fex
import random

X = "X"
O = "O"
EMPTY = None
DIM = 3

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    return fex.player(board)


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return fex.actions(board)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    return fex.result(board, action)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    return fex.winner(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    return fex.terminal(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return fex.utility(board)


def minimax(board):                     # if you wanted to use a chess other than 3x3 this function would have to be changed
    """
    Returns the optimal action for the current player on the board.
    """
    gamer = player(board)
    num = 0

    if terminal(board):
      return None

    if gamer == X:
        print('AI move: X')
        num = fex.number_of_move(board, X)
        if num == 1:
            best_action = fex.first_move_X(board)
            if best_action != None:
                return best_action
        elif num == 2:
            best_action = fex.second_move_X(board)
            if best_action != None:
                return best_action
        else:
            poss = fex.check_last(board)
            if poss != None:
                    return poss
            return fex.max_p(board)[1]

    elif gamer == O:
        print('AI move: O')
        num = fex.number_of_move(board, O)
        if num == 1:
            best_action = fex.first_move_O(board)
            if best_action != None:
                return best_action

        poss = fex.check_last(board)
        if poss != None:
            return poss

        return fex.min_p(board)[1]

    raise Exception("Not found palyer")

