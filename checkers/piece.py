import pygame
from .constants import *

pygame.font.init()
FONT = pygame.font.SysFont('arial', 30)

king = 'KING'
king_text = FONT.render(king, 1, BLACK)

class Piece :
    PADDING = 15
    OUTLINE = 2
    def __init__(self, row, col, color) :
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        if self.color == RED :
            self.direction = -1
        else :
            self.direction = 1

        self.x = 0
        self.y = 0
        self.calc_pos()
    def calc_pos(self) :
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE//2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE//2
    
    def make_king(self) :
        self.king = True

    def draw_piece(self , win) :
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y) , radius + self.OUTLINE )
        pygame.draw.circle(win, self.color, (self.x, self.y) , radius)
        if self.king :
            win.blit(king_text, (self.x - king_text.get_width() // 2 , self.y - king_text.get_height() // 2))
            
        
    def move(self, row, col) : #this will reset the position of the piece to the position after moving so we can draw it in that position 
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self): # the internal representation of our object , it has to be a string 
        return str(self.color)