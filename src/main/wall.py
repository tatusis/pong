# wall.py

import pygame
from side import Side


class Wall(pygame.sprite.Sprite):
    """Define uma instância de uma parede"""

    def __init__(self, screen: pygame.surface.Surface, side: Side, settings: dict) -> None:
        """Inicializa uma instância de uma parede"""
        super().__init__()
        self.settings = settings
        self._layer = 1
        self.screen = screen
        self.side = side
        self.image = pygame.surface.Surface((self.screen.get_rect().width, self.settings["wall.size"]))
        self.image.fill(pygame.color.THECOLORS[self.settings["wall.color"]])
        self.rect = self.image.get_rect()

        if self.side == Side.TOP:
            self.rect.top = self.screen.get_rect().top
            self.rect.left = self.screen.get_rect().left
        elif self.side == Side.BOTTOM:
            self.rect.bottom = self.screen.get_rect().bottom
            self.rect.left = self.screen.get_rect().left
