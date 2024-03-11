import pygame
import math
import physics

class Spacecraft(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("fusee.png"), 0.15), 90)
        self.image_copy = self.image
        self.image.set_colorkey((0, 0, 0))
        self.mass = 1
        self.pos = [200, 500]
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = math.pi / 2
        self.angle_copy = self.angle

        self.movement_vector = (0, 0)
        self.propulsion = (0, 0)

    def boost(self):
        self.propulsion = physics.propulsion(self.angle_copy)

    def boost_back(self):
        self.thrust_vector = physics.thrust_vector(self.angle_copy + math.pi)

    def no_boost(self):
        self.thrust_vector = (0,0)

    def turn_left(self):
        self.angle_copy -= math.pi / 60
        self.image_copy = pygame.transform.rotate(self.image, math.degrees(self.angle - self.angle_copy))

    def turn_right(self):
        self.angle_copy += math.pi / 60
        self.image_copy = pygame.transform.rotate(self.image, math.degrees(self.angle - self.angle_copy))

    def move(self, move_vector, thrust_vector, grav_vector=(0, 0)):
        self.movement_vector = physics.movement_vector(thrust_vector, move_vector, grav_vector)
        self.pos[0] += self.movement_vector[0]
        self.pos[1] += self.movement_vector[1]

