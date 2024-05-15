"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Constants for game
"""

# game window dimensions
WIDTH = 580
HEIGHT = 690
CENTER = WIDTH / 2
# number of player lives
START_LIVES = 3
# Game states
PAUSED = 0
IN_PLAY = 1
GAME_OVER = 2
END_OF_LEVEL_DELAY = 150
# Width of each screen grid
GRID_WIDTH = 20
# Frame rate
FRAME_REFRESH = 60
# Timers in screen refreshes
DISPLAY_FRUIT = FRAME_REFRESH * 7     # 7 seconds
CHASE_TIMER = FRAME_REFRESH * 20    # 20 seconds - timer
SCATTER_TIMER = FRAME_REFRESH * 10  # 10 seconds - timer
FRIGHT_TIMER = FRAME_REFRESH * 10		# frame count
CATCH_TIMER = FRAME_REFRESH * 3     # 3 seconds
NEW_LIFE_TIMER = FRAME_REFRESH * 3     # 3 seconds
# Short Pause in game
DELAY = FRAME_REFRESH           # 1 second
# Points to get a new life - up to a max of 5
NEW_LIFE_INTERVAL = 10000
# Direction of movement - emulate an enum
HOLD = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
# User selected mode
SILENT = 0
MUSIC = 1
START = 2
WAIT = 3
