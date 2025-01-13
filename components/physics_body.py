import pygame
from constants import *

class PhysicsBody:
    def __init__(self, game, pos = (0, 0), size = (16,16)):
        self.game = game
        self.hitbox = pygame.FRect(*pos, *size)

        self.velocity = [0, 0]
        self.collision = [False, False]

    def check_for_collision(self, tiles):
        collisions = []
        for tile in tiles:
            if self.hitbox.colliderect(tile):
                collisions.append(tile)
        return collisions
            
    def tick(self, dt):
        self.velocity[1] += GRAVITY_FALLING * dt

        self.hitbox.x += self.velocity[0]

        for rect in self.check_for_collision(self.game.tiles):
            if self.velocity[0] > 0:
                self.hitbox.right = rect.left
            else:
                self.hitbox.left = rect.right
            self.velocity[0] = 0

        self.hitbox.y += self.velocity[1]

        for rect in self.check_for_collision(self.game.tiles):
            if self.velocity[1] > 0:
                self.hitbox.bottom = rect.top
            else:
                self.hitbox.top = rect.bottom
            self.velocity[1] = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.hitbox)