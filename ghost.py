"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Ghost class and functions
"""


import pygame
from game_sprite import GameSprite
from constants import *
import random

pygame.init()

# Speed reached at level 6 and above
ghost_mex_speed = 3.33

# number of frames between change of random target
random_interval = 250
# Ghosts will look in the direction of movement
ghost_image = [
    [   # blinky
        pygame.image.load('images/BlinkyUp.png'),    # For hold
        pygame.image.load('images/BlinkyLeft.png'),
        pygame.image.load('images/BlinkyRight.png'),
        pygame.image.load('images/BlinkyUp.png'),
        pygame.image.load('images/BlinkyDown.png')
    ],
    [   # pinky
        pygame.image.load('images/PinkyUp.png'),
        pygame.image.load('images/PinkyLeft.png'),
        pygame.image.load('images/PinkyRight.png'),
        pygame.image.load('images/PinkyUp.png'),
        pygame.image.load('images/PinkyDown.png')
    ],
    [   # inky
        pygame.image.load('images/InkyUp.png'),
        pygame.image.load('images/InkyLeft.png'),
        pygame.image.load('images/InkyRight.png'),
        pygame.image.load('images/InkyUp.png'),
        pygame.image.load('images/InkyDown.png')
    ],
    [   # clyde
        pygame.image.load('images/ClydeUp.png'),
        pygame.image.load('images/ClydeLeft.png'),
        pygame.image.load('images/ClydeRight.png'),
        pygame.image.load('images/ClydeUp.png'),
        pygame.image.load('images/ClydeDown.png')
    ]
]

frightened = pygame.image.load('images/frightened.png')
frightenedW = pygame.image.load('images/frightened2.png')
caught = pygame.image.load('images/caught.png')

caught_sound = pygame.mixer.Sound('sounds/eatghost.wav')


# Ghosts
BLINKY = 0
PINKY = 1
INKY = 2
CLYDE = 3

# Score increases the more ghosts caught in a fright cycle
ghost_score = [200, 400, 800, 1600]
# The number of dots eaten before the release of each ghost type
delay_to_release = [1, 10, 30, 90]
delay_to_release_after_caught = [1, 5, 15, 25]

# Ghost modes
CHASE = 0
SCATTER = 1
FRIGHTENED = 2
RANDOM = 3
CAUGHT = 4
TO_PEN = 5

# Used if ghost cannot move towards the target to cycle through to find a
# direction that it can move
cycle_order = [
    # for target x > 0 and > target y > 0
    [RIGHT, DOWN, LEFT, UP],
    # for target x < 0 and > target y > 0
    [LEFT, DOWN, RIGHT, UP],
    # for target x > 0 and > target y < 0
    [RIGHT, UP, LEFT, DOWN],
    # for target x < 0 and > target y < 0
    [LEFT, UP, RIGHT, DOWN],
    # for target x > 0 and < target y > 0
    [DOWN, RIGHT, UP, LEFT],
    # for target x < 0 and < target y > 0
    [DOWN, LEFT, UP, RIGHT],
    # for target x > 0 and < target y < 0
    [UP, RIGHT, DOWN, LEFT],
    # for target x < 0 and < target y < 0
    [UP, LEFT, DOWN, RIGHT]
]


class Ghost(GameSprite):
    # Set when an energiser eaten
    fright_timer = 0
    # The positions ghosts move to when released from pen
    ghost_exit_point = ()

    def __init__(self, gtype, x, y):
        self.gtype = gtype
        # set grid position
        x = x * 20 + 20
        y = y * 20 + 40
        if gtype == BLINKY:
            # Center between bricks
            x -= 10
            # Set the ghost exit point
            Ghost.ghost_exit_point = (x, y)
        # use frightened just to initialise
        super().__init__(frightened, x, y)
        self.start_position = (x, y)
        self.speed = ghost_mex_speed
        self.speed_for_level = ghost_mex_speed
        # Just set to a random position as will be set as soon as ghost released
        self.target = (400, 600)
        self.last_target = (400, 600)
        self.mode = CHASE
        self.current_direction = HOLD
        self.delay = 0
        self.set_default_mode(False)
        self.random_timer = random_interval
        self.set_delay()

    def reverse_direction(self):
        # reverses the direction of movement - called on mode changes
        if self.current_direction == LEFT:
            self.current_direction = RIGHT
        elif self.current_direction == RIGHT:
            self.current_direction = LEFT
        elif self.current_direction == UP:
            self.current_direction = DOWN
        else:
            self.current_direction = UP

    def set_default_mode(self, reverse):
        # Set default image and mode of movement
        if self.mode != CAUGHT:
            self.image = ghost_image[self.gtype][HOLD]
            if self.gtype == CLYDE:
                self.mode = RANDOM
            else:
                self.mode = CHASE
            if reverse:
                self.reverse_direction()
            self.speed = self.speed_for_level

    def set_speed_percent(self, perc):
        # Adjust the speed of the ghost
        if perc <= 100 and perc >= 0:
            self.speed = ghost_mex_speed * perc / 100
            self.speed_for_level = self.speed

    def set_scatter_mode(self):
        # Set scatter mode
        if self.mode != CAUGHT:
            self.mode = SCATTER
            self.reverse_direction()

    def set_frightened_mode(self):
        # set frightened mode
        self.mode = FRIGHTENED
        self.image = frightened
        self.reverse_direction()
        # reduce speed in frightened mode
        self.speed = self.speed * 0.66

    def return_to_pen(self):
        # Ghost caught so set to return to pen
        caught_sound.play()
        self.image = caught
        self.mode = CAUGHT
        self.speed = ghost_mex_speed * 2

    def set_delay(self):
        # Set the delay in dots eaten before ghost can leave the pen
        self.delay = delay_to_release[self.gtype]

    def reduce_delay(self):
        # called when a dot is eaten
        if self.delay > 0:
            self.delay -= 1

    def jump_to_start(self):
        # return ghost to its start position
        self.x = self.start_position[0]
        self.y = self.start_position[1]
        self.mode = CHASE
        self.set_default_mode(False)
        self.set_delay()
        self.speed = self.speed_for_level
        self.current_direction = HOLD

    def set_direction_image(self, direction):
        if self.mode != FRIGHTENED and self.mode != CAUGHT:
            # Set image for direction
            self.image = ghost_image[self.gtype][direction]

    def set_dirction(self, pacman):
        if self.delay <= 0:
            # If currently hold then in the pen so position ghost outside the pen
            # If self.x == self.start_position[0] and self.y == self.start_position[1]:
            if self.current_direction == HOLD:
                self.x = Ghost.ghost_exit_point[0]
                self.y = Ghost.ghost_exit_point[1]
            # Set target grid cell based on ghost and mode
            if self.mode == CHASE:
                if self.gtype == BLINKY or self.gtype == CLYDE:
                    # never put in chase mode but here as a catch-all
                    # set target to players current position
                    self.target = (pacman.x, pacman.y)
                elif self.gtype == PINKY:
                    # set target ahead of player
                    if pacman.current_direction == LEFT or pacman.current_direction == HOLD:
                        self.target = (pacman.x - 80, pacman.y)
                    elif pacman.current_direction == RIGHT:
                        self.target = (pacman.x + 80, pacman.y)
                    elif pacman.current_direction == UP:
                        self.target = (pacman.x, pacman.y - 80)
                    elif pacman.current_direction == DOWN:
                        self.target = (pacman.x, pacman.y + 80)
                elif self.gtype == INKY:
                    # set target behind player
                    if pacman.current_direction == LEFT or pacman.current_direction == HOLD:
                        self.target = (pacman.x + 80, pacman.y)
                    elif pacman.current_direction == RIGHT:
                        self.target = (pacman.x - 80, pacman.y)
                    elif pacman.current_direction == UP:
                        self.target = (pacman.x, pacman.y + 80)
                    elif pacman.current_direction == DOWN:
                        self.target = (pacman.x, pacman.y - 80)
            elif self.mode == SCATTER:
                # In scatter mode so set each ghosts target as a corner of the maze
                if self.gtype == BLINKY:
                    self.target = (-200, -100)
                elif self.gtype == PINKY:
                    self.target = (WIDTH + 200, -100)
                elif self.gtype == INKY:
                    self.target = (-200, HEIGHT + 250)
                elif self.gtype == CLYDE:
                    self.target = (WIDTH + 200, HEIGHT + 250)
            elif self.mode == RANDOM or self.mode == FRIGHTENED:
                # Move to a random target at each interval
                self.random_timer += 1
                if self.random_timer >= random_interval - 1:
                    self.last_target = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
                    self.random_timer = 0
                    self.target = self.last_target
                if self.mode == FRIGHTENED and Ghost.fright_timer < 120:
                    if Ghost.fright_timer % 15 == 0:
                        if self.image == frightened:
                            self.image = frightenedW
                        else:
                            self.image = frightened
            elif self.mode == CAUGHT:
                # Ghost has been caught so see if reached exit_point
                if abs(Ghost.ghost_exit_point[0] - self.x) < 20 and abs(Ghost.ghost_exit_point[1] - self.y) < 20:
                    self.x = self.start_position[0]
                    self.y = self.start_position[1]
                    self.mode = CHASE
                    self.set_default_mode(False)
                    self.current_direction = HOLD
                    self.delay = delay_to_release_after_caught[self.gtype]
                # OK to leave as exit_point as will be changed next refresh
                self.target = Ghost.ghost_exit_point

            # set direction to go to target and return
            tx = self.target[0] - self.x
            ty = self.target[1] - self.y
            # Test to see if just escaped so default to either left or right
            if self.current_direction == HOLD:
                if tx > 0:
                    self.current_direction = RIGHT
                else:
                    self.current_direction = LEFT
            if abs(tx) > abs(ty):
                # See if ghost can go in x direction of largest distance
                # if not try and go y direction
                if self.target[0] > self.x:
                    if self.current_direction != LEFT:
                        go_to = RIGHT
                    elif self.target[1] > self.y:
                        go_to = DOWN
                    else:
                        go_to = UP
                elif self.current_direction != RIGHT:
                    go_to = LEFT
                elif self.target[1] < self.y:
                    go_to = UP
                else:
                    go_to = DOWN
            else:
                if self.target[1] > self.y:
                    if self.current_direction != UP:
                        go_to = DOWN
                    elif self.target[0] > self.x:
                        go_to = RIGHT
                    else:
                        go_to = LEFT
                elif self.current_direction != DOWN:
                    go_to = UP
                elif self.target[0] > self.x:
                    go_to = RIGHT
                else:
                    go_to = LEFT
            return go_to
        else:
            return HOLD

    def get_order(self):
        # set new direction sequence to try
        tx = self.target[0] - self.x
        ty = self.target[1] - self.y
        if tx > 0 and ty > 0 and abs(tx) > abs(ty):
            order = cycle_order[0]
        elif tx > 0 and ty > 0 and abs(tx) < abs(ty):
            order = cycle_order[4]
        elif tx < 0 and ty > 0 and abs(tx) > abs(ty):
            order = cycle_order[1]
        elif tx < 0 and ty > 0 and abs(tx) < abs(ty):
            order = cycle_order[5]
        elif tx > 0 and ty < 0 and abs(tx) > abs(ty):
            order = cycle_order[2]
        elif tx > 0 and ty < 0 and abs(tx) < abs(ty):
            order = cycle_order[6]
        elif tx < 0 and ty < 0 and abs(tx) > abs(ty):
            order = cycle_order[3]
        else:
            order = cycle_order[7]
        return order
