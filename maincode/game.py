import pygame
import physics
import math
from tools_functions import *


from planets import Planets
from spacecraft import Spacecraft
from projectiles import Projectiles

class Game():

    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 600))
        self.spacecraft = pygame.sprite.GroupSingle()
        self.spacecraft_sprite = Spacecraft()
        self.spacecraft.add(self.spacecraft_sprite)

        self.planets_group = pygame.sprite.Group()
        self.projectiles = pygame.sprite.GroupSingle()

        self.player_fired = False
    def config(self):
        f = open('debug.txt', 'r', encoding='UTF8')
        self.config_list = f.readlines()
        debug = {}
        f.close()
        for ligne in self.config_list:
            config = split_ch(ligne, '=')
            debug[config[0]] = config[1]

        # debug bool
        self.grav_attraction = int(debug['grav_attraction'])
        self.can_move = int(debug['player_move'])
        self.can_fire = int(debug['player_fire'])
        self.can_rotate = int(debug['player_rotate'])


    def map_init(self):
        f = open('data.txt', 'r', encoding='UTF8')
        self.data_list = f.readlines()[1:]
        f.close()
        for ligne in self.data_list:
            data = split_ch(ligne, ';')
            planet = Planets((int(data[2]), int(data[3])), int(data[1]), str(data[4]))
            self.planets_group.add(planet)


    def get_input(self):
        keys = pygame.key.get_pressed()
        # power
        if self.can_move:
            if keys[pygame.K_UP]:
                self.spacecraft_sprite.boost()
            elif keys[pygame.K_DOWN]:
                self.spacecraft_sprite.boost_back()
            else:
                self.spacecraft_sprite.no_boost()
        # rotations
        if self.can_rotate:
            if keys[pygame.K_RIGHT]:
                self.spacecraft_sprite.turn_right()
            if keys[pygame.K_LEFT]:
                self.spacecraft_sprite.turn_left()
        # fire
        if self.can_fire:
            if keys[pygame.K_SPACE]:
                self.player_fired = True
                self.projectile_sprite = Projectiles(self.spacecraft_sprite.pos, self.spacecraft_sprite.angle_copy, self.spacecraft_sprite.image_copy)
                self.projectiles.add(self.projectile_sprite)

    def draw_game(self):
        self.screen.fill('white')

        self.screen.blit(self.spacecraft_sprite.image_copy, (
            self.spacecraft_sprite.pos[0] - int(self.spacecraft_sprite.image_copy.get_width() / 2),
            self.spacecraft_sprite.pos[1] - int(self.spacecraft_sprite.image_copy.get_height() / 2)))


        if self.grav_attraction:
            g_vec = physics.force_grav(self.spacecraft_sprite.pos, self.data_list)
        else:
            g_vec = (0,0)
        self.spacecraft_sprite.move(self.spacecraft_sprite.movement_vector, self.spacecraft_sprite.thrust_vector, g_vec)

        if self.player_fired:
            self.projectile_sprite.move()
            self.screen.blit(self.projectile_sprite.image, (
                self.projectile_sprite.pos[0],
                self.projectile_sprite.pos[1]))


    def update(self):
        self.spacecraft_sprite.update()
        self.planets_group.update()
        self.planets_group.draw(self.screen)
        if self.player_fired:
            self.projectile_sprite.update()

