import pygame
import physics
from math import *

class Projectiles(pygame.sprite.Sprite):
    def __init__(self, player_rect, direction_angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill("green")
        self.movement_vector = (-5*cos(direction_angle), -5*sin(direction_angle))

        self.pos = [player_rect[0] - self.image.get_width()/2
            , player_rect[1] - self.image.get_height()/2]
        self.rect = self.image.get_rect(center=self.pos)



    def move(self, grav_vector):
        self.movement_vector = physics.movement_vector((0,0), self.movement_vector , grav_vector)
        self.pos[0] += self.movement_vector[0]
        self.pos[1] += self.movement_vector[1]

