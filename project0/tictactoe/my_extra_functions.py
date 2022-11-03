# if you wanted to use a chess other than 3x3 this library would have to be changed

from copy import deepcopy
import random

X = "X"
O = "O"
EMPTY = None
DIM = 3
DDIMM = DIM - 1

best_first_moves = [(0,0),        (0,DDIMM),
                      (DDIMM,0),    (DDIMM,DDIMM)]

def player(board):
    count = 0

    for i in range(DIM):
        for j in range(DIM):
            count += 1 if board[i][j] == X else -1 if board[i][j] == O else 0

    return O if count == 1 else X

def actions(board):
    possibilities = set()

    for i in range(DIM):
        for j in range(DIM):
            if board[i][j] == EMPTY:
                possibilities.add((i,j))

    return possibilities


def result(board, action):
    if action not in actions(board):
        raise Exception("Action is not a valid action for the board")

    board2 = deepcopy(board)
    board2[action[0]][action[1]] = player(board)

    return board2

def winner(board):

    for i in range(DIM):                                    # ---
        if board[i][0] != EMPTY:                            
            for j in range(1, DIM):
                if board[i][j] != board[i][0]:
                    break
                elif j == DIM-1:
                    return board[i][0]

    for i in range(DIM):                                    # |||
        if board[0][i] != EMPTY:                            
            for j in range(1, DIM):
                if board[j][i] != board[0][i]:
                    break
                elif j == DIM-1:
                   return board[0][i]

    if board[0][0] != EMPTY:                                # \\\
        for i in range(1,DIM):                                    
            if board[i][i] != board[0][0]:
                break
            elif i == DIM-1:
                return board[0][0]

    if board[0][DIM-1] != EMPTY:                        # ///
        for i in range(DIM):
            if board[(DIM-1)-i][i] != board[0][DIM-1]:
                break
            elif (DIM-2)-i == 0:
                return board[DIM-1][DIM-1]

    """
    col = []
    num_l = 0
    diag_l = []
    diag_r = []

    for line in board:
        if line.count(X) == DIM:                # ---
            return X
        if line.count(O) == DIM:                # ---
            return O

        for j in range(DIM):
            if num_l == 0:
                col[j].append([])
            col[j].append(line[j])              # |||
            if j == num_l:
                diag_l.append(line[j])          # \\\
                diag_r.append(line[(DIM-1)-j])  # ///
        num_l += 1

    for i in range(DIM):
        if col[i].count(X) == DIM:              # ---
            return X
        if col[i].count(O) == DIM:              # ---
            return O

    if diag_l.count(X) == DIM:                  # \\\
            return X
    if diag_l.count(O) == DIM:                  # \\\
        return O

    if diag_r.count(X) == DIM:                  # ///
            return X
    if diag_r.count(O) == DIM:                  # ///
        return O
    """
    return None


def terminal(board):

    return False if (len(actions(board)) > 0 and winner(board) == None) else True

def utility(board):
    result = winner(board)

    return 1 if result == X else (-1 if result == O else 0)



def move_number(board, sign, move):
    count = 0

    for i in range(DIM):
        for j in range(DIM):
            if board[i][j] == sign:
                if count >= move:
                    return False
                else:
                    count += 1

    return True

def first_move_X(board):

    return random.choice(best_first_moves) if move_number(board, X, 1) == True else None

def number_of_move(board, sign):
    count = 0

    for i in range(DIM):
        for j in range(DIM):
            if board[i][j] == sign:
                count += 1

    return count + 1

def random_choise_only(tupla):
    list = []
    range = len(tupla) - 1

    for i in range(range):
        list.append(best_first_moves(tupla[i]))

    return random.choice(list)

def second_move_X(board):
    j = 0

    if not move_number(board, X, 2):
        return None

    for i in range(4):
        if board[best_first_moves[i][0]][best_first_moves[i][1]] == X:
            if board[1][1] == O:
                if i == 0:
                    j = 3
                elif i == 1:
                    j = 2
                elif i == 2:
                    j = 1
                elif i == 3:
                    j = 0
                else:
                    raise Exception("second_move_X 1")

                return (best_first_moves[j][0], best_first_moves[j][1])

            elif i == 0:    # °-
                if (board[0][0 + 1]) or (board[0 + 1][0]) == O:
                    return random_choise_only((1,2))
                else:
                    return random_choise_only((1,2,3))
            elif i == 3:    # -.
                if (board[DDIMM][DDIMM - 1]) or (board[DDIMM - 1][DDIMM]) == O:
                    return random_choise_only((1,2))
                else:
                    return random_choise_only((0,1,2))
            elif i == 1:    # -°
                if (board[0][DDIMM - 1]) or (board[0 + 1][DDIMM]) == O:
                    return random_choise_only((0,3))
                else:
                    return random_choise_only((0,2,3))
            elif i == 2:    # .-
                if (board[DDIMM][0 + 1]) or (board[DDIMM - 1][0]) == O:
                    return random_choise_only((0,3))
                else:
                    return random_choise_only((0,1,3))
    raise Exception("second_move_X 2")

def three_move_X(board):
    j = 0

    if not move_number(board, X, 3):
        return None

    raise Exception("second_move_X 3")

def first_move_O(board):

    if move_number(board, O, 1) == False:
        return None

    return (1,1) if board[1][1] == EMPTY else random.choice(best_first_moves) 

def check_last(board):

    for x in actions(board):
        board2 = result(board, x)
        win = utility(board2)
        if win != 0:
            if win != 0:
                return x

    for x in actions(board):
        board2 = result_opp(board, x)
        win = utility(board2)
        if win != 0:
            return x

    return None

def result_opp(board, action):
    if action not in actions(board):
        raise Exception("Action is not a valid action for the board")

    board2 = deepcopy(board)
    board2[action[0]][action[1]] = X if player(board) == O else X 

    return board2

def max_p(board, min_v = 10):
    
    v = -10
    best_poss = None
    possibilities = actions(board)

    if terminal(board):
        return (utility(board), None)

    while len(possibilities) > 0:
        poss = random.choice(tuple(possibilities))
        possibilities.remove(poss)
        
        if min_v <= v:
            break

        min_p_ = min_p(result(board, poss), v)
        if min_p_[0] > v:
            best_poss = poss
            v = min_p_[0]

    return (v, best_poss)

def min_p(board, best_max = -10):

    v = 10
    best_poss = None
    possibilities = actions(board)

    if terminal(board):
        return (utility(board), None)

    while len(possibilities) > 0:
        poss = random.choice(tuple(possibilities))
        possibilities.remove(poss)
        
        if best_max >= v:
            break
        
        max_p_ = max_p(result(board, poss), v)
        if max_p_[0] < v:
            best_poss = poss
            v = max_p_[0]

    return (v, best_poss)