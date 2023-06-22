"""
Tic Tac Toe Player
"""

import math
import copy


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
    # find number of moves made on the board
    moves_made = 9 - sum([row.count(EMPTY) for row in board])
    
    # if number of moves made is even -> it is X turn and O turn otherwise
    if moves_made%2==0:
        return X
    return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    # possible acitons includes all empty cells on board
    for row, row_items in enumerate(board):
        for col, cell in enumerate(row_items):
            if cell == EMPTY:
                possible_actions.add((row, col))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    # check if action is legal
    possible_actions = actions(board)
    if action not in possible_actions:
        raise Exception("Illegal move")
    
    # create the result board from given move
    curr_player = player(board)
    i, j = action
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = curr_player
    
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # check each row of the board
    for row in board:
        # count number of moves each row and return the winner if no moves is 3
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O
        
    # check each column of the board
    for col in range(len(board[0])):
        # return winner if they have 3 moves in a column
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            return board[0][col]

    # check diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[1][1]
    
    # if no winner found, return None
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # game is over when there are no possible action or a winner is found
    return (len(actions(board)) == 0) or (winner(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: 
        return 1
    elif winner(board) == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # X wins when value is 1 -> X is max player and O is the min player
    if terminal(board):
        return None
    elif player(board) == X: 
        optimal_move, _ = max_player(board)
        return optimal_move
    else:
        optimal_move, _ = min_player(board)
        return optimal_move
    
    
def max_player(board, alpha=-math.inf, beta=math.inf):
    """
        Return tuple of (optimal action, optimal value) for max player
    """
    
    if terminal(board):
        return None, utility(board)
    
    optimal_move = None
    optimal_value = -math.inf
    
    # go through all possible moves:
    for move in actions(board):            
        # get moves that return min utility
        _, val = min_player(result(board, move), alpha=alpha, beta=beta)
        
        # update optimal value and move if a move with higher value is found
        if val > optimal_value:
            optimal_move = move
            optimal_value = val
            
        # update alpha value
        alpha = max(optimal_value, alpha)
        # if lower bound i.e. alpha is higher than beta -> prune
        if alpha > beta:
            break
        
    return optimal_move, optimal_value
        
        
def min_player(board, alpha=-math.inf, beta=math.inf):
    """
        Return tuple of (optimal action, optimal value) for min player
    """
    
    if terminal(board):
        return None, utility(board)
    
    optimal_move = None
    optimal_value = math.inf
    
    # go through all possible moves:
    for move in actions(board):
        # get moves that return min utility
        _, val = max_player(result(board, move), alpha=alpha, beta=beta)
        
        # update optimal value and move if a move with lower value is found
        if val < optimal_value:
            optimal_move = move
            optimal_value = val
            
        # update beta value
        beta = min(optimal_value, beta)
        # if lower bound i.e. alpha is higher than beta -> prune
        if alpha > beta:
            break
            
    return optimal_move, optimal_value