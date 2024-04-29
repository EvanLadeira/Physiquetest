import pygame, sys
from game import Game

pygame.init()

clock = pygame.time.Clock()

game = Game()

game.map_init()
game.config()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.get_input()
    game.draw_game()
    game.update()

    clock.tick(60)
    pygame.display.flip()
