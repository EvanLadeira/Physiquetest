import pygame
import physics
from tools_functions import *


from items import Item
from planets import Planets
from spacecraft import Spacecraft
from projectiles import Projectiles

#Calcul de la taille de l'écran (Changement)
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

class Game():

    def __init__(self):

        #initialisation de l'écran a la bonne taille (Changement)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.spacecraft = pygame.sprite.GroupSingle()
        self.spacecraft_sprite = Spacecraft((screen_width, screen_height))
        self.spacecraft.add(self.spacecraft_sprite)

        self.planets_group = pygame.sprite.Group()
        self.projectiles = pygame.sprite.GroupSingle()

        self.player_fired = False

        self.items = []



    def config(self):
        '''
        Permet d'activer les fonctionnalités du jeu à son démarrage
        '''
        f = open('debug.txt', 'r', encoding='UTF8')
        self.config_list = f.readlines()
        debug = {}
        f.close()
        for ligne in self.config_list:
            config = split_ch(ligne, '=')
            debug[config[0]] = config[1]

        # debug bool
        self.grav_attraction_fusee = int(debug['grav_attraction_fusee'])
        self.grav_attraction_proj = int(debug['grav_attraction_proj'])
        self.can_move = int(debug['player_move'])
        self.can_fire = int(debug['player_fire'])
        self.can_rotate = int(debug['player_rotate'])


    def map_init(self):
        '''
        Permet d'afficher les planètes
        '''
        f = open('data.txt', 'r', encoding='UTF8')
        self.data_list = f.readlines()[1:]
        f.close()
        for ligne in self.data_list:
            data = split_ch(ligne, ';')
            planet = Planets((int(data[2]), int(data[3])), int(data[1]), str(data[4]), float(data[5]))
            self.planets_group.add(planet)
        a = Item()


    def get_input(self):
        '''
        Detecte la pression des touches dans le jeu et appelle les méthodes liées aux actions
        '''
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

        '''
        Gère l'affichage du jeu
        '''

        self.screen.fill('black')

        #Vérifie si la gravité des projectiles est activée
        if self.grav_attraction_proj:
            if self.player_fired:
                self.g_vec_projectile = physics.force_grav(self.projectile_sprite.pos, self.data_list) * 100
        else:
            self.g_vec_projectile = (0, 0)

        #Déplace le projectile si le joueur a tiré
        if self.player_fired:
            self.projectile_sprite.move(self.g_vec_projectile)
            self.screen.blit(self.projectile_sprite.image, (
                self.projectile_sprite.pos[0],
                self.projectile_sprite.pos[1]))

        #Vérifie si la gravité de la fusée est activée
        if self.grav_attraction_fusee:
            self.g_vec_spacecraft = physics.force_grav(self.spacecraft_sprite.pos, self.data_list)
        else:
            self.g_vec_spacecraft = (0, 0)

        #Déplace la fusée
        self.spacecraft_sprite.move(self.spacecraft_sprite.movement_vector, self.spacecraft_sprite.propulsion,
                                    self.g_vec_spacecraft)

        self.screen.blit(self.spacecraft_sprite.image_copy, (
            self.spacecraft_sprite.pos[0] - int(self.spacecraft_sprite.image_copy.get_width() / 2),
            self.spacecraft_sprite.pos[1] - int(self.spacecraft_sprite.image_copy.get_height() / 2)))


    def update(self):
        '''
        Met à jour tous les sprites
        '''
        self.spacecraft_sprite.update()
        self.planets_group.update()
        self.planets_group.draw(self.screen)
        if self.player_fired:
            self.projectile_sprite.update()

