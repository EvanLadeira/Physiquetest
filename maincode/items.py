import pygame
import physics

class Item(pygame.sprite.Sprite):

    def __init__(self, pos=(200,200)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load("square.png"), 0.1), 90)
        self.rect = self.image.get_rect(center=self.pos)

class Shield(Item):
    def __init__(self, pos):
        Item.__init__(self, pos)

    def give_pu(self, ship):
        ship.shield += 1


class Heal(Item):
    def __init__(self, pos):
        Item.__init__(self, pos)

    def give_pu(self, ship):
        ship.hp = 3

