"""
Author Paul Brace April 2024
PacMan game developed using PyGame
Class to hold a list of game objects
"""


class SpriteList:
    def __init__(self):
        self.items = []

    # Add a new game image to list
    def add(self, item):
        self.items.append(item)

    # Draw all item on the screen
    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

    # return the number of items in the list
    def number(self):
        return len(self.items)

    # Delete all items where done flag is True
    def clear_done(self):
        for item in self.items:
            if item.done:
                self.items.remove(item)

    # Delete all items
    def clear_all(self):
        self.items.clear()
