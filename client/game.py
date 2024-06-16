import pygame
from button import Button, TextBtn
from board import Board
from top_bar import TopBar
from main_menu import MainMenu
from menu import Menu
from tool_bar import ToolBar
from leadboard import Leaderboard
from player import Player


class Game:
    BG = (255,255,255)

    def __init__(self):
        self.WIDTH = 1300
        self.HEIGHT = 900
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.leadboard = Leaderboard(50, 120)
        self.board = Board(310, 120)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.players = [Player('Dima'),Player('Oleg'),Player('Gena'),Player('Vlad')]
        self.skip_btn = TextBtn(85, 790, 125, 60, (255,255,0), 'Skip')
       

        for player in self.players:
            self.leadboard.add_player(player)

    def draw(self):
        self.win.fill(self.BG)
        self.leadboard.draw(self.win)
        self.top_bar.draw(self.win)
        self.board.draw(self.win)
        self.skip_btn.draw(self.win)
        pygame.display.update()

    def check_click(self):
        """handless click on buttons and screen
        """
        mouse = pygame.mouse.get_pos()

        # Check click on skip button
        if self.skip_btn.click(*mouse):
            print('Clicked skip btn')
        
        clicked_board = self.board.click(*mouse)
        if clicked_board:
            self.board.update(*clicked_board, (0,0,0))


    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(120)
            self.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                    break

                if pygame.mouse.get_pressed()[0]:
                    self.check_click()
        
        pygame.quit()
        
if __name__ == '__main__':
    pygame.font.init()
    g = Game()
    g.run()

