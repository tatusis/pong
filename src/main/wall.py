# wall.py

import pygame
from side import Side

WALL_HEIGHT = 10
WALL_COLOR = pygame.color.THECOLORS["grey49"]


class Wall(pygame.sprite.Sprite):
    """Define uma instância de uma parede"""

    def __init__(self, screen: pygame.surface.Surface, side: Side) -> None:
        """Inicializa uma instância de uma parede"""
        super().__init__()
        self._layer = 1
        self.screen = screen
        self.image = pygame.surface.Surface((self.screen.get_rect().width, WALL_HEIGHT))
        self.image.fill(WALL_COLOR)
        self.rect = self.image.get_rect()
        self.side = side

        if self.side == Side.TOP:
            self.rect.top = self.screen.get_rect().top
            self.rect.left = self.screen.get_rect().left
        elif self.side == Side.BOTTOM:
            self.rect.bottom = self.screen.get_rect().bottom
            self.rect.left = self.screen.get_rect().left
