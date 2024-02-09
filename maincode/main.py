import pygame, sys

import physics
from spacecraft import Spacecraft
from planets import Planets
from tools_functions import *

pygame.init()
screen = pygame.display.set_mode((1200,600))
clock = pygame.time.Clock()
spacecraft = pygame.sprite.GroupSingle()
spacecraft_sprite = Spacecraft()
spacecraft.add(spacecraft_sprite)

planets_group = pygame.sprite.Group()
f = open('data.txt', 'r', encoding='UTF8')
data_list = f.readlines()[1:]
f.close()
for ligne in data_list:
    data = split_ch(ligne, ';')
    print(data)
    planet = Planets((int(data[2]), int(data[3])), int(data[1]), str(data[4]))
    planets_group.add(planet)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill('black')
    spacecraft_sprite.update()
    screen.blit(spacecraft_sprite.image_copy, (
    spacecraft_sprite.pos[0] - int(spacecraft_sprite.image_copy.get_width() / 2),
    spacecraft_sprite.pos[1] - int(spacecraft_sprite.image_copy.get_height() / 2)))

    g_vec = physics.force_grav(spacecraft_sprite.pos, data_list)
    spacecraft_sprite.move(spacecraft_sprite.movement_vector, spacecraft_sprite.thrust_vector, g_vec)
    #spacecraft_sprite.rotation(spacecraft_sprite.pos, (600,250), 6.67*10E23)

    planets_group.update()
    planets_group.draw(screen)


    #pygame.display.update()
    pygame.display.flip()
    clock.tick(60)