import pygame
import pymunk
from utils import *
from frame import *


class Entity:
    def __init__(self, game, position, size):
        self.game = game
        self.rect = pygame.FRect(*position, *size)

        self.collided = [False, False]
        self.velocity = [0, 0]

    def collision(self, tiles):
        collisions = []

        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)

        return collisions
    
    def move(self, amount):
        self.rect.x += amount[0]
        self.collided[0] = False
        for tile in self.collision(self.game.get_tiles()):
            if amount[0] > 0:
                self.rect.right = tile.left
            if amount[0] < 0:
                self.rect.left = tile.right
            self.collided[0] = True
            self.velocity[0] = 0
                
        self.rect.y += amount[1]
        self.collided[1] = False
        for tile in self.collision(self.game.get_tiles()):
            if amount[1] > 0:
                self.rect.bottom = tile.top
            if amount[1] < 0:
                self.rect.top = tile.bottom
            self.collided[1] = True
            self.velocity[1] = 0

    def handle_event(self, event):
        pass

    def tick(self, dt):
        pass

    def draw(self, screen):
        pass

class Player(Entity):
    def __init__(self, game, position):
        self.game = game

        super().__init__(game, position, (16, 16))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.collided[1]:
                self.velocity[1] -= 7.4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self.velocity[1] < -1:
                self.velocity[1] = -1

    def tick(self, dt):
        keys = pygame.key.get_pressed()

        self.velocity[0] += (keys[pygame.K_d] - keys[pygame.K_a]) * 50 * dt 
        self.velocity[0] *= 0.85

        self.velocity[1] += ((GRAVITY * 2) if self.velocity[1] > 0 else GRAVITY) * dt

        self.move(self.velocity)

    def draw(self, screen, frame):
        pygame.draw.rect(screen, (255,0,0), self.rect.move(-frame.position[0], -frame.position[1]))

class Game:
    def __init__(self):
        pygame.init()

        self.done = False
        self.clock = pygame.Clock()

        #frames owns only entities that lie inside it.
        self.frames = []

        self.new_frame()
        self.entities = [Player(self, (self.frames[0].position))]

    def new_frame(self):
        for frame in self.frames:
            frame.z_order += 1

        self.frames.append(Frame(self))
        
    def get_tiles(self):
        total_tiles = []
        for frame in self.frames:
            for tile in frame.tiles:
                total_tiles.append((frame, tile)) 

        #subtract from total tiles because we wouldn't be aware of other frame's tiles otherwise
        tiles = []
        for tile_frame, tile in total_tiles:
            difference = sub_rect_list(tile, [frame.get_rect() for frame in self.frames if frame.id != tile_frame.id])
            tiles.extend(difference)
            
        return tiles

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.WINDOWFOCUSGAINED:
                z_orders = [frame.z_order for frame in self.frames]

                swap_frame_id = z_orders.index(0)

                #it swaps it, so zorder 2 -> zorder 0 and 0 -> 2, but completely ignores 1
                temp = self.frames[swap_frame_id].z_order
                self.frames[swap_frame_id].z_order = event.window.z_order
                event.window.z_order = temp

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
        print(
            'z order high to low ', 
            ['id:'+str(frame.id)+','+'zorder:'+str(frame.z_order) for frame in self.frames],end='\r'
        )

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