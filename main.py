import pygame, sys
from pygame.locals import *


clock = pygame.time.Clock()

WINDOW_SIZE = (400, 400)

pygame.init()
pygame.display.set_caption("Fazendo um jogo de plataforma")

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)


run = True
while run :

    for event in pygame.event.get() :
        if event.type == QUIT :
            run = False

    
    pygame.display.update()
    clock.tick(60)


pygame.quit()
sys.exit()