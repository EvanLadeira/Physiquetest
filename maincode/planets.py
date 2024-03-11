import pygame.sprite

class Planets(pygame.sprite.Sprite):

    def __init__(self, pos, mass, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("planets_assets/"+image)
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.mass = mass
