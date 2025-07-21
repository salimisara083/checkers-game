import pygame
from checkers.constants import *
from checkers.piece import Piece
from checkers.game import Game
from minimax.pruning_algorithm import minimax
FPS = 60    

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Checkers')

def red_move(game, event) :
    if event.type == pygame.MOUSEBUTTONDOWN :
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        game.select(row, col)

def white_move(game) :
    value, new_board = minimax(game.get_board(), 5, WHITE, game, float('-inf'), float('inf'))
    game.ai_move(new_board)
            
def get_row_col_from_mouse(pos) :
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col

def main() :

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    
    while run :  #event loop 
        clock.tick(FPS)
       
        if game.turn == WHITE:
            white_move(game)
        
        
        if game.winner() != None :
            if game.winner == WHITE :
                white_move(game)
                game.change_turn()
            elif game.winner == RED :
                red_move(game, event)
                game.change_turn()
            game.final_page()
            pygame.time.delay(5000)
            run = False

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False

            red_move(game, event)


        game.update()

    pygame.quit()

main()