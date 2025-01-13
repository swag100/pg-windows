import sys
import pygame

from components.player import Player

class Game:
    def __init__(self):
        self.done = False

        pygame.init()

        self.screen = pygame.display.set_mode((480,360))
        self.clock = pygame.Clock()

        self.tiles = [
            pygame.Rect(0,300,self.screen.get_size()[0] / 2 - 20,60),
            pygame.Rect(self.screen.get_size()[0] / 2 + 30,300,self.screen.get_size()[0] / 2 - 20,60),
            pygame.Rect(400,180,50,180),
            pygame.Rect(290,90,50,100)
        ]
        self.player = Player(self)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            self.player.handle_event(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def tick(self, dt):
        self.player.tick(dt)

    def draw(self, screen):
        screen.fill((0,0,0))
        for tile in self.tiles:
            pygame.draw.rect(screen, (170,170,170), tile)
        self.player.draw(screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(60) / 1000

            self.handle_events()
            self.tick(dt)
            self.draw(self.screen)

            pygame.display.flip()

Game().run()