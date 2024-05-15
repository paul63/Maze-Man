"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Grid layouts
"""

#  Definition of mazes and initial positions
#  X = a wall/border (no limit)
#  O = pen opening from which ghosts escape
#  . = a small dot (244 per level)
#  E = an energiser (4 per level)
#  B = ghost blinky (1 per level - start outside pen and is pen escape point - will be offset 10 to left to centralise)
#  I = ghost inky (1 per level - start in pen)
#  P = ghost pinky (1 per level - start in pen)
#  C = ghost clyde (1 per level - start in pen)
#  Y = You the player (1 per level - will be offset 10 to the left to centralise)
#  F = Position bonus fruit will appear (will be offset 10 to the left to centralise)

maze_layouts = [
[
    # MAZE 1
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "XEXXXX.XXXXX.XX.XXXXX.XXXXEX",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "XXXXXX.XX     B    XX.XXXXXX",
    "XXXXXX.XX XXXOOXXX XX.XXXXXX",
    "XXXXXX.XX XX I  XX XX.XXXXXX",
    "      .   XX  P XX   .      ",
    "XXXXXX.XX XX C  XX XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX     F    XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "XE..XX....... Y.......XX..EX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
],
[
    # MAZE 2
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X......XX..........XX......X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "XEXXXX.XX.XXXXXXXX.XX.XXXXEX",
    "X..........................X",
    "XXX.XX.XXXXX.XX.XXXXX.XX.XXX",
    "XXX.XX.XXXXX.XX.XXXXX.XX.XXX",
    "XXX.XX.XXXXX.XX.XXXXX.XX.XXX",
    "   .XX.......XX.......XX.   ",
    "XXX.XXXXX.XXXXXXXX.XXXXX.XXX",
    "XXX.XXXXX.XXXXXXXX.XXXXX.XXX",
    "XXX.          B         .XXX",
    "XXX.XXXXX XXXOOXXX XXXXX.XXX",
    "XXX.XXXXX XX I  XX XXXXX.XXX",
    "XXX.XX    XX  P XX    XX.XXX",
    "XXX.XX XX XX C  XX XX XX.XXX",
    "XXX.XX XX XXXXXXXX XX XX.XXX",
    "   ....XX     F    XX....   ",
    "XXX.XXXXXXXX.XX.XXXXXXXX.XXX",
    "XXX.XXXXXXXX.XX.XXXXXXXX.XXX",
    "XXX..........XX..........XXX",
    "XXX.XXXXX.XXXXXXXX.XXXXX.XXX",
    "XXX.XXXXX.XXXXXXXX.XXXXX.XXX",
    "X............ Y............X",
    "X.XXXX.XXXXX.XXX.XXXX.XXXX.X",
    "XEXXXX.XXXXX.XXX.XXXX.XXXXEX",
    "X.XXXX.XX....XXX...XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
],
[
    # MAZE 3
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X.........XX....XX.........X",
    "X.XXXX.XX.XX.XX.XX.XX.XXXX.X",
    "X.XXXX.XX.XX.XX.XX.XX.XXXX.X",
    "X....E.XX....XX....XX.E....X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XX.........XX.........XX.X",
    "X.XX.XXXX XXXXXXXX XXXX.XX.X",
    "X.XX.XXXX XXXXXXXX XXXX.XX.X",
    " ......       B      ...... ",
    "X.XXXX.XX XXXOOXXX XX.XXXX.X",
    "X.XXXX.XX XX I  XX XX.XXXX.X",
    "X......XX XX  P XX XX......X",
    "X XXXX.XX XX C  XX XX.XXXX X",
    "X XXXX.XX XXXXXXXX XX.XXXX X",
    "X   XX.XX     F    XX.XX   X",
    "XXX XX.XX XXXXXXXX XX.XX XXX",
    "XXX XX.XX XXXXXXXX XX.XX XXX",
    "XXX XX.......XX.......XX XXX",
    "    XX.XXXXX.XX.XXXXX.XX    ",
    "X XXXX.XXXXX.XX.XXXXX.XXXX X",
    "X XXXX.XX.... Y....XX.XXXX X",
    "X......XX.XX.XX.XX.XX......X",
    "X.XX.XXXX.XX.XX.XX.XXXX.XX.X",
    "X.XX.XXXX.XX.XX.XX.XXXX.XX.X",
    "X.XX.E....XX.XX.XX....E.XX.X",
    "X.XXXXXXX.XX....XX.XXXXXXX.X",
    "X.XXXXXXX.XXXXXXXX.XXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
],
[
    # MAZE 4
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X.........XXXXXXXX.........X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X....E.XX....XX....XX.E....X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XX.........XX.........XX.X",
    "X.XX.XXXX XXXXXXXX XXXX.XX.X",
    "X.XX.XXXX XXXXXXXX XXXX.XX.X",
    " ......       B      ...... ",
    "X.XXXX.XX XXXOOXXX XX.XXXX.X",
    "X.XXXX.XX XX I  XX XX.XXXX.X",
    "X......XX XX  P XX XX......X",
    "X.XXXX.XX XX C  XX XX.XXXX.X",
    "X.XXXX.XX XXXXXXXX XX.XXXX.X",
    "X...XX.XX     F    XX.XX...X",
    "XXX.XX.XX XXXXXXXX XX.XX.XXX",
    "XXX.XX.XX XXXXXXXX XX.XX.XXX",
    "XXX.XX.......XX.......XX.XXX",
    "X...XXXXXXXX.XX.XXXXXXXX...X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X.XXXXXXX.... Y....XXXXXXX.X",
    "X....XXXX.XX.XX.XX.XXXX....X",
    "X.XX.XXXX.XX.XX.XX.XXXX.XX.X",
    "X.XX.XXXX.XX.XX.XX.XXXX.XX.X",
    "X.XX.E.......XX.......E.XX.X",
    "X.XXXXXXX.XXXXXXXX.XXXXXXX.X",
    "X.XXXXXXX.XXXXXXXX.XXXXXXX.X",
    "X.........XXXXXXXX.........X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]
]
