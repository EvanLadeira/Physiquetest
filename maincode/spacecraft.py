import pygame
import math
import physics

class Spacecraft(pygame.sprite.Sprite):

    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)

        #limites de la carte (Changement)
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

        #Images
        self.image = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("fusee.png"), 0.15), 90)
        self.image_copy = self.image
        self.image.set_colorkey((0, 0, 0))

        #Specs
        self.mass = 1
        self.pos = [1200, 400]
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = math.pi / 2
        self.angle_copy = self.angle

        #Vectors
        self.movement_vector = (0, 0)
        self.propulsion = (0, 0)

    def boost(self):
        #Permet de propulser la fusée
        self.propulsion = physics.propulsion(self.angle_copy)

    def boost_back(self):
        #Permet de propulser la fusée en arrière
        self.propulsion = physics.propulsion(self.angle_copy + math.pi)

    def no_boost(self):
        #Met la fusée est à l'arrêt
        self.propulsion = (0,0)

    def turn_left(self):
        #Tourne la fusée vers la gauche
        self.angle_copy -= math.pi / 60
        self.image_copy = pygame.transform.rotate(self.image, math.degrees(self.angle - self.angle_copy))

    def turn_right(self):
        #Tourne la fusée vers la droite
        self.angle_copy += math.pi / 60
        self.image_copy = pygame.transform.rotate(self.image, math.degrees(self.angle - self.angle_copy))

    def move(self, movement_vector, propulsion, grav_vector=(0, 0)):
        #Calcule le vecteur de déplacement de la fusée
        self.movement_vector = physics.movement_vector(propulsion, movement_vector, grav_vector)
        #Déplace la fusée
        self.pos[0] += self.movement_vector[0]
        self.pos[1] += self.movement_vector[1]

        #calcul des dépassement des limites du terrain (Changement)
        if self.pos[0] > self.screen_width:
            self.pos[0] -= self.screen_width
        elif self.pos[0] < 0:
            self.pos[0] += self.screen_width
        if self.pos[1] > self.screen_height:
            self.pos[1] -= self.screen_height
        elif self.pos[1] < 0:
            self.pos[1] += self.screen_height

