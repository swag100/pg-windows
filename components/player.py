import pygame
from constants import *

from components.physics_body import PhysicsBody

class Player(PhysicsBody):
    def __init__(self, game, pos = (0, 0), size = (16,16)):
        PhysicsBody.__init__(self, game, pos, size)
        
        self.time_in_air = 0
        self.time_on_ground = 0

        self.jumpbuffer_activated = False
        self.jumpbuffer_time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                can_jump = self.collision[1]

                if not can_jump:
                    self.jumpbuffer_activated = True

                #coyote time
                can_coyote_jump = self.time_in_air <= TIME_COYOTE and self.velocity[1] > 0

                if can_jump or can_coyote_jump:
                    self.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.velocity[1] < 0:
                    self.velocity[1] *= JUMP_LET_GO_DAMPER
    
    def jump(self):
        self.velocity[1] = -JUMP_FORCE
    
    def get_true_gravity(self):
        if self.velocity[1] > 0:
            return GRAVITY_FALLING
        else:
            return GRAVITY_JUMPING
            
    def tick(self, dt):
        keys = pygame.key.get_pressed()
        speed = SPEED_WALK
        if keys[pygame.K_LSHIFT]:
            speed = SPEED_RUN
        self.velocity[0] = (keys[pygame.K_d] - keys[pygame.K_a]) * speed * dt
        self.velocity[1] += self.get_true_gravity() * dt

        self.hitbox.x += self.velocity[0]

        self.collision[0] = False
        for rect in self.check_for_collision(self.game.tiles):
            if self.velocity[0] > 0:
                self.hitbox.right = rect.left
            else:
                self.hitbox.left = rect.right
            self.collision[0] = True
            self.velocity[0] = 0

        self.hitbox.y += self.velocity[1]

        self.collision[1] = False
        for rect in self.check_for_collision(self.game.tiles):
            if self.velocity[1] > 0:
                self.hitbox.bottom = rect.top
            else:
                self.hitbox.top = rect.bottom
            self.collision[1] = True
            self.velocity[1] = 0
            
        if self.collision[1]: 
            self.time_on_ground += dt
            self.time_in_air = 0
            self.jumpbuffer_activated = False
        else:
            self.time_in_air += dt
            self.time_on_ground = 0

        if self.collision[1] and 0 < self.jumpbuffer_time <= TIME_JUMPBUFFER and keys[pygame.K_SPACE]:
            self.jumpbuffer_activated = False
            self.jump()

        #jumpbuffer jump
        if self.jumpbuffer_activated:
            self.jumpbuffer_time += dt
        else:
            self.jumpbuffer_time = 0