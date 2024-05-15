"""
Author Paul Brace April 2024
PacMan game developed using PyGame
PacMan class and functions
"""

import pygame
from constants import *
from game_sprite import GameSprite

pygame.init()

# Speed reached at level 6 and above
player_max_speed = 3.66
# Timer used to display packman animation on caught
caught_timer_default = int(FRAME_REFRESH * 1.5)

life_lost = pygame.mixer.Sound('sounds/lifeLost.wav')
pacman_whole = pygame.image.load('images/pacWhole.png')

pacman_moving = [
    pygame.image.load('images/pacOpenLeft.png'),
    pygame.image.load('images/pacOpenRight.png'),
    pygame.image.load('images/pacOpenUp.png'),
    pygame.image.load('images/pacOpenDown.png')
]

caught_image = [
    pygame.image.load('images/lost1.png'),
    pygame.image.load('images/lost2.png'),
    pygame.image.load('images/lost3.png'),
    pygame.image.load('images/lost4.png'),
    pygame.image.load('images/lost5.png'),
    pygame.image.load('images/lost6.png')
]


class PacMan(GameSprite):
    def __init__(self, x, y):
        # initialise positioned offset 10 to left to center between bricks
        x = x * 20 + 10
        y = y * 20 + 40
        super().__init__(pacman_whole, x, y)
        # True when whole image displayed
        self.whole = True
        self.start_position = (x, y)
        self.speed = player_max_speed
        self.speed_for_level = player_max_speed
        self._caught = False
        self.caught_timer = 0
        self.frame_count = 0
        self.current_direction = HOLD
        self.change_direction = False

    def set_speed_percent(self, perc):
        # Adjust the speed of the player
        if perc <= 100 and perc >= 0:
            self.speed = player_max_speed * perc / 100
            self.speed_for_level = self.speed

    def set_caught(self):
        # PacMan has been caught so start animation
        self._caught = True
        life_lost.play()
        self.caught_timer = caught_timer_default
        self.image = pacman_whole
        self.whole = True

    def caught(self):
        return self._caught

    def return_to_start(self):
        # reposition at start point
        self.x = self.start_position[0]
        self.y = self.start_position[1]
        self.speed = self.speed_for_level
        self.current_direction = HOLD
        self.image = pacman_whole
        self.whole = True
        self._caught = False
        self.done = False

    def update(self):
        # If we have been caught then animate image
        if self._caught:
            self.caught_timer -= 1
            if self.caught_timer <= -6:
                self.done = True
            elif self.caught_timer % 6 == 0:
                self.image = caught_image[5 - self.caught_timer // 15]
        else:
            # Set image
            if self.current_direction == HOLD:
                self.image = pacman_whole
            else:
                self.frame_count += 1
                if self.frame_count > 10 or self.change_direction:
                    self.frame_count = 0
                    self.change_direction = False
                    if self.whole:
                        self.image = pacman_moving[self.current_direction - 1]
                        self.whole = False
                    else:
                        self.image = pacman_whole
                        self.whole = True
