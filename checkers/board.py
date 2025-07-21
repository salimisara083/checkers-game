from .constants import  ROWS, COLS, BLUE, RED, WHITE,GREY, WIDTH, HEIGHT, SQUARE_SIZE, BLACK 
import pygame
from .piece import Piece

class Board:
    def __init__(self) :
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board() 
        
    def draw_squares(self,win) :
        win.fill(BLACK)
        for row in range(ROWS) :
            for col in range(row % 2 , COLS , 2) :
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE , SQUARE_SIZE, SQUARE_SIZE)  )

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def create_board(self) : #creating(initializing) all the pieces and putting them in the board list , so we can draw them later
        for row in range(ROWS) :
            self.board.append([])
            for col in range(COLS) :
                if col % 2 ==  ( row + 1 ) % 2 : 
                    if row < 3 :
                        self.board[row].append(Piece(row,col,WHITE))
                    elif row > 4 :
                        self.board[row].append(Piece(row,col,RED))
                    else : 
                        self.board[row].append(0)
                else :
                    self.board[row].append(0)
    
    def evaluate(self) :
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)
    
    def get_all_pieces(self, color) :
        pieces = []
        for row in self.board :
            for piece in row :
                if piece != 0 and piece.color == color :
                        pieces.append(piece)
        return pieces
    
    def move(self, piece, row, col):
       
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
 
        if row == ROWS - 1 or row == 0 :
            piece.make_king()
            if piece.color == WHITE :
                self.white_kings += 1
            else :
                self.red_kings += 1


    def draw(self, win) :
        self.draw_squares(win)
        for row in range(ROWS) :
            for col in range(COLS) :
                piece = self.board[row][col]
                if piece != 0 :
                    piece.draw_piece(win)

    def remove(self, pieces) :
        for piece in pieces :
            self.board[piece.row][piece.col] = 0
            if piece != 0 :
                if piece.color == RED :
                    self.red_left -= 1
                else :
                    self.white_left -= 1
    def winner(self, turn) :
        if self.red_left <= 0 :
                return WHITE
        if self.white_left <= 0 :
                return RED
            
        for r in range(0, ROWS) :
            for piece in self.board[r] :
                if piece != 0 :
                    if piece.color == turn :
                        if self.get_valid_moves(piece) :
                            return None
                        else:
                            continue
        if turn == WHITE :
            return RED
        if turn == RED :
            return WHITE
        
        
    
    def get_valid_moves(self, piece) :
        moves = {} # (valid_destination.x, valid.y) : [(jumped_over.x, jumped_over.y), ( , ) , (,)] , later we will remove the jumped_overs
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row 

        if piece.color == RED or piece.king :
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king :
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped = []) : #step tells the direction , and skipped tells us : have we skipped any pieces yet , if yes so we can move to the squares if we skip another piece
        moves = {}
        last = []

        for r in range(start, stop, step) : #rows
            
            if left < 0 :
                break

            current = self.board[r][left]
            if current == 0 :
                if skipped and not last : #skipped determines whethere we've jumped over an opposit color piece or not 
                    break #this is for when current is an empty square after another empty square after a jump
                elif skipped :
                    moves[(r, left)] = last + skipped

                else : #for the first empty blank , for the first jump over a blank with opposit color 
                    moves[(r, left)] = last

                if last : #preparing for the next jump(double jump)
                    if step == -1 :
                        row = max(r-3,-1)
                    else :
                        row = min(r+3, ROWS)
                    
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color,left+1, skipped=last))
                break
            else :
                if current.color == color :
                    break
                else :
                    last = [current]

            left -= 1
        return moves
        
    def _traverse_right(self, start, stop, step, color, right, skipped = []) :
        moves = {}
        last = []
        
        for r in range(start, stop, step) :
            
            if right >= COLS :
              break

            current = self.board[r][right]
            if current == 0 :
                if skipped and not last :
                    break
                elif skipped :
                    moves[(r, right)] = skipped + last
                else :
                    moves[(r, right)] = last

                if last :
                    if step == -1 :
                        row = max(r - 3, -1) 
                    else :
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped = last)) #actually this is where we initialize the skipped
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break

            else :
                if current.color == color :
                    break

                else :
                    last = [current]

            right += 1
        return moves
    



            


    


















