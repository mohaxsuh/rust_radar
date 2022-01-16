#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import exit
import time

import pygame
from pygame.locals import *
import pygame.freetype

from db import load_full_tracks
from config import SIZE


player_tracks = load_full_tracks()

print('Список игроков:\n')
plrs = {}
for player in player_tracks.keys():
    print('\t', player[0], player[1])
    plrs[player[0]] = player[1]

select = input('\nВведите steamid игрока: ')
if select not in plrs:
    print('ERROR! Ответ не распознан!')
    exit()

target = player_tracks[(select, plrs[select])]


WIDTH = 1440
HEIGHT = 900

MAP_SIZE = SIZE
IMAGE_SIZE = 1440
STEP_GRID = int(MAP_SIZE / 34)
SCALE = IMAGE_SIZE / MAP_SIZE
SENTER_X = int(IMAGE_SIZE/2)
SENTER_Y = int(IMAGE_SIZE/2)
HALF_PLUS = MAP_SIZE // 2
HALF_MINUS = MAP_SIZE // -2

SPRITE_IMAGE_FILENAME = 'map.png'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
sprite = pygame.image.load(SPRITE_IMAGE_FILENAME).convert()
clock = pygame.time.Clock()
X, Y = 0, 0
m_x_start, m_y_start = None, None
time_loop = time.time()

points = []
steps = iter(target)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    now = time.time() - time_loop
    if now >= 0.01:
        time_loop = time.time()
        try:
            step = next(steps)
            points.append(step[:2])
            if len(points) > 100:
                del points[0]
        except StopIteration:
            steps = iter(target)
            points = []
    
    screen.fill((18, 64, 77))
    screen.blit(sprite, (X, Y))
    
    new_points = []
    for point in points:
        pat_x, pat_y = point
        d_pat_x = int(X + SENTER_X + pat_x * SCALE)
        d_pat_y = int(Y + SENTER_Y - pat_y * SCALE)
        new_points.append((d_pat_x, d_pat_y))

    if len(new_points) > 1:
        pygame.draw.aalines(screen, (255, 0, 0), False, new_points, 2)
    
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

