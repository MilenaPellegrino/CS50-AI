"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


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
    tot_X = 0
    tot_O = 0
    turn = X
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == X):
                tot_X +=1
            elif (board[i][j] == O):
                tot_O +=1 
    if(tot_X > tot_O):
        turn = O
    
    return turn
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range (len(board[i])):
            if(board[i][j] == EMPTY):
                possible_actions.add((i, j))
                
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # I check that it's within the limits 
    if((action[0] >2) or (action[0] <0) or (action[1] <0) or (action[1] >2)): 
        raise ValueError("Action Action outside the board limits.")
    
    aux_board = board
    poss_actions = actions(board)
    turn = player(board)
    if(action in poss_actions):
        aux_board[action[0]][action[1]] = turn
        return aux_board
    else: 
        raise ValueError("The cell is already busy")
        


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = None
    # Horizontally winner? 
    for i in range(len(board)):
        if((board[i][0] != EMPTY) and (board[i][0] == board[i][1]) and (board[i][1] == board[i][2]) ):
            winner = board[i][0]

    # Vertically winner? 
    for i in range(len(board)):
        if((board[0][i] != EMPTY) and (board[0][i] == board[1][i]) and (board[1][i] == board[2][i]) ):
            winner = board[0][i]
    
    # Diagonally winner? 
    values1 = [board[0][0], board[1][1], board[2][2]]
    values2 = [board[0][2], board[1][1], board[2][0]]
    
    if((values1[0] != EMPTY) and values1[0] == values1[1] and values1[1] ==  values1[2]):
        winner = values1[0]
    elif ((values2[0] != EMPTY) and values2[0] == values2[1] and values2[1] ==  values2[2]):
        winner = values2[0]
        
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    terminal =  True
    winners = winner(board)
    
    if(winners == None):
        terminal = False
        
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == EMPTY):
                terminal = False
    
    return terminal


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if (win == None):
        return 0
    elif (win == X):
        return 1
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board) == True):
        return None
    
    current_player = player(board)
    
    if(current_player == X):  # Maximizes x's victory 
        best_score = - math.inf
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            new_score = min_value(new_board)
            if (new_score > best_score):
                best_score = new_score
                best_move = action
        return best_move
    else: # Maximizes O's victory
        best_score = math.inf
        best_move = None
        for action in actions(board):
            new_board = result(board, action)
            new_score = max_value(new_board)
            if (new_score < best_score):
                best_score = new_score
                best_move = action
        return best_move
        
def max_value(board):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        new_board = result(board, action)
        value = max(value, min_value(new_board))
    return value

def min_value(board):
    if terminal(board):
        return utility(board)
    value = float('inf')
    for action in actions(board):
        new_board = result(board, action)
        value = min(value, max_value(new_board))
    return value