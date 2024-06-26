import pygame

class Chat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.WIDTH = 210
        self.HEIGHT = 650
        self.BORDER_THICKNESS = 5
        self.content = []
        self.typing = ""
        self.chat_font = pygame.font.SysFont("comicsans", 15)
        self.type_font = pygame.font.SysFont("comicsans", 15)
        self.CHAT_GAP = 20

    def update_chat(self, content):
        self.content = content

    def draw(self, win):
        pygame.draw.rect(win, (200, 200, 200), (self.x, self.y + self.HEIGHT - 40, self.WIDTH, 40))
        pygame.draw.line(win, (0,0,0), (self.x, self.y + self.HEIGHT - 40), (self.x + self.WIDTH, self.y + self.HEIGHT - 40), self.BORDER_THICKNESS)
        pygame.draw.rect(win, (0,0,0),(self.x, self.y, self.WIDTH, self.HEIGHT) ,self.BORDER_THICKNESS)

        while len(self.content) * self.CHAT_GAP > self.HEIGHT - 60:
            self.content = self.content[:-1]

        for i, chat in enumerate(self.content):
            txt = self.chat_font.render("- " + chat, 1, (0,0,0))
            win.blit(txt, (self.x + 8, 10 + self.y + i*self.CHAT_GAP))

        type_chat = self.type_font.render(self.typing, 1, (0,0,0))
        win.blit(type_chat, (self.x + 10, self.y+self.HEIGHT-type_chat.get_height()-12))

    def type(self, char):
        if len(char) == 1:
            self.typing += char

        if len(self.typing) >= 15:
            self.typing = self.typing[:15]

