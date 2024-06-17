import pygame
import random

class Board:
    ROWS = COLS = 90
    COLORS ={
        0:(255,255,255), # white
        1:(0,0,0), # black
        2:(255,0,0), # red
        3:(0,255,0), # green
        4:(0,0,255), # blue
        5:(255,255,0), # yellow
        6:(255,140,0), # orange
        7:(165,42,42), # brown
        8:(128,0,128), # purple
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 720
        self.height = 720
        self.compressed_board = []
        self.board = self.create_board()
        self.BORDER_THICKNESS = 5

    def create_board(self):
        return [[(255,255,255) for _ in range(self.COLS)] for _ in range(self.ROWS)]
    
    def translate_board(self):
        for y, _ in enumerate(self.compressed_board):
            for x, col in enumerate(self.compressed_board[y]):
                self.board[y][x] = self.COLORS[col]

    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (self.x-self.BORDER_THICKNESS, self.y-self.BORDER_THICKNESS, self.width+self.BORDER_THICKNESS*2, self.height+self.BORDER_THICKNESS*2), self.BORDER_THICKNESS)
        for y, _ in enumerate(self.board):
            for x, col in enumerate(self.board[y]):
                pygame.draw.rect(win, col, (self.x + x*8, self.y + y*8, 8, 8), 0)

    def click(self, x, y):
        """none if not in board, oyherwise return place clicked on in terms of row and col

        Args:
            x (float)
            y (float)

        Returns:
            (int, int)
        """
        row = int((x - self.x)/8)
        col = int((y - self.y)/8)

        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return row, col

        return None

    def update(self, x, y, color, thickness=3):
        neighs = [(x,y)] + self.get_neighbour(x,y)
        for x,y in neighs:
            if 0 <= x < self.COLS and 0 <= y < self.ROWS:
                self.board[y][x] = color

    def get_neighbour(self,x,y):
        return [ (x-1, y-1), (x, y-1), (x+1, y-1), 
                 (x-1, y), (x, y), (x+1, y),
                 (x-1, y+1), (x, y+1), (x+1, y+1)]

    def clear(self):
        self.board = self.create_board()
