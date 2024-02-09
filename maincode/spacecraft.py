import pygame
import math
import physics

class Spacecraft(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("fusee.png"), 0.15), 90)
        self.image_copy = self.image
        self.image.set_colorkey((0, 0, 0))
        self.mass = 1
        self.pos = [200, 500]
        self.vel = [0, 0]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.angle = math.pi / 2
        self.angle_copy = self.angle

        self.movement_vector = (0, 0)
        self.thrust_vector = (0, 0)


    def get_input(self):
        keys = pygame.key.get_pressed()
        # power
        if keys[pygame.K_UP]:
            self.thrust_vector = physics.thrust_vector(self.angle_copy)
        elif keys[pygame.K_DOWN]:
            self.thrust_vector = physics.thrust_vector(self.angle_copy + math.pi)
        else:
            self.thrust_vector = (0, 0)
        # rotations
        if keys[pygame.K_RIGHT]:
            self.angle_copy += math.pi / 60
            self.image_copy = pygame.transform.rotate(self.image, math.degrees(self.angle - self.angle_copy))
        if keys[pygame.K_LEFT]:
            self.angle_copy -= math.pi / 60
            self.image_copy = pygame.transform.rotate(self.image, math.degrees(self.angle - self.angle_copy))

    def move(self, move_vector, thrust_vector, grav_vector=(0, 0)):
        self.movement_vector = physics.movement_vector(thrust_vector, move_vector, grav_vector)
        self.pos[0] += self.movement_vector[0]
        self.pos[1] += self.movement_vector[1]

    def rotation(self, pos1, pos2, mass):
        Fx, Fy = physics.force_grav(pos1, pos2, mass)
        self.vel[0] += Fx / 1
        self.vel[1] += Fy / 1
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def update(self):
        self.get_input()