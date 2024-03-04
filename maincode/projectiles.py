import pygame
from math import *

class Projectiles(pygame.sprite.Sprite):
    def __init__(self, player_rect, direction_angle, player_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill("green")
        self.movement_vector = [0.0, 0.0]

        self.pos = [player_rect[0] - self.image.get_width()/2
            , player_rect[1] - self.image.get_height()/2]
        self.rect = self.image.get_rect(center=self.pos)
        self.direction_angle = direction_angle



    def move(self):
        print(self.direction_angle)
        self.pos[0] += -5*cos(self.direction_angle)
        self.pos[1] += -5*sin(self.direction_angle)