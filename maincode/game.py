import pygame
import physics
import random
from tools_functions import *


from planets import Planets
from spacecraft import Spacecraft
from projectiles import Projectiles

class Game():

    def __init__(self):

        self.screen = pygame.display.set_mode((1600, 800))

        self.planets_group = pygame.sprite.Group()
        self.projectiles = pygame.sprite.GroupSingle()
        self.player_fired = False

        self.changing_turn = False
        self.turn_of_player = 1

        self.nb_players = 3
        self.list_players = []

        self.h_is_pressed = False



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
        self.players()

        # debug bool
        self.grav_attraction_fusee = int(debug['grav_attraction_fusee'])
        self.grav_attraction_proj = int(debug['grav_attraction_proj'])
        self.can_move = int(debug['player_move'])
        self.can_fire = int(debug['player_fire'])
        self.can_rotate = int(debug['player_rotate'])
        self.collision = int(debug['collision'])



    def players(self):
        for i in range(self.nb_players):
            self.spacecraft_sprite = Spacecraft(([random.randint(0, 1000), 500]))
            self.list_players.append(self.spacecraft_sprite)



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



    def get_input(self):
        '''
        Detecte la pression des touches dans le jeu et appelle les méthodes liées aux actions
        '''
        keys = pygame.key.get_pressed()
        # power
        if self.can_move:
            if keys[pygame.K_UP]:
                self.list_players[self.turn_of_player-1].boost()
            elif keys[pygame.K_DOWN]:
                self.list_players[self.turn_of_player-1].boost_back()
            else:
                self.list_players[self.turn_of_player-1].no_boost()
        # rotations
        if self.can_rotate:
            if keys[pygame.K_RIGHT]:
                self.list_players[self.turn_of_player-1].turn_right()
            if keys[pygame.K_LEFT]:
                self.list_players[self.turn_of_player-1].turn_left()
        # fire
        if self.can_fire:
            if keys[pygame.K_SPACE]:
                self.player_fired = True
                self.projectile_sprite = Projectiles(self.list_players[self.turn_of_player-1].pos, self.list_players[self.turn_of_player-1].angle_copy, self.list_players[self.turn_of_player-1].image_copy)
                self.projectiles.add(self.projectile_sprite)

        #STOP the spacecraft
        if keys[pygame.K_h]:
            if self.h_is_pressed == False:
                self.changing_turn = True
                self.list_players[self.turn_of_player-1].movement_vector = (0,0)
                print("Tour du joueur : ", self.turn_of_player)
                self.h_is_pressed = True
        else:
            self.h_is_pressed = False


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
            self.g_vec_spacecraft = physics.force_grav(self.list_players[self.turn_of_player-1].pos, self.data_list)
        else:
            self.g_vec_spacecraft = (0, 0)

        #Déplace la fusée
        self.list_players[self.turn_of_player-1].move(self.list_players[self.turn_of_player-1].movement_vector, self.list_players[self.turn_of_player-1].propulsion,
                                                      (self.g_vec_spacecraft[0]/10, self.g_vec_spacecraft[1]/10))

        #affiche les fusées
        for sprite in self.list_players:
            self.screen.blit(sprite.image_copy, (
                sprite.pos[0] - int(sprite.image_copy.get_width() / 2),
                sprite.pos[1] - int(sprite.image_copy.get_height() / 2)))


    def collide_proj(self):
        for planet in self.planets_group:
            if physics.calcul_distance(self.projectile_sprite.pos, planet.pos)["distance"] < planet.image.get_width()/2:
                print("collision planet-proj")
                self.projectiles.remove(self.projectile_sprite)
                self.projectile_sprite.kill()
                self.player_fired = False
                break



    def collide_spacecraft(self):
        for planet in self.planets_group:
            if physics.calcul_distance(self.list_players[self.turn_of_player-1].pos, planet.pos)["distance"] < planet.image.get_width()/2:
                print("collision spacecraft-planet")
                break

    def collide_proj_spacecraft(self):
        for spacecraft in self.list_players:
            if spacecraft != self.list_players[self.turn_of_player-1]:
                if physics.calcul_distance(self.projectile_sprite.pos, spacecraft.pos)["distance"] < 30:
                    print("collision proj-spacecraft")
                    self.projectiles.remove(self.projectile_sprite)
                    self.projectile_sprite.kill()
                    self.player_fired = False
                    break




    def update(self):
        '''
        Met à jour tous les sprites
        '''
        self.list_players[self.turn_of_player-1].update()
        self.planets_group.update()
        self.planets_group.draw(self.screen)


        if self.collision:
            self.collide_spacecraft()

            if self.player_fired:
                self.list_players[self.turn_of_player-1].update()
                self.collide_proj()



    def change_turn(self):
        if self.changing_turn:
            if self.turn_of_player == self.nb_players:
                self.turn_of_player = 1
            else:
                self.turn_of_player += 1
        self.changing_turn = False