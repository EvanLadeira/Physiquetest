import pygame, sys
from game import Game

pygame.init()

clock = pygame.time.Clock()

game = Game()

game.map_init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.get_input()
    game.draw_game()
    game.update()


    pygame.display.flip()
    clock.tick(60)