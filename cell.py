import pygame
from pygame.locals import Rect

INACTIVE_COLOR = "#808080"
ACTIVE_COLOR = "#00FF00"


class Cell:
    def __init__(self, surface, pos: tuple, dimensions: tuple, alive=False):
        self.active = alive
        self.future_state = None
        self.surface = surface
        print("new cell:")
        print(pos)
        print(dimensions)
        self.rectangle = Rect(pos[0], pos[1], dimensions[0], dimensions[1])

    def draw(self):
        """
            The cell keeps track of the surface it should draw on, and of its shape.
            This method checks what state the cell is in, and draws it in the appropriate color
        """

        if self.active:
            pygame.draw.rect(self.surface, ACTIVE_COLOR, self.rectangle, width=2)
        else:
            pygame.draw.rect(self.surface, INACTIVE_COLOR, self.rectangle, width=2)

    def __str__(self):
        return "X" if self.active else "_"

    def flip(self):
        self.active = not self.active

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def set_future_state(self, living_neighbors: int):
        if self.active and (living_neighbors == 2 or living_neighbors == 3):
            self.future_state = True
        elif not self.active and living_neighbors == 3:
            self.future_state = True
        else:
            self.future_state = False

    def update(self):
        self.active = self.future_state
        self.future_state = None
