import pygame


class Board(object):
    ROWS = 110
    COLS = 110
    scale = 5
    COLORS = {
        0: (255,255,255),
        1: (0,0,0),
        2: (255,0,0),
        3: (0,255,0),
        4: (0,0,255),
        5: (255,255,0),
        6: (255,140,0),
        7: (165,42,42),
        8: (128,0,128)
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.WIDTH = self.COLS*self.scale
        self.HEIGHT = self.ROWS*self.scale
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
        pygame.draw.rect(win, (0,0,0), (self.x - self.BORDER_THICKNESS, self.y-self.BORDER_THICKNESS, self.WIDTH + self.BORDER_THICKNESS*2, self.HEIGHT + self.BORDER_THICKNESS*2), self.BORDER_THICKNESS)
        for y, _ in enumerate(self.board):
            for x, col in enumerate(self.board[y]):
                pygame.draw.rect(win, col, (self.x + x*self.scale, self.y + y*self.scale, self.scale, self.scale), 0)

    def click(self,x,y):
        """
        none if not in board, otherwise return place clicked on
        in terms of row and col
        :param x: float
        :param y: float
        :return: (int, int) or None
        """
        row = int((x - self.x)/self.scale)
        col = int((y - self.y)/self.scale)

        if 0 <= row < self.ROWS and 0 <= col < self.COLS-1:
            return row, col

        return None

    def update(self, x, y, color):
        neighs = [(x,y)] + self.get_neighbour(x,y)
        for x,y in neighs:
            if 0 <= x < self.COLS-1 and 0 <= y < self.ROWS:
                self.board[x][y] = color

    def get_neighbour(self,x,y):
        return [ (x-1, y-1), (x, y-1),
                 (x-1, y), (x, y), 
                 (x-1, y+1), (x, y+1),]

    def clear(self):
        self.board = self.create_board()