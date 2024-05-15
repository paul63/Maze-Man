"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Brick class used for maze walls
"""

import pygame
from game_sprite import GameSprite

pygame.init()

brick_image = [
	pygame.image.load('images/brick0.png'),
	pygame.image.load('images/brick1.png'),
	pygame.image.load('images/brick2.png'),
	pygame.image.load('images/brick3.png'),
	pygame.image.load('images/penOpening.png')
]

# position of opening image
BRICK = 1
OPENING = 4


class Brick(GameSprite):
	def __init__(self, element, x, y):
		image = brick_image[element]
		x = x * 20 + 20
		y = y * 20 + 40
		super().__init__(image, x, y)
		if element < 4:
			self.type = BRICK
		else:
			self.type = OPENING
