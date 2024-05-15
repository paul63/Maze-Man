"""
Author Paul Brace April 2024
Base object for game sprites
"""

import math


class GameSprite:
    # Base object for game sprites
    def __init__(self, image, x, y):
        """
        :param image: pygame image
        :param x: x position of center of image
        :param y: y position of center of image
        """
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        # Amount to move on an update
        self.dx = 0
        self.dy = 0
        # Done is used to indicate that the object is finished with and can be deleted
        self.done = False

    def set_image(self, value):
        # use if setting an image of a different size
        self.image = value
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        """ move object dx and dy """
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        """ draw on screen - x,y is center of image """
        screen.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def collide_rect(self, game_object):
        """
        :param game_object: GameObject to test
        :return: True if the rectangles of both objects collide
        """
        if abs(abs(self.x) - abs(game_object.x)) < self.width / 2 + game_object.width / 2 \
                and abs(abs(self.y) - abs(game_object.y)) < self.height / 2 + game_object.height / 2:
            return True
        else:
            return False

    def collide_circle(self, game_object):
        """
        :param game_object:  GameObject to test
        :return: True if the distance between self and the object
        is < the sum of half the widths of the objects. I.e. intersection of
        two imaginary circles with a radius of half the width of the objects
        """
        if math.dist((self.x, self.y), (game_object.x, game_object.y)) \
                < self.width / 2 + game_object.width / 2:
            return True
        else:
            return False
