from copy import deepcopy
import pygame
from checkers.board import Board

RED = (255, 0, 0)
WHITE = (255, 255, 255)

#beta is for the RED level and alpha is for the WHITE level
# position is the current board , max_player is a bool . True for white and False for red
def minimax(position, depth, max_player, game, alpha, beta) :#alpha is the worst evaluate for white and beta is the worst for red
    if max_player :
        turn = WHITE
    else :
        turn = RED

    if depth == 0 or position.winner(turn) != None :
        return position.evaluate(), position
    
    if max_player : 
        maxEval = float('-inf')
        best_move = None
        
        for move in get_all_moves(position, WHITE, game) :
            evaluation = minimax(move, depth - 1, False, game, alpha, beta)[0] 
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation :
               best_move = move
           
            alpha = max(alpha, maxEval)
            
            if alpha >= beta :
                break

        return maxEval, best_move

    else :
        minEval = float('inf')
        best_move = None
        
        for move in get_all_moves(position, RED, game) :
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            
            if minEval == evaluation :
                best_move = move

            
           
            beta = min(minEval, beta)
            
            if beta <= alpha :
                break

        return minEval, best_move


def simulate_move(piece, move, board, game, skip) :
    board.move(piece, move[0], move[1])

    if skip :
        board.remove(skip)
    
    
    return board



def get_all_moves(board, color, game) :
    moves = [] #this is a list of all moves of all the pieces of color on the board
    
    for piece in board.get_all_pieces(color) :
        valid_moves = board.get_valid_moves(piece)
        
        for move, skip in valid_moves.items() :
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

"""def draw_moves(game, board, piece): #showcasing the algorithm of AI
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)"""