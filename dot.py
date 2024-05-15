"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Dot class used to display dots, energisers and fruit
"""

import pygame
from game_sprite import GameSprite
from constants import *

pygame.init()

dot_image = pygame.image.load('images/dot.png')
energiser_image = pygame.image.load('images/energiser.png')

# Dot type constants
DOT = 0
ENERGISER = 1
FRUIT = 2


fruit_image = [
    pygame.image.load('images/Cherry.png'),
    pygame.image.load('images/Strawberry.png'),
    pygame.image.load('images/Orange.png'),
    pygame.image.load('images/Apple.png'),
    pygame.image.load('images/Melon.png'),
    pygame.image.load('images/Galaxian.png'),
    pygame.image.load('images/Bell.png')
]

# Score earned for each type of fruit when eaten
fruit_score = [100, 300, 500, 700, 1000, 2000, 3000, 5000]


def draw_fruit_for_level(screen, level):
    for i in range(0, level):
        if i < 7:
            screen.blit(fruit_image[i], (WIDTH - i * 25 - 45, HEIGHT - 30))


class Dot(GameSprite):
    def __init__(self, dtype, x, y, fruit_number=1):
        self.dtype = dtype
        x = x * 20 + 20
        y = y * 20 + 40
        self.timer = 0
        image = None
        if dtype == DOT:
            image = dot_image
            self.score = 20
        elif dtype == ENERGISER:
            image = energiser_image
            self.score = 50
        elif dtype == FRUIT:
            if fruit_number > 7:
                fruit_number = 7
            image = fruit_image[fruit_number - 1]
            self.score = fruit_score[fruit_number - 1]
            # Time fruit remains on screen
            self.timer = DISPLAY_FRUIT
            # position between 2 bricks
            x = x - 10
        super().__init__(image, x, y)

    def update(self):
        if self.dtype == FRUIT:
            self.timer -= 1
            if self.timer <= 0:
                self.done = True
