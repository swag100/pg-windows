import pygame
import pymunk
from utils import *
from frame import *

class Game:
    def __init__(self):
        pygame.init()

        self.done = False
        self.clock = pygame.Clock()

        #frames owns only entities that lie inside it.
        self.frames = []
        self.entities = []

        self.new_frame()

    def new_frame(self):
        for frame in self.frames:
            frame.z_order += 1

        self.frames.append(Frame(self))
        
    def get_tiles(self):
        total_tiles = []
        for frame in self.frames:
            for tile in frame.tiles:
                total_tiles.append(tile)
        return total_tiles

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.WINDOWENTER:
                #swaps WHENEVER you enter the window, but not the original window?
                #the original window ALREADY IS 0
                temp = self.frames[0].z_order
                self.frames[0].z_order = event.window.z_order
                event.window.z_order = temp

                print(event.window.id)

            if event.type == pygame.WINDOWCLOSE:
                if event.window:
                    self.frames.remove(event.window)
                    event.window.destroy() 

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.done = True
                pygame.quit()
                raise SystemExit
            
            for entity in self.entities:
                entity.handle_event(event)

            # JUST GOING TO PASS EVENTS TO FOCUSED WINDOW FOR NOW
            # CHANGE LATER IF NECESSARY
            for frame in self.frames: 
                if frame.focused:
                    frame.handle_event(event)

            #test code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.new_frame()

    def tick(self, dt):
        for frame in self.frames:
            frame.tick(dt)

        #TODO: clear overlapping rects
        #only clear a rect if it is not a title and it belongs to a frame LOWER than us.
        #higher than us ignore title
        frame.title = str(frame.id)
        print('z order high to low ', ['id:'+str(frame.id)+','+'zorder:'+str(frame.z_order) for frame in self.frames],end='\r')

        for entity in self.entities:
            entity.tick(dt)

            for frame in self.frames:
                frame.entities = []
                if entity.rect.colliderect(frame.get_rect()):
                    frame.entities.append(entity)

    def draw(self):
        for frame in self.frames:
            frame.draw(frame.get_surface())
            frame.flip()

    def loop(self, framerate = FRAMERATE):
        dt = self.clock.tick(framerate) / 1000

        self.handle_events()
        self.tick(dt)
        self.draw()

    def run(self):
        while not self.done:
            self.loop()