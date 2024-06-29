import pygame
from network import Network
from game import Game
from player import Player
from button import Button, TextButton


class MainMenu:
    BG = (255,255,255)

    def __init__(self):
        """start main menu and lobby stage
        """
        self.width = 1000
        self.height = 750
        self.win = pygame.display.set_mode((self.width, self.height))
        self.name = ""
        self.waiting = False
        self.name_font = pygame.font.SysFont("comicsans", 60)
        self.title_font = pygame.font.SysFont("comicsans", 100)
        self.enter_font = pygame.font.SysFont("comicsans", 30)
        self.player_list=''
        self.start_game_btn = TextButton(self.width/2-100, 500, 200, 60, (255,255,255), "Готовий!")
        self.first_player = False
        
    
    def run(self):
        """master loop main menu
        """
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            self.draw()

            if self.waiting:
                response = self.n.send({-1:[]})
                get_player = self.n.send({-2:[]})
                try:
                    if self.name == get_player[0]:   
                        self.first_player = True 
                except:
                    pass
                self.player_list = ', '.join(get_player)
   
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
                        if len(self.name) >= 1:
                            self.waiting = True
                            self.n = Network(self.name)
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.type(event.unicode)

    def draw(self):

        self.win.fill(self.BG) 
        title = self.title_font.render("Pictonary!", 1, (0,0,0)) 
        self.win.blit(title, (self.width/2 - title.get_width()/2, 50)) 

        name = self.name_font.render("Введіть ім'я: " + self.name, 1, (0,0,0))
        self.win.blit(name, (100, 400))

        if self.waiting:
            self.win.fill(self.BG) 

            enter = self.enter_font.render("В черзі...", 1, (0, 0, 0))
            self.win.blit(enter, (self.width / 2 - enter.get_width() / 2, 200))

            enter = self.enter_font.render(self.player_list, 1, (0, 0, 0))
            self.win.blit(enter, (self.width / 2 - enter.get_width() / 2, 320))

            self.start_game_btn.draw(self.win)
            mouse = pygame.mouse.get_pos()



            if self.start_game_btn.click(*mouse) and pygame.mouse.get_pressed()[0]:
                self.n.send({-3:[self.name]})
                self.start_game_btn = TextButton(self.width/2-100, 500, 200, 60, 'green', "Готовий!", (255,255,255), 'green')
                

        else:
            enter = self.enter_font.render("Натисніть enter, щоб приєднатися до гри...", 1, (0, 0, 0))
            self.win.blit(enter, (self.width / 2 - enter.get_width()/2, 600))
            
        pygame.display.update()


    def type(self, char):
        if len(char) == 1:
            self.name += char

        if len(self.name) >= 20:
            self.name = self.name[:20]

        


if __name__ == "__main__":
    pygame.font.init()
    main = MainMenu()
    main.run()