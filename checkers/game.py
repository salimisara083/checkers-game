import pygame
from .constants import *
from .board import Board

pygame.font.init()
FONT = pygame.font.SysFont('comicsans' , 60)



class Game:

    def __init__(self, win) :
        self.win = win
        self._init()
        
    def update(self) :
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self) : 
        self.selected = None
        self.board = Board()
        self.valid_moves =[]
        self.turn = RED
    
    def reset(self) :
        self._init()

    def select(self, row, col) : #its a recursive function selecting valid piece
        if self.selected:
            result = self._move(row, col)
            
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False
    
    def _move(self, row, col) : # its job is to check if the destination is a valid destianation if not return False
        destination_piece = self.board.get_piece(row, col)
        if self.selected and destination_piece == 0 and (row, col) in self.valid_moves :
            self.board.move(self.selected, row, col)
            
            skipped = self.valid_moves[(row, col)]
            if skipped :
                self.board.remove(skipped)
            self.change_turn()
            return True
        return False
    
    def change_turn(self) :
        self.valid_moves = {}
        if self.turn == RED :
            self.turn = WHITE
        else :
            self.turn = RED

    def draw_valid_moves(self, moves) :
        for move in moves :
            x, y = move
            pygame.draw.circle(self.win, BLUE, (y * SQUARE_SIZE + SQUARE_SIZE//2, x * SQUARE_SIZE + SQUARE_SIZE//2), 15)
            
    def remove_valid_moves(self) :
        self.valid_moves = {}

    def final_page(self) :
        self.update()
        pygame.time.delay(1000)
        WINNING_TEXT = f"WINNER : {self.winner()}"
        TEXT = FONT.render(WINNING_TEXT, 1, BLUE)
        x = (COLS * SQUARE_SIZE - TEXT.get_width())//2
        y = (ROWS * SQUARE_SIZE - TEXT.get_height())//2
        self.win.blit(TEXT, (x, y))
        pygame.display.update()

    def winner(self) :
        return self.board.winner(self.turn)

    
    def get_board(self) :
        return self.board

    def ai_move(self, board) :  # getting the new board object and changing the previouse board to new one
        self.board = board
        self.change_turn()  




















