"""
Author Paul Brace April 2024
ScoreBoard class for Maze-Man game
"""

import pygame
from constants import *

pygame.init()
font = "veranda"
heading = pygame.font.SysFont(font, 50, False, False)
text = pygame.font.SysFont(font, 30, False, False)
info_text = pygame.font.SysFont(font, 25, False, False)
italic = pygame.font.SysFont(font, 30, False, True)
bold = pygame.font.SysFont(font, 30, True, False)
small = pygame.font.SysFont(font, 20, False, False)
scores = pygame.font.SysFont("freesans", 15, True, False)

extra_life = pygame.mixer.Sound('sounds/extraLife.wav')

instructions = [
    "Press left, right, up and down arrows to move",
    "Avoid being caught by the ghosts",
    "Ghosts switch between chase and scatter mode",
    "Eat the dots and bonus fruit to score points",
    "Eating an energiser puts ghosts into fright mode",
    "Catch ghosts in fright mode to score points",
    "Clear all dots to move to next level",
    "Scores:",
    "    Small dot = 20 points   Energiser = 50 points",
    "    Ghost from 200 to 1,600 points",
    "    Fruit from 100 to 5,000 points"]

further_info = [
    "Further information:",
    "The ghosts alternate between chase mode and scatter mode.",
    "In scatter mode they head for their designated corner",
    "  this happens 3 times a level.",
    "Chase mode initially lasts 20 seconds and scatter 10 seconds.",
    "Chase mode time increases and scatter reduces each level.",
    "In chase mode:",
    "    Blinky (red) will head directly for you.",
    "    Pinky (pink) tries to get ahead of you.",
    "    Inky (blue) tries to get behind you.",
    "    Clyde (orange) just wanders about randomly.",
    "Ghost fright mode initially lasts 10 seconds but reduces each level.",
    "Ghosts start flashing 2 seconds before the end of fright mode.",
    "3 bonus fruits appear for 7 seconds on each level and get more",
    "  valuable in higher levels.",
    "You get an extra life every 10,000 points - max 5 at any time."]


class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.high_saved = False
        # score of last ghost or fruit eaten for display
        self.catch_score = 0
        # True when catch score displayed
        self.display_catch_score = False
        self.catch_position = (0, 0)
        self.catch_timer = 0
        self.new_life_timer = 0
        # True when new life message to be displayed
        self.display_new_life = False
        self.level = 1
        self.lives = 0
        self.life_image = pygame.image.load('images/pacOpen.png')
        self.game_state = PAUSED
        # 2 possible pages of instruction/information
        self.inst_page = 1

    def load_high_score(self):
        try:
            with open("scores.txt", "r") as file:
                self.high_score = int(file.read())
        except:
            self.high_score = 0

    def draw_text(self, screen, text, pos, font, color):
        label = font.render(text, False, color)
        screen.blit(label, pos)
        return label.get_height() * 2

    def draw_text_center(self, screen, text, pos, font, color):
        label = font.render(text, False, color)
        cent_pos = (pos[0] - label.get_width() / 2, pos[1])
        screen.blit(label, cent_pos)
        return label.get_height() * 2

    def draw(self, screen):
        self.draw_text(screen, f"Your score: {self.score}", (20, 10),
                         scores,"white"),
        self.draw_text(screen, f"High score: {self.high_score}", (200, 10),
                         scores, "white")
        self.draw_text(screen, f"Level: {self.level}", (400, 10),
                         scores, "white")
        # draw an image for each life remaining
        for i in range(self.lives):
            screen.blit(self.life_image, (i * 25 + 30, HEIGHT - 30))
        # check if last catch score to be displayed
        if self.display_catch_score:
            self.show_catch_score(screen)
        # check if new life needs to be displayed
        if self.display_new_life:
            self.show_new_life(screen)

    def draw_game_over(self, screen):
        self.draw_text_center(screen, "Game over",  (CENTER, 100),
                              heading,"yellow")
        self.draw_text_center(screen, f"Your score: {self.score}", (CENTER, 225),
                         heading, "white")
        self.draw_text_center(screen, f"You reached level: {self.level}", (CENTER, 300),
                         heading, "white")
        if self.score > self.high_score:
            # high_score = Player.score
            self.draw_text_center(screen, "Congratulations a new high score!", (CENTER, 400),
                             heading, "green")
            if not self.high_saved:
                # save high score
                with open("scores.txt", "w") as file:
                    file.write(str(self.score))
                self.high_saved = True
        self.draw_text_center(screen, "Press space bar for another game",  (CENTER, 475),
                        text,"aqua")
        self.draw_text_center(screen, "Press 'm' to start with music", (CENTER, 515),
                              text, "aqua")
        self.draw_text_center(screen, "Author: Paul Brace 2024", (CENTER, 550),
                              small, "white")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return START, SILENT
        elif keys[pygame.K_m]:
            return START, MUSIC
        else:
            return WAIT, SILENT

    def draw_game_instructions(self, screen):
        # fill the screen with black to clear last frame
        screen.fill("black")
        if self.inst_page == 1:
            y = 50
            y += self.draw_text_center(screen, "Maze-Man - Instructions",  (CENTER, y),
                                  heading, "yellow")
            for line in instructions:
                y += self.draw_text(screen, line, (40, y), text, "white")
            y += self.draw_text_center(screen, "Press 'i' for more information", (CENTER, 570),
                                  text, "aqua")
            y += self.draw_text_center(screen, "Press space bar to start with no music", (CENTER, 600),
                                  text, "aqua")
            self.draw_text_center(screen, "Press 'm' to start with music", (CENTER, 630),
                                  text, "aqua")
            self.draw_text_center(screen, "Author: Paul Brace 2024", (CENTER, 660),
                                  small, "white")
        else:
            y = 40
            y += self.draw_text_center(screen, "Maze-Man - Information",  (CENTER, y),
                                  heading, "yellow")
            for line in further_info:
                y += self.draw_text(screen, line, (20, y), info_text, "white")
                y -= 6  # reduce gap to fit
            y += self.draw_text_center(screen, "Press space bar to start with no music", (CENTER, 600),
                                  text, "aqua")
            self.draw_text_center(screen, "Press 'm' to start with music", (CENTER, 630),
                                  text, "aqua")
            self.draw_text_center(screen, "Author: Paul Brace 2024", (CENTER, 660),
                                  small, "white")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return START, SILENT
        elif keys[pygame.K_m]:
            return START, MUSIC
        elif keys[pygame.K_i]:
            self.inst_page += 1
        return WAIT, SILENT

    def draw_level_over(self, screen):
        self.draw_text_center(screen, "Level Completed", (CENTER, 300),
                              heading, "red")

    def set_catch_score(self, score, pos):
        self.catch_score = score
        self.catch_position = (pos[0], pos[1] - 5)
        self.catch_timer = CATCH_TIMER
        self.display_catch_score = True

    def show_catch_score(self, screen):
        self.catch_timer -= 1
        if self.catch_timer <= 0:
            self.display_catch_score = False
            return
        self.draw_text_center(screen, f"{self.catch_score}", self.catch_position,
                              small, "white")

    def set_new_life(self):
        if self.lives < 5:
            self.lives += 1
            self.new_life_timer = NEW_LIFE_TIMER
            self.display_new_life = True
            extra_life.play()

    def show_new_life(self, screen):
        self.new_life_timer -= 1
        if self.new_life_timer <= 0:
            self.display_new_life = False
            return
        self.draw_text_center(screen, "Extra life added", (CENTER, HEIGHT - 30),
                              text, "red")
