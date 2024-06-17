import pygame 
from button import Button, TextBtn

class BottomBar:
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


    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 730
        self.height = 100
        self.game = game
        self.BORDER_THICKNESS = 5
        self.clear_btn = TextBtn(self.x + self.width - 150, self.y + 25, 100, 50, (128, 128, 128), 'Clear')
        self.eraser_btn = TextBtn(self.x + self.width - 300, self.y + 25, 100, 50, (128, 128, 128), 'Eraser')
        self.color_buttons = [Button(self.x + 20, self.y + 5, 30, 30, self.COLORS[0]),
                              Button(self.x + 50, self.y + 5, 30, 30, self.COLORS[1]),
                              Button(self.x + 80, self.y + 5, 30, 30, self.COLORS[2]),
                              Button(self.x + 20, self.y + 35, 30, 30, self.COLORS[3]),
                              Button(self.x + 50, self.y + 35, 30, 30, self.COLORS[4]),
                              Button(self.x + 80, self.y + 35, 30, 30, self.COLORS[5]),
                              Button(self.x + 20, self.y + 65, 30, 30, self.COLORS[6]),
                              Button(self.x + 50, self.y + 65, 30, 30, self.COLORS[7]),
                              Button(self.x + 80, self.y + 65, 30, 30, self.COLORS[8]),
                              ]

    def draw(self, win):
        pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height), self.BORDER_THICKNESS)
        self.clear_btn.draw(win)
        self.eraser_btn.draw(win)

        for btn in self.color_buttons:
            btn.draw(win)


    def button_events(self):
        """
        handle all button press events here
        :return: None
        """
        mouse = pygame.mouse.get_pos()

        if self.clear_btn.click(*mouse):
            self.game.board.clear()

        if self.eraser_btn.click(*mouse):
            self.game.draw_color = self.COLORS[0]

        for btn in self.color_buttons:
            if btn.click(*mouse):
                self.game.draw_color = btn.color