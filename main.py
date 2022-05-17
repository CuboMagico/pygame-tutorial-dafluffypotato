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
player_rect = pygame.rect.Rect(50, 100, player.get_width(), player.get_height())

grass = pygame.image.load("./images/grass.png")
dirt = pygame.image.load("./images/dirt.png")


gravity = GRAVITY
momentum = VERTICAL_MOMENTUM
air_timer = 0

scroll = [0, 0]
true_scroll = [0, 0]

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


def load_map (map : str) -> List[str] :
    with open(f"./{map}.txt", "r") as file:
        map = file.read().split("\n")
        game_map = []

        for row in map :
            game_map.append(list(row))
        file.close()

        return game_map


run = True
while run :


    # Preenchimento de fundo e paralax

    display.fill(SKY_BLUE)

    pygame.draw.rect(display, BACKGRUND_LIME_GREEN_STANDARD, pygame.Rect(0, 120, 300, 80))
    for item in BACKGROUND :
        obj_back_speed = item[0]
        obj_rect = pygame.rect.Rect(item[1][0] - scroll[0] * obj_back_speed, item[1][1], item[1][2], item[1][3])

        if item[0] == 0.5 :
            pygame.draw.rect(display, BACKGRUND_LIME_GREEN_PRIMARY, obj_rect)
        
        else :
            pygame.draw.rect(display, BACKGRUND_LIME_GREEN_SECONDARY, obj_rect)


    # Câmera

    true_scroll[0] += (player_rect.x - true_scroll[0] - RESOLUTION[0] / 2) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - RESOLUTION[1] / 2) / 20

    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])

    # Renderização do mapa

    hit_list = []

    y_tile = 0
    for row in load_map("map") :
        x_tile = 0

        for tile in row :
            if tile != "0" :
                hit_list.append(pygame.rect.Rect(x_tile, y_tile, 16, 16))

            if tile == "1" :
                display.blit(grass, (x_tile - scroll[0], y_tile - scroll[1]))

            elif tile == "2" :
                display.blit(dirt, (x_tile - scroll[0], y_tile - scroll[1]))


            x_tile += 16
        y_tile += 16


    
    # Movimentação do player

    player_movement = [0, 0]
    

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

    display.blit(player, (player_rect.x - scroll[0], player_rect.y - scroll[1]))
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))

    # Configurações
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()