import pygame
from network import Network
from game import Game
from player import Player


class MainMenu:
    BG = (255,255,255)

    def __init__(self):
        self.WIDTH = 1000
        self.HEIGHT = 800
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.name = ""
        self.waiting = False
        self.name_font = pygame.font.SysFont("comicsans", 60)
        self.title_font = pygame.font.SysFont("comicsans", 100)
        self.enter_font = pygame.font.SysFont("comicsans", 30)

    def draw(self):
        self.win.fill(self.BG)
        title = self.title_font.render("Pictonary!", 1, (0,0,0))
        self.win.blit(title, (self.WIDTH/2 - title.get_width()/2, 50))

        name = self.name_font.render("Введіть ім'я: " + self.name, 1, (0,0,0))
        self.win.blit(name, (100, 400))

        if self.waiting:
            enter = self.enter_font.render("В черзі...", 1, (0, 0, 0))
            self.win.blit(enter, (self.WIDTH / 2 - enter.get_width() / 2, 600))
        else:
            enter = self.enter_font.render("Натисніть enter, щоб приєднатися до гри...", 1, (0, 0, 0))
            self.win.blit(enter, (self.WIDTH / 2 - enter.get_width()/2, 600))

        pygame.display.update()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)
            self.draw()
            if self.waiting:
                response = self.n.send({-1:[]})
                if response:
                    run = False
                    g = Game(self.win, self.n)

                    for player in response:
                        p = Player(player)
                        g.add_player(p)
                    g.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.name) > 1:
                            self.waiting = True
                            self.n = Network(self.name)
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.type(event.unicode)

    def type(self, char):
        if len(char) == 1:
            self.name += char

        if len(self.name) >= 20:
            self.name = self.name[:20]


if __name__ == "__main__":
    pygame.font.init()
    main = MainMenu()
    main.run()