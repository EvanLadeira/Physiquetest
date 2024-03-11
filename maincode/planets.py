import pygame.sprite

class Planets(pygame.sprite.Sprite):

    def __init__(self, pos, mass, image, factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(pygame.image.load("planets_assets/"+image), factor)
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.mass = mass
