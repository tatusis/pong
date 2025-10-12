# wall.py

import pygame
from side import Side


class Goal(pygame.sprite.Sprite):
    """Define uma instância de um gol"""

    def __init__(self, screen: pygame.surface.Surface, side: Side, settings: dict) -> None:
        """Inicializa uma instância de um gol"""
        super().__init__()
        self.settings = settings
        self._layer = 1
        self.screen = screen
        self.side = side
        self.image = pygame.surface.Surface(
            (self.settings["goal.size"], self.screen.get_rect().height + (self.settings["goal.size"] * 4))
        )
        self.image.fill(pygame.color.THECOLORS[self.settings["goal.color"]])
        self.rect = self.image.get_rect()

        if self.side == Side.LEFT:
            self.rect.top = self.screen.get_rect().top - (self.settings["goal.size"] * 2)
            self.rect.left = self.screen.get_rect().left - (self.settings["goal.size"] * 2)
        elif self.side == Side.RIGHT:
            self.rect.top = self.screen.get_rect().top - (self.settings["goal.size"] * 2)
            self.rect.right = self.screen.get_rect().right + (self.settings["goal.size"] * 2)
