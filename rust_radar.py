#!/usr/bin/python3
# -*- coiding: utf-8 -*-

'''
Рисование карты сервера игры Rust с местонахождением игроков на ней.
Создано mohaxsuh.
'''

from sys import exit
import time

import pygame
from pygame.locals import *
import pygame.freetype

from gps import player_info, airdrop_info, patrolhelicopter_info
from db import save_position, load_last_point
from config import SIZE

WIDTH = 1440
HEIGHT = 900

# GRID_X = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', \
          # 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', \
          # 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', \
          # 'AE', 'AF', 'AG', 'AH')
GRID_X = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', \
          'K', 'L', 'M', 'N', 'O', 'P', 'Q')
# GRID_Y = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, \
          # 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33)  
# GRID_Y = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
GRID_Y = tuple([x for x in range(0, len(GRID_X))])

MAP_SIZE = SIZE
IMAGE_SIZE = 1440
STEP_GRID = int(MAP_SIZE / len(GRID_X))
SCALE = IMAGE_SIZE / MAP_SIZE
SENTER_X = int(IMAGE_SIZE/2)
SENTER_Y = int(IMAGE_SIZE/2)
HALF_PLUS = MAP_SIZE // 2
HALF_MINUS = MAP_SIZE // -2
Gamers = []
airdrops = []
patrols = []
identifier = 1001
SPRITE_IMAGE_FILENAME = 'map.png'   # 'map.jpg'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# font = pygame.font.SysFont("arial", 20)
pygame.freetype.init()
font = pygame.freetype.Font("NotoSerif-BoldItalic.ttf", 20, ucs4=True)

sprite = pygame.image.load(SPRITE_IMAGE_FILENAME).convert()

clock = pygame.time.Clock()

X, Y = 0, 0
m_x_start, m_y_start = None, None

last_pos_players = {}

time_loop = time.time()
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == pygame.KEYUP \
                and event.key == pygame.K_s:
            pygame.image.save(screen, 'day.png')

    now = time.time() - time_loop
    # if Gamers and now >= 4:
        # Gamers = player_info(Gamers)
        # time_loop = time.time()
        # # print(Gamers)
    # elif not Gamers and now >= 4:
        # Gamers = player_info()
        # time_loop = time.time()
    
    if now >= 4:
        Gamers = player_info(idnt=identifier)
        identifier += 1
        time_loop = time.time()

    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_x = int((mouse_pos_x - (X + SENTER_X)) / SCALE)
    mouse_y = int(((Y + SENTER_Y) - mouse_pos_y) / SCALE)
    # print(mouse_x, mouse_y)

    screen.fill((18, 64, 77))
    screen.blit(sprite, (X, Y))
    gamer_pool = []
    for gamer in Gamers:
        gmr_x = int(X + SENTER_X + gamer.x * SCALE)
        gmr_y = int(Y + SENTER_Y - gamer.y * SCALE)
        pygame.draw.circle(screen, (255, 69, 0), (gmr_x, gmr_y), 5)

        if abs(mouse_x - gamer.x) <= 30 and abs(mouse_y - gamer.y) <= 30:
            gamer_pool.append(gamer)
        
        # save position player
        last_pos = last_pos_players.get(gamer.steamid)
        if last_pos:
            if last_pos[0] != gamer.x or last_pos[1] != gamer.y:
                last_pos_players[gamer.steamid] = (gamer.x, gamer.y)
                save_position(gamer)
        else:
            last_pos = load_last_point(gamer)
            if last_pos:
                last_pos_players[gamer.steamid] = (gamer.x, gamer.y)
                if last_pos != (gamer.x, gamer.y):
                    save_position(gamer)
            else:
                last_pos_players[gamer.steamid] = (gamer.x, gamer.y)
                save_position(gamer)

    if now >= 4:
        airdrops = airdrop_info(idnt=identifier+10)
        identifier += 1
        patrols = patrolhelicopter_info(idnt=identifier+20)
        identifier += 1

    for air_cor in airdrops:
        air_x, air_y = air_cor
        d_air_x = int(X + SENTER_X + air_x * SCALE)
        d_air_y = int(Y + SENTER_Y - air_y * SCALE)
        pygame.draw.circle(screen, (0, 0, 255), (d_air_x, d_air_y), 5)

        air_name_x = '-'
        air_name_y = '-'
        if HALF_MINUS <= air_x <= HALF_PLUS and \
                HALF_MINUS <= air_y <= HALF_PLUS:
            real_x = HALF_PLUS + air_x
            real_y = HALF_PLUS - air_y

            square_x = int(real_x / STEP_GRID)
            square_y = int(real_y / STEP_GRID)
            air_name_x = GRID_X[square_x]
            air_name_y = GRID_Y[square_y]
        advanced = ' ({}{})'.format(air_name_x, air_name_y)
        text_surface_air = font.render(advanced, (1, 248, 182))
        if abs(mouse_x - air_x) <= 30 and abs(mouse_y - air_y) <= 30:
            screen.blit(text_surface_air[0],
                (d_air_x-text_surface_air[0].get_width()//2, d_air_y-25)
            )

    player_out = 1
    fon_for_names = 0
    for player in gamer_pool:
        name_x = '-'
        name_y = '-'
        if HALF_MINUS <= player.x <= HALF_PLUS and \
                HALF_MINUS <= player.y <= HALF_PLUS:
            real_x = HALF_PLUS + player.x
            real_y = HALF_PLUS - player.y

            square_x = int(real_x / STEP_GRID)
            square_y = int(real_y / STEP_GRID)
            name_x = GRID_X[square_x]
            name_y = GRID_Y[square_y]
            # print('{} [{}, {}]'.format(gamer.nic, gamer.x, gamer.y))

        advanced = ' ({}{})'.format(name_x, name_y)
        
        text_surface = font.render(player.nic+advanced, (0, 0, 0))
        if not fon_for_names:
            pygame.draw.rect(screen, (255, 255, 215), (20, 20, 250, 300))
            fon_for_names = 1
        screen.blit(text_surface[0], (25, player_out * 25))
        player_out += 1

    for patrol in patrols:
        pat_x, pat_y = patrol
        d_pat_x = int(X + SENTER_X + pat_x * SCALE)
        d_pat_y = int(Y + SENTER_Y - pat_y * SCALE)
        pygame.draw.circle(screen, (255, 0, 255), (d_pat_x, d_pat_y), 5)

    time_passed = clock.tick(30)
    # time_passed_seconds = time_passed / 1000.0

    if pygame.mouse.get_pressed()[0]:
        m_x_cur, m_y_cur = pygame.mouse.get_pos()

        if m_x_start is None or m_y_start is None:
            m_x_start, m_y_start = m_x_cur, m_y_cur

        if (m_x_start and m_y_start) and \
            (m_x_start != m_x_cur or m_y_start != m_y_cur):
            scale_x = m_x_start - m_x_cur
            scale_y = m_y_start - m_y_cur
            X -= scale_x
            Y -= scale_y
            m_x_start, m_y_start = m_x_cur, m_y_cur

        if X > WIDTH//2:
            X = WIDTH//2
        elif X < WIDTH//2 - sprite.get_width():
            X = WIDTH//2 - sprite.get_width()

        if Y > HEIGHT//2:
            Y = HEIGHT//2
        elif Y < HEIGHT//2 - sprite.get_height():
            Y = HEIGHT//2 - sprite.get_height()
    else:
        if m_x_start is not None and m_y_start is not None :
            m_x_start, m_y_start = None, None

    pygame.display.update()
