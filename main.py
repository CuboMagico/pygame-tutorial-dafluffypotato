import pygame, sys, random
from pygame.locals import *

from constants import *
import data.engine as engine

from typing import List


clock = pygame.time.Clock()

pygame.init()
pygame.mixer.pre_init()

pygame.display.set_caption("Fazendo um jogo de plataforma")


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.surface.Surface(RESOLUTION)

collision_types = { "top" : False, "bottom" : False, "left" : False, "right" : False }

engine.load_animations("data/images/entities/")
player = engine.entity(100, 100, 5, 13, "player")
player_rect = pygame.rect.Rect(50, 100, 5, 13)

grass = pygame.image.load("data/images/grass.png")
grass_sounds = [pygame.mixer.Sound("data/sounds/grass_0.wav"), pygame.mixer.Sound("data/sounds/grass_1.wav")]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)
grass_sound_timer = 0

pygame.mixer.music.load("data/sounds/music.wav")
pygame.mixer.music.play(-1)

dirt = pygame.image.load("data/images/dirt.png")
plant_img = pygame.image.load("data/images/plant.png")
plant_img.set_colorkey(COLOR_KEY)

tile_index = { 1 : grass, 2 : dirt, 3 : plant_img}

global animation_frames
animation_frames = {}

gravity = GRAVITY
momentum = VERTICAL_MOMENTUM
air_timer = 0

jump_sound = pygame.mixer.Sound("data/sounds/jump.wav")


scroll = [0, 0]
true_scroll = [0, 0]

moving_left = moving_right = False


animation_database = {}

def generate_chunk (x, y) :
    chunck_data = []

    for y_pos in range(CHUNCK_SIZE) :
        for x_pos in range(CHUNCK_SIZE) :
            target_x = x * CHUNCK_SIZE + x_pos
            target_y = y * CHUNCK_SIZE + y_pos
            tile_type = 0

            if target_y > 10 :
                tile_type = 2

            elif target_y == 10 :
                tile_type = 1

            elif target_y == 9 :
                if random.randint(1, 5) == 1 :
                    tile_type = 3

            if tile_type != 0 :
                chunck_data.append([[target_x, target_y], tile_type])
    
    return chunck_data


class Jumper_obj :
    
    def __init__ (self, loc : List) :
        self.loc = loc
        self.jumper_img = pygame.image.load("data/images/jumper.png")
        self.jumper_img.set_colorkey(COLOR_KEY)
    
    def render (self, surf : pygame.Surface, scroll) :
        surf.blit(self.jumper_img, (self.loc[0] - scroll[0], self.loc[1] - scroll[1]))

    def get_rect (self) :
        return pygame.Rect(self.loc[0], self.loc[1], 8, 9)

    def collision_test (self, rect) :
        jumper_rect = self.get_rect()
        return jumper_rect.colliderect(rect)


game_map = {}

enimies_objs = []
for i in range(5) :
    enimies_objs.append([0, engine.entity(random.randint(0, 60) * 10 - 300, 80, 13, 13, "enemy")])


jumper_objs : List[Jumper_obj] = []
for i in range(5) :
    jumper_objs.append(Jumper_obj((random.randint(0, 60) * 10 - 300, 100)))


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


    tile_rects = []
    for y in range(3) :
        for x in range(4) :
            target_x = x - 1 + int(round(scroll[0] / (CHUNCK_SIZE * 16)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNCK_SIZE * 16)))
            target_chunck = f"{target_x};{target_y}"

            if target_chunck not in game_map :
                game_map[target_chunck] = generate_chunk(target_x, target_y)

            for tile in game_map[target_chunck] :
                display.blit(tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                if tile[1] in [1, 2] :
                    tile_rects.append(pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16))

    # Câmera

    true_scroll[0] += (player.x - true_scroll[0] - RESOLUTION[0] / 2) / 20
    true_scroll[1] += (player.y - true_scroll[1] - RESOLUTION[1] / 2) / 20

    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])


    # Sound effects

    if grass_sound_timer > 0 :
        grass_sound_timer -= 1

    
    # Movimentação do player

    player_movement = [0, 0]
    

    if moving_right :
        player_movement[0] += 2

    elif moving_left :
        player_movement[0] -= 2


    for jumper in jumper_objs :
        jumper.render(display, scroll)
        if jumper.collision_test(player.obj.rect) :
            momentum = -8

    display_r = pygame.Rect(scroll[0], scroll[1], RESOLUTION[0], RESOLUTION[1])
    
    for enemy in enimies_objs :
        if display_r.colliderect(enemy[1].obj.rect) :
            enemy[0] += 0.2
            if enemy[0] > 3 :
                enemy[0] = 3

            enemy_movement = [0, enemy[0]]

            if player.x > enemy[1].x - 5 :
                enemy_movement[0] = 1
            
            elif player.x < enemy[1].x + 5:
                enemy_movement[0] = -1

            e_collision_types = enemy[1].move(enemy_movement, tile_rects)
            if e_collision_types["bottom"] :
                enemy[0] = 0

            enemy[1].display(display, scroll)

            if player.obj.rect.colliderect(enemy[1].obj.rect) :
                momentum = -4


        


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
                jump_sound.play()

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

        if player_movement[0] != 0 and grass_sound_timer == 0 :
            grass_sound_timer = 30
            random.choice(grass_sounds).play()
            

    else :
        air_timer += 1
        player_movement[1] += momentum


    if momentum > 5 :
        momentum = 5


    collision_types = player.move(player_movement, tile_rects) # Definição de movimentação

    # Renderização na tela
    player.change_frame(1)
    player.display(display, scroll)


    if player_movement[0] > 0 :
        player.set_action("run")
        player.set_flip(False)

    elif player_movement[0] < 0 :
        player.set_action("run")
        player.set_flip(True)
    
    else :
        player.set_action("idle")
    

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))

    # Configurações
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()