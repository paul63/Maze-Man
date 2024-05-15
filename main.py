"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Music Monkeys Spinning Monkeys by Kevin MacLeod
"""

import pygame
from time import time
from constants import *
from score_board import ScoreBoard
from maze_grids import maze_layouts
from sprite_list import SpriteList
from pac_man import PacMan
from brick import Brick, OPENING
from dot import *
from ghost import *
import system_variables as sys

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Maze-Man (Pac-Man)')
clock = pygame.time.Clock()
running = True

score_board = ScoreBoard()
score_board.lives = START_LIVES
score_board.load_high_score()

music = pygame.mixer.Sound('sounds/MazeTune.mp3')
music.set_volume(0.25)
game_over = pygame.mixer.Sound('sounds/GameOver.wav')
level_over = pygame.mixer.Sound('sounds/LevelCompleted.wav')
energiser_eaten = pygame.mixer.Sound('sounds/eatEnergiser.wav')

grid = SpriteList()
dots = SpriteList()
ghosts = SpriteList()

pacman = None


def timer_func(func):
    # for decorating functions
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {t2 - t1:.5f}s')
        return result
    return wrap_func


def initialise_new_game():
    # Set defaults for new game
    score_board.score = 0
    score_board.level = 1
    score_board.lives = START_LIVES
    set_for_level()
    # reset timers
    sys.chase_timer = CHASE_TIMER
    sys.scatter_timer = SCATTER_TIMER
    sys.fright_length = FRIGHT_TIMER
    sys.new_life_target = NEW_LIFE_INTERVAL
    score_board.game_state = PAUSED


def create_maze():
    # Generate the maze elements and set up for the new maze
    global pacman
    level = (score_board.level - 1) % len(maze_layouts)
    maze = maze_layouts[level]
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == "X":
                grid.add(Brick(level, x, y))
            elif char == "O":
                grid.add(Brick(OPENING, x, y))
            elif char == "Y":
                pacman = PacMan(x, y)
            elif char == ".":
                dots.add(Dot(DOT, x, y))
            elif char == "E":
                dots.add(Dot(ENERGISER, x, y))
            elif char == "F":
                sys.fruit_position = (x, y)
            elif char == "B":
                ghosts.add(Ghost(BLINKY, x, y))
            elif char == "I":
                ghosts.add(Ghost(INKY, x, y))
            elif char == "P":
                ghosts.add(Ghost(PINKY, x, y))
            elif char == "C":
                ghosts.add(Ghost(CLYDE, x, y))


def set_for_level():
    # resetGame board - called at launch and at the end of each level
    # Clear existing elements
    grid.clear_all()
    dots.clear_all()
    ghosts.clear_all()
    # Stop player movement
    sys.next_direction = HOLD
    # Reset number of scatters invoked for new level
    sys.scatter_count = 0
    #  reset in case grid cleared while in fright mode
    sys.ghosts_eaten = 0
    # reset dots_eaten counter for new level
    sys.dots_eaten = 0
    sys.level_cleared = False
    create_maze()
    sys.current_ghost_mode = CHASE
    sys.mode_timer = CHASE_TIMER
    sys.fright_counter = 0
    # set pacman and ghost speed for level slow down for first 5 levels
    if score_board.level < 6:
        speed_percent = 100 - (6 - score_board.level) * 5
        pacman.set_speed_percent(speed_percent)
        for ghost in ghosts.items:
            ghost.set_speed_percent(speed_percent)


initialise_new_game()


def clear_done_objects():
    dots.clear_done()


def get_direction(direction):
    # Check keyboard for player instructions
    if score_board.game_state != GAME_OVER:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            direction = LEFT
        elif keys[pygame.K_RIGHT]:
            direction = RIGHT
        elif keys[pygame.K_UP]:
            direction = UP
        elif keys[pygame.K_DOWN]:
            direction = DOWN
        return direction


def snap_to_grid(pos, speed):
    # Check the position ( x or y) of the object and if near a grid (20x20) edge reposition grid center
    # this is so that object can change direction if required
    ipos = round(pos)
    dist = pos - ipos // 20 * 20
    # check if near forward grid edge
    if dist >= 20 - speed / 1.5:
        # Move to next grid position
        ipos = ipos + 20 - ipos % 20
        return ipos
    elif dist <= speed / 1.5:
        # Move back to last grid position
        ipos = ipos - ipos % 20
        return ipos
    else:
        return pos


def try_to_move(direction, game_object):
    # Try to move in the direction given
    # return Ture if object can move
    x_vel = 0
    y_vel = 0
    if direction != game_object.current_direction:
        # snap to grid so if required and possible can change direction
        game_object.x = snap_to_grid(game_object.x, game_object.speed)
        game_object.y = snap_to_grid(game_object.y, game_object.speed)
    if direction == RIGHT:
        x_vel = game_object.speed
    elif direction == LEFT:
        x_vel = -game_object.speed
    elif direction == UP:
        y_vel = -game_object.speed
    elif direction == DOWN:
        y_vel = game_object.speed

    game_object.x += x_vel
    game_object.y += y_vel

    # Check if hit a wall and if so stop at wall
    for brick in grid.items:
        # check if we have hit a wall
        if game_object.collide_rect(brick):
            # move back to next grid position
            if direction == LEFT or direction == RIGHT:
                if game_object.x % 20 > 10:
                    # move to right edge
                    game_object.x = brick.x + 20
                else:
                    game_object.x = brick.x - 20
                    # move to left edge
            else:
                if game_object.y % 20 > 10:
                    # move to bottom edge
                    game_object.y = brick.y + 20
                else:
                    # move to top edge
                    game_object.y = brick.y - 20
            return False
    if game_object.current_direction != direction:
        game_object.current_direction = direction
        game_object.change_direction = True
    return True


def move_pacman(next_direction):
    # try and move the packman in the direction provided
    if not try_to_move(next_direction, pacman):
        try_to_move(pacman.current_direction, pacman)
    # Check if exiting screen left or right
    if pacman.x < 2:
        pacman.x = WIDTH - 22
    elif pacman.x > WIDTH - 22:
        pacman.x = 2


def move_ghost(ghost, direction):
    # try and move the ghost in the direction provided
    # return True if ghost can move
    if not try_to_move(direction, ghost):
        return False
    ghost.set_direction_image(direction)
    if ghost.x < 2:
        ghost.x = WIDTH - 22
    elif ghost.x > WIDTH - 22:
        ghost.x = 2
    return True


def ghost_fright_over():
    # fright mode over - return to ghosts default state
    sys.ghosts_eaten = 0
    for ghost in ghosts.items:
        ghost.set_default_mode(False)
    sys.mode_timer = sys.chase_timer


def change_ghost_mode():
    # called when timer expired to change ghost mode
    if sys.scatter_count < 3 and sys.current_ghost_mode == CHASE:
        # Put ghosts in scatter mode
        sys.scatter_count += 1
        sys.current_ghost_mode = SCATTER
        sys.mode_timer = sys.scatter_timer
        for ghost in ghosts.items:
            ghost.set_scatter_mode()
    else:
        # Put ghosts in chase mode
        sys.current_ghost_mode = CHASE
        sys.mode_timer = sys.chase_timer
        for ghost in ghosts.items:
            ghost.set_default_mode(False)


def increase_score(points):
    # increase the score and add a new life if target reached
    score_board.score += points
    if score_board.score >= sys.new_life_target:
        sys.new_life_target += NEW_LIFE_INTERVAL
        score_board.set_new_life()


def update_game():
    # Called each screen refresh
    # Check for pacman caught
    if pacman.done:
        if score_board.lives < 1:
            score_board.game_state = GAME_OVER
            music.stop()
            game_over.play()
        else:
            pacman.return_to_start()
            sys.next_direction = HOLD
            for ghost in ghosts.items:
                ghost.jump_to_start()
            ghost_fright_over()
            return

    if not sys.level_cleared:
        # get user instruction and move packman
        sys.next_direction = get_direction(sys.next_direction)
        if sys.next_direction != HOLD and not pacman.caught():
            move_pacman(sys.next_direction)
        pacman.update()

    if not pacman.caught():
        # Game loop
        clear_done_objects()
        if dots.number() == 0:
            # End of level
            if not sys.level_cleared:
                # set a timer delay
                sys.level_cleared = True
                sys.end_of_level_timer = END_OF_LEVEL_DELAY
                level_over.play()

            sys.end_of_level_timer -= 1
            if sys.end_of_level_timer <= 0:
                # set for next level
                score_board.level += 1
                set_for_level()
                # increase chase length by 2 seconds
                sys.chase_timer += FRAME_REFRESH * 2
                # reduce scatter and frightened length
                if sys.scatter_timer > FRIGHT_TIMER * 5:
                    sys.scatter_timer -= FRAME_REFRESH / 2
                if sys.fright_length > FRAME_REFRESH * 5:
                    sys.fright_length -= FRAME_REFRESH / 2
            else:
                return

        # Check if player and a ghost have collided
        # If ghost is in fright mode then we have caught it
        # increase score, display catch score and set to return to pen
        # else player has been caught
        for ghost in ghosts.items:
            if pacman.collide_rect(ghost):
                if ghost.mode == FRIGHTENED:
                    sys.ghosts_eaten += 1
                    increase_score(ghost_score[sys.ghosts_eaten - 1])
                    score_board.set_catch_score(ghost_score[sys.ghosts_eaten - 1], (ghost.x, ghost.y))
                    ghost.return_to_pen()
                elif ghost.mode != CAUGHT:
                    # pacman caught
                    pacman.set_caught()
                    score_board.lives -= 1

        # Check if in fright mode and if timer expired
        if Ghost.fright_timer > 0:
            Ghost.fright_timer -= 1
            if Ghost.fright_timer <= 0:
                ghost_fright_over()
        else:
            sys.mode_timer -= 1
            if sys.mode_timer <= 0:
                change_ghost_mode()

        for dot in dots.items:
            if dot.dtype == FRUIT:
                # update fruit display timer
                dot.update()
            # check if packman has eaten the dot
            if pacman.collide_rect(dot):
                increase_score(dot.score)
                dot.done = True
                sys.dots_eaten += 1
                for ghost in ghosts.items:
                    # reduce delay to release for penned ghosts
                    ghost.reduce_delay()
                # Check if just eaten an energiser
                if dot.dtype == ENERGISER:
                    # put ghosts in fright mode
                    energiser_eaten.play()
                    for ghost in ghosts.items:
                        ghost.set_frightened_mode()
                    Ghost.fright_timer = sys.fright_length
                elif dot.dtype == FRUIT:
                    score_board.set_catch_score(dot.score, (dot.x, dot.y))
                # check if fruit to be displayed
                if sys.dots_eaten == 70 or sys.dots_eaten == 170:
                    dots.add(Dot(FRUIT, sys.fruit_position[0], sys.fruit_position[1], score_board.level))
        for ghost in ghosts.items:
            # set movement direction for each ghost
            direction = ghost.set_dirction(pacman)
            if not move_ghost(ghost, direction):
                # try to continue to move in current direction
                if not move_ghost(ghost, ghost.current_direction):
                    # Cannot move in the selected direction so test other directions
                    order = ghost.get_order()
                    for i in range(0, 4):
                        if order[i] == LEFT and ghost.current_direction == RIGHT:
                            continue
                        if order[i] == RIGHT and ghost.current_direction == LEFT:
                            continue
                        if order[i] == UP and ghost.current_direction == DOWN:
                            continue
                        if order[i] == DOWN and ghost.current_direction == UP:
                            continue
                        moved = move_ghost(ghost, order[i])
                        if moved:
                            break
                    if not moved:
                        # reverse direction if ghost cannot move in any of the tried directions
                        if ghost.current_direction == LEFT:
                            direction = RIGHT
                        elif ghost.current_direction == RIGHT:
                            direction = LEFT
                        elif ghost.current_direction == UP:
                            direction = DOWN
                        elif ghost.current_direction == DOWN:
                            direction = UP
                        move_ghost(ghost, direction)


def draw_game_screen():
    # fill the screen with black to clear last frame
    screen.fill("black")
    # draw frame
    grid.draw(screen)
    dots.draw(screen)
    ghosts.draw(screen)
    pacman.draw(screen)
    draw_fruit_for_level(screen, score_board.level)
    score_board.draw(screen)
    if sys.level_cleared:
        score_board.draw_level_over(screen)


def game_loop():
    if score_board.game_state == IN_PLAY:
        update_game()
        draw_game_screen()
    elif score_board.game_state == GAME_OVER:
        start, play = score_board.draw_game_over(screen)
        if start == START:
            initialise_new_game()
            if play == MUSIC:
                music.play(-1)
    else:
        start, play = score_board.draw_game_instructions(screen)
        if start == START:
            score_board.game_state = IN_PLAY
            if play == MUSIC:
                music.play(-1)
    pygame.display.flip()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X so end game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game_loop()
    clock.tick(FRAME_REFRESH)  # limits FPS to 60 FPS

pygame.quit()
