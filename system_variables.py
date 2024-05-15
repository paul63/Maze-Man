"""
Author Paul Brace April 2024
PacMan game developed using PyGame
System wide "global" variables
"""

# position of fruit for current level
fruit_position = (0, 0)
# number of dots eaten for current level
dots_eaten = 0
# Number of scatters so far in level
scatter_count = 0
# Number of ghosts eaten during fright
ghosts_eaten = 0
# Timers for the different modes
chase_timer = None
scatter_timer = None
mode_timer = None
fright_length = None
# Current score target to eran a new life
new_life_target = None
# Current mode of play
current_ghost_mode = None
# True when all dots eaten
level_cleared = False
# Timer for end of level message to be displayed
end_of_level_timer = 0
# direction selected by player
next_direction = None
