import pygame, sys
from pygame.locals import *
from constants import *

clock = pygame.time.Clock()


pygame.init()
pygame.display.set_caption("Fazendo um jogo de plataforma")

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)


player = pygame.image.load("./images/player.png")
player_location = [0, 0]
player_rect = pygame.rect.Rect(player_location[0], player_location[1], player.get_width(), player.get_height())


gravity = GRAVITY
momentum = VERTICAL_MOMENTUM


test_rect = pygame.rect.Rect(50, 50, 200, 300)

moving_left = moving_right = False


run = True
while run :


    # Renderização na tela
    screen.fill(SKY_BLUE)
    screen.blit(player, player_location)



    # Eventos e captura de teclas
    for event in pygame.event.get() :
        if event.type == QUIT :
            run = False

        if event.type == KEYDOWN :
            if event.key == K_a :
                moving_left = True

            elif event.key == K_d :
                moving_right = True

        if event.type == KEYUP :
            if event.key == K_a :
                moving_left = False

            elif event.key == K_d :
                moving_right = False


    # Movimento do personagem
    
    if moving_left :
        player_location[0] -= 5

    elif moving_right :
        player_location[0] += 5


    # Colisão

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    if player_rect.colliderect(test_rect) :
        pygame.draw.rect(screen, (255, 0, 0), test_rect)
    else :
        pygame.draw.rect(screen, (0, 255, 0), test_rect)


    # Gravidade
    
    if player_location[1] > WINDOW_SIZE[1] - player.get_height() :
        momentum = -momentum
    else :
        momentum += 0.2
    
    player_location[1] += momentum


    # Configurações
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()