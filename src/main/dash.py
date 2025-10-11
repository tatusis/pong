# dash.py

import pygame

DASH_SIZE = 10
DASH_COLOR = pygame.color.THECOLORS["grey50"]


class Dash(pygame.sprite.Sprite):
    """Define uma instância de um traço do traçado central"""

    def __init__(self, screen: pygame.surface.Surface) -> None:
        """Inicializa uma instância de um traço do traçado central"""
        super().__init__()
        self._layer = 1
        self.screen = screen
        self.image = pygame.surface.Surface((DASH_SIZE, DASH_SIZE))
        self.image.fill(DASH_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
