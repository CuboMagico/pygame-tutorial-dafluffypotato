from math import ceil, floor
import pygame, sys
from pygame.locals import *

from constants import *

from typing import List


clock = pygame.time.Clock()


pygame.init()
pygame.display.set_caption("Fazendo um jogo de plataforma")


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.surface.Surface(RESOLUTION)

collision_types = { "top" : False, "bottom" : False, "left" : False, "right" : False }

player = pygame.image.load("./images/player.png")
player.set_colorkey(COLOR_KEY)
player_rect = pygame.rect.Rect(0, 0, player.get_width(), player.get_height())

grass = pygame.image.load("./images/grass.png")
dirt = pygame.image.load("./images/dirt.png")


gravity = GRAVITY
momentum = VERTICAL_MOMENTUM
air_timer = 0

moving_left = moving_right = False


def collision_test (rect : Rect, tiles : List[Rect]) -> List[Rect] :
    hit_list = []

    for tile in tiles :
        if rect.colliderect(tile) :
            hit_list.append(tile)
            pygame.draw.rect(screen, (255, 0, 0), tile)

    return hit_list


def move (rect : Rect, movement : List, tiles : List) :
    collision_types = { "top" : False, "bottom" : False, "left" : False, "right" : False }

    rect.x += movement[0]
    hit_list : List = collision_test(rect, tiles)
    for tile in hit_list :
        if movement[0] > 0 :
            rect.right = tile.left
            collision_types["right"] = True
        
        elif movement[0] < 0 :
            rect.left = tile.right
            collision_types["left"] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list :
        if movement[1] > 0 :
            rect.bottom = tile.top
            collision_types["bottom"] = True

        
        elif movement[1] < 0 :
            rect.top = tile.bottom
            collision_types["top"] = True

    return rect, collision_types


run = True
while run :


    # Preenchimento de fundo

    display.fill(SKY_BLUE)



    # Renderização do mapa

    hit_list = []

    y_tile = 0
    for row in MAP :
        x_tile = 0

        for tile in row :
            if tile != "0" :
                hit_list.append(pygame.rect.Rect(x_tile, y_tile, 16, 16))

            if tile == "1" :
                display.blit(grass, (x_tile, y_tile))

            elif tile == "2" :
                display.blit(dirt, (x_tile, y_tile))


            x_tile += 16
        y_tile += 16


    
    # Movimentação do player

    player_movement = [0, 0]

    print(momentum)
    

    if moving_right :
        player_movement[0] += 2
        player = pygame.image.load("./images/player.png")
        player.set_colorkey(COLOR_KEY)

    if moving_left :
        player_movement[0] -= 2
        player = pygame.transform.flip(pygame.image.load("./images/player.png"), True, False)
        player.set_colorkey(COLOR_KEY)




    # Eventos e captura de teclas

    for event in pygame.event.get() :
        if event.type == QUIT :
            run = False

        if event.type == KEYDOWN :
            if event.key == K_a :
                moving_left = True

            elif event.key == K_d :
                moving_right = True

            if event.key == K_w and air_timer < 10 :
                momentum = -5

        if event.type == KEYUP :
            if event.key == K_a :
                moving_left = False

            elif event.key == K_d :
                moving_right = False


    # Gravidade
    momentum += gravity

    if collision_types["top"] or collision_types["bottom"] :
        momentum = 0
        air_timer = 0

    else :
        air_timer += 1
        player_movement[1] += momentum


    if momentum > 5 :
        momentum = 5

    # print(collision_types)

    player_rect, collision_types = move(player_rect, player_movement, hit_list) # Definição de movimentação

    # Renderização na tela

    display.blit(player, (player_rect.x, player_rect.y))
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))

    # Configurações
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()